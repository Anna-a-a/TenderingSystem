from fastapi import FastAPI
import psycopg2
from psycopg2 import sql
from psycopg2 import OperationalError
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
        ts.description AS tender_status_description,
        tu.name AS tender_user_name,
        tu.login AS tender_user_login,
        tsup.supplier_id AS supplier_id,
        s.name AS supplier_name,
        tsup.price AS supplier_price,
        tsup.is_winner AS is_winner
    FROM 
        tender t
    JOIN 
        tender_state ts ON t.tender_status_id = ts.id
    JOIN 
        tender_user tu ON t.user_id = tu.id
    LEFT JOIN 
        tender_supplier tsup ON t.id = tsup.tender_id AND tsup.is_winner = TRUE
    LEFT JOIN 
        supplier s ON tsup.supplier_id = s.id
   
    """


    # Execute the query
    cur.execute(query, )

    # Fetch all the rows
    rows = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    return rows

def fetch_pending_tenders():
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
    	ts.description AS status_description,
    	tu.name AS user_name,
    	array_agg(s.id) AS supplier_id,
    	array_agg(s.name) AS supplier_name,
    	CASE WHEN COUNT(tsup.supplier_id) > 1 THEN NULL ELSE MIN(tsup.price) END AS supplier_price,
    	tsup.is_winner AS is_winner
FROM 
    tender t
JOIN 
    tender_state ts ON t.tender_status_id = ts.id
JOIN 
    tender_user tu ON t.user_id = tu.id
LEFT JOIN 
    tender_supplier tsup ON t.id = tsup.tender_id
LEFT JOIN 
    supplier s ON tsup.supplier_id = s.id
WHERE 
    ts.id IN (1, 2)
GROUP BY 
    t.id, t.description, t.created_date_time, t.start_date_time, t.end_date_time, t.first_price, t.title, t.delivery_address, t.delivery_area, ts.description, tu.name, tu.login, tsup.is_winner


    """

    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows




def insert_tender_info(tender_status_id, description, start_date_time, user_id, created_date_time=None, end_date_time=None, first_price=None, title=None, delivery_address=None, delivery_area=None):
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost", # Или "127.0.0.1"
        port="5432"
    )

    cursor = conn.cursor()
    query = """
            INSERT INTO tender(tender_status_id, description, start_date_time, user_id, created_date_time, end_date_time, first_price, title, delivery_address, delivery_area)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    try:
        cursor.execute(query, (tender_status_id, description, start_date_time, user_id, created_date_time, end_date_time, first_price, title, delivery_address, delivery_area))
        conn.commit()
        return True
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        conn.close()
