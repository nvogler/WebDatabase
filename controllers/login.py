from flask import *
import MySQLdb

# Initialize Flask app with the template folder address
login = Blueprint('login', __name__, template_folder='templates')

@login.route('/fcda9697ef8a4a3aac8d/pa3/login', methods=['GET', 'POST'])
def login_route():
	if 'username' in session:
		return redirect('fcda9697ef8a4a3aac8d/pa3/user/edit')
	return render_template("login.html")