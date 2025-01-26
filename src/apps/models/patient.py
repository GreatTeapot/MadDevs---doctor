from datetime import date
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from common.models.base import Base
from common.models.mixins import CreatedUpdatedMixin


class Patient(Base, CreatedUpdatedMixin):

    id: Mapped[Optional[int]] = mapped_column(sa.Integer, primary_key=True, index=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(nullable=False)
    diagnoses: Mapped[Optional[list[str]]] = mapped_column(sa.String, nullable=True)
    deleted: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
