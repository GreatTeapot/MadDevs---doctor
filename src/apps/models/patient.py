from datetime import date
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from common.models.base import Base
from common.models.mixins import CreatedUpdatedMixin, IDMixin


class Patient(Base, CreatedUpdatedMixin, IDMixin):

    date_of_birth: Mapped[Optional[date]] = mapped_column(nullable=False)
    diagnoses: Mapped[Optional[list[str]]] = mapped_column(sa.ARRAY(sa.String), nullable=True)
    deleted: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
