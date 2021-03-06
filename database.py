import re
import random
import hashlib
import hmac
from string import letters
import utility
import populate as pop


from google.appengine.ext import ndb

class GroupName(ndb.Model):
	condition_group_title = ndb.StringProperty(required = True)
	#diseases_group_title = ndb.StringProperty(required = True)

	@classmethod
	def CreateGroup(self,_user_condition_group_title):

		if not 	(self.isUniqueGroup(_user_condition_group_title)): #make is unique group
			print 'database:GroupName:CreateGroup: ERROR: condition already exists'
			return (-1, 'There already exists a condition with that name.')
		
		new_condition_group_title = GroupName(condition_group_title = _user_condition_group_title)
		new_condition_group_title.put()

		print 'database:GroupName:CreateGroup: Entered', _user_condition_group_title
		return (0,'New Condition group Added')
	
	@classmethod
	def isUniqueGroup(self, _group_title):
		users = self.query(GroupName.condition_group_title == _group_title).fetch()
		return len(users) <  1

	@classmethod
	def populate(self):
		group_titles = pop.get_groups()
		for group in group_titles:
			if self.isUniqueGroup(_group_title = group):
				self.CreateGroup(_user_condition_group_title = group)

	@classmethod
	def getKeyFromName(self,_group_title):
		users = self.query(GroupName.condition_group_title == _group_title).fetch()
		if len(users) > 0:
			return users[0].key		#Maybe brackets not required.
			

class Conditions(ndb.Model):
	condition_title = ndb.StringProperty(required = True)
	condition_group_key = ndb.KeyProperty(kind = GroupName)
   ## patients_with_condition_count = ndb.IntegerProperty()

   	@classmethod
	def CreateCondition(self,_user_condition_title, _condition_group_key):

		if not 	(self.isUniqueCondition(_user_condition_title)): #make is unique group
			print 'database:Conditions:CreateCondition: ERROR: condition already exists'
			return (-1, 'There already exists a condition with that name.')
		
		new_condition_title = Conditions(condition_title = _user_condition_title, condition_group_key = _condition_group_key)
		new_condition_title.put()

		print 'database:Conditions:CreateCondition: Entered', _user_condition_title
		return (0,'New Conditions Added')


   	@classmethod
	def isUniqueCondition(self, _condition_title):
		users = self.query(Conditions.condition_title == _condition_title).fetch()
		return len(users) <  1



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
		


	@classmethod
	def populate(self):

		condition_titles = pop.get_conditions()

		for condition in condition_titles:
			condition_name = condition[0]
			condition_group = condition[1]

			key = GroupName.getKeyFromName(_group_title = condition_group)

			conditions = self.CreateCondition(_user_condition_title = condition_name , _condition_group_key = key)


   

class Treatments(ndb.Model):
	treatment_title = ndb.StringProperty()

	@classmethod
	def search(self,_user_treatment):
		return True


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
	def CreateAdmin(self, _username , _name, _password, _email, _age):

		admin = User(name = _name , username = _username , password = _password , email = _email , age = _age)
		admin.put()

		return (True , 'Welcome Admin')





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
			return (0,(session_id, user.key.urlsafe()))
		else:
			#Password do not match
			return (-2,"Login credentials are incorrect")



	@classmethod
	def CreateSession(self,_user):
		#Create a random string of 20 size
		
		session_id = utility.createRandomString()
		_user.active_sessions.append(session_id)
		_user.put()
		return session_id


	@classmethod
	def CheckSession(self,_userid,_sessionid):
		#From the userid, get the user from the DB
		

		try:
			user = ndb.Key(urlsafe = _userid).get()
		except :
			print "database:CheckSession: user not found" 
			return False 
		#print "user is -" ,user
		if user is None: 
			return False
		return _sessionid in user.active_sessions



	
	@classmethod
	def RemoveSession(self, _userid ,_sessionid):
		#Get user from userid
		try:
			user = ndb.Key(urlsafe = _userid).get()
			print "user is ", user

			user.active_sessions.remove(_sessionid)
			user.put()



		# 	if _sessionid.index(""):
		# 		i = _sessionid.index("")
		# 		del _sessionid[i]
		# #in User:
			#delete current active session
		except:

			return False
		return True

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

   	@classmethod
   	def getEntityByKey(self,_user_id):
   		#This expects only a key. Not a urlsafe, or an ID
   		return _user_id.get()

class Posts(ndb.Model):
    post_text = ndb.StringProperty()
    post_time = ndb.DateTimeProperty(auto_now_add = True)
    post_mood = ndb.StringProperty()
    user_id= ndb.KeyProperty(kind= User)
    #post_up 
    #post_down

    @classmethod
    def CreatePosts(self, _post_text , _post_mood, _user_id ):

    	if not utility.isValidMood(_post_mood):
    		print "database.Posts.CreatePosts: Not a valid mood", _post_mood
    		return(-1, 'Not a valid mood.')

    	user_key = ndb.Key(urlsafe = _user_id)
    	print "database.Posts.CreatePosts: User %s has posted %s." % (user_key, _post_text)


    	new_post = Posts(post_text = _post_text, post_mood = _post_mood, user_id = user_key)
    	new_post.put()

    	return(0 ,'Successsfully posted')

    @classmethod
    def getPostsForUser(self , _user_id):
    	user_key = ndb.Key(urlsafe = _user_id)
    	
    	posts = self.query().fetch()

    	print "database:Posts:getPostsForUser: Query found."
    	print posts
    	return posts
    	

class Crisis(ndb.Model):
	crisis_name = ndb.StringProperty()
	crisi_helpline_number = ndb.IntegerProperty()

class Forums(ndb.Model):
	forum_id = ndb.IntegerProperty()
	forum_time_date = ndb.DateTimeProperty(auto_now = True)
	user = ndb.KeyProperty(kind= User)
	#forum_up
	#forum_down

		