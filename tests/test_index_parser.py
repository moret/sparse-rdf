from app.graph_parser import graph_parser
from app.index_parser import index_parser
from app.persistance import db

from tests.assets.paper import paper_nodes
from tests.assets.paper import paper_paths
from tests.assets.paper import paper_templates
from tests.assets.paper import paper_matrix


def mock_method_with_counter(monkeypatch, obj, method_name):
    counters = {'invocations': 0}
    proxied = getattr(obj, method_name)

    def mock(*args, **kwargs):
        counters['invocations'] += 1
        return proxied(*args, **kwargs)

    monkeypatch.setattr(obj, method_name, mock)
    return counters


def create_indexes():
    nodes = ['nod1', 'nod2', 'nod3']
    paths = [['nod1', 'edge1', 'nod2'], ['nod2', 'edge2', 'nod3']]
    templates = [['nod1', 'nod2'], ['nod2', 'nod3']]
    db.replace_all_nodes(nodes)
    db.replace_all_paths(paths)
    db.replace_all_templates(templates)

    return nodes, paths, templates


def test_exists():
    assert index_parser


def test_get_tuple_tries_to_get_template_index(monkeypatch):
    counters = mock_method_with_counter(monkeypatch, db, 'get_template_index')

    index_parser.get_tuple('nod1', ['nod1', 'nod2'])
    assert 1 == counters['invocations']


def test_get_tuple_returns_size_three_list():
    graph_parser.parse('tests/assets/paper.nt')
    graph_parser.persist_index()
    t = index_parser.get_tuple('nod1', ['nod1', 'nod2'])
    assert isinstance(t, list)
    assert 3 == len(t)


def test_generate_sparse_matrix_clears_old_sparse_matrix(monkeypatch):
    counters = mock_method_with_counter(monkeypatch, db, 'clear_sparse_matrix')

    index_parser.generate_sparse_matrix()
    assert 1 == counters['invocations']


def test_generate_sparse_matrix_loops_all_paths(monkeypatch):
    counters = mock_method_with_counter(monkeypatch, db, 'get_path')
    nodes, paths, templates = create_indexes()

    index_parser.generate_sparse_matrix()
    assert len(paths) == counters['invocations']


def test_generate_sparse_matrix_loops_all_nodes_for_each_paths(monkeypatch):
    counters = mock_method_with_counter(monkeypatch, db, 'get_node')
    nodes, paths, templates = create_indexes()

    index_parser.generate_sparse_matrix()
    assert len(paths) * len(nodes) == counters['invocations']


def test_generate_sparse_matrix_equals_to_paper_example():
    db.replace_all_nodes(paper_nodes)
    db.replace_all_paths(paper_paths)
    db.replace_all_templates(paper_templates)

    index_parser.generate_sparse_matrix()

    assert paper_matrix == db.get_sparse_matrix()
