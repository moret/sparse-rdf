from app.db import redis as app_redis


class MatrixSearcher(object):
    def __init__(self):
        self.redis = app_redis

    def node_query(self, node_index):
        col = self.redis.get_column(node_index)
        paths = []
        for path_index in col.keys():
            paths.append(self.redis.get_path(path_index))
        return paths

    def final_node_query(self, node_index):
        col = self.redis.get_column(node_index)
        paths = []
        for path_index, t in col.items():
            if t[0] == (t[1] - 1):
                paths.append(self.redis.get_path(path_index))
        return paths

    # def path_query(self):
    #     pass

    # def path_intersection_query(self):
    #     pass

    # def path_intersection_retrieval_query(self):
    #     pass

    # def path_cutting_retrieval_query(self):
    #     pass

matrix_searcher = MatrixSearcher()
