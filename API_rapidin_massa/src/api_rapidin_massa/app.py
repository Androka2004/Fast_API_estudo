from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from api_rapidin_massa.schemas import (
    DatabasePublico,
    Message,
    UserDB,
    UserPublic,
    UserSchema,
)

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def lendo_raiz():
    return {'message': 'Raios Funde'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def criando_usuario(user: UserSchema):
    usuario_id_incluso = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(usuario_id_incluso)

    return usuario_id_incluso


@app.get('/users/', response_model=DatabasePublico)
def trazendo_usuarios():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def atualizando_usuarios(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    usuario_id_incluso = UserDB(id=user_id, **user.model_dump())

    database[user_id - 1] = usuario_id_incluso

    return usuario_id_incluso


@app.delete('/users/{user_id}', response_model=Message)
def pulverizando_usuarios(user_id: int, password: str):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    if database[user_id - 1].password == password:
        database.pop(user_id - 1)

        return {'message': 'usuario deletado'}

    else:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Wrong password'
        )
