from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column




class IDMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


class CreatedUpdatedMixin:
    """Common model for specifying creation and update timestamps."""

    created_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)