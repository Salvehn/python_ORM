from fields import CharField, IntegerField
from orm import SqliteDatabase, Model
import pytest


@pytest.fixture()
def create_db():
    db = SqliteDatabase(':memory:')
    db.connect()
    yield db
    db.close()


@pytest.fixture()
def create_table(create_db):
    class BaseModel(Model):
        class Meta:
            database = create_db

    class Advert(BaseModel):
        title = CharField(max_length=180, min_length=2)
        price = IntegerField(min_value=0)

    create_db.create_tables([Advert])
    yield Advert
    Advert.drop()

# Tests VVVVVV


def test_tables(create_db):
    class BaseModel(Model):
        class Meta:
            database = create_db

    class Games(BaseModel):
        title = CharField(max_length=80)
        price = IntegerField(min_value=0)
        rating = IntegerField(min_value=0, max_value=100)

    class Stores(BaseModel):
        name = CharField(max_length=80)
        cut = IntegerField(min_value=0, max_value=100)

    create_db.create_tables([Games, Stores])

    Games.create(title='Payday', price=700, rating=86)
    Stores.create(name='Steam', cut=30)

    assert str(Games.select()[0]) == 'Payday | 700 | 86'
    assert str(Stores.select()[0]) == 'Steam | 30'


def test_is_char(create_table):
    with pytest.raises(ValueError):
        create_table.create(title=100)


def test_min_char(create_table):
    with pytest.raises(ValueError):
        create_table.create(title='')


def test_max_char(create_table):
    with pytest.raises(ValueError):
        create_table.create(title=' ' * 181)


def test_is_int(create_table):
    with pytest.raises(ValueError):
        create_table.create(price='80')


def test_min_int(create_table):
    with pytest.raises(ValueError):
        create_table.create(price=-1)


def test_max_int(create_table):
    with pytest.raises(ValueError):
        create_table.create(price=1000000000)

def test_update(create_table):
    create_table.create(title='iPhone X', price=100)
    create_table.update(set={"title":'Samsung Galaxy S20'},where={"price":100})
    adverts = create_table.select(where={"price":100})
    assert str(adverts[0]) == 'Samsung Galaxy S20 | 100'

def test_select_title(create_table):
    create_table.create(title='iPhone X', price=100)
    adverts = create_table.select('title')
    assert str(adverts[0]) == 'iPhone X'


def test_select_all(create_table):
    create_table.create(title='iPhone X', price=100)
    adverts = create_table.select()
    assert str(adverts[0]) == 'iPhone X | 100'

def test_select_where(create_table):
    create_table.create(title='iPhone X', price=100)
    adverts = create_table.select(where={"price":100})
    assert str(adverts[0]) == 'iPhone X | 100'
