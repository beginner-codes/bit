from sqlalchemy import Column, Integer, Unicode
from bit.models.base import Base


class Bit(Base):
    __tablename__ = "Bit"
    id = Column(Integer, primary_key=True)
    code = Column(Unicode, nullable=False)
    user_id = Column(Integer, nullable=False)
