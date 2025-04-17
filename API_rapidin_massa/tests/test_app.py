from http import HTTPStatus


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
    assert response.json() == {
        'users': [
            {
                'username': 'Raios Funde',
                'id': 1,
                'email': 'test@test.com',
            }
        ]
    }


def test_alterador_usuario(client):
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


def test_pulverizar_teste(client):
    response = client.delete('/users/1', params={'password': '12345'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'usuario deletado'}
