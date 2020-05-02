from urler import create_app


def test_shorten(client):
    response = client.get('/')
    assert b'Home' in response.data
