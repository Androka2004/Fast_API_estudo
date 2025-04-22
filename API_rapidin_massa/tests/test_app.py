from http import HTTPStatus

from api_rapidin_massa.schemas import UserPublic


def test_ler_root_ok(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Raios Funde'}


def test_criador_de_usuario(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Raios Funde',
            'password': '12345',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Raios Funde',
        'id': 1,
        'email': 'test@test.com',
    }


def test_leitor_database(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_leitor_database_com_manos(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_alterador_usuario(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'Funde Raios',
            'password': '12345',
            'email': 'lomba@test.com',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Funde Raios',
        'id': 1,
        'email': 'lomba@test.com',
    }


def test_pulverizar_mano(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Mano deleted'}


def test_criador_erro_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Raios Funde',
            'password': '12345',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'User already exists'}


def test_criador_erro_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Funde Raios',
            'password': '12345',
            'email': 'teste@mail.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_atualizador_erro_id(client, user):
    response = client.put(
        '/users/12',
        json={
            'username': 'Funde Raios',
            'password': '12345',
            'email': 'lomba@test.com',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Mano not found'}


def test_atualizador_erro_username(client, user):
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response = client.put(
        '/users/1',
        json={
            'username': 'fausto',
            'password': '12345',
            'email': 'lomba@test.com',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_erro_pulverizar_mano(client, user):
    response = client.delete('/users/12')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Mano not found'}
