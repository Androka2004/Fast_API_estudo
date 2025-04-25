from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from api_rapidin_massa.database import get_session
from api_rapidin_massa.models import Mano

pwd_cenario = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'your-secret-Key'
ALGORITHM = 'HS256'
ACESS_TOKEN_EXPIRE_MINUTES = 30


def get_passespada_hash(password: str):
    return pwd_cenario.hash(password)


def analisar_passespada(plain_password: str, hashed_password: str):
    return pwd_cenario.verify(plain_password, hashed_password)


def gerador_token_acesso(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def puxar_mano_atual(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Credenciais Invalidas',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user_db = session.scalar(select(Mano).where(Mano.email == username))
    if not user_db:
        raise credentials_exception

    return user_db
