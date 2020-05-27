from orm import SqliteDatabase, Model, CharField, IntegerField
##, Model, fields



db = SqliteDatabase(':memory:')

#
class BaseModel(Model):
    class Meta:
        database = db
#

class Advert(BaseModel):
    """
    constraint syntax: begin key with con_ then sqlite function, then operator(<,>,= etc), then value
    """

    title = CharField({'con_length<':6,'PARAMS':'NOT NULL'})
    price = IntegerField({'con_<':30,'PARAMS':'NOT NULL'})

class Offer(BaseModel):
    """
    constraint syntax: begin key with con_ then sqlite function, then operator(<,>,= etc), then value
    """

    title = CharField({'con_length<':6,'PARAMS':'NOT NULL'})
    price = IntegerField({'con_<':30,'PARAMS':'NOT NULL'})
    author = CharField({'con_length<':40,'PARAMS':'NOT NULL'})

db.connect()



print('Current date',db.execute('SELECT date(\'now\')').fetchone()[0])

db.create_tables([Advert,Offer])


Advert.create(title='test1',price=10)
Advert.create(title='test2',price=20)
Advert.create(title='test3',price=25)
print('\nSELECT RESULT#1:',Advert.select(['title','price']))

Advert.delete({'title=':'test2'})

print('\nSELECT RESULT#2:',Advert.select(['title','price'],{'price=':25}))


Offer.create(title='test1',price=10,author='me')
Offer.create(title='test2',price=20,author='you')

#
# Advert.create(title='iPhone X', price=100)
# adverts = Advert.select()
# assert str(adverts[0]) == 'iPhone X | 100 ₽'
