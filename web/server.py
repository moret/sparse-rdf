# coding: utf-8
from __future__ import absolute_import

import os
import daemon
import lockfile
import tornado.ioloop
import tornado.web
import tornado.auth

from conf.settings import confs


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('for the future')


def start():
    application = tornado.web.Application([
            (r'/', HomeHandler),
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
