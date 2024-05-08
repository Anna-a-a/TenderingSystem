from pydantic import BaseModel


class UpdateNameRequest(BaseModel):
    user_id: int
    name: str


class UpdateEmailRequest(BaseModel):
    user_id: int
    email: str