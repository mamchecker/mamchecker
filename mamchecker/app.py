# -*- coding: utf-8 -*-

#https://code.google.com/status/appengine

import sys
import os, os.path
import logging
import datetime

def python_path():
    """
    Add to sys.path to import correct (local) helper packages.
    """
    this_file = os.path.abspath(__file__)
    local_dir = os.path.join(os.path.dirname(this_file), "..")
    local_dir = os.path.normpath(local_dir)
    if local_dir not in sys.path: sys.path.insert(0, local_dir)
    def add(name):
        modpath = os.path.join(local_dir,name)
        if modpath not in sys.path: sys.path.insert(0, modpath)
    add('bottle')
    add('sympy')
    #there is oauth2 and httplib2 and simpleauth symlink
    add(os.path.join('simpleauth','example','lib'))

python_path()

##execute the following in vim py to use google appengine in vim
#>> from mamchecker.conftest import gaetestbed
#>> class requestdummy:
#>>     def addfinalizer(self,fin):
#>>         self.fin=fin
#>> finrequest = requestdummy()
#>> finalize = gaetestbed(finrequest)
##finalize()

from bottle import template

import webapp2
from webapp2_extras import sessions

from mamchecker.hlp import import_module 
from mamchecker.util import AuthUser
from mamchecker.model import stored_secret, set_student

#this will fill Index 
#initdb is generate via `doit -k initdb`
import mamchecker.initdb
from mamchecker.kinds import kinds, Error

#conftest.py will set this to False for py.test2 run
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

cached_lang = 'en'

from simpleauth import SimpleAuthHandler

class PageHandler(webapp2.RequestHandler, SimpleAuthHandler, AuthUser):
    '''http://mamchecker.appspot.com/<lang>/[<pagename>]?<query_string>
    '''
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        ##set_student will modify the session 
        #if self.session_store.get_session().new:
        #    self.session.update({})#modifies session to re-put/re-send
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    # Enable optional OAuth 2.0 CSRF guard
    OAUTH2_CSRF_STATE = True #needs self.session
    ATTRS = {
      'facebook' : {
        'id'     : lambda id: ('avatar_url', 
          'http://graph.facebook.com/{0}/picture?type=large'.format(id)),
        'name'   : 'name',
        'link'   : 'link'
      },
      'google'   : {
        'picture': 'avatar_url',
        'name'   : 'name',
        'profile': 'link'
      },
      'twitter'  : {
        'profile_image_url': 'avatar_url',
        'screen_name'      : 'name',
        'link'             : 'link'
      },
      'linkedin2' : {
        'picture-url'       : 'avatar_url',
        'first-name'        : 'name',
        'public-profile-url': 'link'
      },
      'foursquare'   : {
        'photo'    : lambda photo: ('avatar_url', photo.get('prefix') + '100x100' + photo.get('suffix')),
        'firstName': 'firstName',
        'lastName' : 'lastName',
        'contact'  : lambda contact: ('email',contact.get('email')),
        'id'       : lambda id: ('link', 'http://foursquare.com/user/{0}'.format(id))
      },
      'openid'   : {
        'id'      : lambda id: ('avatar_url', '/img/missing-avatar.png'),
        'nickname': 'name',
        'email'   : 'link'
      }
    }
    #
    #secrets need to be uploaded manually
    #http://stackoverflow.com/questions/1782906/how-do-i-activate-the-interactive-console-on-app-engine
    #https://developers.google.com/appengine/docs/adminconsole/
    #https://developers.google.com/appengine/articles/remote_api
    #remote_api_shell.py #http://mamchecker.appspot.com/admin/interactive is off
    #$remote_api_shell.py -s mamchecker.appspot.com
    #>> import mamchecker.model as mdl
    #>> mdl.Secret.query().fetch()
    #>> mdl.Secret.get_or_insert("test", secret = "test secret")
    #
    #client ids need to be registed:
    #http://code.google.com/apis/console
    #https://developers.facebook.com/apps
    #https://www.linkedin.com/secure/developer
    #https://dev.twitter.com/apps
    #openid no registration needed, but Authentication Type = Federated Login at 
    #  https://appengine.google.com/settings?app_id=s~mamchecker
    SECRETS = {p:(stored_secret(p+'mamcheckerid'),stored_secret(p)) for p in ATTRS.keys()}
    SCOPES = {
      # OAuth 2.0 providers
      'google'      : 'https://www.googleapis.com/auth/userinfo.profile',
      'linkedin2'   : 'r_basicprofile',
      'facebook'    : 'user_about_me',
      'foursquare'  : 'authorization_code',
      # OAuth 1.0 providers don't have scopes
      'twitter'     : '',
      'linkedin'    : '',
      # openid doesn't need any key/secret
    }

    def _callback_uri_for(self, provider):
        return self.uri_for('callback', provider=provider, _full=True)
    
    def _get_consumer_info_for(self, provider):
        return tuple(filter(None,list(self.SECRETS[provider])+[self.SCOPES[provider]]))
    
    def _on_signin(self, data, auth_info, provider):
        auth_id = '%s:%s' % (provider, data['id'])
        user = self.user_model.get_by_auth_id(auth_id)
        _attrs = {}
        for k, v in self.ATTRS[provider].iteritems():
            attr = (v, data.get(k)) if isinstance(v, str) else v(data.get(k))
            _attrs.setdefault(*attr)
        if user:
            user.populate(**_attrs)
            user.put()
            self.auth.set_session(
                self.auth.store.user_to_dict(user))
        else:
            if self.logged_in:
                u = self.user
                u.populate(**_attrs)
                success,info = u.add_auth_id(auth_id)# this will put()
                if not success:
                     logging.warning('Update existing user failed')
            else:
                ok, user = self.auth.store.user_model.create_user(auth_id, **_attrs)
                if ok:
                     self.auth.set_session(self.auth.store.user_to_dict(user))
        self.redirect(self.uri_for('entry_lang', lang=cached_lang))

    def logout(self, lang=cached_lang):
        self.auth.unset_session()
        self.redirect(self.uri_for('entry_lang', lang=lang))

    def arguments_ok(self, kwargs):
        #kwargs = {}
        self.request.lang = kwargs.get('lang',None)
        global cached_lang
        cached_lang = self.request.lang
        self.request.pagename = kwargs.get('pagename',None)

        if not self.request.lang or not self.request.lang in kinds:
            #TODO: http://stackoverflow.com/questions/8514017/how-to-decide-the-language-from-cookies-headers-session-in-webapp2
            self.request.lang = 'en' 
            redirect_address = self.uri_for('entry_lang', lang=self.request.lang)
            self.redirect(redirect_address)
            return False
        else:
            if not self.request.pagename:
                self.request.pagename = 'content'
            studentres = set_student(self.request, self.user, self.session)
            if isinstance(studentres,str):
                self.redirect(studentres)
            else:
                return True

    def forward(self,kwargs,toforward):
        if self.arguments_ok(kwargs):
            try:
                self.request.modulename = self.request.pagename
                m = import_module(self.request.modulename)
                page = m.Page(self.request)
                self.response.write(toforward(page))
            except (ImportError, AttributeError, IOError, NameError) as e:
                if debug: raise
                self.redirect(self.uri_for('entry_lang', lang=self.request.lang))

    def get(self,**kwargs):
        self.forward(kwargs,lambda page:page.get_response())

    def post(self,**kwargs):
        self.forward(kwargs,lambda page:page.post_response())

