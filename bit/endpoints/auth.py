from fastapi import FastAPI
from pydantic import BaseModel
from bit.auth import sign_jwt


auth_app = FastAPI()


class Username(BaseModel):
    username: str


@auth_app.post("/login")
async def authenticate(username: Username):
    return sign_jwt(username.username)
