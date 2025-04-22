from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from api_rapidin_massa.database import get_session
from api_rapidin_massa.models import Mano
from api_rapidin_massa.schemas import (
    DatabasePublico,
    Message,
    UserPublic,
    UserSchema,
)

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def lendo_raiz():
    return {'message': 'Raios Funde'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def criando_usuario(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(Mano).where(
            (Mano.username == user.username) | (Mano.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, detail='User already exists'
            )
        elif db_user.email == user.email:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, detail='Email already exists'
            )

    db_user = Mano(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=DatabasePublico)
def trazendo_usuarios(
    limit: int = 10, skip: int = 0, session: Session = Depends(get_session)
):
    resultado = session.scalars(select(Mano).offset(skip).limit(limit))
    return {'users': resultado}


@app.put('/users/{user_id}', response_model=UserPublic)
def atualizando_usuarios(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(Mano).where(Mano.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Mano not found'
        )

    db_confirm_unique = session.scalar(
        select(Mano).where(
            (Mano.username == user.username) | (Mano.email == user.email)
        )
    )
    if db_confirm_unique and db_confirm_unique.id != db_user.id:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def pulverizando_usuarios(
    user_id: int, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(Mano).where(Mano.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Mano not found'
        )

    session.delete(db_user)
    session.commit

    return {'message': 'Mano deleted'}
