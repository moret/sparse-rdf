import urllib
from app.db import redis as app_redis
from lib.ntriples import NTriplesParser


def mark_and_enqueue(path, edge, node, qeue, marked):
    # copy current path to store modified version
    node_path = list(path)
    if edge != None:
        node_path.append(edge.n3())
    node_path.append(node.n3())
    qeue.append((node, node_path))
    marked.append(node)


class TripleSink(object):
    def __init__(self):
        self.length = 0
        self.subjects = set()
        self.objects = set()
        self._predicate_objects = {}

    def triple(self, s, p, o):
        self.length += 1
        self.subjects.add(s)
        self.objects.add(o)
        if s not in self._predicate_objects:
            self._predicate_objects[s] = []
        self._predicate_objects[s].append((p, o))

    def nodes(self):
        nodes = set()
        for s in self.subjects:
            nodes.add(s.n3())
        for o in self.objects:
            nodes.add(o.n3())
        return list(nodes)

    def sources(self):
        sources = set()
        for s in self.subjects:
            sources.add(s)
        for o in self.objects:
            sources.discard(o)
        return list(sources)

    def sinks(self):
        sinks = set()
        for o in self.objects:
            sinks.add(o)
        for s in self.subjects:
            sinks.discard(s)
        return list(sinks)

    def predicate_objects(self, s):
        return self._predicate_objects.get(s, [])


# Reads the RDF triples, builds them in a graph and setup nodes, paths and
# templates indexes
class GraphParser(object):
    def __init__(self):
        self.redis = app_redis
        self.triplesink = TripleSink()

    def parse(self, filename):
        self.__parse_triples__(filename)
        self.__find_paths_templates__()

    def __parse_triples__(self, filename):
        print 'parsing triples'
        parser = NTriplesParser(sink=self.triplesink)
        u = urllib.urlopen(filename)
        parser.parse(u)
        u.close()

    def persist_index(self):
        print 'persisting indexes'
        self.redis.replace_all_nodes(self.triplesink.nodes())
        self.redis.replace_all_paths(self.paths())
        self.redis.replace_all_templates(self.templates())

    def __find_paths_templates__(self):
        print 'running bfs to find paths and templates'
        sources = self.triplesink.sources()
        sinks = self.triplesink.sinks()

        paths = set()
        templates = set()

        for source in sources:
            path = []
            qeue = []
            marked = []
            mark_and_enqueue(path, None, source, qeue, marked)
            while len(qeue) > 0:
                current_node, current_path = qeue.pop()
                if current_node in sinks:
                    paths.add(tuple(current_path))
                    templates.add(tuple(current_path[1::2]))
                for edge, node in self.triplesink.predicate_objects(current_node):
                    if node not in marked:
                        mark_and_enqueue(current_path, edge, node, qeue, marked)

        # TODO arrumar forma decente de guardar valores unicos em array
        self.__paths__ = []
        for path in paths:
            self.__paths__.append(list(path))

        self.__templates__ = []
        for template in templates:
            self.__templates__.append(list(template))

    def paths(self):
        return self.__paths__

    def templates(self):
        return self.__templates__

graph_parser = GraphParser()
