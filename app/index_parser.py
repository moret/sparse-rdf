from app.persistance import db


class IndexParser(object):
    def generate_sparse_matrix(self):
        db.clear_sparse_matrix()
        for path_index in range(db.count_paths()):
            path = db.get_path(path_index)
            for node_index in range(db.count_nodes()):
                node = db.get_node(node_index)
                if node in path:
                    cell_tuple = self.get_tuple(node, path)
                    db.store_tuple(path_index, node_index, cell_tuple)

    def get_tuple(self, node, path):
        nodes_template = tuple(path[::2])
        path_template = path[1::2]
        p = nodes_template.index(node)  # posicao do node no path
        l = len(nodes_template)  # quantos nodes tem no path
        t = db.get_template_index(path_template)  # qual o template
        return [p, l, t]

index_parser = IndexParser()
