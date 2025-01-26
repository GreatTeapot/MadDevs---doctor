from fastapi import HTTPException
from modules.const.patients import const as exc


class PatientNotFoundException(HTTPException):
    """Exception raised when a patient is not found in the database."""

    def __init__(self) -> None:
        self.status_code = 404
        self.detail = exc.PATIENT_NOT_FOUND
        super().__init__(status_code=self.status_code, detail=self.detail)


class PatientBadRequestException(HTTPException):
    """Exception raised when a patient request is invalid."""

    def __init__(self) -> None:
        self.status_code = 400
        self.detail = exc.PATIENT_BAD_REQUEST
        super().__init__(status_code=self.status_code, detail=self.detail)


class PatientConflictException(HTTPException):
    """Exception raised when there is a conflict related to a patient."""

    def __init__(self) -> None:
        self.status_code = 409
        self.detail = exc.PATIENT_CONFLICT
        super().__init__(status_code=self.status_code, detail=self.detail)


class PatientUnauthorizedException(HTTPException):
    """Exception raised for unauthorized access related to a patient."""

    def __init__(self) -> None:
        self.status_code = 401
        self.detail = exc.UNAUTHORIZED_ACCESS
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=self.headers
        )


class PatientForbiddenException(HTTPException):
    """Exception raised for forbidden access related to a patient."""

    def __init__(self, detail: str) -> None:
        self.status_code = 403
        self.detail = detail
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=self.headers
        )
