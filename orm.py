import sqlite3
from fields import CharField, IntegerField

def parseValues(data):
    values = []
    t_fields=data
    for name, field in t_fields.items():
        if isinstance(t_fields[name], str):
            t_fields[name] = f"'{t_fields[name]}'"
        else:
            t_fields[name] = str(t_fields[name])


    return t_fields


class SqliteDatabase:
    def __init__(self, database):
        self.db = database

    def connect(self, *args, **kwargs):
        self.con = sqlite3.connect(self.db, *args, **kwargs)

    def create_tables(self, tables):
        for table in tables:
            table.create_table()

    def close(self):
        self.con.close()


class Model:
    schema = {}

    @classmethod
    def create_table(cls):
        cls.schema.update({cls.__name__: {}})
        dic = cls.__dict__
        keys = []
        check=''
        if 'sqlcheck' in dic:
            check=f"{dic['sqlcheck']}"

        for attr in dic:
            if isinstance(dic[attr], (CharField, IntegerField)):
                keys.append(f'{attr} {dic[attr]}')
            
                cls.schema[cls.__name__].update({attr: dic[attr]})

        if keys:
            query = f"CREATE TABLE {cls.__name__} ({','.join(keys)} {check})"

            cls.Meta.database.con.execute(query)

    @classmethod
    def create(cls, **t_fields):
        keys = cls.schema[cls.__name__]
        values = []

        for name, field in keys.items():
            t_fields.setdefault(name, field.default)

            field.check(t_fields[name])

            if isinstance(t_fields[name], str):
                t_fields[name] = f"'{t_fields[name]}'"
            else:
                t_fields[name] = str(t_fields[name])

            values.append(t_fields[name])

        query = f"INSERT INTO {cls.__name__} ({','.join(keys)}) VALUES ({','.join(values)})"

        metadb = cls.Meta.database
        metadb.con.execute(query)

    @classmethod
    def select(cls, *keys,where={}):
        result = []
        where_data = parseValues(where)
        where_params = ' and '.join([f"{str(i)}={where_data[i]}" for i in where_data])

        if not keys:
            keys = ['*']

        params = ','.join([str(i) for i in keys])
        query = f"SELECT {params} FROM {cls.__name__} {'WHERE '+where_params if len(where_params)>0 else ''}"
        print(query)
        for row in cls.Meta.database.con.execute(query):
            if row:
                result.append(' | '.join([str(i) for i in row]))
        return result

    @classmethod
    def update(cls, set={},where={}):
        set_data= parseValues(set)
        where_data = parseValues(where)

        set_params = ','.join([f"{str(i)}={set_data[i]}" for i in set_data])

        where_params = ' and '.join([f"{str(i)}={where_data[i]}" for i in where_data])
        if len(set_params)>0 and len(where_params)>0:
            query = f'UPDATE {cls.__name__} SET {set_params} WHERE {where_params}'
            cls.Meta.database.con.execute(query)
        else:
            raise ValueError('Incorrect set or where params')

    @classmethod
    def drop(cls):
        cls.Meta.database.con.execute(f'DROP TABLE {cls.__name__}')
