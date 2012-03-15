import rdflib
import redis

def set_from_generator(generator):
    l = []
    for item in generator:
        l.append(item)
    return set(l)

def mark_and_enqueue(path, edge, node, qeue, marked):
    node_path = list(path)
    if edge != None:
        node_path.append(edge)
    node_path.append(node)
    qeue.append((node, node_path))
    marked.append(node)

def find_nodes_sources_and_sinks(graph):
    subjects = set_from_generator(graph.subjects())
    objects = set_from_generator(graph.objects())
    return subjects.union(objects), subjects - objects, objects - subjects

def store_hash_list(l_name, l):
    r = redis.StrictRedis()
    r.delete(l_name)
    for i in l:
        r.lpush(l_name, i)

def find_paths_templates(graph, sources, sinks):
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
            for edge, node in graph.predicate_objects(current_node):
                if node not in marked:
                    mark_and_enqueue(current_path, edge, node, qeue, marked)

    return paths, templates

def store_sparse_rdf(nodes, paths, templates):
    r = redis.StrictRedis()
    for i, path in enumerate(paths):
        r.delete('path:%d' % i)
        for j, node in enumerate(nodes):
            if node in path:
                r.hset('path:%d' % i, j, (j, i))

def main():
    print 'parsing graph...'
    graph = rdflib.Graph()
    graph.parse('paper.nt', format='nt')
    # graph.parse('NTN-individuals.owl')
    # graph.parse('opus_august2007.rdf')
    # graph.parse('swetodblp_april_2008.rdf')
    # graph.parse('linkedmdb-latest-dump.nt', format='nt')

    print 'listing nodes, sources and sinks...'
    nodes, sources, sinks = find_nodes_sources_and_sinks(graph)

    print 'listing paths and templates...'
    paths, templates = find_paths_templates(graph, sources, sinks)

    print 'listed - nodes: %d, paths: %d, templates: %d' % (len(nodes),
            len(paths), len(templates))
    store_hash_list('nodes', nodes)
    store_hash_list('paths', paths)
    store_hash_list('templates', templates)

    print 'storing sparse matrix...'
    store_sparse_rdf(nodes, paths, templates)

    print 'done - bye!'

if __name__ == "__main__":
    main()
