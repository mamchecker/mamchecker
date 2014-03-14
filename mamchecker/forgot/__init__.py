# -*- coding: utf-8 -*-

from mamchecker.util import PageBase
import logging

class Page(PageBase):
    
    def __init__(self, _request):
        super(self.__class__,self).__init__(_request)
        username = self.request.get('username')
        self.params = {'username':username, 'not_found':False }

    def post_response(self):
        username = self.request.get('username')

        user = self.user_model.get_by_auth_id(username)
        if not user:
            logging.warning('Could not find any user entry for username %s', username)
            self.params = {
                'username': username,
                'not_found': True
            }
            return self.get_response()

        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)

        #TODO: send email

        self.redirect('verification?type=p&user_id={}&signup_token={}'.format(user_id,token))
  
