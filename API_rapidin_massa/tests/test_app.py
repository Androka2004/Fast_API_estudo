from http import HTTPStatus

from fastapi.testclient import TestClient

from api_rapidin_massa.app import app


def test_ler_root_ok():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Raios Funde'}
