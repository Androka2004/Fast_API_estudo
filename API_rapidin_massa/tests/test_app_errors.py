from http import HTTPStatus


def test_erro_criador_username(client, user):
    # TESTE USERNAME JÁ EXISTENTE CREATE
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


def test_erro_criador_email(client, user):
    # TESTE EMAIL JA EXISTENTE CREATE
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


def test_erro_enviar_token(client, user):
    # TESTE ERRO AUTENTICAÇÃO
    response = client.post(
        '/token',
        data={'username': user.email, 'password': 'raios funde'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'email ou senha incorreta'}


def test_erro_pulverizar_mano(client, user, token):
    # TESTE DELETE SEM PERMISSÃO
    response = client.delete(
        '/users/12',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Permissão Negada'}


def test_erro_atualizador_nao_autorizado(client, user):
    # TESTE DELETE DIFERENTE DO USER AUTENTICADO
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': 'Bearer token invalido'},
        json={
            'username': 'fausto',
            'password': '12345',
            'email': 'lomba@test.com',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Credenciais Invalidas'}


def test_erro_sem_mano(client, user, token):
    # TESTE DE USAR TOKEN DE USER DELETADO
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Credenciais Invalidas'}


def test_erro_atualizador_negado(client, user, token):
    #TESTE ATUALIZAR USER USER DIFERENTE DO AUTENTICADO
    response = client.put(
        '/users/12',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Funde Raios',
            'password': '12345',
            'email': 'lomba@test.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Permissão negada'}


def test_erro_atualizador_unique(client, user, token):
    # TESTE ATUALIZAR COM DADOS UNICOS QUE JA EXISTEM
    email_copy = 'test@test.com'
    client.post(
        '/users/',
        json={
            'username': 'Funde Raios',
            'password': '12345',
            'email': email_copy,
        },
    )

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Funde Raios',
            'password': '12345',
            'email': email_copy,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


# def test_erro_atualizador_id(client, user, token):
#     response = client.put(
#         '/users/12',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'username': 'Funde Raios',
#             'password': '12345',
#             'email': 'lomba@test.com',
#         },
#     )

#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'Mano not found'}


# def test_erro_atualizador_username(client, user, token):
#     client.post(
#         '/users',
#         json={
#             'username': 'fausto',
#             'email': 'fausto@example.com',
#             'password': 'secret',
#         },
#     )

#     response = client.put(
#         f'/users/{user.id}',
#         json={
#             'username': 'fausto',
#             'password': '12345',
#             'email': 'lomba@test.com',
#         },
#     )

#     assert response.status_code == HTTPStatus.CONFLICT
#     assert response.json() == {'detail': 'Username or Email already exists'}
