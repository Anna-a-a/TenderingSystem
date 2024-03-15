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