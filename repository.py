from fastapi import FastAPI
import psycopg2
from psycopg2 import sql
from psycopg2 import OperationalError
from password_hasher import *
from fastapi import FastAPI, Response, HTTPException
app = FastAPI()


def fetch_tenders_info():
    # Database connection parameters
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost", # Or "127.0.0.1"
        port="5432"
    )

    # Create a cursor object
    cur = conn.cursor()

    # SQL query to get all info about a tender
    query = """
    SELECT
    t.id AS tender_id,
    t.description AS tender_description,
    t.created_date_time AS tender_created_date_time,
    t.start_date_time AS tender_start_date_time,
    t.end_date_time AS tender_end_date_time,
    t.first_price AS tender_first_price,
    t.title AS tender_title,
    t.delivery_address AS tender_delivery_address,
    t.delivery_area AS tender_delivery_area,
    t.tender_status AS tender_status_description,
    tu.name AS tender_user_name,
    tu.login AS tender_user_login,
    tsup.supplier_id AS supplier_id,
    tu2.name AS supplier_name,
    tsup.price AS supplier_price,
    tsup.is_winner AS is_winner
FROM
    tender t
JOIN
    tender_system_user tu ON t.user_id = tu.id AND tu.user_type != 'supplier'
LEFT JOIN
    tender_supplier tsup ON t.id = tsup.tender_id AND tsup.is_winner = TRUE
LEFT JOIN
    tender_system_user tu2 ON tsup.supplier_id = tu2.id AND tu2.user_type = 'supplier'

    """


    # Execute the query
    cur.execute(query, )

    # Fetch all the rows
    rows = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    return rows


def fetch_pending_tender_by_id(tender_id):
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()
    query = """
    SELECT
    t.id AS tender_id,
    t.description AS tender_description,
    t.created_date_time AS tender_created_date_time,
    t.start_date_time AS tender_start_date_time,
    t.end_date_time AS tender_end_date_time,
    t.first_price AS tender_first_price,
    t.title AS tender_title,
    t.delivery_address AS tender_delivery_address,
    t.delivery_area AS tender_delivery_area,
    t.tender_status AS status_description,
    tu.name AS user_name,
    tu.login AS user_login,
    array_agg(tu2.id) AS supplier_id,
    array_agg(tu2.name) AS supplier_name,
    array_agg(tsup.price) AS supplier_prices,
    CASE WHEN COUNT(tsup.supplier_id) < 3 THEN NULL ELSE MIN(tsup.price) END AS supplier_price,
    tsup.is_winner AS is_winner
FROM
    tender t
JOIN
    tender_system_user tu ON t.user_id = tu.id AND tu.user_type != 'supplier'
LEFT JOIN
    tender_supplier tsup ON t.id = tsup.tender_id
LEFT JOIN
    tender_system_user tu2 ON tsup.supplier_id = tu2.id AND tu2.user_type = 'supplier'
WHERE
    t.tender_status IN ('open', 'in progress') AND t.id = %s
GROUP BY
    t.id, t.description, t.created_date_time, t.start_date_time, t.end_date_time, t.first_price, t.title, t.delivery_address, t.delivery_area, t.tender_status, tu.name, tu.login, tsup.is_winner;
            """

    cur.execute(query, (tender_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def is_user_exist(user):
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Define the select query
    query = """SELECT password_hash FROM tender_system_user WHERE login=%s and password_hash=%s"""
    try:
        cursor.execute(query, (user.login, hash_password(user.password),))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        return False
    finally:
        cursor.close()
        conn.close()


def send_tender_suplplier_info(supplier_id, price):
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",  # Или "127.0.0.1"
        port="5432"
    )

    # Создание объекта курсора
    cur = conn.cursor()
    try:
        # SQL-запрос для вставки нового тендера
        query = """
           INSERT INTO tender_supplier(supplier_id,price)
           VALUES(%s, %s)
           """

        # Выполнение запроса с параметрами
        cur.execute(query, (supplier_id, price))

        # Подтверждение транзакции
        conn.commit()

        # Закрытие курсора и соединения
        cur.close()
        conn.close()

        return 1

    except Exception as e:
        print(f"Ошибка: {e}")
        return 0


def add_user(user, hashed_password) :
    # Connect to the database
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Define the insert query
    query = """
                INSERT INTO tender_system_user(name, login, user_type, password_hash, email)
                VALUES(%s, %s, %s, %s, %s);
                """

    # Execute the insert query with the hashed password
    try:
        cursor.execute(query, (user.name, user.login, user.user_type, hashed_password, user.email))
        conn.commit()
        return True
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        conn.close()


def user_id_by_login(login, password_hash):
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Define the select query
    query = """SELECT id FROM tender_system_user WHERE login=%s and password_hash=%s"""
    try:
        cursor.execute(query, (login, password_hash,))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        return False
    finally:
        cursor.close()
        conn.close()


def insert_cookie(user_id, cookie):
    if is_cookie_user_exist(user_id):
        return True
    # Connect to the database
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Define the insert query
    query = """
                INSERT INTO cookies(user_id, cookie)
                VALUES(%s, %s);
                """

    # Execute the insert query with the hashed password
    try:
        cursor.execute(query, (user_id, cookie))
        conn.commit()
        return True
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        conn.close()


def is_cookie_user_exist(user_id):
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Define the select query
    query = """SELECT user_id FROM cookies WHERE user_id=%s"""
    try:
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result is not None:
            return True
        return False
    finally:
        cursor.close()
        conn.close()


def is_cookie_exist(cookie):
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Define the select query
    query = """SELECT cookie FROM cookies WHERE cookie=%s"""
    try:
        cursor.execute(query, (cookie,))
        result = cursor.fetchone()
        if result is not None:
            return True
        return False
    finally:
        cursor.close()
        conn.close()