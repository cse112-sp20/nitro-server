from app import APP
import pytest

def test_home_route():
    client = APP.test_client()
    response = client.get('/')
    assert response.status_code == 200

@pytest.mark.parametrize('url, status_code',
                        [
                            ('/tasks', 401),
                            ('/delete', 401),
                            ('/complete', 401),
                        ])

def test_no_auth_token(url, status_code):
    client = APP.test_client()
    response = client.get(url)
    assert response.status_code == status_code
    response = client.delete('/clear_completed')
    assert response.status_code == status_code
    