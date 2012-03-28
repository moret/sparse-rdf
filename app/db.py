import json

from redis import StrictRedis


class Redis(object):
    def _get_connection(self):
        return StrictRedis()

    r = property(_get_connection)

    def _replace_list(self, n, l):
        self.r.delete(n)
        for i, e in enumerate(l):
            self.r.rpush(n, e)

    def _count_list(self, n):
        return int(self.r.llen(n))

    def _get_list_element(self, n, i):
        return self.r.lindex(n, i)

    def _get_list(self, n):
        return self.r.lrange(n, 0, -1)

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

    def _get_collection_of_lists(self, n):
        c = []
        for i in self.r.zrange(n, 0, -1):
            c.append(json.loads(i))
        return c

    def replace_all_nodes(self, nodes):
        self._replace_list('nodes', nodes)

    def count_nodes(self):
        return self._count_list('nodes')

    def get_node(self, index):
        return self._get_list_element('nodes', index)

    def get_nodes(self):
        return self._get_list('nodes')

    def replace_all_paths(self, paths):
        self._replace_collection_of_lists('paths', paths)

    def count_paths(self):
        return self._count_collection_of_lists('paths')

    def get_path(self, index):
        return self._get_collection_of_lists_element('paths', index)

    def get_paths(self):
        return self._get_collection_of_lists('paths')

    def replace_all_templates(self, templates):
        self._replace_collection_of_lists('templates', templates)

    def count_templates(self):
        return self._count_collection_of_lists('templates')

    def get_template(self, index):
        return self._get_collection_of_lists_element('templates', index)

    def get_template_index(self, template):
        return self._get_collection_of_lists_index('templates', template)

    def get_templates(self):
        self._get_collection_of_lists('templates')

    def store_tuple(self, path_index, node_index, cell_tuple):
        self.r.sadd('sparse_matrix_rows', 'row:%d' % path_index)
        self.r.hset('row:%d' % path_index, node_index, json.dumps(cell_tuple))

    def get_tuple(self, path_index, node_index):
        cell = self.r.hget('row:%d' % path_index, node_index)
        if cell:
            return tuple(json.loads(cell))
        else:
            return None

    def clear_sparse_matrix(self):
        for row_name in self.r.smembers('sparse_matrix_rows'):
            self.r.srem('sparse_matrix_rows', row_name)
            self.r.delete(row_name)

redis = Redis()
