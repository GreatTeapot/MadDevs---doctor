from typing import Self

from common.unit_of_works.base import BaseUnitOfWork
from modules.repositories.users.user_rep import UserRepository


class UserUOW(BaseUnitOfWork):
    """Class for working with profile transactions."""

    async def __aenter__(self) -> Self:
        """Profile context manager entry method."""
        await super().__aenter__()
        self.repo = UserRepository(self._session)
        return self
