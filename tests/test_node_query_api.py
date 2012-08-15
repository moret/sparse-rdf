import json

from tornado.httpclient import HTTPClient

from tests.assets.paper import paper_nodes
from tests.assets.paper import paper_paths
from tests.assets.paper import paper_templates

from app.index_parser import index_parser
from app.persistance import db


def url(param):
    return 'http://lvh.me:9999/node-query/%s' % param


def set_default_paper_matrix():
    db.replace_all_nodes(paper_nodes)
    db.replace_all_paths(paper_paths)
    db.replace_all_templates(paper_templates)

    index_parser.generate_sparse_matrix()


def test_pub1_selected():
    set_default_paper_matrix()
    pub1 = '<http://demo.com/publications.rdf#pub1>'
    response = HTTPClient().fetch(url('pub1'))
    assert 200 == response.code
    assert pub1 == json.loads(response.body)['selected_node']
