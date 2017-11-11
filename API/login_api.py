from datetime import datetime
from collections import namedtuple
from flask import *
import MySQLdb, string, re, hashlib, uuid

conn = MySQLdb.connect(host = 'DEIDENTIFIED',
 user='DEIDENTIFIED',
 passwd='DEIDENTIFIED',
 db='DEIDENTIFIED')
 
algorithm = 'sha512'

# Pair with app.py
login_api = Blueprint('login_api', __name__, template_folder='views')

@login_api.route('/api/v1/login', methods = ['POST'])
def login():
	# Currently authenticated, redirect to edit
	if 'username' in session:
		return redirect('DEIDENTIFIED/user/edit')
	# Verify post request
	if request.method == 'POST':
		# Open connection 
		cursor = conn.cursor()
		conn.begin()
		
		# Extract user input
		## Validate
		errors = []
		try:
			username_from_user = request.get_json()["username"]
			password_from_user = request.get_json()["password"]
		except HTTPException:
			errors.append({'message': "You did not provide the necessary fields"})
			return jsonify(errors = errors), 422
		
		# Verify user information in DB
		cursor.execute("SELECT password FROM User WHERE username = %s", [username_from_user]) 
		password_stored = cursor.fetchone()
		## Confirm username
		if not password_stored:
			errors.append({'message': "Username does not exist"})
			return jsonify(errors = errors), 404
		else:
			# Confirm password
			# ALG | SALT | PASS
			m = hashlib.new(algorithm)
			password_stored = password_stored[0]
			salt_from_db = str(password_stored).split('$')[1]
			m.update(salt_from_db + password_from_user)
			pass_hash_from_user = m.hexdigest()
			attemptd_password = "$".join([algorithm, salt_from_db, pass_hash_from_user])
			
			## Password valid
			if attemptd_password == password_stored:
				session['username'] = username_from_user
				# Fetch additional user data for session
				cursor.execute("SELECT firstname FROM User WHERE username = %s", [username_from_user])
				session['firstname'] = cursor.fetchone()[0]
				cursor.execute("SELECT lastname FROM User WHERE username = %s", [username_from_user])
				session['lastname'] = cursor.fetchone()[0]
				return make_response(jsonify(username=username_from_user), 200)
			else:
				## Password invalid
				errors.append({'message': "Password is incorrect for the specified username"})
				return jsonify(errors = errors), 404
	# Invalid request method
	return abort(500)
	
# Handle logout
@login_api.route('/api/v1/logout', methods = ['POST'])
def logout():
	errors = []
	if 'username' in session:
		session.pop('username', None)
		return make_response("", 204)
	else:
		errors.append({'message': "You do not have the necessary credentials for the resource"})
		return jsonify(errors = errors), 401
		
		
		
		
		
		
		