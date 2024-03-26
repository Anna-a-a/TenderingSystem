from models.tender import Tender
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from repository import *

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

@app.get("/tenderss")
async def get_tenders():
    tender_info = fetch_pending_tenders()
    tenders = set()
    print(tender_info[0])

    for i in range(len(tender_info)):
        for j in range(len(tender_info[0])):
            tenders.add(tender_info[i][j])

    return tenders

@app.post("/new_tender_form")
async def send_tender_info(tender_status_id, description, start_date_time, user_id, created_date_time, end_date_time, first_price, title, delivery_address, delivery_area):
    return insert_tender_info(tender_status_id, description, start_date_time, user_id, created_date_time,
                              end_date_time, first_price, title, delivery_address, delivery_area)



@app.post("/supplier_form")
async def tender_suplplier(supplier_id, price):
    return 1

