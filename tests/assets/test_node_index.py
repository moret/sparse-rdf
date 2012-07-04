from app.persistance import ni


def test_exist():
    assert ni


def test_replace_all_nodes_with_two_nodes():
    nodes = ['nod1', 'nod2']
    ni.replace_all_nodes(nodes)
    assert 2 == ni.count_nodes()


def test_replace_all_nodes_with_three_nodes():
    nodes = ['nod1', 'nod2', 'nod3']
    ni.replace_all_nodes(nodes)
    assert 3 == ni.count_nodes()


def test_stored_node_returns_as_string():
    nodes = ['nod1', 'nod2', 'nod3']
    ni.replace_all_nodes(nodes)
    assert isinstance(ni.get_node(1), str)


def test_stored_nodes_maintains_order():
    nodes = ['nod1', 'nod2', 'nod3']
    ni.replace_all_nodes(nodes)
    assert 'nod1' == ni.get_node(0)
    assert 'nod2' == ni.get_node(1)
    assert 'nod3' == ni.get_node(2)


def test_get_node_index_by_exact_name():
    nodes = ['the_first_node', 'a_second_node', 'third_node_returns']
    ni.replace_all_nodes(nodes)
    assert 0 == ni.search_node(nodes[0])
    assert 1 == ni.search_node(nodes[1])
    assert 2 == ni.search_node(nodes[2])
