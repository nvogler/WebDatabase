from flask import *
import MySQLdb, string, re, hashlib, uuid

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/fcda9697ef8a4a3aac8d/pa3/user', methods = ['GET'])
def new_user_route():
	if 'username' in session:
		return redirect('fcda9697ef8a4a3aac8d/pa3/user/edit')
	return render_template("user.html")

@user.route('/fcda9697ef8a4a3aac8d/pa3/user/edit', methods = ['GET'])
def user_edit_route():
	if 'username' in session:
		options = {"sensitive" :True}
		return render_template("user_edit.html", **options)
	return abort(403)

		