#access via self.app.config.get('foo')
app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': 'mamcheckersessionkey',
    'secret_key': stored_secret('session_secret')
  },
  'webapp2_extras.auth': {
    'cookie_name': None, #use the one from session config and not 'auth'
    'user_model': 'mamchecker.model.User',
    'user_attributes': ['name']
  }
}

def _error(request, response, exception, status):
    logging.exception(exception)
    lang = filter(lambda k:'/'+k in request.url, Error.keys())
    lang = lang and lang[0] or 'en'
    response.write(Error[lang]+' '+str(status)+' ('+exception.message+')')
    response.set_status(status)

def make_app(debug=debug):
    app = webapp2.WSGIApplication([
        webapp2.Route('', handler=PageHandler, name='entry'),
        webapp2.Route('/', handler=PageHandler, name='entry_'),
        webapp2.Route('/<lang:[^/]+>', handler=PageHandler, name='entry_lang'),
        webapp2.Route('/<lang:[^/]+>/', handler=PageHandler, name='entry_lang_'),
        webapp2.Route('/<lang:[^/]+>/logout'
            , handler='mamchecker.app.PageHandler:logout'
            , name='logout'),
        webapp2.Route('/auth/<provider>'
            , handler='mamchecker.app.PageHandler:_simple_auth'
            , name='authlogin'),
        webapp2.Route('/auth/<provider>/callback'
            , handler='mamchecker.app.PageHandler:_auth_callback', name='callback'),
        webapp2.Route('/<lang:[^/]+>/<pagename:[^?]+>', handler=PageHandler, name='page'),
        ],config=app_config,debug=debug)
    app.error_handlers[400] = lambda q,a,e: _error(q,a,e,400)
    app.error_handlers[404] = lambda q,a,e: _error(q,a,e,404)
    app.error_handlers[500] = lambda q,a,e: _error(q,a,e,500)
    return app

app = make_app()

