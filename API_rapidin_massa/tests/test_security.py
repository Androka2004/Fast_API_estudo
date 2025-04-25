from jwt import decode

from api_rapidin_massa.security import (
    ALGORITHM,
    SECRET_KEY,
    gerador_token_acesso,
)


def test_jwt():
    data = {'sub': 'test@test.com'}
    result = gerador_token_acesso(data)

    decoded = decode(result, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['sub'] == data['sub']
    assert decoded['exp']
