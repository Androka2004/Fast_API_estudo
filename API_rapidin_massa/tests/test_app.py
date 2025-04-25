from http import HTTPStatus

from api_rapidin_massa.schemas import UserPublic

# TESTES DE SUCESSO ###


def test_ler_root_ok(client):
    # TESTE RAIZ SERVIDOR
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Raios Funde'}


def test_criador_de_usuario(client):
    # TESTE INSERT PARA MODELO MANO
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
    # TESTE DATABASE VAZIO
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_leitor_database_com_manos(client, user):
    # TESTE DATABASE POPULADO
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_enviador_token(client, user):
    # TESTE PARA CONFIMAR TOKEN AUTENTICAÇÃO
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'acess_token' in token


def test_alterador_usuario(client, user, token):
    # TESTE ALTERAR DADO DA TABELA MANO
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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


def test_pulverizar_mano(client, user, token):
    # TESTE PARA DELETAR DE TABELA MANO
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Mano deleted'}


