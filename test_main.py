from urler import create_app


def test_shorten(client):
    response = client.get('/')
    assert b'Create' in response.data
