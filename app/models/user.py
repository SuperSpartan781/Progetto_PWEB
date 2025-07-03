from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    """
    ORM per la tabella `users`.
    La chiave primaria è `username`.
    """
    username: str = Field(
        primary_key=True,
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

class UserCreate(SQLModel):
    """
    Payload per creare un nuovo utente.
    """
    username: str
    name: str
    email: str

class UserRead(SQLModel):
    """
    Modello di risposta per un utente.
    """
    username: str
    name: str
    email: str