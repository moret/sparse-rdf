import json

import pyes
import pycassa
from redis import StrictRedis


class ElasticSearchBasedStorage(object):
    def _get_connection(self):
        return pyes.ES()

    es = property(_get_connection)


class RedisBasedStorage(object):
    def _get_connection(self):
        return StrictRedis()

    r = property(_get_connection)


class RedisBasedIndex(RedisBasedStorage):
    def _replace_collection_of_lists(self, n, l):
        self.r.delete(n)
        for s, i in enumerate(l):
            self.r.zadd(n, s, json.dumps(i))

    def _count_collection_of_lists(self, n):
        return self.r.zcard(n)

    def _get_collection_of_lists_element(self, n, i):
        return json.loads(self.r.zrangebyscore(n, i, i)[0])

    def _get_collection_of_lists_index(self, n, e):
        return self.r.zrank(n, json.dumps(e))


class CassandraBasedStorage(object):
    ks = 'sparse_keyspace'

    def _get_system_manager(self):
        return pycassa.system_manager.SystemManager()

    sm = property(_get_system_manager)

    def _get_connection(self):
        return pycassa.ConnectionPool(self.ks)

    c = property(_get_connection)

    def _ks_created(self):
        return self.ks in self.sm.list_keyspaces()

    def _ks_init(self):
        self.sm.create_keyspace(self.ks,
                pycassa.system_manager.SIMPLE_STRATEGY,
                {'replication_factor': '1'})

    def __init__(self, family_name):
        if not self._ks_created():
            self._ks_init()
        if not self._cf_created(family_name):
            self._cf_init(family_name)

    def _cf_created(self, family_name):
        return family_name in self.sm.get_keyspace_column_families(self.ks)

    def _cf_list(self, family_name):
        return pycassa.ColumnFamily(self.c, family_name)

    def _cf_init(self, family_name):
        self.sm.create_column_family(self.ks, family_name)


class NodesIndex(ElasticSearchBasedStorage):
    def replace_all_nodes(self, nodes):
        self.es.delete_index_if_exists('nodes')
        self.es.create_index('nodes')

        self.es.put_mapping('node-type', {'properties': {
                'value': {
                    'boost': 1.0,
                    'index': 'analyzed',
                    'store': 'yes',
                    'type': 'string',
                    'term_vector': 'with_positions_offsets'
                }
            }
        }, ['nodes'])

        # indexes must be larger than zero
        for index, node in enumerate(nodes):
            self.es.index({'value': node}, 'nodes', 'node-type', index + 1)

        self.es.refresh(['nodes'])

    def count_nodes(self):
        return self.es.index_stats()._all.indices['nodes'].total.docs.count

    def get_node(self, index):
        return str(self.es.get('nodes', 'node-type', index + 1)['value'])

    def search_node(self, word):
        query = pyes.FieldQuery(pyes.FieldParameter('value', word))
        result = self.es.search(query=query)
        if result:
            return int(result[0]._meta['id']) - 1

ni = NodesIndex()


class PathsIndex(CassandraBasedStorage):
    def __init__(self):
        super(PathsIndex, self).__init__('paths')

    def _paths(self):
        return self._cf_list('paths')

    paths = property(_paths)

    def replace_all_paths(self, paths):
        self.paths.truncate()
        for index, path in enumerate(paths):
            self.paths.insert(str(index), {'value': json.dumps(path)})

    def count_paths(self):
        return len(list(self.paths.get_range()))

    def get_path(self, index):
        return json.loads(self.paths.get(str(index))['value'])

pi = PathsIndex()


class TemplatesIndex(RedisBasedIndex):
    def replace_all_templates(self, templates):
        self._replace_collection_of_lists('templates', templates)

    def count_templates(self):
        return self._count_collection_of_lists('templates')

    def get_template(self, index):
        return self._get_collection_of_lists_element('templates', index)

    def get_template_index(self, template):
        return self._get_collection_of_lists_index('templates', template)

ti = TemplatesIndex()


class SparseMatrix(RedisBasedStorage):
    def store_tuple(self, path_index, node_index, cell_tuple):
        if cell_tuple == None or (isinstance(cell_tuple, list) and len(cell_tuple) == 3):
            self.r.sadd('sparse_matrix_rows', 'row:%d' % path_index)
            self.r.hset('row:%d' % path_index, node_index, json.dumps(cell_tuple))

            self.r.sadd('sparse_matrix_cols', 'col:%d' % node_index)
            self.r.hset('col:%d' % node_index, path_index, json.dumps(cell_tuple))
        else:
            raise ValueError('must be a size three list or None')

    def get_tuple(self, path_index, node_index):
        cell = self.r.hget('row:%d' % path_index, node_index)
        if cell:
            return json.loads(cell)
        else:
            return None

    def get_row(self, path_index):
        raw_row = self.r.hgetall('row:%d' % path_index)
        if raw_row:
            row = {}
            for key, value in raw_row.items():
                row[int(key)] = json.loads(value)
            return row
        else:
            return None

    def get_column(self, node_index):
        raw_col = self.r.hgetall('col:%d' % node_index)
        if raw_col:
            col = {}
            for key, value in raw_col.items():
                col[int(key)] = json.loads(value)
            return col
        else:
            return None

    def get_sparse_matrix(self):
        matrix = {}
        for row_name in self.r.smembers('sparse_matrix_rows'):
            path_index = int(row_name.split(':')[1])
            matrix[path_index] = self.get_row(path_index)
        return matrix

    def clear_sparse_matrix(self):
        for row_name in self.r.smembers('sparse_matrix_rows'):
            self.r.srem('sparse_matrix_rows', row_name)
            self.r.delete(row_name)

        for col_name in self.r.smembers('sparse_matrix_cols'):
            self.r.srem('sparse_matrix_cols', col_name)
            self.r.delete(col_name)

sm = SparseMatrix()


class DB(object):
    def __init__(self):
        self.ni = ni
        self.pi = pi
        self.ti = ti
        self.sm = sm

    def replace_all_nodes(self, nodes):
        return self.ni.replace_all_nodes(nodes)

    def count_nodes(self):
        return self.ni.count_nodes()

    def get_node(self, index):
        return self.ni.get_node(index)

    def search_node(self, word):
        return self.ni.search_node(word)

    def replace_all_paths(self, paths):
        return self.pi.replace_all_paths(paths)

    def count_paths(self):
        return self.pi.count_paths()

    def get_path(self, index):
        return self.pi.get_path(index)

    def replace_all_templates(self, templates):
        return self.ti.replace_all_templates(templates)

    def count_templates(self):
        return self.ti.count_templates()

    def get_template(self, index):
        return self.ti.get_template(index)

    def get_template_index(self, template):
        return self.ti.get_template_index(template)

    def store_tuple(self, path_index, node_index, cell_tuple):
        return self.sm.store_tuple(path_index, node_index, cell_tuple)

    def get_tuple(self, path_index, node_index):
        return self.sm.get_tuple(path_index, node_index)

    def get_row(self, path_index):
        return self.sm.get_row(path_index)

    def get_column(self, node_index):
        return self.sm.get_column(node_index)

    def get_sparse_matrix(self):
        return self.sm.get_sparse_matrix()

    def clear_sparse_matrix(self):
        return self.sm.clear_sparse_matrix()

db = DB()
