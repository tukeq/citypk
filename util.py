# -*- coding: utf-8 -*-

def get_abs_url(path, server='localhost', port='8000'):
  return 'http://%s:%s%s' % (server, port, path)

def get_first_url_from_string(content):
  import re
  try:
    return re.search(r"(?P<url>https?://[^\s]+\.(jpg|jpeg))", content).group("url")
  except:
    return None