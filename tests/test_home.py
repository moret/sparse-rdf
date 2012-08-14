from tornado.httpclient import HTTPClient


def test_exists():
    response = HTTPClient().fetch('http://lvh.me:9999/')
    assert 200 == response.code
