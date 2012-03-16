import rdflib
import redis

def list_from_generator(generator):
    l = []
    for item in generator:
        l.append(item)
    return l

def mark_and_enqueue(path, edge, node, qeue, marked):
    # copy current path to store modified version
    node_path = list(path)
    if edge != None:
        node_path.append(edge)
    node_path.append(node)
    qeue.append((node, node_path))
    marked.append(node)

def find_nodes_sources_and_sinks(graph):
    subjects = list_from_generator(graph.subjects())
    objects = list_from_generator(graph.objects())

    # TODO arrumar forma decente de guardar valores unicos em array
    nodes = list(set(subjects).union(set(objects)))
    sources = list(set(subjects) - set(objects))
    sinks = list(set(objects) - set(subjects))

    return nodes, sources, sinks

def store_hash_list(l_name, l):
    r = redis.StrictRedis()
    r.delete(l_name)
    for i in l:
        r.rpush(l_name, i)

def find_paths_templates(graph, sources, sinks):
    paths = []
    templates = []

    for source in sources:
        path = []
        qeue = []
        marked = []
        mark_and_enqueue(path, None, source, qeue, marked)
        while len(qeue) > 0:
            current_node, current_path = qeue.pop()
            if current_node in sinks:
                paths.append(tuple(current_path))
                templates.append(tuple(current_path[1::2]))
            for edge, node in graph.predicate_objects(current_node):
                if node not in marked:
                    mark_and_enqueue(current_path, edge, node, qeue, marked)

    # TODO arrumar forma decente de guardar valores unicos em array
    unique_paths = list(set(paths))
    unique_templates = list(set(templates))
    return unique_paths, unique_templates

def build_sparse_rdf(nodes, paths, templates):
    r = redis.StrictRedis()
    for i, path in enumerate(paths):
        r.delete('row:%d' % i)
        for j, node in enumerate(nodes):
            if node in path:
                nodes_template = path[::2]
                path_template = path[1::2]
                p = nodes_template.index(node) # posicao do node no path
                l = len(nodes_template) # quantos nodes tem no path
                t = templates.index(path_template) # qual o template
                r.hset('row:%d' % i, j, (p, l, t))

def main():
    print 'parsing graph...'
    # parsing the whole graph at once is dumb - it never ends for large sets
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

    print 'building sparse matrix...'
    build_sparse_rdf(nodes, paths, templates)

    print 'done - bye!'

if __name__ == "__main__":
    main()
