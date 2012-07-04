import json

from redis import StrictRedis
import pyes


class Redis(object):
    def _get_connection(self):
        return StrictRedis()

    r = property(_get_connection)

    def _replace_collection_of_lists(self, n, l):
        self.r.delete(n)
        for s, i in enumerate(l):
            self.r.zadd(n, s, json.dumps(i))

    def _get_collection_of_lists_element(self, n, i):
        return json.loads(self.r.zrangebyscore(n, i, i)[0])

    def replace_all_paths(self, paths):
        self._replace_collection_of_lists('paths', paths)

    def get_path(self, index):
        return self._get_collection_of_lists_element('paths', index)

    def replace_all_templates(self, templates):
        self._replace_collection_of_lists('templates', templates)

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

redis = Redis()


class ElasticSearch(object):
    def _get_connection(self):
        return pyes.ES()

    es = property(_get_connection)

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

    def get_node(self, index):
        return str(self.es.get('nodes', 'node-type', index + 1)['value'])

es = ElasticSearch()
