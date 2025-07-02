from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Event(SQLModel, table=True):
    """
    ORM per la tabella `events`.
    L'ID viene generato automaticamente dal DB (INTEGER AUTOINCREMENT).
    """
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="ID univoco dell'evento (auto-increment)"
    )
    title: str = Field(
        nullable=False,
        description="Titolo dell'evento"
    )
    description: str = Field(
        nullable=False,
        description="Descrizione dell'evento"
    )
    date: str = Field(
        nullable=False,
        description="Data e ora dell'evento"
    )
    location: str = Field(
        nullable=False,
        description="Luogo dell'evento"
    )
