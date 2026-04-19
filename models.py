from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True)
    email: Mapped[str] = mapped_column(sa.String, unique=True)

class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(sa.DateTime, default=sa.func.now())
    author_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("users.id"))