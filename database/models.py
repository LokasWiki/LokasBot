from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime


import enum

from .engine import engine


class Base(DeclarativeBase):
    pass


class Status(enum.Enum):
    PENDING = "pending"
    RECEIVED = "received"
    COMPLETED = "completed"


class TaskName(enum.Enum):
    MAINTENANCE = "maintenance"
    RECEIVED = "received"
    COMPLETED = "completed"


class Page(Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[Status] = mapped_column(insert_default=Status.PENDING)
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    update_date: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())
    task_name: Mapped[Status] = mapped_column(insert_default=TaskName.MAINTENANCE)

    def __repr__(self) -> str:
        return f"pages(id={self.id!r}, title={self.title!r})"


Base.metadata.create_all(engine)
