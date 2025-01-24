from datetime import datetime
from types import NoneType
from typing import Optional, TypeAlias, Union
from uuid import UUID

import sqlalchemy as sa
from modules.exceptions.users import user as exc

from common.enums.role import UserRoleEnum
from common.repositories.mixins import PaginatedPageRepository
from common.schemas.filters.mixins import DataRangeBaseFilterSchema
from models.patient import Patient

RegisterData: TypeAlias = dict[str, Union[str, datetime, bool, UserRoleEnum, NoneType, UUID]]
EditData: TypeAlias = dict[str, Union[UUID, str, bool, datetime, int, None, UserRoleEnum]]


class PatientRepository(PaginatedPageRepository):
    """Repository for patients"""

    model = Patient

    def __get_stmt_for_method_list(self) -> sa.Select:
        """Get the query for the list method."""
        stmt = (
            sa.select(self.model)
            .where(self.model.deleted.__eq__(False))
        )
        return stmt

    def __is_there_search_string(
        self, stmt: sa.Select, filters: DataRangeBaseFilterSchema
    ) -> sa.Select:
        """Check for the existence of a search string."""
        if filters.search_string:
            stmt = stmt.filter(
                sa.or_(
                    self.model.date_of_birth.ilike(f"%{filters.search_string}"),
                    self.model.diagnoses.ilike(f"%{filters.search_string}"),
                ))
        return stmt

    async def get_all(
        self, filters: DataRangeBaseFilterSchema) \
            -> tuple[int, Optional[sa.ScalarResult]]:
        """Get all patients with filtering """
        stmt = self.__get_stmt_for_method_list()
        stmt = self.__is_there_search_string(stmt, filters)
        stmt = self._is_there_start_and_end_date(stmt, filters)
        count_records = await self._get_count_records(stmt)
        records = await self._is_there_records(count_records, stmt, filters)
        return count_records, records

