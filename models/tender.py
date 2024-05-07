from pydantic import BaseModel, validator
from datetime import datetime


class Tender:
    def __init__(self, id, description, created_data_time, start_data_time, end_data_time, first_price, title,
                 delivery_address, delivery_area, status,
                 user_name, user_login, supplier_id, supplier_name, supplier_price, is_winner, ):
        self.id = id
        self.description = description
        self.created_data_time = created_data_time
        self.start_data_time = start_data_time
        self.end_data_time = end_data_time
        self.first_price = first_price
        self.title = title
        self.delivery_address = delivery_address
        self.delivery_area = delivery_area
        self.status = status
        self.user_name = user_name
        self.user_login = user_login
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.supplier_price = supplier_price
        self.is_winner = is_winner

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'created_data_time': self.created_data_time,
            'start_data_time': self.start_data_time,
            'end_data_time': self.end_data_time,
            'first_price': self.first_price,
            'title': self.title,
            'delivery_address': self.delivery_address,
            'delivery_area': self.delivery_area,
            'status': self.status,
            'user_name': self.user_name,
            'user_login': self.user_login,
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier_name,
            'supplier_price': self.supplier_price,
            'is_winner': self.is_winner
        }


class Post_tender(BaseModel):
    tender_status: str
    description: str
    start_date_time: datetime
    user_id: int
    created_date_time: datetime
    end_date_time: datetime
    first_price: str
    title: str
    delivery_address: str
    delivery_area: str

    @validator("start_date_time", "created_date_time", "end_date_time", pre=True)
    def validate_datetime(cls, v):
        try:
            return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD HH:MM:SS")


class User_tender:
    def __init__(self, id, tender_status, description, created_date_time, start_date_time, end_date_time, user_id,
                 first_price, title, delivery_address, delivery_area):
        self.id = id
        self.tender_status = tender_status
        self.description = description
        self.created_date_time = created_date_time
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.user_id = user_id
        self.first_price = first_price
        self.title = title
        self.delivery_address = delivery_address
        self.delivery_area = delivery_area


class Tender_winner(BaseModel):
    login: str
    tender_id: int



