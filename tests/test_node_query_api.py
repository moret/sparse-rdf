import json

from tornado.httpclient import HTTPClient

from util.test import set_default_paper_matrix

from tests.assets.paper import paper_nodes


def url(param):
    return 'http://lvh.me:9999/node-query/%s' % param


def test_pub1_selected():
    set_default_paper_matrix()
    response = HTTPClient().fetch(url('pub1'))
    assert 200 == response.code
    assert paper_nodes[3] == json.loads(response.body)['selected_node']
