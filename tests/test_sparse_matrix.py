import pytest
from app.persistance import sm


def test_exists():
    assert sm


def test_accepts_store_size_three_list():
    sm.clear_sparse_matrix()
    l = [3, 4, 5]
    sm.store_tuple(4, 5, l)
    assert l == sm.get_tuple(4, 5)


def test_accepts_store_None():
    sm.clear_sparse_matrix()
    sm.store_tuple(4, 5, None)
    assert None == sm.get_tuple(4, 5)


def test_rejects_store_size_two_list():
    sm.clear_sparse_matrix()
    l = [3, 4]
    with pytest.raises(ValueError):
        sm.store_tuple(4, 5, l)


def test_rejects_store_size_four_list():
    sm.clear_sparse_matrix()
    l = [3, 4, 5, 6]
    with pytest.raises(ValueError):
        sm.store_tuple(4, 5, l)


def test_rejects_store_tuple():
    sm.clear_sparse_matrix()
    t = (2, 3, 4)
    with pytest.raises(ValueError):
        sm.store_tuple(3, 4, t)


def test_stored_cell_in_sparse_matrix_is_a_size_three_list():
    sm.clear_sparse_matrix()
    sm.store_tuple(3, 4, [2, 3, 4])
    t = sm.get_tuple(3, 4)
    assert isinstance(t, list)
    assert 3 == len(t)


def test_read_sparse_matrix_tuple_out_of_range_returns_None():
    sm.clear_sparse_matrix()
    assert None == sm.get_tuple(3, 4)


def test_read_sparse_matrix_row_returns_dict_of_size_three_lists():
    sm.clear_sparse_matrix()
    sm.store_tuple(0, 0, [1, 2, 3])
    sm.store_tuple(0, 2, [2, 3, 4])
    row = sm.get_row(0)
    assert isinstance(row, dict)
    assert isinstance(row[0], list)
    with pytest.raises(KeyError):
        row[1]
    assert isinstance(row[2], list)
    assert 3 == len(row[0])
    assert 3 == len(row[2])


def test_read_sparse_matrix_row_out_of_range_returns_None():
    sm.clear_sparse_matrix()
    assert None == sm.get_row(3)


def test_read_sparse_matrix_column_returns_dict_of_size_three_lists():
    sm.clear_sparse_matrix()
    sm.store_tuple(0, 0, [1, 2, 3])
    sm.store_tuple(2, 0, [2, 3, 4])
    col = sm.get_column(0)
    assert isinstance(col, dict)
    assert isinstance(col[0], list)
    with pytest.raises(KeyError):
        col[1]
    assert isinstance(col[2], list)
    assert 3 == len(col[0])
    assert 3 == len(col[2])


def test_read_sparse_matrix_column_out_of_range_returns_None():
    sm.clear_sparse_matrix()
    assert None == sm.get_column(3)
