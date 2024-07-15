from datetime import datetime, UTC
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()


def utc_now() -> datetime:
    """Helper to return UTC datetime for created and updated metadata columns

    Returns:
        datetime: Current timestamp in Coordinated Universal Time (UTC)
    """
    return datetime.now(UTC)


class Base(DeclarativeBase):
    id: Mapped[int] = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    created: Mapped[datetime] = db.Column(db.DateTime, default=utc_now)
    updated: Mapped[datetime] = db.Column(
        db.DateTime,
        default=utc_now,
        onupdate=utc_now,
    )


class User(db.Model):
    username: Mapped[str] = db.Column(db.String, unique=True, nullable=False)
    password: Mapped[str] = db.Column(db.String, nullable=False)


class Collection(db.Model):
    name: Mapped[str] = db.Column(db.String, nullable=False)
    user_id: Mapped[int] = db.Column(
        db.Integer,
        db.ForeignKey(User.id),
        nullable=False,
    )
    user = db.relationship("User")


class Document(db.Model):
    name: Mapped[str] = db.Column(db.String, nullable=False)


class Chunk(db.Model):
    content: Mapped[str] = db.Column(db.String, nullable=False)
