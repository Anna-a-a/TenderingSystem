from fastapi import FastAPI
import psycopg2
from psycopg2 import sql
from psycopg2 import OperationalError
from password_hasher import *
from fastapi import FastAPI, Response, HTTPException
app = FastAPI()
from fastapi.encoders import jsonable_encoder


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
    SELECT DISTINCT ON (t.id)
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
    LEFT JOIN
    tender_system_user tu ON t.user_id = tu.id
    LEFT JOIN
    tender_supplier tsup ON t.id = tsup.tender_id
    LEFT JOIN
    tender_system_user tu2 ON tsup.supplier_id = tu2.id AND tu2.user_type = 'supplier'
    ORDER BY t.id, tsup.is_winner DESC, tsup.price ASC
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
WITH winner_check AS (
SELECT
t.id AS tender_id,
BOOL_OR(tsup.is_winner) AS has_winner
FROM
tender t
LEFT JOIN
tender_supplier tsup ON t.id = tsup.tender_id
WHERE
t.tender_status IN ('open', 'in progress', 'closed') AND t.id = 3
GROUP BY
t.id
),
winner_supplier AS (
SELECT
t.id AS tender_id,
tu2.id AS supplier_id,
tu2.name AS supplier_name,
tu2.login AS supplier_login,
tu2.email AS supplier_email,
tsup.price AS supplier_price,
tsup.is_winner AS is_winner
FROM
tender t
JOIN
tender_supplier tsup ON t.id = tsup.tender_id AND tsup.is_winner = true
JOIN
tender_system_user tu2 ON tsup.supplier_id = tu2.id AND tu2.user_type = 'supplier'
WHERE
t.tender_status IN ('open', 'in progress', 'closed') AND t.id = 3
)
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
CASE
WHEN wc.has_winner AND t.tender_status = 'closed' THEN ARRAY[ws.supplier_id]
ELSE array_agg(DISTINCT tu2.id)
END AS supplier_id,
CASE
WHEN wc.has_winner AND t.tender_status = 'closed' THEN ARRAY[ws.supplier_name]
ELSE array_agg(DISTINCT tu2.name)
END AS supplier_name,
CASE
WHEN wc.has_winner AND t.tender_status = 'closed' THEN ARRAY[ws.supplier_login]
ELSE array_agg(DISTINCT tu2.login)
END AS supplier_login,
CASE
WHEN wc.has_winner AND t.tender_status = 'closed' THEN ARRAY[ws.supplier_email]
ELSE array_agg(DISTINCT tu2.email)
END AS supplier_email,
CASE
WHEN wc.has_winner AND t.tender_status = 'closed' THEN ARRAY[ws.supplier_price]
ELSE array_agg(DISTINCT tsup.price)
END AS supplier_prices,
CASE WHEN COUNT(tsup.supplier_id) < 3 OR wc.has_winner THEN NULL ELSE MIN(tsup.price) END AS supplier_price,
CASE WHEN wc.has_winner THEN ws.is_winner ELSE tsup.is_winner END AS is_winner
FROM
tender t
JOIN
winner_check wc ON t.id = wc.tender_id
JOIN
tender_system_user tu ON t.user_id = tu.id AND tu.user_type != 'supplier'
LEFT JOIN
tender_supplier tsup ON t.id = tsup.tender_id
LEFT JOIN
tender_system_user tu2 ON tsup.supplier_id = tu2.id AND tu2.user_type = 'supplier'
LEFT JOIN
winner_supplier ws ON t.id = ws.tender_id
WHERE
t.tender_status IN ('open', 'in progress', 'closed') AND t.id = 3
GROUP BY
t.id, t.description, t.created_date_time, t.start_date_time, t.end_date_time, t.first_price, t.title, t.delivery_address, t.delivery_area, t.tender_status, tu.name, tu.login, wc.has_winner, ws.supplier_id, ws.supplier_name, ws.supplier_login, ws.supplier_email, ws.supplier_price, ws.is_winner, tsup.is_winner;"""

    cur.execute(query, (tender_id, tender_id, tender_id, ))
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


def send_tender_supplier_info(supplier_id, price):
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

    query = """SELECT id, user_type FROM tender_system_user WHERE login=%s and password_hash=%s"""
    try:
        cursor.execute(query, (login, password_hash,))
        result = cursor.fetchone()
        if result is not None:
            return [result[0], result[1]]
        return None # Изменено с False на None
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


def supplier_id_by_login(login):
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    query = """SELECT id FROM tender_system_user WHERE login=%s"""
    try:
        cursor.execute(query, (login,))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        return None # Изменено с False на None
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
    conn = None
    try:
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
        cursor.execute(query, (cookie,))
        result = cursor.fetchone()
        if result is not None:
            return True
        return False
    except psycopg2.Error as e:
        print(f"Error: {e}")
        return False
    finally:
        if conn is not None:
            cursor.close()
            conn.close()


def user_id_by_cookie(auth_cookie):
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Define the select query
    query = """SELECT user_id FROM cookies WHERE cookie=%s"""
    try:
        cursor.execute(query, (auth_cookie,))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        return False
    finally:
        cursor.close()
        conn.close()


def user_data_by_cookie(auth_cookie):
    id = user_id_by_cookie(auth_cookie)
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Define the select query
    query = """SELECT * FROM tender_system_user WHERE id=%s"""
    try:
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if result is not None:
            return result
        return False
    finally:
        cursor.close()
        conn.close()


def end_tender(login, tender_id):
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # SQL query to check if the user has a bid on the specified tender
    check_query = """
    SELECT price FROM tender_supplier
    WHERE tender_id = %s AND supplier_id = (SELECT id FROM tender_system_user WHERE login = %s);
    """

    # Execute the check query
    cursor.execute(check_query, (tender_id, login))
    result = cursor.fetchone()

    # If the user has a bid on the tender, update the tender and tender_supplier tables
    if result is not None:
        proposed_price = result[0]

        update_tender_query = """
        UPDATE tender
        SET end_date_time = NOW(),
            first_price = %s,
            tender_status = 'closed'
        WHERE id = %s;
        """

        cursor.execute(update_tender_query, (proposed_price, tender_id))

        update_supplier_query = """
        UPDATE tender_supplier
        SET is_winner = true,
            price = %s
        WHERE tender_id = %s AND supplier_id = (SELECT id FROM tender_system_user WHERE login = %s);
        """

        cursor.execute(update_supplier_query, (proposed_price, tender_id, login))

        conn.commit()
    else:
        print(f"User with login '{login}' does not have a bid on tender with ID {tender_id}")

    # Close the cursor and connection
    cursor.close()
    conn.close()


def add_supplier_for_tender(tender_id, price, supplier_login):
    supplier_id = supplier_id_by_login(supplier_login)
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    update_query = """
    INSERT INTO tender_supplier(tender_id, price, supplier_id, is_winner)
