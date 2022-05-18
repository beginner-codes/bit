from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import logging
import os
import time
import jwt


if os.getenv("DEBUG", False) == "True":
    logging.basicConfig(filename="out.log")

app = FastAPI()
logger = logging.getLogger("Site")
logger.setLevel(logging.DEBUG)


# Todo: Change this to use an RSA public/private key
JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"


def token_response(token: str):
    return {
        "access_token": token
    }


def sign_jwt(user_id: str) -> dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600,
        "bot": True
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except jwt.InvalidTokenError:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt: str) -> bool:
        return bool(decode_jwt(jwt))


def decoded_token(token=Depends(JWTBearer())):
    return decode_jwt(token)


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
