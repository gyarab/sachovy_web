from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import text
import uuid

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(PGUUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    ELO: Mapped[int] = mapped_column(default=1000, server_default=text("1000"), index=True)
    vyhry: Mapped[int] = mapped_column(default=0, server_default=text("0"))
    prohry: Mapped[int] = mapped_column(default=0, server_default=text("0"))
    hash_password: Mapped[str] = mapped_column(nullable=False)
