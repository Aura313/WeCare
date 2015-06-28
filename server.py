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
        print "check_cookies: session,user = ", session_id, " ", user_id
        # session_id = self.request.get("session_id")
        # user_id = self.request.get("_userid")

        # status_session_id = utility.createRandomString()
        # status_user_id = utility.createRandomString()

        return db.User.CheckSession(_sessionid = session_id, _userid = user_id)

class MainPage(Handler): #Register
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
            self.render("You're registered!",error_name = name_verify_message, error_email = email_verify_message)
            return 

        status_code, status_message = db.User.CreateUser(_name = name , _username = username , _password = password , _email = email , _age = 69)
        print 'Register Works'

class LoginPage(Handler):
    def get(self):
        self.render("login-form.html")

    def post(self):
        #email_or_username
        login_id = self.request.get("username_email")
        password = self.request.get("password")

        login_id_verify_status, login_id_verify_message = utility.isString(login_id)
        password_verify_status, password_verify_message = utility.isPassword(password)
              
        #Sanitize the input (else statement with error message)

        status_code , status_message = db.User.CheckCredentials(_email_or_username = login_id , _password = password)
        if status_code == 0:
            session_id = status_message[0]
            user_id = status_message[1]

            print 'user id, session_id', user_id , session_id
            #Create cookies out of this
        
            self.response.headers['Content-Type'] = 'text/plain'
            # session_id = self.request.cookies.get('session_id', '0')
            # user_id = self.request.cookies.get('user_id', '1')

            self.response.headers.add_header('Set-Cookie', 'session_id=%s'  % session_id)
            self.response.headers.add_header('Set-Cookie', 'user_id=%s' % user_id)


            print 'LoginPage:Post ', session_id , user_id
            self.redirect('/')

        else:
            self.render("login-form.html", error_username_email = status_message)

        #self.redirect("/homepage")

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
        session_id = self.request.cookies.get('session_id')
        user_id = self.request.cookies.get('user_id')
        if self.check_cookies(session_id, user_id):
            self.write("You're in your home")
        else:
            self.redirect("/login")

    def post(self):
            #self.write("""<label> HomePage <input type = "button" name ="HomePage"></label>""")
        session_id = self.request.cookies.get('session_id')
        user_id = self.request.cookies.get('user_id')
        if self.check_cookies(session_id, user_id):
            self.write("You're in your home")
        else:
            self.redirect("/login")


class LogoutPage(Handler):
    def get(self):

        session_id = self.request.cookies.get('session_id')
        user_id = self.request.cookies.get('user_id')

        #delete cookies
        #call removesession(userid , sessionid)


        self.redirect("/")




class ConditionsPage(Handler):
    def get(self):
        self.render("conditions.html")

    def post(self):
        #self.write("""<label><input type = "button" name ="Conditions"></label>""")

        user_condition = self.request.get("condition_title")
        user_condition_verify_status , user_condiion_verify_message = utility.isString(user_condition)

        status_code , status_message = db.Conditions.conditionSearch(_condition_title = user_condition)
        

class TreatmentsPage(Handler):
    def get(self):
        self.write("Hi, I'm the treatments you should follow to get fixed!")

    def post(self):
        self.write("")

class Forums(Handler):
    def get(self):
        self.write("Hi , I just might be able to connect with people who are willing to share their experience!Keep posting!")
    
    def post(self):
        self.write("""<label><input type = "button" name ="Forums"></label>""")



app = webapp2.WSGIApplication([('/signup', MainPage),
                                ('/login', LoginPage),
                                ('/', HomePage),
                                ('/logout', LogoutPage),
                                ('/conditions', ConditionsPage),
                                ('/treatments', TreatmentsPage),
                                ('/forums', Forums)
                               ],
                              debug=True)

