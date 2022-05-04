from sqlalchemy import Column, Integer, Unicode, Boolean
from bit.models.base import Base


class User(Base):
    __tablename__ = "User"
    discord_id = Column(Integer, primary_key=True)
    name = Column(Unicode(256), nullable=False)
    auto_update = Column(Boolean, default=True)
    banned = Column(Boolean, default=False)
    mod = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
