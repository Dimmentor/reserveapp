from fastapi import HTTPException, status


class ReservationConflictException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Столик уже забронирован на это время."
        )

class TableNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Столика с таким id не существует."
        )