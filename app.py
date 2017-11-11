from flask import *
from extensions import mysql
import MySQLdb
import controllers
import API
import hashlib, uuid

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

# Initialize MySQL database connector
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'group74pa1'
app.config['localhost'] = '127.0.0.1'
mysql.init_app(app)
# Register the controllers
app.register_blueprint(controllers.album)
app.register_blueprint(controllers.albums)
app.register_blueprint(controllers.pic)
app.register_blueprint(controllers.login)
app.register_blueprint(controllers.user)
app.register_blueprint(API.user_api)
app.register_blueprint(API.login_api)
app.register_blueprint(API.album_api)
app.register_blueprint(API.pic_api)
app.register_blueprint(API.api)
######################################################
app.secret_key = 'some_secret485-74'

#Establishes connection
conn = MySQLdb.connect(host = 'localhost',
 user='root',
 passwd='root',
 db='group74pa1')

@app.route('/fcda9697ef8a4a3aac8d/pa4/live')
def live_route():
	return send_file('templates/live.html')
	
@app.route('/fcda9697ef8a4a3aac8d/pa4')
def index():
	
	cursor = conn.cursor()
	conn.begin()

	if 'username' in session:
		## sensitive 
		options = {
			"sensitive": True
		}
		username = session['username']
		cursor.execute("SELECT firstname, lastname FROM User WHERE username=%s",[username])
		first_lastname=cursor.fetchone()
		############
		cursor.execute("SELECT albumid, title FROM Album WHERE access=\'public\'")
		albumid_title=[]
		for id_title in cursor.fetchall():
			albumid_title.append([id_title[0],id_title[1]])
		cursor.execute("SELECT albumid FROM AlbumAccess WHERE username=%s",[username])
		for albumid in cursor.fetchall():
			cursor.execute("SELECT title FROM Album WHERE albumid=%s",[albumid[0]])
			albumid_title.append([albumid[0],cursor.fetchone()[0]])
		cursor.execute("SELECT albumid, title FROM Album WHERE username=%s", [username])
		for id_title in cursor.fetchall():
			albumid_title.append([id_title[0],id_title[1]])

		return render_template("index.html", 
								first_last=first_lastname, 
								albumid_title=albumid_title,
								**options)

	else:
		## public
		options = {
			"sensitive": False
		}
		## no session involed, public page
		cursor.execute("SELECT albumid, title FROM Album WHERE access=\'public\'")
		albumid_title = cursor.fetchall()
		return render_template("index.html", 
								albumid_title=albumid_title,
								**options)

######################################################
# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host='0.0.0.0', port=3000, debug=True)

