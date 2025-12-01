from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    registry,
)

# registry, record thing that will be mapped between python and database
table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    # init="False" set that the database will manage the id creation
    username: Mapped[str] = mapped_column(unique=True)
    # Mapped handle the relation between, for example, VARCHAR to String
    email: Mapped[str] = mapped_column(unique=True)
    # only one email registered
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    # server_default = func.now guarantee that the created_at fiel is
    # filled with the datetime when the transaction appear in the database
