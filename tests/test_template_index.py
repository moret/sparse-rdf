from app.persistance import db


def test_exist():
    from app.persistance import ti
    assert ti


def test_replace_all_templates_with_two_templates():
    templates = [['nod1', 'nod2'], ['nod2', 'nod3']]
    db.replace_all_templates(templates)
    assert 2 == db.count_templates()


def test_stored_template_returns_as_list():
    templates = [['nod1', 'nod2'], ['nod2', 'nod3']]
    db.replace_all_templates(templates)
    assert isinstance(db.get_template(1), list)


def test_not_stored_template_returns_None():
    templates = [['nod1', 'nod2'], ['nod2', 'nod3']]
    db.replace_all_templates(templates)
    assert None == db.get_template(3)


def test_stored_templates_maintains_order():
    templates = [['nod1', 'nod2'], ['nod2', 'nod3']]
    db.replace_all_templates(templates)
    assert ['nod1', 'nod2'] == db.get_template(0)
    assert ['nod2', 'nod3'] == db.get_template(1)


def test_replace_all_nodes_doesnt_change_templates():
    templates = [['nod1', 'nod2'], ['nod2', 'nod3']]
    db.replace_all_templates(templates)
    nodes = ['nod1', 'nod2', 'nod3']
    db.replace_all_nodes(nodes)
    assert 3 == db.count_nodes()
    assert 2 == db.count_templates()


def test_find_template_index():
    t1 = ['nod1', 'nod2']
    t2 = ['nod2', 'nod3']
    templates = [t1, t2]
    db.replace_all_templates(templates)
    assert 0 == db.get_template_index(t1)
    assert 1 == db.get_template_index(t2)


def test_not_found_template_index_returns_None():
    t1 = ['nod1', 'nod2']
    t2 = ['nod2', 'nod3']
    templates = [t1, t2]
    db.replace_all_templates(templates)
    assert None == db.get_template_index(['nod3', 'nod4'])
