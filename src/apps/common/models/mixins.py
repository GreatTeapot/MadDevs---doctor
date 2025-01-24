from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class CreatedUpdatedMixin:
    """Common model for specifying creation and update timestamps."""

    created_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)