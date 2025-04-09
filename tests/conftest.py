import pytest_asyncio
from httpx import AsyncClient
from fastapi import Depends
from app.main import app


# Фейковая сессия
class FakeSession:
    def __init__(self):
        self.tables = []
        self.reservations = []
        self._table_id = 1
        self._res_id = 1

    async def add_table(self, data):
        table = data.model_dump()
        table["id"] = self._table_id
        self._table_id += 1
        self.tables.append(table)
        return table

    async def get_tables(self):
        return self.tables

    async def delete_table(self, table_id):
        self.tables = [t for t in self.tables if t["id"] != table_id]
        self.reservations = [r for r in self.reservations if r["table_id"] != table_id]

    async def add_reservation(self, data):
        # Конфликт по времени
        for r in self.reservations:
            if r["table_id"] == data.table_id and not (
                    data.end_time <= r["start_time"] or data.start_time >= r["end_time"]
            ):
                raise Exception("This table is already reserved at this time.")

        reservation = data.model_dump()
        reservation["id"] = self._res_id
        self._res_id += 1
        self.reservations.append(reservation)
        return reservation

    async def get_reservations(self):
        return self.reservations

    async def delete_reservation(self, reservation_id):
        self.reservations = [r for r in self.reservations if r["id"] != reservation_id]


@pytest_asyncio.fixture
def fake_session():
    return FakeSession()


@pytest_asyncio.fixture
def override_dependencies(fake_session):
    async def _get_session():
        return fake_session

    app.dependency_overrides.clear()
    app.dependency_overrides[Depends] = lambda: _get_session()

    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(override_dependencies):
    async with AsyncClient(base_url="http://test") as ac:
        yield ac
