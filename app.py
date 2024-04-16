from models.tender import Tender
from models.tender_suppliers import Tender_suppliers
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from repository import *
from pydantic import BaseModel
from models.tender import Post_tender
import psycopg2
from psycopg2 import sql
from psycopg2 import OperationalError


app = FastAPI()

@app.get("/tenders")
async def get_tenders_info():
    tender_info = fetch_tenders_info()
    tenders = set()
    for i in range(len(tender_info)):
        tenders.add(Tender(tender_info[i][0], tender_info[i][1], tender_info[i][2], tender_info[i][3], tender_info[i][4],
                           tender_info[i][5],tender_info[i][6], tender_info[i][7], tender_info[i][8], tender_info[i][9],
                           tender_info[i][10], tender_info[i][11], tender_info[i][12], tender_info[i][13], tender_info[i][14], tender_info[i][15]))

    return tenders


@app.get("/tenders_suppliers/{tender_id}")
async def get_pending_tenders(tender_id: int):
    rows = fetch_pending_tender_by_id(tender_id)  # Assuming the new function is named fetch_pending_tender_by_id_new
    tenders = []
    for row in rows:
        tender_id, tender_description, tender_created_date_time, tender_start_date_time, tender_end_date_time, tender_first_price, tender_title, tender_delivery_address, tender_delivery_area, status_description, user_name, user_login, supplier_ids, supplier_names, supplier_prices, supplier_price, is_winner = row
        tender = Tender_suppliers(
            id=tender_id,
            description=tender_description,
            created_date_time=tender_created_date_time,
            start_date_time=tender_start_date_time,
            end_date_time=tender_end_date_time,
            first_price=tender_first_price,
            title=tender_title,
            delivery_address=tender_delivery_address,
            delivery_area=tender_delivery_area,
            status_description=status_description,
            user_name=user_name,
            user_login=user_login,
            supplier_ids=supplier_ids,
            supplier_names=supplier_names,
            supplier_prices=supplier_prices,
            supplier_price=supplier_price,
            is_winner=is_winner
        )
        tenders.append(tender.serialize())
    return tenders[0] if tenders else None  # Возвращаем первый тендер или None, если список пуст


@app.post("/send_tender_info")
def insert_tender_info(item: Post_tender):
    conn = psycopg2.connect(
        dbname="tendering-system-db",
        user="username",
        password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    query = """
            INSERT INTO tender(tender_status, description, start_date_time, user_id, created_date_time, end_date_time, 
            first_price, title, delivery_address, delivery_area)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
    try:
        cursor.execute(query, (item.tender_status, item.description, item.start_date_time, item.user_id, item.created_date_time, item.end_date_time, item.first_price, item.title, item.delivery_address, item.delivery_area))
        conn.commit()
        return True
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        cursor.close()
        conn.close()


@app.post("/tender_supplier")
async def tender_suplplier(supplier_id, price):
    return send_tender_suplplier_info(supplier_id, price)



