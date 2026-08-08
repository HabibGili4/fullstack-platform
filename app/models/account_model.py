from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
