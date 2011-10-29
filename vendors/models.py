# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
from datetime import datetime, timedelta
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import StringField, DateTimeField, IntField, EmbeddedDocumentField, ListField, ReferenceField
from mongoengine.queryset import Q
from const import BATTLE_ONGOING, BATTLE_FINISHED, BATTLE_NOT_STARTED
from mongoengine import connect

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
      'photo': self.photo,
      'blood': self.blood,
      'desc': self.desc,
      }


class Battle(Document):
  start = DateTimeField()
  end = DateTimeField()
  desc = StringField()

  fighter1 = EmbeddedDocumentField(Fighter)
  fighter2 = EmbeddedDocumentField(Fighter)

  participants = IntField(default = lambda:0)
  created_at = DateTimeField(default=lambda:datetime.now())

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
      return 1 if self.fighter1.blood > self.fighter2.blood else 2
    return 0

  @property
  def time_left(self):
    if self.status == BATTLE_ONGOING:
      return (datetime.now() - self.start).seconds
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
      'fighter1': self.fighter1.to_dict(),
      'fighter2': self.fighter2.to_dict(),
      }
    if detail:
      info['fighter1'].update({
        'recent_posts': [p.to_dict() for p in Post.battle_posts(self, 1, 'recent')],
        'hottest_posts': [p.to_dict() for p in Post.battle_posts(self, 1, 'hottest')]
      })
      info['fighter2'].update({
        'recent_posts': [p.to_dict() for p in Post.battle_posts(self, 2, 'recent')],
        'hottest_posts': [p.to_dict() for p in Post.battle_posts(self, 2, 'hottest')]
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
      return Post.objects(Q(battle=battle) & Q(fighter=fighter)).order_by('-created_on')[:5]

    return Post.objects(Q(battle=battle) & Q(fighter=fighter)).order_by('-votes')[:5]

  def vote_by(self, user):
    if user not in self.voters:
      self.voters.append(user)
      self.votes += 1
      self.save()


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
  connect('citypk')
  battle = Battle(

    start=datetime.now(),
    end=datetime.now() + timedelta(hours=3),
    desc='帝都与魔都的大战',
    fighter1 = Fighter(
      name='北京',
      photo='http://www.williamlong.info/google/upload/497_2.jpg',
      desc='帝都'
    ),

    fighter2 = Fighter(
      name='上海',
      photo='http://imgs.soufun.com/news/2010_05/13/office/1273713782423_000.jpg',
      desc='魔都'
    ),
  )

  battle.save()

if __name__ == "__main__":
#  _init_data()
  connect('citypk')
  battle=Battle.objects[0]
  print(battle)




