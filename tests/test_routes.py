import pytest
from datetime import datetime, timedelta
from app.schemas.table_schema import TableCreate
from app.schemas.reservation_schema import ReservationCreate


@pytest.mark.asyncio
async def test_create_table(fake_session):
    payload = TableCreate(table_number=1, capacity=4)
    table = await fake_session.add_table(payload)

    assert table["id"] == 1
    assert table["capacity"] == 4


@pytest.mark.asyncio
async def test_get_tables(fake_session):
    tables = await fake_session.get_tables()
    print(tables)
    assert isinstance(tables, list)



@pytest.mark.asyncio
async def test_delete_table(fake_session):
    await fake_session.add_table(TableCreate(table_number=99, capacity=2))
    await fake_session.delete_table(1)
    assert len(fake_session.tables) == 0


@pytest.mark.asyncio
async def test_create_reservation(fake_session):
    table = await fake_session.add_table(TableCreate(table_number=2, capacity=2))
    now = datetime.utcnow()

    payload = ReservationCreate(
        table_id=table["id"], start_time=now, end_time=now + timedelta(hours=1)
    )
    reservation = await fake_session.add_reservation(payload)

    assert reservation["id"] == 1


@pytest.mark.asyncio
async def test_conflict_reservation(client, fake_session):
    table = await fake_session.add_table(TableCreate(table_number=3, capacity=2))
    now = datetime.utcnow()

    await fake_session.add_reservation(
        ReservationCreate(
            table_id=table["id"], start_time=now, end_time=now + timedelta(hours=1)
        )
    )

    with pytest.raises(Exception, match="This table is already reserved at this time."):
        await fake_session.add_reservation(
            ReservationCreate(
                table_id=table["id"],
                start_time=now + timedelta(minutes=30),
                end_time=now + timedelta(hours=2),
            )
        )


@pytest.mark.asyncio
async def test_get_reservations(client, fake_session):
    res = await fake_session.get_reservations()
    assert isinstance(res, list)


@pytest.mark.asyncio
async def test_delete_reservation(client, fake_session):
    table = await fake_session.add_table(TableCreate(table_number=4, capacity=2))
    now = datetime.utcnow()
    res = await fake_session.add_reservation(
        ReservationCreate(
            table_id=table["id"], start_time=now, end_time=now + timedelta(hours=1)
        )
    )
    await fake_session.delete_reservation(res["id"])
    assert len(fake_session.reservations) == 0