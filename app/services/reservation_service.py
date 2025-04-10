from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.reservation_schema import ReservationCreate
from app.utils.exceptions import ReservationConflictException, TableNotFoundException
from datetime import timedelta


async def create_reservation(session: AsyncSession, data: ReservationCreate):
    table_stmt = select(Table).where(Table.id == data.table_id)

    result = await session.execute(table_stmt)

    if not result.scalars().first():
        raise TableNotFoundException()

    end_time = data.reservation_time + timedelta(minutes=data.duration_minutes)

    stmt = select(Reservation).where(
        Reservation.table_id == data.table_id,
        Reservation.reservation_time < end_time,
        Reservation.reservation_time + timedelta(minutes=data.duration_minutes) > data.reservation_time
    )

    result = await session.execute(stmt)

    if result.scalars().first():
        raise ReservationConflictException()

    reservation = Reservation(**data.dict())
    session.add(reservation)
    await session.commit()
    await session.refresh(reservation)
    return reservation


async def get_reservations(session: AsyncSession):
    return (await session.execute(select(Reservation))).scalars().all()


async def delete_reservation(session: AsyncSession, reservation_id: int):
    reservation = await session.get(Reservation, reservation_id)

    if reservation:
        await session.delete(reservation)
        await session.commit()
