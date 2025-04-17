import pytest
from fastapi.testclient import TestClient

from api_rapidin_massa.app import app


@pytest.fixture
def client():
    return TestClient(app)
