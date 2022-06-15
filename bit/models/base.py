from sqlalchemy.orm import declarative_base as _declarative_base

Base = _declarative_base()
Base.__mapper_args__ = {"eager_defaults": True}
