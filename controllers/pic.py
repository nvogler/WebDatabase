from flask import *
import MySQLdb

pic = Blueprint('pic', __name__, template_folder='templates')

@pic.route('/fcda9697ef8a4a3aac8d/pa3/pic', methods = ['GET', 'POST'])
def pic_route():
	if 'username' in session:
		options = {"sensitive":True}
	return render_template("pic.html", **options)
