import pytest
from datetime import datetime
from app.schemas.table_schema import TableCreate
from app.schemas.reservation_schema import ReservationCreate


@pytest.mark.asyncio
async def test_create_table(fake_session):
    payload = TableCreate(name="Столик 1", seats=4, location="Первый этаж")
    table = await fake_session.add_table(payload)

    assert table["id"] == 1
    assert table["seats"] == 4
    assert table["name"] == "Столик 1"
    assert table["location"] == "Первый этаж"


@pytest.mark.asyncio
async def test_get_tables(fake_session):
    tables = await fake_session.get_tables()
    assert isinstance(tables, list)


@pytest.mark.asyncio
async def test_delete_table(fake_session):
    await fake_session.add_table(TableCreate(name="Столик 99", seats=2, location="Второй этаж"))
    await fake_session.delete_table(1)
    assert len(fake_session.tables) == 0


@pytest.mark.asyncio
async def test_create_reservation(fake_session):
    table = await fake_session.add_table(TableCreate(name="Столик 2", seats=2, location="Третий этаж"))

    reservation_time = "2023-10-01T18:00:00"

    payload = ReservationCreate(
        customer_name="Дмитрий",
        table_id=table["id"],
        reservation_time=reservation_time,
        duration_minutes=60
    )

    reservation = await fake_session.add_reservation(payload)

    assert reservation["id"] == 1


@pytest.mark.asyncio
async def test_conflict_reservation(fake_session):
    table = await fake_session.add_table(TableCreate(name="Столик 3", seats=2, location="Четвертый этаж"))

    reservation_time = datetime.fromisoformat("2023-10-01T18:00:00")

    await fake_session.add_reservation(
        ReservationCreate(
            customer_name="Дмитрий",
            table_id=table["id"],
            reservation_time=reservation_time,
            duration_minutes=60
        )
    )

    with pytest.raises(Exception, match="Столик уже забронирован на это время."):
        await fake_session.add_reservation(
            ReservationCreate(
                customer_name="Александр",
                table_id=table["id"],
                reservation_time=reservation_time,
                duration_minutes=30
            )
        )


@pytest.mark.asyncio
async def test_get_reservations(fake_session):
    res = await fake_session.get_reservations()
    assert isinstance(res, list)


@pytest.mark.asyncio
async def test_delete_reservation(fake_session):
    table = await fake_session.add_table(TableCreate(name="Столик 4", seats=2, location="Пятый этаж"))

    reservation_time = "2023-10-01T18:00:00"

    res = await fake_session.add_reservation(
        ReservationCreate(
            customer_name="Дмитрий",
            table_id=table["id"],
            reservation_time=reservation_time,
            duration_minutes=60
        )
    )

    await fake_session.delete_reservation(res["id"])

    assert len(fake_session.reservations) == 0
