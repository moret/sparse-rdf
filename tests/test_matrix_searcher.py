from app.index_parser import index_parser

from app.matrix_searcher import matrix_searcher
from app.persistance import db
from tests.assets.paper import paper_nodes
from tests.assets.paper import paper_paths
from tests.assets.paper import paper_templates


def set_default_paper_matrix():
    db.replace_all_nodes(paper_nodes)
    db.replace_all_paths(paper_paths)
    db.replace_all_templates(paper_templates)

    index_parser.generate_sparse_matrix()


def mock_method_with_counter(monkeypatch, obj, method_name):
    counters = {'invocations': 0}
    proxied = getattr(obj, method_name)

    def mock(*args, **kwargs):
        counters['invocations'] += 1
        return proxied(*args, **kwargs)

    monkeypatch.setattr(obj, method_name, mock)
    return counters


def test_exist():
    assert matrix_searcher


def test_node_query_retrieves_column(monkeypatch):
    counters = mock_method_with_counter(monkeypatch, db, 'get_column')

    matrix_searcher.node_query(2)
    assert 1 == counters['invocations']


def test_node_query_researcher_retrieves_expected_subset():
    set_default_paper_matrix()
    paths = matrix_searcher.node_query(2)
    assert 2 == len(paths)
    assert paper_paths[6] in paths
    assert paper_paths[9] in paths


def test_final_node_query_researcher_retrieves_expected_subset():
    set_default_paper_matrix()
    paths = matrix_searcher.final_node_query(2)
    assert 2 == len(paths)
    assert paper_paths[6] in paths
    assert paper_paths[9] in paths


def test_node_query_pub1_retrieves_expected_subset():
    set_default_paper_matrix()
    paths = matrix_searcher.node_query(3)
    assert 5 == len(paths)
    assert paper_paths[0] in paths
    assert paper_paths[2] in paths
    assert paper_paths[4] in paths
    assert paper_paths[5] in paths
    assert paper_paths[6] in paths


def test_final_node_query_pub1_retrieves_expected_subset():
    set_default_paper_matrix()
    paths = matrix_searcher.final_node_query(3)
    assert 0 == len(paths)


def test_path_query_retrieves_column(monkeypatch):
    counters = mock_method_with_counter(monkeypatch, db, 'get_row')

    matrix_searcher.path_query(0)
    assert 1 == counters['invocations']


def test_path_query_path0_retrieves_expected_subset():
    set_default_paper_matrix()
    nodes = matrix_searcher.path_query(0)
    assert 2 == len(nodes)
    assert paper_nodes[3] in nodes
    assert paper_nodes[5] in nodes


def test_path_query_path4_retrieves_expected_subset():
    set_default_paper_matrix()
    nodes = matrix_searcher.path_query(4)
    assert 3 == len(nodes)
    assert paper_nodes[3] in nodes
    assert paper_nodes[6] in nodes
    assert paper_nodes[7] in nodes
