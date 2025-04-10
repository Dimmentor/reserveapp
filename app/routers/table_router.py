from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.schemas.table_schema import TableCreate, TableOut
from app.models.table import Table
from sqlalchemy import select
from fastapi import HTTPException
from app.session import get_session

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.get("/", response_model=list[TableOut])
async def get_tables(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Table))
    return result.scalars().all()


@router.post("/", response_model=TableOut, status_code=status.HTTP_201_CREATED)
async def create_table(data: TableCreate, session: AsyncSession = Depends(get_session)):
    table = Table(**data.dict())
    session.add(table)
    await session.commit()
    await session.refresh(table)
    return table


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(table_id: int, session: AsyncSession = Depends(get_session)):
    table = await session.get(Table, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Столика с таким id не существует")
    await session.delete(table)
    await session.commit()
