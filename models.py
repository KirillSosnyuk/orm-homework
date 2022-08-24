import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import json
import sys

Base = declarative_base()

# Функция для вставки данных
def inserting_data(session, filepath='tests_data.json'):

    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for string in data:
        classname = getattr(sys.modules[__name__], string['model'].capitalize())
        session.add(classname(id=string.get('pk'), **string.get('fields')))
    session.commit()

# Функции
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# Классы
class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    books = relationship('Book', back_populates="publisher")

    def __str__(self):
        return f"{self.id} : {self.name}"


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    stock = relationship('Stock', back_populates = "shop")

    def __str__(self):
        return f"{self.id} : {self.name}"


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key = True)
    title = sq.Column(sq.String(length=40), nullable = False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable = False)

    publisher = relationship(Publisher, back_populates="books")
    stocks = relationship('Stock', back_populates = "book")

    def __str__(self):
        return f"{self.id} : ({self.title}, {self.id_publisher})"


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key = True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable = False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable = False)
    count = sq.Column(sq.Integer, nullable = False)

    book = relationship(Book, back_populates = "stocks")
    shop = relationship(Shop, back_populates = "stock")
    in_stock = relationship('Sale', back_populates = 'sale')

    def __str__(self):
        return f"{self.id} : ({self.id_book}, {self.id_shop}, {self.count})"


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key = True)
    price = sq.Column(sq.REAL, nullable = False)
    date_sale = sq.Column(sq.Date, nullable = False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable = False)
    count = sq.Column(sq.Integer, nullable = False)

    sale = relationship(Stock, back_populates = 'in_stock')

    def __str__(self):
        return f"{self.id} : ({self.price}, {self.date_sale}, {self.id_stock}, {self.count})"