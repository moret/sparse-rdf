from app.db import es


def test_exist():
    assert es


def test_replace_all_nodes_with_two_nodes():
    nodes = ['nod1', 'nod2']
    es.replace_all_nodes(nodes)
    assert 2 == es.count_nodes()


def test_replace_all_nodes_with_three_nodes():
    nodes = ['nod1', 'nod2', 'nod3']
    es.replace_all_nodes(nodes)
    assert 3 == es.count_nodes()


def test_stored_node_returns_as_string():
    nodes = ['nod1', 'nod2', 'nod3']
    es.replace_all_nodes(nodes)
    assert isinstance(es.get_node(1), str)


def test_stored_nodes_maintains_order():
    nodes = ['nod1', 'nod2', 'nod3']
    es.replace_all_nodes(nodes)
    assert 'nod1' == es.get_node(0)
    assert 'nod2' == es.get_node(1)
    assert 'nod3' == es.get_node(2)


def test_get_node_index_by_exact_name():
    nodes = ['the_first_node', 'a_second_node', 'third_node_returns']
    es.replace_all_nodes(nodes)
    assert 0 == es.search_node(nodes[0])
    assert 1 == es.search_node(nodes[1])
    assert 2 == es.search_node(nodes[2])
