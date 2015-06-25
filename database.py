import re
import random
import hashlib
import hmac
from string import letters


from google.appengine.ext import ndb

class Conditions(ndb.Model):
	condition_title = ndb.StringProperty()
   # patients_with_condition_count = ndb.IntegerProperty()
   	@classmethod
   	def search(self,_user_condition):
   		return

class Treatments(ndb.Model):
	treatment_title = ndb.StringProperty()

	@classmethod
   	def search(self,_user_treatment):
   		return


class User(ndb.Model):
	name = ndb.StringProperty(required = True)
	username = ndb.StringProperty(required = True , indexed = True)
	active_sessions = ndb.StringProperty(repeated = True)
	password = ndb.StringProperty(required = True)
	email = ndb.StringProperty(required = True)
	interests = ndb.StringProperty()
	age = ndb.IntegerProperty(required = True)
	location = ndb.StringProperty()
	user_condition = ndb.KeyProperty(kind = Conditions)
	user_treatment =ndb.KeyProperty(kind = Treatments)
	user_status = ndb.StringProperty() 			# I'm here for myself. | I'm looking up for someone. | Other 
	user_registrationtime = ndb.DateTimeProperty(auto_now_add = True)

	@classmethod
	def create_user(self, _username , _name, _password, _email, _age):
		#register.
		#Assuming that the all the four parameters are proper strings with appropriate lengths
        #This function will however check if the email id and username are unique or not.

        #Check uniqueness here
        
		if not (self.isUniqueUsername(_username) and self.isUniqueEmail(_email)):
			print 'database:User:create_user: ERROR: _username/email not unique'
			return (-1, 'There already exists an account with this username/email.')

		new_user = User(name = _name , username = _username , password = _password , email = _email , age = _age) #Write this properly
		
		new_user.put()
		print 'database:User:create_user: Successsfully Registered', new_user.key.id()
		return (0,'Welcome to WeCare!')

	@classmethod
	def isUniqueUsername(self,_username):
        #Takes in a valid username
        #Return true if username is unique
        #Return false if username is not unique 
		users = self.query(User.username == _username).fetch()
		print 'database:User:isUniqueUsername: ', len(users)
		return not len(users) > 0

	@classmethod
	def isUniqueEmail(self,_email):
		users_email = self.query(User.email == _email).fetch()
		print 'database:User:isUniqueUsername: ', len(users_email)
		return not len(users_email) > 0


	@classmethod
	def check_credentials(self,_email_or_username, _password):	#Login
		
		users = User.query(ndb.OR( User_username == _email_or_username , User_email = _email_or_username)).fetch()
		
		#Check if the users list contains something or not
			#If contains nothing. Then no user exists by this email or username. Ask the client to sign up instead
			#return (-1, 0)

		#Else if it the case
		#user = users[0]
		
		#Check if user.password == _password
			#If not then return -1 or -2 status, message (invalid credentials)

		#The credentials match and user should be logged in.
		session_id = self.create_session(user)

		return (session_id,user.key.id())

	
	@classmethod
	def logout(self, _username ,_sessionid):
		#for username in User:
			#delete current active session
		return


	@classmethod
	def create_session(self,_userid):
		return


	@classmethod
	def check_session(self,_userid,_sessionid):
		return

	@classmethod
	def edit_profile(self,_username, _name, _currentpassword, _age , _location, _email):
		return


	@classmethod
	def condition_user(self, _user_condition):
		return

	@classmethod
	def treatment_user(self, _user_treatment):
		return

   	@classmethod
   	def search(self,_name,_username):
   		return





class Posts(ndb.Model):
    post_text = ndb.StringProperty()
    post_time = ndb.DateTimeProperty(auto_now_add = True)
    post_mood = ndb.StringProperty()
    user = ndb.KeyProperty(kind= User)
    #post_up 
    #post_down


class Crisis(ndb.Model):
	crisis_name = ndb.StringProperty()
	crisi_helpline_number = ndb.IntegerProperty()

class Forums(ndb.Model):
	forum_id = ndb.IntegerProperty()
	forum_time_date = ndb.DateTimeProperty(auto_now = True)
	user = ndb.KeyProperty(kind= User)
	#forum_up
	#forum_down

		