# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function

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
import vendors.tornado_session as session


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


class BattleViewHandler(BaseHandler):
    @login_required
    def get(self, *args, **kargs):
        self.render('battle.html', host=options.host, port=options.port)

    def post(self, *args, **kwargs):
        print('get message')
#        print(self.request.)
        for listener in LISTENERS:
          listener.write_message('this is from server, websocket is okay')
