import rdflib

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

def find_sources_and_sinks(graph):
    subjects = set_from_generator(graph.subjects())
    objects = set_from_generator(graph.objects())
    return subjects.union(objects), subjects - objects, objects - subjects

def main():
    graph = rdflib.Graph()
    graph.parse('paper.nt', format='nt')
    # graph.parse('linkedmdb-latest-dump.nt', format='nt')

    nodes, sources, sinks = find_sources_and_sinks(graph)
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

    print ':: nodes (total: %d) ::' % len(nodes)
    for node in nodes:
        print node
    print

    print ':: paths (total: %d) ::' % len(paths)
    for path in paths:
        print path
    print

    print ':: templates (total: %d) ::' % len(templates)
    for template in templates:
        print template
    print

if __name__ == "__main__":
    main()
