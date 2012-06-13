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
    cov = coverage.coverage()
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

    graph_parser.parse('tests/assets/paper.nt')
    graph_parser.persist_index()
    index_parser.generate_sparse_matrix()

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
