from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from api_rapidin_massa.database import get_session
from api_rapidin_massa.models import Mano
from api_rapidin_massa.schemas import (
    DatabasePublico,
    Message,
    Token,
    UserPublic,
    UserSchema,
)
from api_rapidin_massa.security import (
    analisar_passespada,
    gerador_token_acesso,
    get_passespada_hash,
    puxar_mano_atual,
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
        username=user.username,
        password=get_passespada_hash(user.password),
        email=user.email,
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
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user=Depends(puxar_mano_atual),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Permissão negada'
        )

    db_confirm_unique = session.scalar(
        select(Mano).where(
            (Mano.username == user.username) | (Mano.email == user.email)
        )
    )
    if db_confirm_unique and db_confirm_unique.id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_passespada_hash(user.password)
    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete('/users/{user_id}', response_model=Message)
def pulverizando_usuarios(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(puxar_mano_atual),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Permissão Negada'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'Mano deleted'}


@app.post('/token', response_model=Token)
def autenticar_token_acesso(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(Mano).where(Mano.email == form_data.username))

    if not user or not analisar_passespada(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='email ou senha incorreta',
        )

    acess_token = gerador_token_acesso({'sub': user.email})

    return {'acess_token': acess_token, 'token_type': 'Bearer'}
