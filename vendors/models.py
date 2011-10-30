# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
from datetime import datetime, timedelta
import logging
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import StringField, DateTimeField, IntField, EmbeddedDocumentField, ListField, ReferenceField
from mongoengine.queryset import Q
from const import BATTLE_ONGOING, BATTLE_FINISHED, BATTLE_NOT_STARTED
from mongoengine import connect

logger=logging.getLogger(__name__)

class User(Document):
  name = StringField()
  avatar = StringField()
  weibo_id = StringField()


class Fighter(EmbeddedDocument):
  name = StringField()
  photo = StringField()
  blood = IntField(default=lambda:1000)
  desc = StringField()

  def to_dict(self):
    """
    name: 'BJ',
    current_photo: 'http://test.com/bj.jpg',
    description: 'BJ is bla bla bla...',
    blood: 10, // how many blood left
    recent_posts: [{
      // see API 1.3
    }],
    hottest_posts: [{
    }]
    }, {          // city 1

    }]
    """
    return {
      'name': self.name,
      'current_photo': self.photo,
      'blood': self.blood,
      'desc': self.desc,
      }


class Battle(Document):
  start = DateTimeField()
  end = DateTimeField()
  desc = StringField()

  fighter0 = EmbeddedDocumentField(Fighter)
  fighter1 = EmbeddedDocumentField(Fighter)

  participants = IntField(default = lambda:0)
  created_at = DateTimeField(default=lambda:datetime.now())


  def update_one(self, *args, **kwargs):
    self.__class__.objects(id=self.id).update_one(*args, **kwargs)


  def blood(self, fighter, amount):
    f = self.fighter0 if fighter == 0 else self.fighter1
    f.blood -= amount
    if fighter == 0:
      self.update_one(set__fighter0=f)
    else:
      self.update_one(set__fighter1=f)

  @property
  def status(self):
    if datetime.now() < self.start:
      return BATTLE_NOT_STARTED
    if datetime.now() > self.end:
      return BATTLE_FINISHED
    return BATTLE_ONGOING

  @property
  def winner(self):
    if self.status == BATTLE_FINISHED:
      return 0 if self.fighter0.blood > self.fighter1.blood else 1
    return -1

  @property
  def time_left(self):
    if self.status == BATTLE_ONGOING:
      logger.info(datetime.now())
      logger.info(self.end)
      return (self.end - datetime.now()).seconds
    return 0

  def to_dict(self, detail=False):
    """
    bf_id: 12345, //which battle field this is for
    description: 'describe this battle field',
    participants: 12300,
    winner: 0/1,
    time_left: 10800, // how many seconds this battle will be over
    fighters: [{  // city 0
    name: 'BJ',
    current_photo: 'http://test.com/bj.jpg',
    description: 'BJ is bla bla bla...',
    blood: 10, // how many blood left
    recent_posts: [{
      // see API 1.3
    }],
    hottest_posts: [{
    }]
    }, {          // city 1

    }]
  """
    info = {
      'bf_id': str(self.id),
      'description': self.desc,
      'participants': self.participants,
      'status': self.status,
      'winner': self.winner,
      'time_left': self.time_left,
      'fighters': [self.fighter0.to_dict(), self.fighter1.to_dict()],
#      'fighter1': self.fighter1.to_dict(),
      }
    if detail:
      info['fighters'][0].update({
        'recent_posts': [p.to_dict() for p in Post.battle_posts(self, 0, 'recent')],
        'hottest_posts': [p.to_dict() for p in Post.battle_posts(self, 0, 'hottest')]
      })
      info['fighters'][1].update({
        'recent_posts': [p.to_dict() for p in Post.battle_posts(self, 1, 'recent')],
        'hottest_posts': [p.to_dict() for p in Post.battle_posts(self, 1, 'hottest')]
      })

    return info

  @classmethod
  def get_list(cls):
    return cls.objects.order_by('-participants', '-created_at')


class  Post(Document):
  battle = ReferenceField(Battle)
  author = ReferenceField(User)
  fighter = IntField()

  voters = ListField(ReferenceField(User), default=lambda:[])
  votes = IntField(default=lambda:0)

  comment = StringField()
  photo_url = StringField()

  created_at = DateTimeField(default=lambda:datetime.now())

  @classmethod
  def battle_posts(cls, battle, fighter, type):
    if type == 'recent':
      return [p for p in Post.objects(Q(battle=battle) & Q(fighter=fighter)).order_by('-created_on')[:5]]

    return [p for p in Post.objects(Q(battle=battle) & Q(fighter=fighter)).order_by('-created_on')[:5]]

  def vote_by(self, user):
    if user not in self.voters:
      self.voters.append(user)
    self.votes += 1
    self.save()
    return True

  def to_dict(self):
    """
    {
    post_id: 123456, // id for the post,
    author_id: 3445236, // weibo account id,
    author_name: xxx
    author_avatar: xxx
    comment: "this is cool", // comment user posted.
    photo_url: "http://test.com/test.jpg",
    votes: 178
    }
    """
    return {
      'post_id': str(self.id),
      'author_id': str(self.author.id),
      'author_name': self.author.name,
      'author_avatar': self.author.avatar,
      'comment': self.comment,
      'photo_url': self.photo_url,
      'votes': self.votes
    }

def _init_data():

  battle = Battle(

    start=datetime.now(),
    end=datetime.now() + timedelta(hours=3),
    desc='帝都与魔都的大战',
    fighter0 = Fighter(
      name='北京',
      photo='http://www.williamlong.info/google/upload/497_2.jpg',
      desc='帝都'
    ),

    fighter1 = Fighter(
      name='上海',
      photo='http://a2.att.hudong.com/55/24/14300000491308127624242862280.jpg',
      desc='魔都'
    ),
  )

  battle.save()


def _clear():
  for b in Battle.objects:
    b.delete()

if __name__ == "__main__":
  connect('citypk')
  _clear()
  _init_data()





