# coding: utf-8
from __future__ import absolute_import

import sys
sys.path = ['.'] + sys.path

from paver.easy import task
from paver.easy import sh
import pytest
import coverage


@task
def tests():
    clean()
    cov = coverage.coverage(omit=['lib/ntriples.py'])
    cov.erase()
    cov.start()
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
    from app.db import es

    node_index = es.search_node('pub1')
    node = es.get_node(node_index)
    print node
    print matrix_searcher.node_query(node_index)

    clean()


@task
def show():
    clean()

    from app.db import redis
    print redis.get_sparse_matrix()

    clean()


@task
def clean():
    sh('find . -name "__pycache__" -delete')
    sh('find . -name "*.pyc" -delete')
    sh('find . -name "*~" -delete')
