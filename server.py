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
from util import get_abs_url
from vendors.base_handler import BaseHandler
from vendors.sina_auth import login_required, AuthLoginCheckHandler, AuthLoginHandler, AuthLogoutHandler
from vendors.weibo_auth import _oauth
import vendors.tornado_session as session

LISTENERS = []
logger = logging.getLogger(__name__)

define('port', default=8000, type=int)
define('host', default='localhost', type=str)

class RealtimeHandler(BaseHandler):
    def open(self, *args, **kargs):
        print('new connection')
        LISTENERS.append(self)

    def on_message(self, message):
        print(message)

    def on_close(self):
#      pass
        LISTENERS.remove(self)

class IndexHandler(BaseHandler):
    @login_required
    def get(self, *args, **kargs):
        self.render('index.html', host=options.host, port=options.port)

    def post(self, *args, **kwargs):
        print('get message')
#        print(self.request.)
        for listener in LISTENERS:
          listener.write_message('this is from server, websocket is okay')

class WeiboLoginHandler(BaseHandler):
  @login_required
  def get(self):
    self.render("login.html")

class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            (r'/', IndexHandler),
            (r'/login', AuthLoginHandler),
            (r'/login_check', AuthLoginCheckHandler),
            (r'/logout', AuthLogoutHandler),
            (r'/messages', RealtimeHandler),
            (r'/api/battles', BattleListHandler),
            (r'/api/battle/%s' % const.MATCH_NAME, BattleHandler),
            (r'/api/posts/%s/([0|1])/%s' % (const.MATCH_NAME, const.MATCH_NAME), PostListHandler),
            (r'/api/post', PostMessageHandler),
            (r'/api/vote', PostVoteHandler),
        ]
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            #login_url="/auth/login",
            session_secret='some secret password!!',
            session_dir='sessions',
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.session_manager = session.TornadoSessionManager(settings["session_secret"], settings["session_dir"])

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    connect('citypk')
    print("start on port %s..."%options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
