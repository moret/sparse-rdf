from app.graph_parser import graph_parser
from app.index_parser import index_parser

from app.matrix_searcher import matrix_searcher
from app.db import Redis


class TestRedis(Redis):
    pass


def test_exist():
    assert matrix_searcher


def test_node_query_retrieves_column(monkeypatch):
    graph_parser.parse('tests/assets/paper.nt')

    test_redis = TestRedis()

    def mock_get_matrix_column():
        test_redis.get_matrix_column_invoked = True

    test_redis.get_matrix_column = mock_get_matrix_column
    monkeypatch.setattr(matrix_searcher, 'redis', test_redis)

    matrix_searcher.node_query()
    assert test_redis.get_matrix_column_invoked
