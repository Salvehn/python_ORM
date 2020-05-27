from fields import CharField, IntegerField
from orm import SqliteDatabase, Model


db = SqliteDatabase(':memory:')


class BaseModel(Model):
    class Meta:
        database = db


class Advert(BaseModel):
    title = CharField(max_length=180)
    price = IntegerField(min_value=0)
    sqlcheck=f"CHECK (length(title)<=180 AND price>0)"


db.connect()
db.create_tables([Advert])

Advert.create(title='iPhone X', price=100)
Advert.create(title='Xiaomi Mi8', price=80)
Advert.update(set={"title":'Xiaomi Redmi Note 3',"price":40},where={"title":'Xiaomi Mi8'})

adverts = Advert.select()
adverts2 = Advert.select(where={"price":40})
print(adverts,adverts2)
assert str(adverts[0]) == 'iPhone X | 100'
