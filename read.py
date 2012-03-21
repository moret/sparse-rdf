import redis

def print_matrix(nodes, paths):
    print 'matrix:'
    r = redis.StrictRedis()
    s = ''
    nodes_len = int(r.get('nodes_len'))
    paths_len = int(r.get('paths_len'))
    for i in range(paths_len):
        for j in range(nodes_len):
            entry = r.hget('row:%d' % i, j)
            if entry:
                s += entry
            else:
                s += '    .    '
            s += ' '
        s += '\n'
    print s

def print_index(l_name, l):
    print '%s:' % l_name
    for i, entry in enumerate(l):
        print '%d: %s' % (i, entry)
    print

def main():
    r = redis.StrictRedis()
    nodes = r.zrange('nodes', 0, -1)
    paths = r.zrange('paths', 0, -1)
    templates = r.zrange('templates', 0, -1)

    print_index('nodes', nodes)
    print_index('paths', paths)
    print_index('templates', templates)

    print_matrix(nodes, paths)

if __name__ == "__main__":
    main()
