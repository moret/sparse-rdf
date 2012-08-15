# coding: utf-8
from __future__ import absolute_import

import os
import json

import daemon
import lockfile

import tornado.ioloop
import tornado.web
import tornado.auth

from conf.settings import confs


class NodeQueryHandler(tornado.web.RequestHandler):
    def get(self, node_param):
        from app.matrix_searcher import matrix_searcher
        from app.persistance import db

        node_index = db.search_node(node_param)

        result = {
                'query': node_param,
                'selected_node': None,
                'query_result': None
        }

        if node_index != None:
            result['selected_node'] = db.get_node(node_index)
            result['query_result'] = matrix_searcher.node_query(node_index)

        self.finish(json.dumps(result))


def start():
    application = tornado.web.Application([
            (r'/node-query/(.*)', NodeQueryHandler),
        ], **{
            'static_path': os.path.join('static'),
            'template_path': os.path.join('templates'),
            'debug': confs.debug,
            'cookie_secret': confs.cookie_secret
    })
    application.listen(confs.port)
    print(' => Listening on %d' % confs.port)
    tornado.ioloop.IOLoop.instance().start()


def start_daemon():
    context = daemon.DaemonContext(working_directory='.', detach_process=True,
        pidfile=lockfile.FileLock(confs.pidfile))

    with context:
        start()
