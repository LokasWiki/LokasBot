import enum
from datetime import datetime
from typing import List as typing_list

from sqlalchemy import String, INTEGER, func, ForeignKey, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .engine import engine
from .hellper import get_namespace


class Base(DeclarativeBase):
    pass

class Status(enum.Enum):
    PENDING = "pending"
    RECEIVED = "received"
    COMPLETED = "completed"

class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    from_title: Mapped[str] = mapped_column(String(255))
    to_title: Mapped[str] = mapped_column(String(255),nullable=True)
    from_namespace: Mapped[int] = mapped_column(INTEGER)
    to_namespace: Mapped[int] = mapped_column(INTEGER,nullable=True)
    request_type: Mapped[int] = mapped_column(INTEGER)
    extra: Mapped[str] = mapped_column(Text,nullable=True)
    status: Mapped[Status] = mapped_column(insert_default=Status.PENDING)
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    update_date: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())


    @hybrid_property
    def to_name(self):
        return get_namespace(self.to_namespace)  + self.to_title
    @hybrid_property
    def from_name(self):
         return get_namespace(self.from_namespace) + self.from_title

    pages: Mapped[typing_list["Page"]] = relationship(
        back_populates="request", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, from={self.from_title!r}, to={self.to_title!r})"


class Page(Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    namespace: Mapped[int] = mapped_column(INTEGER)
    status: Mapped[Status] = mapped_column(insert_default=Status.PENDING)
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    update_date: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())
    extra: Mapped[str] = mapped_column(Text, nullable=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id"))
    request: Mapped["Request"] = relationship(back_populates="pages")

    @hybrid_property
    def page_name(self):
        return get_namespace(self.namespace) + self.title

    def __repr__(self) -> str:
        return f"pages(id={self.id!r}, title={self.title!r})"


class Request_Move_Page(Base):
    __tablename__ = "request_move_page"

    id: Mapped[int] = mapped_column(primary_key=True)
    from_title: Mapped[str] = mapped_column(String(255))
    from_namespace: Mapped[int] = mapped_column(INTEGER)
    to_title: Mapped[str] = mapped_column(String(255))
    to_namespace: Mapped[int] = mapped_column(INTEGER)
    status: Mapped[Status] = mapped_column(insert_default=Status.PENDING)
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    update_date: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())
    task_description: Mapped[str] = mapped_column(Text, nullable=True)
    task_options: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"pages(id={self.id!r}, title={self.from_title!r})"


Base.metadata.create_all(engine)
