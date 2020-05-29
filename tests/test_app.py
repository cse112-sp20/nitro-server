from app import APP
import pytest

def test_home_route():
    client = APP.test_client()
    response = client.get('/')
    assert response.status_code == 200
