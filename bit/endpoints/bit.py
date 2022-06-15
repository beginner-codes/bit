from typing import Callable, Optional

from fastapi import FastAPI, Depends, UploadFile, Body, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from bit.database import session_maker
from bit.models import Bit, Code, File

bit_app = FastAPI()


class NewBitModel(BaseModel):
    name: str


@bit_app.post("/create")
async def create_bit(
    bit: NewBitModel, session: Callable[[], AsyncSession] = Depends(session_maker)
):
    async with session() as conn:
        async with conn.begin():
            new_bit = Bit(name=bit.name, user_id=0)
            conn.add(new_bit)

    return {
        "bit": {
            "name": new_bit.name,
            "archived": new_bit.archived,
            "user_id": new_bit.user_id,
            "id": new_bit.id,
        }
    }


@bit_app.post("/{bit_id}/files/add")
async def add_file(
    bit_id: int,
    file: UploadFile,
    filename: Optional[str] = Body(None),
    session: Callable[[], AsyncSession] = Depends(session_maker),
):
    async with session() as conn:
        result = await conn.execute(select(Bit).where(Bit.id == bit_id))
        bit = result.scalars().first()

        if not bit:
            raise HTTPException(404, "Bit not found")

    async with session() as conn:
        async with conn.begin():
            new_file = File(name=filename or file.filename, bit_id=bit_id)
            conn.add(new_file)
            await conn.flush()

            contents = await file.read(-1)
            new_code = Code(code=contents, file_id=new_file.id)
            conn.add(new_code)

        await conn.commit()

    return {
        "file": {
            "bit_id": new_file.bit_id,
            "file_id": new_file.id,
            "code_id": new_code.id,
            "name": new_file.name,
            "created": new_code.created,
            "code": new_code.code,
        }
    }
