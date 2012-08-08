import pycassa
from app.persistance import CassandraBasedStorage


test_ks = 'test_ks'
test_cf = 'test_cf'


class CassandraTestBasedStorage(CassandraBasedStorage):
    def __init__(self):
        self.ks = test_ks
        super(CassandraTestBasedStorage, self).__init__(test_cf)


def test_exists():
    assert CassandraBasedStorage


def test_keyspace_is_created_at_init():
    cs = CassandraTestBasedStorage()
    pycassa.system_manager.SystemManager().drop_keyspace(test_ks)

    cs = CassandraTestBasedStorage()
    assert cs._ks_created()
