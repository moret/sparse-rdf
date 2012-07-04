from app.persistance import db


def test_exist():
    from app.persistance import ni
    assert ni


def test_replace_all_nodes_with_two_nodes():
    nodes = ['nod1', 'nod2']
    db.replace_all_nodes(nodes)
    assert 2 == db.count_nodes()


def test_replace_all_nodes_with_three_nodes():
    nodes = ['nod1', 'nod2', 'nod3']
    db.replace_all_nodes(nodes)
    assert 3 == db.count_nodes()


def test_stored_node_returns_as_string():
    nodes = ['nod1', 'nod2', 'nod3']
    db.replace_all_nodes(nodes)
    assert isinstance(db.get_node(1), str)


def test_stored_nodes_maintains_order():
    nodes = ['nod1', 'nod2', 'nod3']
    db.replace_all_nodes(nodes)
    assert 'nod1' == db.get_node(0)
    assert 'nod2' == db.get_node(1)
    assert 'nod3' == db.get_node(2)


def test_get_node_index_by_exact_name():
    nodes = ['the_first_node', 'a_second_node', 'third_node_returns']
    db.replace_all_nodes(nodes)
    assert 0 == db.search_node(nodes[0])
    assert 1 == db.search_node(nodes[1])
    assert 2 == db.search_node(nodes[2])
