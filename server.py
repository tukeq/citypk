from __future__ import unicode_literals, print_function, division
import asyncore
import json
import logging
import os

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options
from mongoengine import connect
import const
from api import *

LISTENERS = []
logger = logging.getLogger(__name__)

define('port', default=8000, type=int)
define('host', default='localhost', type=str)

class RealtimeHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kargs):
        print('new connection')
        LISTENERS.append(self)

    def on_message(self, message):
        print(message)

    def on_close(self):
#      pass
        LISTENERS.remove(self)

class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kargs):
        self.render('index.html', host=options.host, port=options.port)

    def post(self, *args, **kwargs):

        print('get message')
#        print(self.request.)
        for listener in LISTENERS:
          listener.write_message('this is from server, websocket is okay')

def start_web():
    settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            )

    application = tornado.web.Application([
            (r'/', IndexHandler),
            (r'/messages', RealtimeHandler),
            (r'/api/battles', BattleListHandler),
            (r'/api/battle/%s' % const.MATCH_NAME, BattleHandler),
            (r'/api/posts/%s/([0|1])/%s' % (const.MATCH_NAME, const.MATCH_NAME), PostListHandler),
            (r'/api/post', PostMessageHandler),
            (r'/api/vote', PostVoteHandler),

            ], **settings)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print('start server at %s:%s' % (options.host, options.port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    connect(db='citypk')
    start_web()
