from sqlalchemy.orm import as_declarative as _as_declarative


@_as_declarative()
class Base:
    __mapper_args__ = {"eager_defaults": True}
