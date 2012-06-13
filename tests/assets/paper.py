paper_nodes = [
    '<http://demo.com/authors.rdf#aut1>',
    '<http://demo.com/authors.rdf#aut2>',
    '<http://demo.com/types.rdf#Researcher>',
    '<http://demo.com/publications.rdf#pub1>',
    '<http://demo.com/publications.rdf#pub2>',
    '<http://demo.com/types.rdf#Publication>',
    '<http://demo.com/conferences.rdf#conf1>',
    '<http://demo.com/types.rdf#Conference>',
    '\"ISWC\"',
    '\"2008\"'
]

paper_paths = [
    ['<http://demo.com/publications.rdf#pub1>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', '<http://demo.com/types.rdf#Publication>'],
    ['<http://demo.com/publications.rdf#pub2>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', '<http://demo.com/types.rdf#Publication>'],
    ['<http://demo.com/publications.rdf#pub1>', '<http://demo.com/syntax#year>', '"2008"'],
    ['<http://demo.com/publications.rdf#pub2>', '<http://demo.com/syntax#year>', '"2008"'],
    ['<http://demo.com/publications.rdf#pub1>', '<http://demo.com/syntax#acceptedBy>', '<http://demo.com/conferences.rdf#conf1>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', '<http://demo.com/types.rdf#Conference>'],
    ['<http://demo.com/publications.rdf#pub1>', '<http://demo.com/syntax#acceptedBy>', '<http://demo.com/conferences.rdf#conf1>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#name>', '"ISWC"'],
    ['<http://demo.com/publications.rdf#pub1>', '<http://demo.com/syntax#author>', '<http://demo.com/authors.rdf#aut1>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', '<http://demo.com/types.rdf#Researcher>'],
    ['<http://demo.com/publications.rdf#pub2>', '<http://demo.com/syntax#acceptedBy>', '<http://demo.com/conferences.rdf#conf1>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', '<http://demo.com/types.rdf#Conference>'],
    ['<http://demo.com/publications.rdf#pub2>', '<http://demo.com/syntax#acceptedBy>', '<http://demo.com/conferences.rdf#conf1>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#name>', '"ISWC"'],
    ['<http://demo.com/publications.rdf#pub2>', '<http://demo.com/syntax#author>', '<http://demo.com/authors.rdf#aut2>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', '<http://demo.com/types.rdf#Researcher>']
]

paper_templates = [
    ['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'],
    ['<http://demo.com/syntax#year>'],
    ['<http://demo.com/syntax#acceptedBy>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'],
    ['<http://demo.com/syntax#acceptedBy>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#name>'],
    ['<http://demo.com/syntax#author>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>']
]

paper_matrix = {
    0: {3: [0, 2, 0], 5: [1, 2, 0]},
    1: {4: [0, 2, 0], 5: [1, 2, 0]},
    2: {3: [0, 2, 1], 9: [1, 2, 1]},
    3: {4: [0, 2, 1], 9: [1, 2, 1]},
    4: {3: [0, 3, 2], 6: [1, 3, 2], 7: [2, 3, 2]},
    5: {3: [0, 3, 3], 6: [1, 3, 3], 8: [2, 3, 3]},
    6: {0: [1, 3, 4], 2: [2, 3, 4], 3: [0, 3, 4]},
    7: {4: [0, 3, 2], 6: [1, 3, 2], 7: [2, 3, 2]},
    8: {4: [0, 3, 3], 6: [1, 3, 3], 8: [2, 3, 3]},
    9: {1: [1, 3, 4], 2: [2, 3, 4], 4: [0, 3, 4]},
}
