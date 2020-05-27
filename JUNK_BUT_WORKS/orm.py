import sqlite3
import keyword
from typing import Iterable, List, Callable, Iterator, Union
import re

def parseConstraint(entry):
    constraint=[]
    for kk,v in entry:
        for key in [x for x in v if x.startswith('con')]:
            m=re.match(r'con_([a-z]+)?(=$|>$|<$|>=$|<=$)',key)
            if m:
                func=''
                if m.group(1):
                    func=m.group(1)
                constraint.append('{}({}){}{}'.format(func,kk,m.group(2),v[key ]))

    return ' and '.join(constraint)


def paramStr(param):
    if len(param)>0:
        param=' '+param
    return param

def quote(value):
    return '\'{}\''.format(value) if isinstance(value,str) else '{}'.format(value)

def operator(str):
    m=re.match(r'([a-z]+)(=$|>$|<$|>=$|<=$)',str)
    if m:
        return {'str':m.group(1),'op':m.group(2)}
    else:
        raise ValueError("Incorrect operator")
        return {'str':'','op':''}



class SqliteDatabase:

    def __init__(self,conn):
         self.conn=conn

    def connect(self):
        self.connection=sqlite3.connect(self.conn)
        self.execute=self.connection.cursor().execute



    def create_tables(self,tables: list):
        for k in tables:
            keys=['{} {}{}'.format(key,value['type'],paramStr(value['PARAMS']))  for (key,value) in k.__dict__.items() if not key.startswith('__')]
            constraint=parseConstraint([(key,value) for (key,value) in k.__dict__.items() if not key.startswith('__') and any([x for x in value.keys() if x.startswith('con_')])])
            query="""CREATE TABLE IF NOT EXISTS {} ({} CHECK({})) """.format(' '.join([k.__name__]), ','.join(keys),constraint)
            print('Executing:',query)
            self.execute(query)
            self.connection.commit()


class Model:
    @classmethod
    def create(self,**kwargs):
        keys=', '.join(kwargs.keys())
        values=', '.join([quote(value) for value in kwargs.values()])
        query='INSERT INTO {} ({}) VALUES({})'.format(self.__name__,keys,values)
        print('Executing:',query)
        result = self.database.execute(query).fetchone()
        self.database.connection.commit()
        return result


    @classmethod
    def select(self,fields,where=''):
        fields=', '.join(fields)
        if where:
            where=' WHERE '+' and '.join(['{}{}'.format(''.join(operator(key).values()),quote(value))  for (key,value) in where.items()])

        query='SELECT {} FROM {} {}'.format(fields,self.__name__,where)
        print('Executing:',query)
        result = self.database.execute(query).fetchall()
        self.database.connection.commit()
        return result

    @classmethod
    def delete(self,where=''):
        if where:
            where=' WHERE '+' and '.join(['{}{}'.format(''.join(operator(key).values()),quote(value))  for (key,value) in where.items()])

        query='DELETE FROM {} {}'.format(self.__name__,where)
        print('Executing:',query)
        result = self.database.execute(query)
        self.database.connection.commit()
        return result


class Field:
    def __init__(self,response):
     for k,v in response.items():
        if not keyword.iskeyword(k):
            if isinstance(v,dict):
                self.__dict__[k] = Field(v)
            else:
                self.__dict__[k] = v


class IntegerField:
    def __new__(cls,field):
        field.update({'type':'INTEGER'})
        return Field(field).__dict__

class CharField:
    def __new__(cls,field):
        field.update({'type':'TEXT'})
        return Field(field).__dict__
