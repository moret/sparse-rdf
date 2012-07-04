import rdflib

from app.graph_parser import graph_parser
from app.persistance import db


def mock_method_with_counter(monkeypatch, obj, method_name):
    counters = {'invocations': 0}
    proxied = getattr(obj, method_name)

    def mock(*args, **kwargs):
        counters['invocations'] += 1
        counters['args'] = args
        counters['kwargs'] = kwargs
        return proxied(*args, **kwargs)

    monkeypatch.setattr(obj, method_name, mock)
    return counters


def test_exists():
    assert graph_parser


def test_tries_to_store_nodes(monkeypatch):
    counters = mock_method_with_counter(monkeypatch, db, 'replace_all_nodes')

    graph_parser.parse('tests/assets/paper.nt')
    graph_parser.persist_index()

    assert 1 == counters['invocations']
    assert 0 < len(counters['args'][0])


def test_tries_to_store_paths(monkeypatch):
    counters = mock_method_with_counter(monkeypatch, db, 'replace_all_paths')

    graph_parser.parse('tests/assets/paper.nt')
    graph_parser.persist_index()

    assert 1 == counters['invocations']
    assert 0 < len(counters['args'][0])


def test_tries_to_store_templates(monkeypatch):
    counters = mock_method_with_counter(monkeypatch, db, 'replace_all_templates')

    graph_parser.parse('tests/assets/paper.nt')
    graph_parser.persist_index()

    assert 1 == counters['invocations']
    assert 0 < len(counters['args'][0])


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
