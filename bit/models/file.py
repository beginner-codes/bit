from sqlalchemy import Column, Integer, Unicode
from bit.models.base import Base


class File(Base):
    __tablename__ = "File"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(256), nullable=False)
    bit_id = Column(Integer, nullable=False)