from flask import *
import MySQLdb
import os, hashlib, sys

conn = MySQLdb.connect(host = 'REDACTED',
 user='REDACTED',
 passwd='REDACTED',
 db='REDACTED')

# Pair with app.py
album = Blueprint('album', __name__, template_folder='templates')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp', 'gif'])

def allowed_file(filename):
	extension = filename.rsplit('.', 1)[1].lower()	
	return extension in ALLOWED_EXTENSIONS

# EDIT
@album.route('REDACTED/album/edit', methods=['GET', 'POST'])
def album_edit_route():
	# Authenticate
	if 'username' in session:
		username = session['username']
		options = {
			"edit": True, "sensitive": True
		}
		
		# Post specific response
		if request.method == 'POST':
			# Retrieve albumid
			albumid = request.form['albumid']

		elif request.method == 'GET':

            # Open connection
		    cursor = conn.cursor()
		    conn.begin()

            # Fetch album ID from url
			albumid = request.args.get('id')

			# Verify album ownership
			cursor.execute("SELECT username FROM Album WHERE albumid=%s",[albumid])
			if username != cursor.fetchone()[0]:
				return abort(403)	
			
			# Validate other users with permissions
            allowed_users = []
			cursor.execute("SELECT username FROM AlbumAccess WHERE albumid=%s",[albumid])
			for username in cursor.fetchall():
				allowed_users.append(username[0])

			# Fetch album data
			cursor.execute("SELECT title FROM Album WHERE albumid = %s", [albumid])
			title = cursor.fetchone()[0]
			cursor.execute("SELECT Contain.picid, Photo.format \
			FROM Contain, Photo \
			WHERE Contain.picid = Photo.picid AND Contain.albumid=%s \
			ORDER BY Contain.sequencenum ASC",[albumid])
			
			# Fetch photo data, file types -> render
			if cursor.rowcount != 0:	
				picid_format = []	
				for p_f in cursor.fetchall():
					picid_format.append([p_f[0],p_f[1]])
				return render_template("album.html", 
										picsList = picid_format, 
										albumTitle = title, 
										albumid = albumid,
										username_access=allowed_users,
										users=users,
										**options)
			# No data available
			## Catch -> render null 
			picsList = []
			return render_template("album.html",
									picsList=picsList,
									albumTitle=title,
									albumid=albumid,
									username_access=allowed_users,
									users=users,
									**options)
		# Invalid request method (not POST/GET)
		else:
			return abort(404)	

        # POST (continued)
		cursor.execute("SELECT title, username FROM Album WHERE albumid=%s",[albumid])

        # Verify request integrity, authority
		valid_test = cursor.fetchone()
		if not valid_test:
			return abort(404)
		title = valid_test[0]			
		owner = valid_test[1]
		if username != owner:
			return abort(403)
	
		# Retrieve op
		op = request.form['op']
		# ADD a new photo
		if op == "add":
			file = request.files['file']				
			if file and allowed_file(file.filename):	
				filename = file.filename
				extension = filename.rsplit('.', 1)[1].lower()	
                					
				# Hash picname for storage
				cursor.execute("SELECT username, title FROM Album WHERE albumid = %s", [albumid])
				username_title = cursor.fetchone()
				username = username_title[0]
				title = username_title[1]
				picid = hashlib.md5(username + title + filename).hexdigest()

				# Save, update backend db
				file.save('static/images/'+picid+'.'+extension)
				cursor.execute("INSERT INTO Photo (picid, format, date) VALUES (%s, %s, CURDATE())",[picid, extension])
				cursor.execute("SELECT MAX(sequencenum) FROM Contain WHERE albumid = %s", [albumid])

                # Fetch order (maintain consistency)
				sequencenum = cursor.fetchone()[0]
				if sequencenum == None:
					sequencenum = 0
				else:
					sequencenum += 1
				cursor.execute("INSERT INTO Contain (albumid, picid, sequencenum) VALUES (%s, %s, %s)",[albumid,picid,sequencenum])

		# DELETE a photo
		elif op == "delete":
            # Fetch pic data
			picid = request.form['picid']
			cursor.execute("SELECT format FROM Photo WHERE picid = %s", [picid])
			extension = cursor.fetchone()[0]

			# Delete from /static/images
			os.remove("static/images/"+picid+'.'+extension)

			# Fetch seqnum
			cursor.execute("SELECT MAX(sequencenum) FROM Contain WHERE albumid=%s", [albumid])
			max_sequenum = cursor.fetchone()[0]
			cursor.execute("SELECT sequencenum FROM Contain WHERE picid=%s", [picid])
			current = cursor.fetchone()[0]
			cursor.execute("UPDATE Contain SET sequencenum=%s WHERE sequencenum=%s",[current, max_sequenum])

            # Delete from Contain, Photo
			cursor.execute("DELETE FROM Contain WHERE picid=%s",[picid])
			cursor.execute("DELETE FROM Photo WHERE picid=%s",[picid])

        # Revoke users access
		elif op == "revoke":
			revokeusername = request.form['username']
			cursor.execute("DELETE FROM AlbumAccess WHERE albumid=%s AND username=%s", [albumid,revokeusername])
        # Grant user access
		elif op == "grant":
			grantusername = request.form['username']
			cursor.execute("INSERT INTO AlbumAccess (albumid, username) VALUES (%s, %s)", [albumid, grantusername])

        # Update album permissions
		elif op == "access":
			access = request.form['access']
			cursor.execute("UPDATE Album SET access=%s, lastupdated=CURDATE() WHERE albumid=%s",[access, albumid])
			if access == "public":
				cursor.execute("DELETE FROM AlbumAccess WHERE albumid=%s", [albumid])
		
        # Update album name
		elif op == "rename":
			title=request.form['newalbumname']
			cursor.execute("UPDATE Album SET title=%s WHERE albumid=%s",[title,albumid])

	    # Invalid op code
		else:
			flash(error)

		# Fetch access information for page return
        ## With
		users_with_access = []
		cursor.execute("SELECT username FROM AlbumAccess WHERE albumid=%s",[albumid])
		for username_incursor in cursor.fetchall():
			users_with_access.append(username_incursor[0])
        ## Without
		cursor.execute("SELECT username FROM User WHERE username !=%s AND username NOT IN(SELECT username FROM AlbumAccess WHERE albumid=%s)",[session['username'], albumid])
		users_without_access =[]
		for user in cursor.fetchall():
			users_without_access.append(user[0])

        # Fetch photos for page return
		cursor.execute("SELECT Contain.picid, Photo.format FROM Contain, Photo WHERE Contain.picid = Photo.picid AND Contain.albumid=%s ORDER BY Contain.sequencenum ASC",[albumid])
		if cursor.rowcount != 0:		
			picid_format = []	
			for p_f in cursor.fetchall():
				picid_format.append([p_f[0],p_f[1]])

            # Sanity check
			conn.commit()
			return render_template("album.html", 
									picsList = picid_format, 
									albumTitle = title, 
									albumid = albumid,
									username_access=users_with_access,
									users=users_without_access,
									**options)
        # Sanity check
		conn.commit()
		return render_template("album.html",
								picsList=list(),
								albumTitle=title,
								albumid=albumid,
								username_access=users_with_access,
								users=users_without_access,
                                **options)
	# No session
    else: 
		return abort(403)

# VIEW
@album.route('/REDACTED/album')
def album_route():
	options = {"sensitive": False}
    # Authenticate
	if 'username' in session:
		options['sensitive'] = True
	return render_template("album.html", **options)
