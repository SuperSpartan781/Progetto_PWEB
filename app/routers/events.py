from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.data.db import get_session
from app.models.event import Event, EventCreate, EventRead
from app.models.registration import Registration

router = APIRouter(prefix="/events", tags=["events"])

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=EventRead
)
def create_event(
    *,
    session: Session = Depends(get_session),
    event_in: EventCreate
) -> Event:
    db_event = Event(**event_in.dict())
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event

@router.get(
    "/",
    response_model=Sequence[EventRead]
)
def get_all_events(
    *,
    session: Session = Depends(get_session)
) -> Sequence[Event]:
    return session.exec(select(Event)).all()

@router.put(
    "/{event_id}",
    response_model=EventRead
)
def update_event(
    *,
    session: Session = Depends(get_session),
    event_id: int,
    updated: EventCreate
) -> Event:
    db_event = session.get(Event, event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    for field, value in updated.dict().items():
        setattr(db_event, field, value)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event

@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_event_by_id(
    *,
    session: Session = Depends(get_session),
    event_id: int
) -> None:
    db_event = session.get(Event, event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    for reg in session.exec(select(Registration)).all():
        if reg.event_id == event_id:
            session.delete(reg)
    session.delete(db_event)
    session.commit()

@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_all_events(
    *,
    session: Session = Depends(get_session),
) -> None:
    """
    Elimina tutti gli eventi e tutte le registrazioni.
    """
    for reg in session.exec(select(Registration)).all():
        session.delete(reg)
    for ev in session.exec(select(Event)).all():
        session.delete(ev)
    session.commit()
