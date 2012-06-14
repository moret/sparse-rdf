from app.graph_parser import graph_parser
from app.db import Redis
import rdflib


class TestGraph(rdflib.Graph):
    pass


class TestRedis(Redis):
    pass


def test_exists():
    assert graph_parser


# def test_tries_to_parse_file(monkeypatch):
#     test_graph = TestGraph()

#     def mock_parse(filename, format):
#         test_graph.parse_invoked = True
#         test_graph.filename_param = filename

#     test_graph.parse = mock_parse
#     monkeypatch.setattr(graph_parser, 'graph', test_graph)

#     graph_parser.parse('test_filename.nt')

#     assert test_graph.parse_invoked
#     assert 'test_filename.nt' == test_graph.filename_param


def test_tries_to_store_nodes(monkeypatch):
    test_redis = TestRedis()

    def mock_replace_all_nodes(nodes):
        test_redis.replace_all_nodes_invoked = True
        test_redis.nodes = nodes

    test_redis.replace_all_nodes = mock_replace_all_nodes
    monkeypatch.setattr(graph_parser, 'redis', test_redis)

    graph_parser.parse('tests/assets/paper.nt')
    graph_parser.persist_index()

    assert test_redis.replace_all_nodes_invoked
    assert 0 < len(test_redis.nodes)


def test_tries_to_store_paths(monkeypatch):
    test_redis = TestRedis()

    def mock_replace_all_paths(paths):
        test_redis.replace_all_paths_invoked = True
        test_redis.paths = paths

    test_redis.replace_all_paths = mock_replace_all_paths
    monkeypatch.setattr(graph_parser, 'redis', test_redis)

    graph_parser.parse('tests/assets/paper.nt')
    graph_parser.persist_index()

    assert test_redis.replace_all_paths_invoked
    assert 0 < len(test_redis.paths)


def test_tries_to_store_templates(monkeypatch):
    test_redis = TestRedis()

    def mock_replace_all_templates(templates):
        test_redis.replace_all_templates_invoked = True
        test_redis.templates = templates

    test_redis.replace_all_templates = mock_replace_all_templates
    monkeypatch.setattr(graph_parser, 'redis', test_redis)

    graph_parser.parse('tests/assets/paper.nt')
    graph_parser.persist_index()

    assert test_redis.replace_all_templates_invoked
    assert 0 < len(test_redis.templates)


def test_aut1_is_a_node():
    graph_parser.parse('tests/assets/paper.nt')
    assert u'<http://demo.com/authors.rdf#aut1>' in graph_parser.triplesink.nodes()


def test_aut2_is_a_node():
    graph_parser.parse('tests/assets/paper.nt')
    assert u'<http://demo.com/authors.rdf#aut2>' in graph_parser.triplesink.nodes()


def test_2008_is_a_node():
    graph_parser.parse('tests/assets/paper.nt')
    assert u'"2008"' in graph_parser.triplesink.nodes()


def test_there_are_10_nodes():
    graph_parser.parse('tests/assets/paper.nt')
    assert 10 == len(graph_parser.triplesink.nodes())


def test_pub1_and_pub2_are_sources():
    graph_parser.parse('tests/assets/paper.nt')
    sources = graph_parser.triplesink.sources()
    assert 2 == len(sources)
    assert rdflib.term.URIRef(u'http://demo.com/publications.rdf#pub1') in sources
    assert rdflib.term.URIRef(u'http://demo.com/publications.rdf#pub2') in sources


def test_conference_is_a_sink():
    graph_parser.parse('tests/assets/paper.nt')
    assert rdflib.term.URIRef(u'http://demo.com/types.rdf#Conference') in graph_parser.triplesink.sinks()


def test_2008_is_a_sink():
    graph_parser.parse('tests/assets/paper.nt')
    assert rdflib.term.Literal(u'2008') in graph_parser.triplesink.sinks()


def test_there_are_5_sinks():
    graph_parser.parse('tests/assets/paper.nt')
    assert 5 == len(graph_parser.triplesink.sinks())


def test_pub1_type_publication_is_a_path():
    graph_parser.parse('tests/assets/paper.nt')
    assert [
        u'<http://demo.com/publications.rdf#pub1>',
        u'<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>',
        u'<http://demo.com/types.rdf#Publication>'
    ] in graph_parser.paths()


def test_there_are_10_paths():
    graph_parser.parse('tests/assets/paper.nt')
    assert 10 == len(graph_parser.paths())


def test_hash_acceptedBy_hash_type_is_a_template():
    graph_parser.parse('tests/assets/paper.nt')
    assert [
        u'<http://demo.com/syntax#acceptedBy>',
        u'<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>',
    ] in graph_parser.templates()


def test_there_are_5_templates():
    graph_parser.parse('tests/assets/paper.nt')
    assert 5 == len(graph_parser.templates())
