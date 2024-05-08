from pydantic import BaseModel


class UpdateNameRequest(BaseModel):
    user_id: int
    name: str
