
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from repository import *

app = FastAPI()

@app.get("/tender/{tender_id}")
async def get_tender_info(tender_id: int):
    tender_info = fetch_tender_info(tender_id)
    if tender_info:
        return jsonable_encoder(tender_info)
    else:
        return {}
