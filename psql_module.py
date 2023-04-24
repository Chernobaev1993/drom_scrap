import psycopg2
from dbconfig import HOST, USER, PASSWORD, DB_NAME

# Имя создаваемой БД
DB_NAME_NEW = 'drom_scrap'


class IsDatabaseExistException(Exception):
    pass


def connect_to_db(host, user, password, dbname):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        connection.autocommit = True
        print('Успешное подключение к БД')
        return connection
    except psycopg2.Error as e:
        print('Ошибка подключения к БД', e)


# Проверяет наличие БД с именем dbname, возвращает кортеж (если БД есть) либо None (если его нету)
def check_exist_db(dbname):
    conn = connect_to_db(HOST, USER, PASSWORD, DB_NAME)
    if conn:
        with conn.cursor() as curs:
            sql = f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'"
            curs.execute(sql)
            exists = curs.fetchone()
        conn.close()
        return exists
    else:
        raise IsDatabaseExistException('Ошибка проверки существования БД')


def create_database(dbname):
    check = check_exist_db(DB_NAME_NEW)
    if check:
        print(f'База данных с именем \'{dbname}\' уже существует. Создание невозможно')
    else:
        conn = connect_to_db(HOST, USER, PASSWORD, DB_NAME)
        sql = f"CREATE DATABASE {dbname};"
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()
        conn.close()
        print(f'База данных \'{dbname}\' создана')


def drop_database(dbname):
    check = check_exist_db(dbname)
    if not check:
        print(f'База данных с именем \'{dbname}\' не существует. Удаление невозможно')
    else:
        conn = connect_to_db(HOST, USER, PASSWORD, DB_NAME)
        sql = f"DROP DATABASE {dbname};"
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()
        conn.close()
        print(f'База данных \'{dbname}\' удалена')


def create_table_features(dbname):
    conn = connect_to_db(HOST, USER, PASSWORD, dbname)
    with conn.cursor() as curs:
        sql = f"""CREATE TABLE IF NOT EXISTS features
                      (
                          feature_id INT PRIMARY KEY,
                          engine TEXT,
                          fuel TEXT,
                          wheel TEXT,
                          trans TEXT,
                          run TEXT,
                          car_id INT REFERENCES cars(car_id)
                      );"""
        curs.execute(sql)
    conn.close()
    print('Таблица features успешно создана')


def create_table_cars(dbname):
    conn = connect_to_db(HOST, USER, PASSWORD, dbname)
    with conn.cursor() as curs:
        sql = f"""CREATE TABLE IF NOT EXISTS cars
                  (
                      car_id INT PRIMARY KEY,
                      brand TEXT NOT NULL,
                      model TEXT NOT NULL,
                      year INT NOT NULL CHECK(year > 0),
                      price INT NOT NULL CHECK(price > 0),
                      link TEXT NOT NULL
                  );"""
        curs.execute(sql)
    conn.close()
    print('Таблица cars успешно создана')


def insert_into_cars(dbname):
    conn = connect_to_db(HOST, USER, PASSWORD, dbname)
    with conn.cursor() as curs:
        sql = f"""INSERT INTO cars(car_id, brand, model, year, price, link) 
                  VALUES
                  (1, 'Honda', 'CIVIC', 2010, 600000, 'https');"""
        curs.execute(sql)
    conn.close()
    print('Данные в таблицу cars занесены')


def insert_into_features(dbname):
    conn = connect_to_db(HOST, USER, PASSWORD, dbname)
    with conn.cursor() as curs:
        values = None
        sql = f"""INSERT INTO features(feature_id, engine, fuel, wheel, trans, run, car_id) 
                  VALUES
                  (%s, %s, %s, %s, %s, %s, %s);"""
        curs.execute(sql, (4, '1.2', 'бензин', values, 'передний', '123', 1))
    conn.close()
    print('Данные в таблицу features занесены')


# connect_to_db(HOST, USER, PASSWORD, DB_NAME)
# print(check_exist_db(DB_NAME_NEW))
# create_database(DB_NAME_NEW)
# drop_database(DB_NAME_NEW)
# create_table_cars(DB_NAME_NEW)
# create_table_features(DB_NAME_NEW)
# insert_into_cars(DB_NAME_NEW)
insert_into_features(DB_NAME_NEW)
