import re

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