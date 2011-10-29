# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import asyncore
import json
import logging
from wsgiref.handlers import BaseHandler
import os

import tornado.httpserver
from tornado.web import RequestHandler
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options

from vendors.models import *

LISTENERS = []
logger = logging.getLogger(__name__)

class BattleListHandler(RequestHandler):
  """
  [
  {
    bf_id: 12345,
    fighters: [
      {
        'name': 'SH',
        'photo': 'http://test.com/sh.jpg'
      },
      {
        'name': 'BJ',
        'photo': 'http://test.com/bj.jpg'
      }
    ]
    description: 'describe this battle field',
    participants: 12300, // how many participants,
    status: 0|1|2, // 0: not started, 1: ongoing, 2: finished
    winner: 0/1/2, // which side wins, 0 means no winner
  }
]
  """
  def get(self):
    self.set_header('Content-Type', 'application/json;charset=utf-8')
    battles = [b.to_dict() for b in Battle.get_list()]
    self.write(json.dumps(battles))

class BattleHandler(RequestHandler):
  def get(self, bf_id):
    self.set_header('Content-Type', 'application/json;charset=utf-8')
    self.write(json.dumps(Battle.objects.get(id=bf_id).to_dict(detail=True)))

class PostListHandler(RequestHandler):
  """
  [{
    post_id: 123456, // id for the post,
    author_id: 3445236, // weibo account id,
    author_name: xxx
    author_avatar: xxx
    comment: "this is cool", // comment user posted.
    photo_url: "http://test.com/test.jpg",
  }]
  """
  def get(self, bf_id, fighter, type):
    self.set_header('Content-Type', 'application/json;charset=utf-8')
    battle = Battle.objects.get(id=bf_id)
    self.write(json.dumps([{p.to_dict()} for p in Post.battle_posts(battle, int(fighter), type)]))

class PostMessageHandler(RequestHandler):
  def post(self):
    pass

class PostVoteHandler(RequestHandler):
  def post(self):
    data = json.loads(self.request.body)
    post_id = data.get('post_id')
    post = Post.objects.get(id=post_id)
    
