from fastapi import HTTPException, status

class ReservationConflictException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="This time slot is already reserved for the selected table."
        )