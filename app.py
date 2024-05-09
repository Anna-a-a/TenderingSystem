import uuid
from fastapi import FastAPI, Response, HTTPException, Request, Cookie
from models.tender import Tender
from models.tender_info import TenderInfo
from models.tender_suppliers import Tender_suppliers
from repository import *
from models.tender import Post_tender, User_tender, Tender_winner
from models.user import Reg_user, Check_user, Info_user
from models.supplier_response import Supplier_response
from models.update import UpdateNameRequest, UpdateEmailRequest
import psycopg2
from password_hasher import *
from fastapi.responses import JSONResponse
import json
from fastapi import FastAPI, HTTPException, Request
from typing import Annotated

app = FastAPI()


@app.get("/tenders")
async def get_tenders_info(request: Request, search=None):
    print(search)
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        raise HTTPException(status_code=404, detail="you are not authorized :(")
    tender_info = fetch_tenders_info()
    tenders = set()
    for i in range(len(tender_info)):
        tenders.add(Tender(tender_info[i][0], tender_info[i][1], tender_info[i][2], tender_info[i][3], tender_info[i][4],
                           tender_info[i][5],tender_info[i][6], tender_info[i][7], tender_info[i][8], tender_info[i][9],
                           tender_info[i][10], tender_info[i][11], tender_info[i][12], tender_info[i][13], tender_info[i][14], tender_info[i][15]))
    if search==None:
        return tenders
    else:
        return search_in_json_list(tenders, search)


@app.get("/tenders_suppliers/{tender_id}")
async def get_pending_tenders(tender_id: int, request: Request):
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        raise HTTPException(status_code=404, detail="you are not authorized :(")
    rows = fetch_pending_tender_by_id(tender_id)
    # Assuming the new function is named fetch_pending_tender_by_id_new
    tenders = []
    for row in rows:
        tender_id, tender_description, tender_created_date_time, tender_start_date_time, tender_end_date_time, tender_first_price, tender_title, tender_delivery_address, tender_delivery_area, status_description, user_name, user_login, supplier_ids, supplier_names, supplier_logins,  supplier_emails, supplier_prices, supplier_price, is_winner = row
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
            supplier_logins=supplier_logins,
            supplier_emails=supplier_emails,
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
        user = user_id_by_login(item.login, hash)
        if user:
            user_id = user[0]
            usertype = user[1]
            insert_cookie(user_id, hash)
            return {"message": "Успешная авторизация",
                    "user_type": f"{usertype}"}
        else:
            return {"message": "Пользователь не найден"}
    else:
        return {"message": "Пользователь не найден"}


@app.post("/registration")
def registration(item: Reg_user):
    hashed_password = hash_password(item.password)
    return add_user(item, hashed_password)


@app.get("/user_info")
async def user_info(request: Request):
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        return None

    user_data = user_data_by_cookie(auth_cookie)
    user = Info_user(user_id=user_data[0], name=user_data[1], login=user_data[2], email=user_data[5], user_type=user_data[3])
    return user


@app.post("/tender_winner")
async def tender_winner(data: Tender_winner, request: Request):
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        raise HTTPException(status_code=403, detail="you are not authorized :(")

    login = data.login
    tender_id = data.tender_id

    # Call the end_tender function with the login and tender_id
    result = end_tender(login, tender_id)

    return {"result": result}


@app.post("/supplier_response")
async def supplier_response(item: Supplier_response, request: Request):
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        raise HTTPException(status_code=403, detail="you are not authorized :(")

    return add_supplier_for_tender(item.tender_id, item.price, item.login)


@app.get("/user_tenders/{user_id}")
async def user_tenders(user_id: int, request: Request):
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        raise HTTPException(status_code=403, detail="you are not authorized :(")
    tenders = tenders_by_user_id(user_id)
    tender_dict = []
    for i in range(len(tenders)):
        tender_dict.append(User_tender(tenders[i][0], tenders[i][1], tenders[i][2], tenders[i][3], tenders[i][4],
                           tenders[i][5], tenders[i][6], tenders[i][7], tenders[i][8], tenders[i][9],
                           tenders[i][10]))

    return tender_dict


@app.get("/supplier_tenders/{supplier_id}")
async def supplier_tenders(supplier_id: int, request: Request):
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        raise HTTPException(status_code=403, detail="you are not authorized :(")

    tenders = get_supplier_tenders(supplier_id)
    tender_list = []
    for tender in tenders:
        tender_list.append(User_tender(tender[0], tender[1], tender[2], tender[3], tender[4],
                                       tender[5], tender[6], tender[7], tender[8], tender[9],
                                       tender[10]))

    return tender_list


@app.get("/responses_to_requests/{supplier_id}")
async def responses_to_requests(supplier_id: int, request: Request):
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        raise HTTPException(status_code=403, detail="you are not authorized :(")

    tenders = get_responses_to_requests(supplier_id)
    tender_list = []
    for tender in tenders:
        tender_list.append(User_tender(tender[0], tender[1], tender[2], tender[3], tender[4],
                                       tender[5], tender[6], tender[7], tender[8], tender[9],
                                       tender[10]))

    return tender_list


@app.post("/update_name")
async def update_name(item: UpdateNameRequest, request: Request):
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        raise HTTPException(status_code=403, detail="you are not authorized :(")

    user_id = item.user_id
    name = item.name

    if update_user_name(user_id, name):
        return {"message": "Name updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update name")


@app.post("/update_email")
async def update_email(item: UpdateEmailRequest, request: Request):
    auth_cookie = request.cookies.get('auth')
    if not is_cookie_exist(auth_cookie):
        raise HTTPException(status_code=403, detail="you are not authorized :(")
    user_id = item.user_id
    email = item.email
    if update_user_email(user_id, email):
        return {"message": "Email updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update name")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)


