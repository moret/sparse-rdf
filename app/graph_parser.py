from app.db import redis as app_redis
import rdflib


def mark_and_enqueue(path, edge, node, qeue, marked):
    # copy current path to store modified version
    node_path = list(path)
    if edge != None:
        node_path.append(edge.n3())
    node_path.append(node.n3())
    qeue.append((node, node_path))
    marked.append(node)


# Reads the RDF triples, builds them in a graph and setup nodes, paths and
# templates indexes
class GraphParser(object):
    def __init__(self):
        self.redis = app_redis
        self.graph = rdflib.Graph()

    def parse(self, filename):
        self.graph.parse(filename, format='nt')
        self.__find_paths_templates__()

    def persist_index(self):
        self.redis.replace_all_nodes(self.nodes())
        self.redis.replace_all_paths(self.paths())
        self.redis.replace_all_templates(self.templates())

    def __find_paths_templates__(self):
        paths = set()
        templates = set()

        for source in self.sources():
            path = []
            qeue = []
            marked = []
            mark_and_enqueue(path, None, source, qeue, marked)
            while len(qeue) > 0:
                current_node, current_path = qeue.pop()
                if current_node in self.sinks():
                    paths.add(tuple(current_path))
                    templates.add(tuple(current_path[1::2]))
                for edge, node in self.graph.predicate_objects(current_node):
                    if node not in marked:
                        mark_and_enqueue(current_path, edge, node, qeue, marked)

        # TODO arrumar forma decente de guardar valores unicos em array
        self.__paths__ = []
        for path in paths:
            self.__paths__.append(list(path))

        self.__templates__ = []
        for template in templates:
            self.__templates__.append(list(template))

    def nodes(self):
        nodes = set()
        for s in self.graph.subjects():
            nodes.add(s.n3())
        for o in self.graph.objects():
            nodes.add(o.n3())
        return list(nodes)

    def sources(self):
        sources = set()
        for s in self.graph.subjects():
            sources.add(s)
        for o in self.graph.objects():
            sources.discard(o)
        return list(sources)

    def sinks(self):
        sinks = set()
        for o in self.graph.objects():
            sinks.add(o)
        for s in self.graph.subjects():
            sinks.discard(s)
        return list(sinks)

    def paths(self):
        return self.__paths__

    def templates(self):
        return self.__templates__

graph_parser = GraphParser()
