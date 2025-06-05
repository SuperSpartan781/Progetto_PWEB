from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

from app.data.db import get_session
from app.models.event import Event
# Se vuoi rendere disponibile solo parte dei campi, puoi definire un Pydantic model a parte;
# qui, per semplicità, restituiamo l'intero modello Event.

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/", response_model=List[Event])
def get_all_events(*, session: Session = Depends(get_session)) -> List[Event]:
    """
    GET /events
    Restituisce la lista di tutti gli eventi esistenti.
    """
    events = session.exec(select(Event)).all()
    return events

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Event)
def create_event(*, session: Session = Depends(get_session), event: Event) -> Event:
    """
    POST /events
    Crea un nuovo evento. Il JSON di input deve contenere:
      {
        "title": "string",
        "description": "string",
        "date": "2025-05-22T16:55:14.958Z",
        "location": "string"
      }
    Restituisce l'oggetto Event completo (compreso `id` generato).
    """
    db_event = Event(
        title=event.title,
        description=event.description,
        date=event.date,
        location=event.location
    )
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event

@router.get("/{event_id}", response_model=Event)
def get_event_by_id(
    *, session: Session = Depends(get_session), event_id: int
) -> Event:
    """
    GET /events/{id}
    Restituisce l'evento con ID = {event_id}.
    """
    db_event = session.get(Event, event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    return db_event

@router.put("/{event_id}", response_model=Event)
def update_event(
    *, session: Session = Depends(get_session),
    event_id: int,
    updated: Event
) -> Event:
    """
    PUT /events/{id}
    Aggiorna l'evento con ID = {event_id}. Il body deve contenere:
      {
        "title": "string",
        "description": "string",
        "date": "2025-05-22T16:57:12.873Z",
        "location": "string"
      }
    Se l'evento non esiste, restituisce 404.
    """
    db_event = session.get(Event, event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    # Aggiorno i campi
    db_event.title = updated.title
    db_event.description = updated.description
    db_event.date = updated.date
    db_event.location = updated.location

    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event_by_id(
    *, session: Session = Depends(get_session), event_id: int
):
    """
    DELETE /events/{id}
    Elimina l'evento con ID = {event_id}.
    (Opzionale secondo README)
    """
    db_event = session.get(Event, event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    session.delete(db_event)
    session.commit()
    return

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_events(*, session: Session = Depends(get_session)):
    """
    DELETE /events
    Elimina tutti gli eventi.
    (Opzionale secondo README)
    """
    # Se vuoi eliminare tutti gli eventi in un colpo:
    session.exec(select(Event).delete())
    session.commit()
    return

@router.post("/{event_id}/register", status_code=status.HTTP_201_CREATED)
def register_user_to_event(
    *,
    session: Session = Depends(get_session),
    event_id: int,
    # JSON di input: { "username": "string", "name": "string", "email": "string" }
    user_data: dict
):
    """
    POST /events/{id}/register
    Registra un utente a un evento. Il body deve contenere:
      {
        "username": "string",
        "name": "string",
        "email": "string"
      }
    → L’API interna dovrebbe:
      1. Verificare che l’evento con event_id esista (altrimenti 404).
      2. Verificare se l’utente esiste già nella tabella users:
         - Se non esiste → crearlo (con lo stesso JSON ricevuto).
         - Se esiste → ignorare (non cambiano i dati, o fare un upsert).
      3. Creare una riga nella tabella “registrations” (presumo esista già un modello e un router dedicato).
    Se la registrazione esiste già, potresti restituire 400 o 409.
    """
    # 1. Controlla che l’evento esista
    db_event = session.get(Event, event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )

    # 2. Controlla se l’utente esiste già
    from app.models.user import User  # import inline per evitare errori circolari
    username = user_data.get("username")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username mancante"
        )
    db_user = session.get(User, username)
    if not db_user:
        db_user = User(
            username=username,
            name=user_data.get("name", ""),
            email=user_data.get("email", "")
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

    # 3. Inserisci nella tabella registrations
    #    Presupponiamo che esista già un modello Registration e un router che banca questo inserimento.
    #    Se il modello Registration si chiama “Registration” e ha campi (username, event_id), 
    #    possiamo fare:
    from app.models.registration import Registration
    existing = session.exec(
        select(Registration)
        .where(Registration.username == username, Registration.event_id == event_id)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utente già registrato a questo evento"
        )
    reg = Registration(username=username, event_id=event_id)
    session.add(reg)
    session.commit()
    session.refresh(reg)

    return {"message": "Registrazione avvenuta con successo"}