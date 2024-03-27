from base_module import Base
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    password: Mapped[str]
    name: Mapped[str]
    tasks: Mapped[List["Task"]] = relationship(back_populates='user', cascade='save-update, merge, delete')
        
class Task(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str]
    describe: Mapped[str]
    ex_date: Mapped[str]
    user_name: Mapped[str] = mapped_column(ForeignKey('user.name'))
    user: Mapped["User"] = relationship(back_populates="tasks")