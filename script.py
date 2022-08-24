import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables, inserting_data, Publisher, Shop, Book, Stock, Sale

# Считываем логин и пароль
try:
    from connection import connection

    if None not in (connection['login'], connection['password'], connection['database']):
        login, password, database = connection['login'], connection['password'], connection['database']
    else:
        print('Ошибка. Пожалуйста определите логин пароль и имя БД в файле connection.py')
        login, password, database = input('Введите Ваш логин от PostreSQL: '), input('Введите Ваш пароль от PostreSQL: '), input('Введите наименование существующей БД: ')
except:
    login, password, database = input('Введите Ваш логин от PostreSQL: '), input('Введите Ваш пароль от PostreSQL: '), input('Введите наименование существующей БД: ')

# Спрашиваем у пользователя запрос
publisher_input = input('Введите имя или идентификатор издателя: ').replace("'", '\u2019')

# Линка для подклюения к БД
DSN = f"postgresql://{login}:{password}@localhost:5432/{database}"
engine = sq.create_engine(DSN)
create_tables(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

#Функция для вставки данных
inserting_data(session, 'D:/Дз/Новая папка/orm-homework/tests_data.json')

# Опрееделяем что введено, идентификатор(число) или имя
if publisher_input.isdigit():
    #session.query(Publisher).join(Book.publisher).join(Stock.book).filter(Publisher.id == publisher_input).all()
    for c in session.query(Shop).join(Stock, Shop.id == Stock.id_shop).join(Book, Stock.id_book == Book.id).join(Publisher, Book.id_publisher == Publisher.id).filter(Publisher.id == int(publisher_input)).all():
        print(c) 
else:
    for c in session.query(Shop).join(Stock, Shop.id == Stock.id_shop).join(Book, Stock.id_book == Book.id).join(Publisher, Book.id_publisher == Publisher.id).filter(Publisher.name == publisher_input).all():
        print(c)

session.close()