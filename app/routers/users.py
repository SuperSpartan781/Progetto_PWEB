from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, delete

from app.data.db import get_session
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=Sequence[User])
def get_all_users(
    *,
    session: Session = Depends(get_session)
) -> Sequence[User]:
    """
    GET /users
    Restituisce la lista di tutti gli utenti.
    """
    users = session.exec(select(User)).all()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(
    *,
    session: Session = Depends(get_session),
    user: User
) -> User:
    """
    POST /users
    Crea un utente. Il JSON di input deve contenere:
        {
          "username": "string",
          "name": "string",
          "email": "string"
        }
    Se l'username esiste già, restituisce 400 BadRequest.
    """
    existing = session.get(User, user.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{user.username}' già presente"
        )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_users(*, session: Session = Depends(get_session)):
    """
    DELETE /users
    Elimina tutti gli utenti.
    """
    session.execute(delete(User))
    session.commit()
    return


@router.get("/{username}", response_model=User)
def get_user_by_username(
    *,
    session: Session = Depends(get_session),
    username: str
) -> User:
    """
    GET /users/{username}
    Restituisce l'utente con username specificato.
    """
    user = session.get(User, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente non trovato"
        )
    return user


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_username(
    *,
    session: Session = Depends(get_session),
    username: str
):
    """
    DELETE /users/{username}
    Elimina l'utente specificato.
    """
    user = session.get(User, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente non trovato"
        )
    session.delete(user)
    session.commit()
    return