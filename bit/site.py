from fastapi import FastAPI
import logging
import os


if os.getenv("DEBUG", False) == "True":
    logging.basicConfig(filename="out.log")

app = FastAPI()
logger = logging.getLogger("Site")
logger.setLevel(logging.DEBUG)


@app.get("/v1/api/list")
async def list_all_bits(limit: int = -1):
    logger.debug("TESTING")
    return {"bits": []}
