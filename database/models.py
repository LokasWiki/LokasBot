from sqlalchemy import String, func, INTEGER
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime

import enum

from .engine import maintenance_engine, webcite_engine, statistics_engine


class Base(DeclarativeBase):
    pass


# todo: for now it will mere in one database with all tables
class BaseS(DeclarativeBase):
    pass


class Status(enum.Enum):
    PENDING = "pending"
    RECEIVED = "received"
    COMPLETED = "completed"


class TaskName(enum.Enum):
    MAINTENANCE = "maintenance"
    WEBCITE = "webcite"


class Page(Base):
    __tablename__ = "pages"
    # todo: comment columns will add in next version
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    # thread_number: Mapped[int] = mapped_column(INTEGER)
    thread: Mapped[int] = mapped_column(INTEGER)
    # status: Mapped[Status] = mapped_column(insert_default=Status.PENDING)
    status: Mapped[int] = mapped_column(insert_default=0)
    date: Mapped[datetime] = mapped_column(insert_default=func.now())

    # create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    # update_date: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())
    # task_name: Mapped[TaskName] = mapped_column(insert_default=TaskName.MAINTENANCE)

    def __repr__(self) -> str:
        return f"pages(id={self.id!r}, title={self.title!r})"


class Statistic(BaseS):
    __tablename__ = "statistics"
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(255), unique=True)
    value: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"statistics(id={self.id!r}, key={self.key!r}), value={self.value!r})"


Base.metadata.create_all(webcite_engine)
Base.metadata.create_all(maintenance_engine)
BaseS.metadata.create_all(statistics_engine)
