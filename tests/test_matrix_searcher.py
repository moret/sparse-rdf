from app.index_parser import index_parser

from app.matrix_searcher import matrix_searcher
from app.db import Redis
from app.db import redis
from tests.assets.paper import paper_nodes
from tests.assets.paper import paper_paths
from tests.assets.paper import paper_templates


class TestRedis(Redis):
    pass


def set_default_paper_matrix():
    redis.replace_all_nodes(paper_nodes)
    redis.replace_all_paths(paper_paths)
    redis.replace_all_templates(paper_templates)

    index_parser.generate_sparse_matrix()


def test_exist():
    assert matrix_searcher


def test_node_query_retrieves_column(monkeypatch):
    test_redis = TestRedis()

    def mock_get_column(node_index):
        test_redis.get_column_invoked = True
        return {}

    test_redis.get_column = mock_get_column
    monkeypatch.setattr(matrix_searcher, 'redis', test_redis)

    matrix_searcher.node_query(2)
    assert test_redis.get_column_invoked


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
    test_redis = TestRedis()

    def mock_get_row(path_index):
        test_redis.get_row_invoked = True
        return {}

    test_redis.get_row = mock_get_row
    monkeypatch.setattr(matrix_searcher, 'redis', test_redis)

    matrix_searcher.path_query(0)
    assert test_redis.get_row_invoked


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
