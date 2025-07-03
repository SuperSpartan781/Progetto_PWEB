from sqlmodel import SQLModel, Field
from typing import Optional

class Event(SQLModel, table=True):
    """
    ORM per la tabella `events`.
    L'ID è auto-increment.
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

class EventCreate(SQLModel):
    """
    Payload per creare o aggiornare un evento.
    """
    title: str
    description: str
    date: str
    location: str

class EventRead(SQLModel):
    """
    Modello di risposta per un evento.
    """
    id: int
    title: str
    description: str
    date: str
    location: str