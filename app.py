import uuid
from fastapi import FastAPI, Response, HTTPException, Request, Cookie
from models.tender import Tender
from models.tender_info import TenderInfo
from models.tender_suppliers import Tender_suppliers
from repository import *
from models.tender import Post_tender
from models.user import Reg_user, Check_user, Info_user
import psycopg2
from password_hasher import *
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler


app = FastAPI()


@app.get("/tenders")
async def get_tenders_info(request: Request):
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        raise HTTPException(status_code=404, detail="you are not authorized :(")
    tender_info = fetch_tenders_info()
    tenders = set()
    for i in range(len(tender_info)):
        tenders.add(Tender(tender_info[i][0], tender_info[i][1], tender_info[i][2], tender_info[i][3], tender_info[i][4],
                           tender_info[i][5],tender_info[i][6], tender_info[i][7], tender_info[i][8], tender_info[i][9],
                           tender_info[i][10], tender_info[i][11], tender_info[i][12], tender_info[i][13], tender_info[i][14], tender_info[i][15]))

    return tenders


@app.get("/tenders_suppliers/{tender_id}")
async def get_pending_tenders(tender_id: int, request: Request):
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        raise HTTPException(status_code=404, detail="you are not authorized :(")
    rows = fetch_pending_tender_by_id(tender_id)
    # Assuming the new function is named fetch_pending_tender_by_id_new
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


@app.post("/login")
async def login(item: Check_user, response: Response):
    hash = is_user_exist(item)
    if hash is not None:
        response.set_cookie(key="auth", value=hash)
        user_id = user_id_by_login(item.login, hash)
        insert_cookie(user_id, hash)
        return {"message": "Успешная авторизация"}
    else:
        return {"message": "Пользователь не найден"}


@app.post("/registration")
def registration(item: Reg_user):
    hashed_password = hash_password(item.password)
    add_user(item, hashed_password)


@app.post("/tender_supplier")
async def tender_supplier(supplier_id, price):
    return send_tender_supplier_info(supplier_id, price)


@app.get("/user_info")
async def user_info(request: Request):
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        raise HTTPException(status_code=404, detail="you are not authorized :(")

    user_data = user_data_by_cookie(auth_cookie)
    # Correctly initialize the Info_user model with keyword arguments
    user = Info_user(name=user_data[1], login=user_data[2], email=user_data[5])
    return user


@app.post("/tender_winner")
def tender_winner(name, request: Request):
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        raise HTTPException(status_code=404, detail="you are not authorized :(")
    return end_tender(name)


def compare_times(time1_str, time2_str):
    dt_obj1 = datetime.strptime(time1_str, "%Y-%m-%dT%H:%M:%S")
    dt_obj2 = datetime.strptime(time2_str, "%Y-%m-%dT%H:%M:%S")

    if time1_str < time2_str:
        return 1
    else:
        return 0

@app.post("/status_change")
def change_tender_status(information=get_tenders_info):
    utc_dt = datetime.now(timezone.utc)
    iso_date = utc_dt.isoformat()

    for i in information:
        tender_endtime = i.get("end_data_time")
        comp = compare_times(tender_endtime, iso_date)
        if comp == 1:
            update_tender_status(i.get("id"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(change_tender_status, 'interval', minutes=5)









