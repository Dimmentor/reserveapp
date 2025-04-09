from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer
from app.database import Base

class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    table_number: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="table", cascade="all, delete-orphan"
    )