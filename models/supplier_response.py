from pydantic import BaseModel


class Supplier_response(BaseModel):
    tender_id: int
    price: int
    login: str

