# app/models/user.py

from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    """
    ORM per la tabella `users`.
    La chiave primaria è `username`, stringa.
    """
    username: str = Field(
        primary_key=True,  # è la PK
        index=True,
        description="Username univoco dell'utente"
    )
    name: str = Field(
        nullable=False,
        description="Nome completo dell'utente"
    )
    email: str = Field(
        nullable=False,
        description="Email dell'utente"
    )
