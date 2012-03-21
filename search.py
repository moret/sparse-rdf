import redis

r = redis.StrictRedis()

# TODO um jeito melhor de encontrar o indice do no buscado

node_index = int(r.zscore('nodes', "http://demo.com/authors.rdf#aut1"))
paths_len = int(r.get('paths_len'))

tuples_search = []
for path_index in range(paths_len):
    tuples_search.append(r.hget('row:%d' % path_index, node_index))

print tuples_search
