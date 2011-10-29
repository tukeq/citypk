# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
from datetime import datetime
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import StringField, DateTimeField, IntField, EmbeddedDocumentField, ListField, ReferenceField

"""
USER = hash{
    id
    name
    avatar
}
BATTLE = hash{
  id
  start
  end
  description
  status
  fighters = [{id0, photo, blood, desc, posts}, {id1, photo, blood, desc}]
  winner
  participants=[user_id,...]
}

POSTS
{
id
battle_id
content
photo_url
voters=[user_id,...]
created_at
}
"""

class User(Document):
  name = StringField()
  avatar = StringField()
  weibo_id = StringField()


class Fighter(EmbeddedDocument):
  name=StringField()
  avatar = StringField()
  blood = IntField(default=10000)
  desc = StringField()


class Battle(Document):
  start=DateTimeField()
  end=DateTimeField()
  desc=StringField()

  fighter1 = EmbeddedDocumentField(Fighter)
  fighter2 = EmbeddedDocumentField(Fighter)

#  participants = ListField(ReferenceField(User), default=lambda :[])
  participants_num = IntField()

  created_at = DateTimeField(default=datetime.now)


class Post(Document):
  battle = ReferenceField(Battle)
  author = ReferenceField(User)
  post_for = IntField()

  voters = ListField(ReferenceField(User))
  votes = IntField()

  content = StringField()
  photo = StringField()

  created_at = DateTimeField(default=datetime.now)







