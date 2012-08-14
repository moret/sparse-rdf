from tornado.httpclient import HTTPClient


def test_exists():
    response = HTTPClient().fetch('http://lvh.me:9999/')
    assert 200 == response.code


def test_home_has_generic_message():
    response = HTTPClient().fetch('http://lvh.me:9999/')
    assert 'for the future' in response.body
