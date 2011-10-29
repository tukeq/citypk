# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function
from redis.client import Redis


class MyRedis(Redis):
  def hgetall(self, name):
    mapping = super(MyRedis, self).hgetall(name)

    for k,v in mapping.iteritems():
      if isinstance(v, basestring):
        mapping[k]=v.decode('utf-8')
    return mapping

  def get(self, name):
    value = super(MyRedis, self).get(name)
    return value.decode('utf-8') if value else value

  def lrange(self, name, start, end):
    return [value.decode('utf-8') for value in super(MyRedis, self).lrange(name, start, end)]

db = MyRedis()
