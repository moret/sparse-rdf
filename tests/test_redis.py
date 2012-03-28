from app.db import redis


def test_exists():
    assert redis


def test_replace_all_nodes_with_two_nodes():
    nodes = ['nod1', 'nod2']
    redis.replace_all_nodes(nodes)
    assert 2 == redis.count_nodes()


def test_replace_all_nodes_with_three_nodes():
    nodes = ['nod1', 'nod2', 'nod3']
    redis.replace_all_nodes(nodes)
    assert 3 == redis.count_nodes()


def test_replace_all_paths_with_two_paths():
    paths = [['nod1', 'edge1', 'nod2'], ['nod2', 'edge2', 'nod3']]
    redis.replace_all_paths(paths)
    assert 2 == redis.count_paths()


def test_replace_all_templates_with_two_templates():
    templates = [['nod1', 'nod2'], ['nod2', 'nod3']]
    redis.replace_all_templates(templates)
    assert 2 == redis.count_templates()


def test_replace_all_paths_doesnt_change_nodes():
    nodes = ['nod1', 'nod2', 'nod3']
    redis.replace_all_nodes(nodes)
    paths = [['nod1', 'edge1', 'nod2'], ['nod2', 'edge2', 'nod3']]
    redis.replace_all_paths(paths)
    assert 2 == redis.count_paths()


def test_replace_all_paths_doesnt_change_templates():
    nodes = ['nod1', 'nod2', 'nod3']
    redis.replace_all_nodes(nodes)
    templates = [['nod1', 'nod2'], ['nod2', 'nod3']]
    redis.replace_all_templates(templates)
    assert 2 == redis.count_paths()


def test_stored_node_returns_as_string():
    nodes = ['nod1', 'nod2', 'nod3']
    redis.replace_all_nodes(nodes)
    assert isinstance(redis.get_node(1), str)


def test_stored_path_returns_as_list():
    paths = [['nod1', 'edge1', 'nod2'], ['nod2', 'edge2', 'nod3']]
    redis.replace_all_paths(paths)
    assert isinstance(redis.get_path(1), list)


def test_stored_template_returns_as_list():
    templates = [['nod1', 'nod2'], ['nod2', 'nod3']]
    redis.replace_all_templates(templates)
    assert isinstance(redis.get_template(1), list)


def test_stored_nodes_maintains_order():
    nodes = ['nod1', 'nod2', 'nod3']
    redis.replace_all_nodes(nodes)
    assert 'nod1' == redis.get_node(0)
    assert 'nod2' == redis.get_node(1)
    assert 'nod3' == redis.get_node(2)


def test_stored_paths_maintains_order():
    paths = [['nod1', 'edge1', 'nod2'], ['nod2', 'edge2', 'nod3']]
    redis.replace_all_paths(paths)
    assert ['nod1', 'edge1', 'nod2'] == redis.get_path(0)
    assert ['nod2', 'edge2', 'nod3'] == redis.get_path(1)


def test_stored_templates_maintains_order():
    templates = [['nod1', 'nod2'], ['nod2', 'nod3']]
    redis.replace_all_templates(templates)
    assert ['nod1', 'nod2'] == redis.get_template(0)
    assert ['nod2', 'nod3'] == redis.get_template(1)


def test_find_template_index():
    t1 = ['nod1', 'nod2']
    t2 = ['nod2', 'nod3']
    templates = [t1, t2]
    redis.replace_all_templates(templates)
    assert 0 == redis.get_template_index(t1)
    assert 1 == redis.get_template_index(t2)


def test_store_read_sparse_matrix():
    t = (2, 3, 4)
    redis.store_tuple(3, 4, t)
    assert t == redis.get_tuple(3, 4)


def test_stored_cell_in_sparse_matrix_is_a_tuple():
    t = (2, 3, 4)
    redis.store_tuple(3, 4, t)
    assert isinstance(redis.get_tuple(3, 4), tuple)


def test_read_sparse_matrix_tuple_out_of_range_returns_None():
    redis.clear_sparse_matrix()
    assert None == redis.get_tuple(3, 4)
