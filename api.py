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

LISTENERS = []
logger = logging.getLogger(__name__)

class BattleListHandler(tornado.websocket.WebSocketHandler):
  def get(self):
    self.render('index.html')

class BattleHandler(tornado.websocket.WebSocketHandler):
  def get(self, bf_id):
    pass

class PostListHandler(tornado.websocket.WebSocketHandler):
  def get(self, bf_id, fighter_id, type):
    pass

class PostMessageHandler(tornado.websocket.WebSocketHandler):
  def post(self):
    pass

class PostVoteHandler(tornado.websocket.WebSocketHandler):
  def post(self):
    pass