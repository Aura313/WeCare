import re
import database as db
import random
import string

def isString(_value, _size = 30):
	#Split the name into all the words
	#Check if every word is alphabets only or not
	#Also check for the size limit

	if len(_value) > _size:
		return (-1,'Size Limit Exceeded')

	words = _value.split()
	for word in words:
		if not word.isalpha:
			return (-2,'Non alphabets found')

	return (0,'Success')

def isEmail(_email):


	EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

	if not EMAIL_REGEX.match(_email):
		return (-1,'Invalid email id')
	return(0,'Success')

def isPassword(_password):

	password_char = re.match(r"[a-zA-Z0-9,\.\_\@\#\$\%\^\&\+\=]",_password)

	if not password_char:
		return(-1,'Invalid password')
	else:
		return(0,'valid password')

def createRandomString(_size = 20):
	strings = string.letters+string.digits
	value = ''
	for i in range(_size):
		value += random.choice(strings)
		
	return value





	# password = raw_input("Enter string to test: ")
	# if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
	# 	return(0,'Success')
	# else:
	# 	return(-1,'Invalid password')