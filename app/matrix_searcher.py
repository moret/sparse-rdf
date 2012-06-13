from app.db import redis as app_redis


class MatrixSearcher(object):
    def __init__(self):
        self.redis = app_redis

    def node_query(self):
        self.redis.get_matrix_column()

    # def final_node_query(self):
    #     pass

    # def path_query(self):
    #     pass

    # def path_intersection_query(self):
    #     pass

    # def path_intersection_retrieval_query(self):
    #     pass

    # def path_cutting_retrieval_query(self):
    #     pass

matrix_searcher = MatrixSearcher()
