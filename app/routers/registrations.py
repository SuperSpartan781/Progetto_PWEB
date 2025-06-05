# app/routers/registrations.py

from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.data.db import get_session
from app.models.registration import Registration

router = APIRouter(prefix="/registrations", tags=["registrations"])


@router.get("/", response_model=Sequence[Registration])
def get_all_registrations(
    *,
    session: Session = Depends(get_session)
) -> Sequence[Registration]:
    """
    GET /registrations
    Restituisce tutte le registrazioni presenti nella tabella.
    """
    registrations = session.exec(select(Registration)).all()
    return registrations


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_registration(
    *,
    session: Session = Depends(get_session),
    username: str = Query(..., description="Username dell'utente registrato"),
    event_id: int = Query(..., description="ID dell'evento a cui l'utente è registrato")
):
    """
    DELETE /registrations?username={username}&event_id={event_id}
    Elimina la registrazione corrispondente ai parametri forniti.
    Se non viene trovata alcuna riga, restituisce 404 Not Found.
    """
    statement = select(Registration).where(
        Registration.username == username,
        Registration.event_id == event_id
    )
    existing = session.exec(statement).first()
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Registrazione non trovata per username '{username}' ed evento ID={event_id}"
        )

    session.delete(existing)
    session.commit()
    return
