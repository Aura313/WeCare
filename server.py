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


template_dir = os.path.join(os.path.dirname(__file__), 'Frontend')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a,**kw)

    def render_Str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_Str(template, **kw))

    def check_cookies(self, session_id, user_id):
        return True

class MainPage(Handler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        name = self.request.get("name")
        username = self.request.get("username")
        password = self.request.get("password")
        verify_password = self.request.get("verify_password")
        email = self.request.get("email")
        age = self.request.get("age")

        name_verify_status, name_verify_message = utility.isString(name)
        email_verify_status, email_verify_message = utility.isEmail(email)


        
        #Verify the status messages before proceeding
        if name_verify_status < 0 or email_verify_status < 0:
            self.render("signup-form.html",error_name = name_verify_message, error_email = email_verify_message)
            return 

        status_code, status_message = db.User.create_user(_name = name , _username = username , _password = password , _email = email , _age = 69)
        
class LoginPage(Handler):
    def get(self):
        self.render("login-form.html")

    def post(self):
        
        #Take username/email from request
        #Take password from request

        #Sanitize the inputs

        #Ask the DB if the credentials match

        #If they match, 
            #Create cookies of sessionID, and userID (add header)

        #Else
            #Return appropriate errors

class HomePage(Handler):
    def get(self):
        #Get sessionID and userId from cookies
        session_id = '1'
        user_id = '2'
        if self.check_cookies(session_id, user_id):
            self.write("You're in :)")

        else:
            self.redirect("/login")



app = webapp2.WSGIApplication([('/', MainPage),
                                ('/login', LoginPage),
                               ],
                              debug=True)

