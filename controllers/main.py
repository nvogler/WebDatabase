from flask import *
import MySQLdb, string, re, os

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/fcda9697ef8a4a3aac8d/pa3/live')
def live_route():
	return send_file('templates/live.html')