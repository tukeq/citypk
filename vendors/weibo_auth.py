# -*- coding: utf-8 -*-
#from __future__ import division, unicode_literals, print_function
from datetime import datetime
import json
import logging
from vendors.weibo import Weibo
#from const import consumer_key, consumer_secret
from vendors.weibopy.auth import OAuthHandler
from vendors.weibopy.error import WeibopError

logger = logging.getLogger(__name__)
class WebOAuthHandler(OAuthHandler):

  def get_authorization_url_with_callback(self, callback, signin_with_twitter=False, parameters={}):
    """Get the authorization URL to redirect the user"""
    try:
      # get the request token
      self.request_token = self._get_request_token()

      # build auth request and return as url
      if signin_with_twitter:
        url = self._get_oauth_url('authenticate')
      else:
        url = self._get_oauth_url('authorize')
      request = oauth.OAuthRequest.from_token_and_callback(
        token=self.request_token,
        callback=callback,
        http_url=url,
        parameters= parameters
      )
      return request.to_url()
    except Exception, e:
        logger.error('error to authorization url, %s', e, exc_info=True)
        raise WeibopError(e)

def _oauth():
  """获取oauth认证类"""
  return WebOAuthHandler(consumer_key, consumer_secret)

def auth(request):
  client_type = request.REQUEST.get('client_type')
  client_identifier = request.REQUEST.get('client_identifier')
  if not client_type:
    return HttpResponseBadRequest('client_type parameter is needed.')

  if not client_identifier:
    return HttpResponseBadRequest('client_identifier parameter is needed.')

  auth_client = _oauth()
  callback = auth_client.get_authorization_url_with_callback(
    request.build_absolute_uri(get_url_by_conf('api_auth_success')), parameters = {'display':'mobile'})
  request.session['oauth_request_token'] = auth_client.request_token
  request.session['client_type'] = client_type
  request.session['client_identifier'] = client_identifier
  return HttpResponseRedirect(callback)


def auth_success(request):
  """用户成功登录授权后，会回调此方法，获取access_token，完成授权"""
  # http://mk2.com/?oauth_token=c30fa6d693ae9c23dd0982dae6a1c5f9&oauth_verifier=603896
  verifier = request.GET.get('oauth_verifier')
  if not verifier:
    return HttpResponseBadRequest('verifier does not exist. URL is %s' % request.path)

  # 设置之前保存在session的request_token
  request_token = request.session.get('oauth_request_token')
  client_type = request.session.get('client_type')
  client_identifier = request.session.get('client_identifier')
  if not request_token:
    return HttpResponseBadRequest('request token lost to access weibo')
  if not client_type:
    return HttpResponseBadRequest('client_type lost to access weibo')
  if not client_identifier:
    return HttpResponseBadRequest('client_identifier lost to access weibo')

  del request.session['oauth_request_token']
  del request.session['client_identifier']
  del request.session['client_type']

  auth_client = _oauth()
  auth_client.set_request_token(request_token.key, request_token.secret)
  access_token = auth_client.get_access_token(verifier)
  weibo_client = Weibo()
  weibo_client.setToken(access_token.key, access_token.secret)

  info = weibo_client.get_info()

  # TODO FIXME only support registered user now
  user = Profile.objects.get(sns_id=info.id)

  if not user:
    return HttpResponseBadRequest('unregistered user')

  api_key = _get_or_create_api_key(access_token, client_identifier, client_type, user)

  return HttpResponse(json.dumps({'slug': user.username, 'name': user.nickname, 'api_key_id': api_key.key_id}),
                      mimetype='application/json')

