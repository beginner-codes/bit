from sqlalchemy import Column, Integer, Boolean, Unicode

from bit.models.base import Base


class Bit(Base):
    __tablename__ = "Bit"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    user_id = Column(Integer, nullable=False)
    archived = Column(Boolean, default=False)
