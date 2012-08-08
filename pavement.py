# coding: utf-8
from __future__ import absolute_import

import sys
sys.path = ['.'] + sys.path

from paver.easy import task
from paver.easy import sh
from paver.easy import cmdopts
import pytest
import coverage


@task
@cmdopts([
    ('keyword=', 'k', 'only run python tests which match given keyword expression')
])
def tests(options):
    clean()
    cov = coverage.coverage(omit=['lib/ntriples.py'])
    cov.erase()
    cov.start()

    if 'keyword' in options:
        pytest.main('-s -v tests -k %s' % options.keyword)
    else:
        pytest.main('-s -v tests')

    cov.stop()
    cov.report()
    clean()


@task
def parse():
    clean()

    from app.graph_parser import graph_parser
    from app.index_parser import index_parser

    graph_parser.parse('example-rdfs/tall/paper.nt')
    # graph_parser.parse('example-rdfs/venti/linkedmdb-latest-dump.nt')
    graph_parser.persist_index()
    index_parser.generate_sparse_matrix()

    clean()


@task
def node_query():
    clean()

    from app.matrix_searcher import matrix_searcher
    from app.persistance import db

    node_index = db.search_node('pub1')
    node = db.get_node(node_index)
    print node
    print matrix_searcher.node_query(node_index)

    clean()


@task
def show():
    clean()

    from app.persistance import db
    print db.get_sparse_matrix()

    clean()


@task
def clean():
    sh('find . -name "__pycache__" -delete')
    sh('find . -name "*.pyc" -delete')
    sh('find . -name "*~" -delete')
