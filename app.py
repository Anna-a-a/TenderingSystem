from models.tender import Tender
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from repository import *

app = FastAPI()

@app.get("/tender/{tender_id}")
async def get_tender_info(tender_id: int):
    tender_info = fetch_tender_info(tender_id)
    tender = Tender(tender_info[0][0], tender_info[0][1], tender_info[0][2], tender_info[0][3], tender_info[0][4], tender_info[0][5],
                    tender_info[0][6], tender_info[0][7], tender_info[0][8], tender_info[0][9], tender_info[0][10], tender_info[0][11])
    if tender_info:
        return tender
    else:
        return {}
