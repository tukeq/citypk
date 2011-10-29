# -*- coding: utf-8 -*-
from weibopy.auth import OAuthHandler
from weibopy.api import API

#from core import consumer_key, consumer_secret

class Weibo(object):
  def __init__(self):
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret

  def getAtt(self, key):
    try:
      return self.obj.__getattribute__(key)
    except Exception, e:
      print e
      return ''

  def getAttValue(self, obj, key):
    try:
      return obj.__getattribute__(key)
    except Exception, e:
      print e
      return ''

  def auth(self):
    self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
    auth_url = self.auth.get_authorization_url()
    print 'Please authorize: ' + auth_url
    verifier = raw_input('PIN: ').strip()
    self.auth.get_access_token(verifier)
    self.api = API(self.auth)

  def setToken(self, token, tokenSecret):
    self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
    self.auth.setToken(token, tokenSecret)
    self.api = API(self.auth)

  def update(self, message, image_name=None, image_url = None):
    message = message.encode("utf-8")
    try:
      if image_name:
        status = self.api.upload(status=message, filename=image_name)
      if image_url:
        status = self.api.update_status_img(status=message, url=image_url)
      else:
        status = self.api.update_status(status=message)
    except:
      return None
    self.obj = status
    id = self.getAtt("id")
    return id

  def destroy_status(self, id):
    status = self.api.destroy_status(id)
    self.obj = status
    id = self.getAtt("id")
    return id

  def comment(self, id, message):
    comment = self.api.comment(id=id, comment=message)
    self.obj = comment
    mid = self.getAtt("id")
    return mid

  def comment_destroy (self, mid):
    comment = self.api.comment_destroy(mid)
    self.obj = comment
    mid = self.getAtt("id")
    text = self.getAtt("text")
    return mid

  def repost(self, id, message):
    post = self.api.repost(id=id, status=message)
    self.obj = post
    mid = self.getAtt("id")
    return mid

  def get_username(self):
    if getattr(self, '_username', None) is None:
        self._username = self.auth.get_username()
    return self._username

  def get_info(self):
    return self.api.me()

  def get_friends(self):
    try:
      return self.api.friends_ids().ids
    except:
      return []

  def show_friendship(self, target_id):
    try:
      return self.api.show_friendship(target_id = target_id)[0]
    except:
      return None
