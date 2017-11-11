from datetime import datetime
from collections import namedtuple
from flask import *
import MySQLdb, string, re, hashlib, uuid

user_api = Blueprint('user_api', __name__, template_folder='views')

conn = MySQLdb.connect(host = 'localhost',
 user='root',
 passwd='root',
 db='group74pa1')
 
allowed_char = string.letters + string.digits + '_'

algorithm = 'sha512'
salt = uuid.uuid4().hex


#account info checks
def password_contain_check(password):
	contain_letter = False
	contain_digits = False
	for char in password:
		if char in string.letters:
			contain_letter = True
		if char in string.digits:
			contain_digits = True
	return contain_digits and contain_letter
	
def check_username(username, errorMsgList):
	cursor = conn.cursor()
	conn.begin()
	cursor.execute("SELECT username FROM User")
	username_tuple = cursor.fetchall()
	for tuple in username_tuple:
		if username == tuple[0]:
			errorMsgList.append({'message': "This username is taken"})
	if len(username) < 3:
		errorMsgList.append({'message': "Usernames must be at least 3 characters long"})
	for char in username:
		if char not in allowed_char:
			errorMsgList.append({'message': "Usernames may only contain letters, digits, and underscores"})
	if len(username) > 20:
		errorMsgList.append({'message': "Username must be no longer than 20 characters"})
	
def check_password(password, cfmpassword, errorMsgList):
	if len(password) < 8:
		errorMsgList.append({'message': "Passwords must be at least 8 characters long"})
	if password_contain_check(password) == False:
		errorMsgList.append({'message': "Passwords must contain at least one letter and one number"})
	for char in password:
		if char not in allowed_char:
			errorMsgList.append({'message': "Passwords may only contain letters, digits, and underscores"})
	if password != cfmpassword:
		errorMsgList.append({'message': "Passwords do not match"})
		
def check_firstname(firstname, errorMsgList):
	if len(firstname) > 20:
		errorMsgList.append({'message': "Firstname must be no longer than 20 characters"})

def check_lastname(lastname, errorMsgList):
	if len(lastname) > 20:
		errorMsgList.append({'message': "Lastname must be no longer than 20 characters"})
		
def check_email(email, errorMsgList):
	if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
		errorMsgList.append({'message': "Email address must be valid"})
	if len(email) > 40:
		errorMsgList.append({'message': "Email must be no longer than 40 characters"})
#end account info checks
	
@user_api.route('/api/v1/user', methods=['POST', 'GET', 'PUT'])
def user():
	
	if request.method == 'POST':
		cursor = conn.cursor()
		if 'username' in session:
			return redirect('fcda9697ef8a4a3aac8d/pa3/user/edit')
		
		errorMsgList = []
		username = request.get_json(force=True)["username"]
		password1 = request.get_json(force=True)["password1"]
		password2 = request.get_json(force=True)["password2"]
		firstname = request.get_json(force=True)["firstname"]
		lastname = request.get_json(force=True)["lastname"]
		email = request.get_json(force=True)["email"]
		check_username(username, errorMsgList)
		check_password(password1, password2, errorMsgList)
		check_firstname(firstname, errorMsgList)
		check_lastname(lastname, errorMsgList)
		check_email(email, errorMsgList)
		if not errorMsgList:
			m = hashlib.new(algorithm)
			m.update(salt + password1)
			password_hashed = m.hexdigest()
			password_encrypted = "$".join([algorithm, salt, password_hashed])
			cursor.execute("INSERT INTO User VALUES(%s, %s, %s, %s, %s)", [username, firstname, lastname, password_encrypted, email])
			conn.commit()
			return make_response(jsonify(errors = errorMsgList), 201)
		else: 
			return make_response(jsonify(errors = errorMsgList), 422)

	elif request.method == 'GET':
	
		errorMsgList = []	
		if 'username' in session:
			username = session['username']
			cursor = conn.cursor()
			cursor.execute("SELECT firstname FROM User WHERE username = %s", [username])
			firstname = cursor.fetchone()[0]
			cursor.execute("SELECT lastname FROM User WHERE username = %s", [username])
			lastname = cursor.fetchone()[0]
			cursor.execute("SELECT email FROM User WHERE username = %s", [username])
			email = cursor.fetchone()[0]
			return jsonify(username=username,
							firstname=firstname,
							lastname=lastname,
							email=email)
		else:
			errorMsgList.append({'message': "You do not have the necessary credentials for the resource"})
			return jsonify(errors = errorMsgList), 401
			
	elif request.method == 'PUT':
				
		errorMsgList = []
		cursor = conn.cursor()
		
		username = session['username']
		password1 = request.get_json(force=True)['password1']
		password2 = request.get_json(force=True)['password2']
		firstname = request.get_json(force=True)['firstname']
		lastname = request.get_json(force=True)['lastname']
		email = request.get_json(force=True)['email']
		if len(password1) != 0 or len(password2) != 0:
			check_password(password1, password2, errorMsgList)
		check_firstname(firstname, errorMsgList)
		check_lastname(lastname, errorMsgList)
		check_email(email, errorMsgList)
		if not errorMsgList:
			if len(password1) != 0 and len(password2) != 0:
				m = hashlib.new(algorithm)
				m.update(salt + password1)
				password_hashed = m.hexdigest()
				new_password = "$".join([algorithm, salt, password_hashed])
				cursor.execute("UPDATE User SET password = %s WHERE username = %s", [new_password, username])
			cursor.execute("UPDATE User SET firstname = %s WHERE username = %s", [firstname, username])
			cursor.execute("UPDATE User SET lastname = %s WHERE username = %s", [lastname, username])
			cursor.execute("UPDATE User SET email = %s WHERE username = %s", [email, username])
			
			conn.commit()
			return make_response(jsonify(errors = errorMsgList), 201)
		else: 
			return make_response(jsonify(errors = errorMsgList), 422)
	#update error
	return abort(403)
