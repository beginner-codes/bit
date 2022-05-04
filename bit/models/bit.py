from sqlalchemy import Column, Integer, Boolean
from bit.models.base import Base


class Bit(Base):
    __tablename__ = "Bit"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    archived = Column(Boolean, default=False)