VALUES (%s , %s, %s, 'false');
        """

    # Execute the query
    cursor.execute(update_query, (tender_id, price, supplier_id))
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return "Supplier response is successfully done!"


def search_in_json_list(json_list, search_string):
    # Преобразование каждого объекта Tender в формат, совместимый с JSON
    data = [jsonable_encoder(item) for item in json_list]

    # Теперь можно безопасно выполнять операции над data, как если бы это был список словарей
    # Используем lower() для преобразования ключей и значений в нижний регистр перед сравнением
    results = [item for item in data if any(search_string.lower() in str(value).lower() for value in item.values())]

    return results


def tenders_by_user_id(user_id):
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Define the select query
    query = """SELECT * FROM tender WHERE user_id=%s"""
    try:
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()  # Use fetchall to get all matching records
        return result
    finally:
        cursor.close()
        conn.close()


def get_supplier_tenders(supplier_id):
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Define the select query
    query = """SELECT
    t.id AS tender_id,
    t.tender_status AS tender_status_description,
    t.description AS tender_description,
    t.created_date_time AS tender_created_date_time,
    t.start_date_time AS tender_start_date_time,
    t.end_date_time AS tender_end_date_time,
    tu.id AS tender_user_id,
    t.first_price AS tender_first_price,
    t.title AS tender_title,
    t.delivery_address AS tender_delivery_address,
    t.delivery_area AS tender_delivery_area
FROM
    tender t
JOIN
    tender_supplier ts ON t.id = ts.tender_id
JOIN
    tender_system_user tu ON t.user_id = tu.id
WHERE
    ts.supplier_id = %s"""
    try:
        cursor.execute(query, (supplier_id,))
        result = cursor.fetchall()  # Use fetchall to get all matching records
        return result
    finally:
        cursor.close()
        conn.close()
