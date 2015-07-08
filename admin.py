import os
import re
import random
import hashlib
import hmac
from string import letters

import webapp2
import jinja2

#Import Local Things
import database as db
import utility


from google.appengine.api import users

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a,**kw)

    def render_Str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_Str(template, **kw))

class AdminLogin(Handler):
	def get(self):
		self.render("admin-login.html")

	def post(self):	
		user = users.get_current_user()

		if user:
		    print 'Welcome, %s!' % user.nickname()
		    if users.is_current_user_admin():
		        print '<a href="/admin/">Go to admin area</a>'



app = webapp2.WSGIApplication([('/admin', AdminLogin), ],debug=True)
