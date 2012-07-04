from app.persistance import db


class MatrixSearcher(object):
    def node_query(self, node_index):
        col = db.get_column(node_index)
        paths = []
        for path_index in col.keys():
            paths.append(db.get_path(path_index))
        return paths

    def final_node_query(self, node_index):
        col = db.get_column(node_index)
        paths = []
        for path_index, t in col.items():
            if t[0] == (t[1] - 1):
                paths.append(db.get_path(path_index))
        return paths

    def path_query(self, path_index):
        row = db.get_row(path_index)
        nodes = []
        for node_index in row.keys():
            nodes.append(db.get_node(node_index))
        return nodes

    # def path_intersection_query(self):
    #     pass

    # def path_intersection_retrieval_query(self):
    #     pass

    # def path_cutting_retrieval_query(self):
    #     pass

matrix_searcher = MatrixSearcher()
