import redis

def print_matrix(nodes, paths):
    print 'matrix:'
    r = redis.StrictRedis()
    s = ''
    for i, path in enumerate(paths):
        for j, node in enumerate(nodes):
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
    nodes = r.lrange('nodes', 0, -1)
    paths = r.lrange('paths', 0, -1)
    templates = r.lrange('templates', 0, -1)

    # print_index('nodes', nodes)
    print_index('paths', paths)
    print_index('templates', templates)

    print_matrix(nodes, paths)

if __name__ == "__main__":
    main()
