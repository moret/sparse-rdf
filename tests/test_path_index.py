from app.persistance import db


def test_exist():
    from app.persistance import pi
    assert pi


def test_replace_all_paths_with_two_paths():
    paths = [['nod1', 'edge1', 'nod2'], ['nod2', 'edge2', 'nod3']]
    db.replace_all_paths(paths)
    assert 2 == db.count_paths()


def test_replace_all_paths_doesnt_change_nodes():
    nodes = ['nod1', 'nod2', 'nod3']
    db.replace_all_nodes(nodes)
    paths = [['nod1', 'edge1', 'nod2'], ['nod2', 'edge2', 'nod3']]
    db.replace_all_paths(paths)
    assert 3 == db.count_nodes()
    assert 2 == db.count_paths()


def test_stored_path_returns_as_list():
    paths = [['nod1', 'edge1', 'nod2'], ['nod2', 'edge2', 'nod3']]
    db.replace_all_paths(paths)
    assert isinstance(db.get_path(1), list)


def test_stored_paths_maintains_order():
    paths = [['nod1', 'edge1', 'nod2'], ['nod2', 'edge2', 'nod3']]
    db.replace_all_paths(paths)
    assert ['nod1', 'edge1', 'nod2'] == db.get_path(0)
    assert ['nod2', 'edge2', 'nod3'] == db.get_path(1)
