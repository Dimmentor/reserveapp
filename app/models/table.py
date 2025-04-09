from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)

    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="table", cascade="all, delete-orphan"
    )