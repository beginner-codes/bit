from sqlalchemy import Column, Integer, Unicode, DateTime
from sqlalchemy.sql import func

from bit.models.base import Base


class Code(Base):
    __tablename__ = "Code"
    id = Column(Integer, primary_key=True)
    code = Column(Unicode(2**14), nullable=False)
    file_id = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False, server_default=func.now())
