from flask import *
import MySQLdb
import os, sys

#Establishes connection
conn = MySQLdb.connect(host = 'localhost',
 user='root',
 passwd='root',
 db='group74pa1')
 
albums = Blueprint('albums', __name__, template_folder='templates')

@albums.route('/fcda9697ef8a4a3aac8d/pa3/albums/edit', methods=['POST','GET'])
def albums_edit_route():
	if 'username' in session:
		options = {
			"edit": True,
			"sensitive": True
		}
		cursor = conn.cursor()
		conn.begin()

		username = session['username']
		if request.method == 'POST':
			op = request.form['op']
			########################## To ADD a new ALBUM
			if op == "add": ## add one more album, username and title
				title = request.form['title']
				username_from_form = request.form['username']
				private = "private"

				cursor.execute("INSERT INTO Album (title, created, lastupdated, username, access) VALUES (%s, NOW(), NOW(), %s, %s)", [title, username_from_form, private])
				conn.commit()

			######################### To DELETE one album
			elif op == "delete":
			## delet albumid-related data in albums, contain, photo
				albumid = request.form['albumid']
				## delete all the permissions granted by the album owner to other users
				cursor.execute("SELECT picid FROM Contain WHERE albumid = %s", [albumid])
				picidlist = cursor.fetchall()
				
				for picid in picidlist:
					cursor.execute("SELECT format FROM Photo WHERE picid = %s", [picid])
					extension = cursor.fetchone()[0]
					cursor.execute("DELETE FROM Photo WHERE picid = %s", [picid])
					os.remove("static/images/"+picid+'.'+extension)
				
				cursor.execute("DELETE FROM Album WHERE albumid = %s", [albumid])
				#cursor.execute("DELETE FROM AlbumAccess WHERE albumid=%s",[albumid])
				## select all the picids in the album with the id of albumid
				
				
				## delete those picid of the album in the database 
				## delete those picture files(.jpg) in /images/status
				## delete the Contain files in Contain
				#cursor.execute("DELETE FROM Contain WHERE albumid = %s", [albumid])
				
				## delete the album in table Album
				conn.commit()
				
			else:
				flash(error)
		else:
			print "alright"
		###############################################
		cursor.execute("SELECT title, albumid, access FROM Album WHERE username = %s",[username])

		title_albumid_access = []
		for album in cursor.fetchall():
			title_albumid_access.append(album)

		return render_template("albums.html",
								username = username,
								List = title_albumid_access,
								**options)
	else:
		return abort(403)



@albums.route('/fcda9697ef8a4a3aac8d/pa3/albums')
def albums_route():
	if 'username' in session:
		options = {
			"edit": False,
			"sensitive": True
		}
		# retrieve the username
		username = session['username']



		cursor = conn.cursor()
		conn.begin()

		cursor.execute("SELECT title, albumid FROM Album WHERE username=%s",[username])

		valid_test = cursor.fetchall()
		##this was used for p1, changed for p2
		##if not valid_test:
			##return abort(404)

		title_albumid = []
		for album in valid_test:
			title_albumid.append(album)
		cursor.close()

		return render_template("albums.html",
								List = title_albumid,
								username = username,
								**options)
	else:
		options = {
			"edit": False,
			"sensitive": False
		}
		username = request.args.get('username')

			
		cursor = conn.cursor()
		conn.begin()

		public = "public"
		cursor.execute("SELECT title, albumid FROM Album WHERE access=%s AND username=%s",[public, username])

		title_albumid = []
		for album in cursor.fetchall():
			title_albumid.append(album)
		cursor.close()

		return render_template("albums.html",
								List = title_albumid,
								username = username,
								**options)




