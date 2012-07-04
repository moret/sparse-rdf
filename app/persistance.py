import json

import pyes
from redis import StrictRedis


class NodesIndex(object):
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


class PathsIndex(object):
    def _get_connection(self):
        return StrictRedis()

    r = property(_get_connection)

    def _replace_collection_of_lists(self, n, l):
        self.r.delete(n)
        for s, i in enumerate(l):
            self.r.zadd(n, s, json.dumps(i))

    def _count_collection_of_lists(self, n):
        return self.r.zcard(n)

    def _get_collection_of_lists_element(self, n, i):
        return json.loads(self.r.zrangebyscore(n, i, i)[0])

    def replace_all_paths(self, paths):
        self._replace_collection_of_lists('paths', paths)

    def count_paths(self):
        return self._count_collection_of_lists('paths')

    def get_path(self, index):
        return self._get_collection_of_lists_element('paths', index)

pi = PathsIndex()


class TemplatesIndex(object):
    def _get_connection(self):
        return StrictRedis()

    r = property(_get_connection)

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

    def replace_all_templates(self, templates):
        self._replace_collection_of_lists('templates', templates)

    def count_templates(self):
        return self._count_collection_of_lists('templates')

    def get_template(self, index):
        return self._get_collection_of_lists_element('templates', index)

    def get_template_index(self, template):
        return self._get_collection_of_lists_index('templates', template)

ti = TemplatesIndex()


class DB(object):
    def __init__(self):
        self.ni = ni
        self.pi = pi

    def replace_all_nodes(self, nodes):
        return self.ni.replace_all_nodes(nodes)

    def count_nodes(self):
        return self.ni.count_nodes()

    # def get_node(self, index):
    #     return self.ni.get_node(index)

    # def search_node(self, word):
    #     return self.ni.search_node(word)

db = DB()
