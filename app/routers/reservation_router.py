from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.reservation_schema import ReservationCreate, ReservationOut
from app.services.reservation_service import create_reservation, get_reservations, delete_reservation
from app.session import get_session


router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("/", response_model=list[ReservationOut])
async def list_reservations(session: AsyncSession = Depends(get_session)):
    return await get_reservations(session)

@router.post("/", response_model=ReservationOut, status_code=status.HTTP_201_CREATED)
async def make_reservation(data: ReservationCreate, session: AsyncSession = Depends(get_session)):
    return await create_reservation(session, data)

@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_reservation(reservation_id: int, session: AsyncSession = Depends(get_session)):
    await delete_reservation(session, reservation_id)