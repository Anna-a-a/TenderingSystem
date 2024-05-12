from pydantic import BaseModel


class Reg_user(BaseModel):
    name: str
    login: str
    user_type: str
    password: str
    email: str


class Check_user(BaseModel):
    login: str
    password: str


class Info_user(BaseModel):
    user_id: int
    name: str
    user_type: str
    login: str
    email: str
