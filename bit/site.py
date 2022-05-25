from fastapi import FastAPI, Depends
from pydantic import BaseModel
import logging
import os
from bit.auth import decoded_token, sign_jwt


if os.getenv("DEBUG", False) == "True":
    logging.basicConfig(filename="out.log")

app = FastAPI()
logger = logging.getLogger("Site")
logger.setLevel(logging.DEBUG)


@app.get("/v1/api/list")
async def list_all_bits(limit: int = -1, token=Depends(decoded_token)):
    return {"bits": [token]}


class Username(BaseModel):
    username: str


@app.post("/v1/api/authenticate")
async def authenticate(username: Username):
    return sign_jwt(username.username)


@app.get("/v1/api/create")
async def create_bit():
    logger.debug("TESTING")
    return {"bits": []}
