from fastapi import FastAPI
import psycopg2

app = FastAPI()

def fetch_tender_info(tender_id):
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
        ts.description AS tender_status_description,
        tu.name AS tender_user_name,
        tu.login AS tender_user_login,
        CASE
            WHEN ts.id IN (2, 1) THEN NULL
            ELSE tsup.supplier_id
        END AS supplier_id,
        CASE
            WHEN ts.id IN (2, 1) THEN NULL
            ELSE s.name
        END AS supplier_name,
        CASE
            WHEN ts.id IN (2, 1) THEN NULL
            ELSE tsup.price
        END AS supplier_price,
        CASE
            WHEN ts.id IN (2, 1) THEN NULL
            ELSE tsup.is_winner
        END AS is_winner
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
    WHERE t.id = %s;
    """


    # Execute the query
    cur.execute(query, (tender_id,))

    # Fetch all the rows
    rows = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    return rows

