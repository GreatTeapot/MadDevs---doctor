from typing import Self

from common.unit_of_works.base import BaseUnitOfWork
from modules.repositories.patients.repository import  PatientRepository


class PatientUOW(BaseUnitOfWork):
    """Class for working with patient transactions."""

    async def __aenter__(self) -> Self:
        """Patient context manager entry method."""
        await super().__aenter__()
        self.repo = PatientRepository(self._session)
        return self
