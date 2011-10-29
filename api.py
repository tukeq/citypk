# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import asyncore
import json
import logging
from vendors.base_handler import BaseHandler
import os

import tornado.httpserver
from tornado.web import RequestHandler
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options
from util import get_first_url_from_string

from vendors.models import *
from vendors.sina_auth import login_required

LISTENERS = []
logger = logging.getLogger(__name__)

class BattleListHandler(RequestHandler):

  def get(self):
    self.set_header('Content-Type', 'application/json;charset=utf-8')
    battles = [b.to_dict() for b in Battle.get_list()]
    self.write(json.dumps(battles))

class BattleHandler(RequestHandler):
  def get(self, bf_id):
    self.set_header('Content-Type', 'application/json;charset=utf-8')
    self.write(json.dumps(Battle.objects.get(id=bf_id).to_dict(detail=True)))

class PostListHandler(RequestHandler):
  def get(self, bf_id, fighter, type):
    self.set_header('Content-Type', 'application/json;charset=utf-8')
    battle = Battle.objects.get(id=bf_id)
    self.write(json.dumps([{p.to_dict()} for p in Post.battle_posts(battle, int(fighter), type)]))

class PostMessageHandler(BaseHandler):
  @login_required
  def post(self):
    self.set_header('Content-Type', 'application/json;charset=utf-8')
    data = json.loads(self.request.body)
    bf_id = data.get('bf_id')
    fighter = data.get('fighter')
    comment = data.get('comment')
    img = get_first_url_from_string(comment)
    if img:
      comment = comment.replace(img, '')
    weibo_id = str(self.session['me'].id)
    try:
      battle = Battle.objects.get(id=bf_id)
      user = User.objects.get(weibo_id=weibo_id)
    except:
      self.write(json.dumps({
        'post_id': None,
        'status': 0,
        'message': u'提交失败'
      }))
      return
    post = Post(
      battle = battle,
      author = user,
      fighter = int(fighter),
      comment = comment,
      photo_url = img
    )
    post.save()
    post.battle.blood(fighter, 15)
    pn('post a new message')
    self.write(json.dumps({
      'post_id': str(post.id),
      'status': 1,
      'message': ''
    }))


class PostVoteHandler(RequestHandler):
  @login_required
  def post(self):
    data = json.loads(self.request.body)
    post_id = data.get('post_id')
    weibo_id=self.session['me']
    user = User.objects.get(weibo_id=weibo_id)
    post = Post.objects.get(id=post_id)
    result = post.vote_by(user)
    if result:
      pn('fight')
      post.battle.blood(post.fighter, 10)


    self.write(json.dumps({
      'post_id': post.id,
      'status': result,
      'message': ''
    }))

def pn(message, update=False, winner=0, delta={}):
  for l in LISTENERS:
        l.write_message(json.dumps({
          'update':update,
          'broadcast':message,
          'winner':winner,
          'delta':delta
        }))
