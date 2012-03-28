from app.index_parser import index_parser
from app.db import Redis


class TestRedis(Redis):
    pass


def test_exists():
    assert index_parser


def test_get_tuple_tries_to_get_template_index(monkeypatch):
    test_redis = TestRedis()

    def mock_get_template_index(template):
        test_redis.get_template_index_invoked = True
        test_redis.template = template

    test_redis.get_template_index = mock_get_template_index
    monkeypatch.setattr(index_parser, 'redis', test_redis)

    index_parser.get_tuple('nod1', ['nod1', 'nod2'])
    assert test_redis.get_template_index_invoked


def test_generate_sparse_matrix_clears_old_sparse_matrix(monkeypatch):
    test_redis = TestRedis()

    def mock_clear_sparse_matrix():
        test_redis.clear_sparse_matrix_invoked = True

    test_redis.clear_sparse_matrix = mock_clear_sparse_matrix
    monkeypatch.setattr(index_parser, 'redis', test_redis)

    index_parser.generate_sparse_matrix()
    assert test_redis.clear_sparse_matrix_invoked


def test_generate_sparse_matrix_loops_all_paths(monkeypatch):
    test_redis = TestRedis()
    test_redis.get_path_invocations = 0

    def mock_get_path(*args, **kwargs):
        test_redis.get_path_invocations += 1
        return super(TestRedis, test_redis).get_path(*args, **kwargs)

    test_redis.get_path = mock_get_path
    monkeypatch.setattr(index_parser, 'redis', test_redis)

    nodes = ['nod1', 'nod2', 'nod3']
    paths = [['nod1', 'edge1', 'nod2'], ['nod2', 'edge2', 'nod3']]
    templates = [['nod1', 'nod2'], ['nod2', 'nod3']]
    test_redis.replace_all_nodes(nodes)
    test_redis.replace_all_paths(paths)
    test_redis.replace_all_templates(templates)

    index_parser.generate_sparse_matrix()
    assert len(paths) == test_redis.get_path_invocations


def test_generate_sparse_matrix_loops_all_nodes_for_each_path(monkeypatch):
    test_redis = TestRedis()
    test_redis.get_node_invocations = 0

    def mock_get_node(*args, **kwargs):
        test_redis.get_node_invocations += 1
        return super(TestRedis, test_redis).get_node(*args, **kwargs)

    test_redis.get_node = mock_get_node
    monkeypatch.setattr(index_parser, 'redis', test_redis)

    nodes = ['nod1', 'nod2', 'nod3']
    paths = [['nod1', 'edge1', 'nod2'], ['nod2', 'edge2', 'nod3']]
    templates = [['nod1', 'nod2'], ['nod2', 'nod3']]
    test_redis.replace_all_nodes(nodes)
    test_redis.replace_all_paths(paths)
    test_redis.replace_all_templates(templates)

    index_parser.generate_sparse_matrix()
    assert len(paths) * len(nodes) == test_redis.get_node_invocations
