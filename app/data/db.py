from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
import os
from faker import Faker
from app.config import config

# Importa tutti i modelli ORM in modo che SQLModel.metadata sappia crearne le tabelle
from app.models.user import User       # NOQA
from app.models.event import Event     # NOQA
from app.models.registration import Registration  # NOQA


sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)


def init_database() -> None:
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)

    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:

            for _ in range(5):
                user = User(
                    username=f.user_name(),
                    name=f.name(),
                    email=f.email()
                )
                session.add(user)
            session.commit()

            for _ in range(5):
                event = Event(
                    title=f.sentence(nb_words=3),
                    description=f.paragraph(nb_sentences=2),
                    date=f.date_time_this_year(),
                    location=f.city()
                )
                session.add(event)
            session.commit()

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]