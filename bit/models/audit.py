from sqlalchemy import Column, Integer, Unicode, DateTime
from sqlalchemy.sql import func
from bit.models.base import Base


class Audit(Base):
    __tablename__ = "Audit"
    id = Column(Integer, primary_key=True)
    action = Column(Unicode(256), nullable=False)
    details = Column(Unicode(1024), nullable=False)
    bit_id = Column(Integer, nullable=True)
    code_id = Column(Integer, nullable=True)
    file_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    when = Column(DateTime, nullable=False, server_default=func.now())
