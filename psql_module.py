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


# connect_to_db(HOST, USER, PASSWORD, DB_NAME)
# print(check_exist_db(DB_NAME_NEW))
# create_database(DB_NAME_NEW)
# drop_database(DB_NAME_NEW)
