# -*- coding: utf-8 -*-

def get_abs_url(path, server='localhost', port='8000'):
  return 'http://%s:%s%s' % (server, port, path)