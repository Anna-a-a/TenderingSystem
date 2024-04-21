from pydantic import BaseModel


class Reg_user(BaseModel):
    name: str
    login: str
    user_type: str = 'supplier'
    password: str
    email: str


class Check_user(BaseModel):
    login: str
    password: str
