# coding: utf-8
from __future__ import absolute_import

import os
import sys
sys.path = ['.'] + sys.path

from paver.easy import task
from paver.easy import sh
from paver.easy import cmdopts
from paver.easy import consume_args
import pytest
import coverage


@task
@cmdopts([
    ('keyword=', 'k', 'only run python tests which match given keyword expression')
])
def tests(options):
    clean()

    try:
        cov = coverage.coverage(omit=['lib/ntriples.py'])
        cov.erase()

        server = start_web_test_server()
        cov.start()

        if hasattr(options, 'keyword'):
            pytest.main('-s -v tests -k %s' % options.keyword)
        else:
            pytest.main('-s -v tests')

        cov.stop()
        cov.report()
    finally:
        server.terminate()

    clean()


def start_web_test_server():
    import pexpect

    print ' --> paver start'
    paver = sys.argv[0]
    cov_cmd = os.path.join(os.path.dirname(paver), 'coverage')
    server = pexpect.spawn('%s run -p %s start' % (cov_cmd, paver))
    server.expect(' => Listening on')
    return server


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
@consume_args
def start(args):
    clean()
    import conf.settings
    if 'prod' in args:
        print 'setting environment to prod!'
        conf.settings.confs = conf.settings.prod
    from web import server
    server.start()
    clean()


@task
def stop():
    clean()
    import conf.settings
    sh("ps aux | egrep '%s/bin/paver' | awk '{print $2}' | xargs kill -9;" % conf.settings.confs.appname)
    sh('rm %s.lock' % conf.settings.confs.pidfile)
    clean()


@task
def clean():
    sh('find . -name "__pycache__" -delete')
    sh('find . -name "*.pyc" -delete')
    sh('find . -name "*~" -delete')
    sh('find . -name ".coverage.*" -delete')
