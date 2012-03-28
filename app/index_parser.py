from app.db import redis as app_redis


class IndexParser(object):
    def __init__(self):
        self.redis = app_redis

    def generate_sparse_matrix(self):
        self.redis.clear_sparse_matrix()
        for path_index in range(self.redis.count_paths()):
            path = self.redis.get_path(path_index)
            for path_index in range(self.redis.count_nodes()):
                node = self.redis.get_node(path_index)
                if node in path:
                    cell_tuple = self.get_tuple(node, path)
                    self.redis.store_tuple(path_index, path_index, cell_tuple)

    def get_tuple(self, node, path):
        nodes_template = tuple(path[::2])
        path_template = path[1::2]
        p = nodes_template.index(node)  # posicao do node no path
        l = len(nodes_template)  # quantos nodes tem no path
        t = self.redis.get_template_index(path_template)  # qual o template
        return (p, l, t)

index_parser = IndexParser()
