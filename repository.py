from fastapi import FastAPI
import psycopg2

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

