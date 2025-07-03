from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.data.db import get_session
from app.models.user import User, UserCreate, UserRead
from app.models.registration import Registration

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead
)
def create_user(
    *,
    session: Session = Depends(get_session),
    user_in: UserCreate
) -> User:
    if session.get(User, user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{user_in.username}' già presente"
        )
    db_user = User(**user_in.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get(
    "/",
    response_model=Sequence[UserRead]
)
def get_all_users(
    *,
    session: Session = Depends(get_session)
) -> Sequence[User]:
    return session.exec(select(User)).all()

@router.delete(
    "/{username}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_by_username(
    *,
    session: Session = Depends(get_session),
    username: str
) -> None:
    user = session.get(User, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente non trovato"
        )
    for reg in session.exec(select(Registration)).all():
        if reg.username == username:
            session.delete(reg)
    session.delete(user)
    session.commit()

@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_all_users(
    *,
    session: Session = Depends(get_session),
) -> None:
    """
    Elimina tutti gli utenti e tutte le registrazioni.
    """
    for reg in session.exec(select(Registration)).all():
        session.delete(reg)
    for u in session.exec(select(User)).all():
        session.delete(u)
    session.commit()
