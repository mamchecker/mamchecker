# -*- coding: utf-8 -*-

from mamchecker.util import PageBase
from mamchecker.hlp import import_module
import logging
from google.appengine.api import mail
via_email = True#!!else everybody can change the password

class Page(PageBase):
    
    def __init__(self, _request):
        super(self.__class__,self).__init__(_request)
        username = self.request.get('username')
        self.params = {'username':username, 'not_found':False }

    def post_response(self):
        username = self.request.get('username')

        user = self.user_model.get_by_auth_id(username)
        if not user:
            self.params = {
                'username': username,
                'not_found': True
            }
            return self.get_response()

        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)

        relative_url = 'verification?type=p&user_id={}&signup_token={}'.format(user_id,token)

        if via_email:
            confirmation_url = self.request.application_url+'/'+self.request.lang+'/'+relative_url
            m = import_module('forgot.'+self.request.lang)
#            sender_address = "Mamchecker Support <roland.puntaier@gmail.com>"
#            subject = "Mamchecker: Password Reset"
#            body = """
#Please click at the link to reset your password:
#
#%s
#""" % confirmation_url
            mail.send_mail(m.sender_address, user.email_adress, m.subject, m.body%confirmation_url)
            self.redirect('message?msg=j')
        else: 
            self.redirect(relative_url)
  
