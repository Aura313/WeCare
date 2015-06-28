import re
import random
import hashlib
import hmac
from string import letters
import utility


from google.appengine.ext import ndb

class GroupName(ndb.Model):
	condition_group_title = ndb.StringProperty(required = True)
	#diseases_group_title = ndb.StringProperty(required = True)


	def CreateGroup(self,_user_condition_group_title):

		if not (self.isUniqueUsername(_user_condition_group_title)):
			print 'database:GroupName:CreateGroup: ERROR: condition already exists'
			return (-1, 'There already exists a condition with that name.')
		
		new_condition_group_title = GroupName(condition_group_title = _user_condition_group_title)
		new_condition_group_title.put()

		print 'database:User:CreateGroup: Entered'
		return (0,'New Conditions Added')
	



class Conditions(ndb.Model):
	condition_title = ndb.StringProperty(required = True)
	condition_group_title = ndb.KeyProperty(kind = GroupName)
   ## patients_with_condition_count = ndb.IntegerProperty()

  	@classmethod
  	def conditionsSearch(self , _condition_title , _condition_group_title):

  		conditions = self.query(ndb.OR(self.condition_title == _condition_title , 
								 self.condition_group_title == _condition_group_title)).fetch()


  		# if condition_title in condition_group_title:
  		# 	return condition_title
  		# else:
  		# 	print "Error"


  		if len(conditions) < 1:
			return (-1,"No such condition exists")

		condition = conditions[0]
		




   	# @classmethod
   	# def search(self,_user_condition):
   	# 	return

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
	def CreateUser(self, _username , _name, _password, _email, _age):
		#register.
		#Assuming that the all the four parameters are proper strings with appropriate lengths
        #This function will however check if the email id and username are unique or not.

        #Check uniqueness here
        
		if not (self.isUniqueUsername(_username) and self.isUniqueEmail(_email)):
			print 'database:User:CreateUser: ERROR: _username/email not unique'
			return (-1, 'There already exists an account with this username/email.')

		new_user = User(name = _name , username = _username , password = _password , email = _email , age = _age)
		new_user.put()
		
		print 'database:User:CreateUser: Successsfully Registered', new_user.key.id()
		return (0,'Welcome to WeCare!')

	@classmethod
	def isUniqueUsername(self,_username):
        #Takes in a valid username
        #Return true if username is unique
        #Return false if username is not unique 
		users = self.query(User.username == _username).fetch()
		print 'database:User:isUniqueUsername: Number of users found-', len(users)
		return not len(users) > 0

	@classmethod
	def isUniqueEmail(self,_email):
		users_email = self.query(User.email == _email).fetch()
		print 'database:User:isUniqueEmail: Number of users found-', len(users_email)
		return not len(users_email) > 0


	@classmethod
	def CheckCredentials(self,_email_or_username, _password):	#Login
		
		# users = self.query(ndb.AND(self.password == _password,
		# 						ndb.OR(self.username == _email_or_username , 
		# 						 self.email == _email_or_username))).fetch()

		#Users contain a list of users by the same username as passed to this function
		users = self.query(ndb.OR(self.username == _email_or_username , 
								 self.email == _email_or_username)).fetch()
		
		#If none user found
		if len(users) < 1:
			return (-1,"No such user exists")

		user = users[0]
		#Checking for password
		if user.password == _password:
			#His credentials are correct.
			session_id = self.CreateSession(user)
			return (0,(session_id, user.key.id()))
		else:
			#Password do not match
			return (-2,"Login credentials are incorrect")

								  

		

	 #  #	@@@@@@@@@@@@@@@@@@@@@@@@@@@@     HELP TEXT!! @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	 #  # qry = Article.query(ndb.AND(Article.tags == 'python',
	 #  #                           ndb.OR(Article.tags.IN(['ruby', 'jruby']),
	 #  #                                  ndb.AND(Article.tags == 'php',
	 #  #                                          Article.tags != 'perl'))))



		# #Check if the users list contains something or not
		# 	#If contains nothing. Then no user exists by this email or username. Ask the client to sign up instead
		# 	#return (-1, 0)

		# #Else if it the case
		# #user = users[0]
		
		# if len(users) > 0:
		# 	#if user_password == _password:
		# 	print 'database:User:CheckCredentials: Found User', users[0]
		# 	return(0,users[0])			
		
		# else:
		# 	print 'database:User:CheckCredentials: EmptyList'
		# 	return(-1,'There are no registered users yet')




		# #Check if user.password == _password
		# 	#If not then return -1 or -2 status, message (invalid credentials)

		# #The credentials match and user should be logged in.
		# session_id = self.CreateSession(user)

		# return (session_id,user.key.id())

	
	@classmethod
	def logout(self, _username ,_sessionid):
		#for username in User:
			#delete current active session
		return


	@classmethod
	def CreateSession(self,_user):
		#Create a random string of 20 size
		session_id = utility.createRandomString()
		_user.active_sessions.append(session_id)
		_user.put()
		return session_id.key.id()


	@classmethod
	def CheckSession(self,_userid,_sessionid):
		#From the userid, get the user from the DB

		if _sessionid in active_sessions:
			return True
		return False 

		#If _sessionid exists in its active session,
			#return true

			#else return false
		#return True

	@classmethod
	def EditProfile(self,_username, _name, _currentpassword, _age , _location, _email):
		return


	@classmethod
	def UserCondition(self, _user_condition):
		return

	@classmethod
	def UserTreatment(self, _user_treatment):
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

		