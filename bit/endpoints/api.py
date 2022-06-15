from fastapi import FastAPI
from bit.endpoints.auth import auth_app
from bit.endpoints.bit import bit_app


api_app = FastAPI()
api_app.mount("/v1/auth", auth_app)
api_app.mount("/v1/bit", bit_app)
