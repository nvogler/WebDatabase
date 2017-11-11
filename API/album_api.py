from collections import namedtuple
from flask import *
import MySQLdb, string, re

album_api = Blueprint('album_api', __name__, template_folder='views')

conn = MySQLdb.connect(host = 'localhost',
 user='root',
 passwd='root',
 db='group74pa1')
cursor=conn.cursor()

@album_api.route('/api/v1/album/<albumid>', methods=['GET'])
def album(albumid):
	errors = []

	cursor.execute("SELECT access, username FROM Album WHERE albumid = %s", [albumid])
	au = cursor.fetchone()
	if not au:
		errors.append({'message': "The requested resource could not be found"})
		return jsonify(errors = errors), 404
	access = au[0]
	owner = au[1]
	if 'username' in session:
		user = session['username']
		if user != owner and access == 'private':
			cursor.execute("SELECT * FROM AlbumAccess WHERE albumid = %s AND username = %s", [albumid, user])
			if not cursor.fetchone():
				errors.append({'message':  "You do not have the necessary permissions for the resource"})
				return jsonify(errors = errors), 403
	elif access == 'private':
		print "here"
		errors.append({'message':  "You do not have the necessary credentials for the resource"})
		return jsonify(errors = errors), 401
	
	cursor.execute("SELECT * FROM Album where albumid=%s",[albumid])
	album = cursor.fetchone()
	cursor.execute("SELECT picid, caption, sequencenum FROM Contain where albumid=%s ORDER BY sequencenum ASC",[albumid])
	picslist = cursor.fetchall()
	pics = []
	for pic in picslist:
		pic_attempt = {}
		pic_attempt['albumid'] = albumid
		pic_attempt['caption'] = pic[1]
		cursor.execute("SELECT picid, format, date FROM Photo where picid=%s",[pic[0]])
		id_format_date = cursor.fetchone()
		pic_attempt['date'] = str(id_format_date[2])
		pic_attempt['format'] = id_format_date[1]
		pic_attempt['picid'] = pic[0]
		pic_attempt['sequencenum'] = pic[2]
		pics.append(pic_attempt)
	access = album[5]
	lastupdated = album[3]
	lastupdated = str(lastupdated)
	created=album[2]
	created = str(created)
	title=album[1]
	username=album[4]
	return jsonify(access=access,
		albumid=albumid,
		created=created,
		lastupdated=lastupdated,
		pics=pics,
		title=title,
		username=username), 200
















