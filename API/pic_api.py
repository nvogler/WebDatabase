from datetime import datetime
from collections import namedtuple
from flask import *
import MySQLdb, string, re, hashlib, uuid

conn = MySQLdb.connect(host = 'localhost',
 user='root',
 passwd='root',
 db='group74pa1')
 
pic_api = Blueprint('pic_api', __name__, template_folder='views')

def getNeighbor(sequencenum, albumid):
	prev = None
	next = None
	prevNum = sequencenum
	nextNum = sequencenum
	cursor = conn.cursor
	cursor.execute("SELECT max(sequencenum) FROM Contain WHERE albumid = %s",[albumid])
	maxSeqNum = cursor.fetchone()[0]
	while not prev and prevNum > 0:
		prevNum = prevNum - 1
		cursor.execute("SELECT picid FROM Contain WHERE sequencenum = %s", [prevNum])
		prev = cursor.fetchone()
	while not next and nextNum < maxSeqNum:
		nextNum = nextNum + 1
		cursor.execute("SELECT picid FROM Contain WHERE sequencenum = %s", [nextNum])
		next = cursor.fetchone()
	prev = prev[0]
	next = next[0]
	return prev, next
 
@pic_api.route('/api/v1/pic/<picid>', methods = ['GET', 'PUT'])
def pic():
	cursor = conn.cursor
	errors = []
	if request.method == 'PUT':
		try:
			picid = request.get_json()["picid"]
		except HTTPException:
			errors.append({'message': "You did not provide the necessary fields"})
			return jsonify(errors = errors), 422
			
	elif request.method == 'GET':
		picid = request.args.get("id")
	cursor.execute("SELECT caption, albumid, sequencenum FROM Contain WHERE picid = %s",[picid])
	cas = cursor.fetchone()
	if not cas:
		errors.append({'message': "The requested resource could not be found"})
		return jsonify(errors = errors), 404
	caption = cas[0]
	albumid = cas[1]
	sequencenum = cas[2]
	cursor.execute("SELECT format FROM Photo WHERE picid =%s",[picid])
	format = cursor.fetchone()[0]
	cursor.execute("SELECT access, username FROM Album WHERE albumid = %s", [albumid])
	au = cursor.fetchone()
	access = au[0]
	owner = au[1]
	
	if 'username' in session:
		user = session['username']
		if user != 'owner' and access == 'private':
			cursor.execute("SELECT * FROM AlbumAccess WHERE albumid = %s AND username = %s", [albumid, user])
			if not cursor.fetchone():
				errors.append({'message':  "You do not have the necessary permissions for the resource"})
				return jsonify(errors = errors), 403
	elif access == 'private':
		errors.append({'message':  "You do not have the necessary credentials for the resource"})
		return jsonify(errors = errors), 401
		
	if request.method == 'GET':
		prevPicid, nextPicid = getNeighbor(sequencenum, albumid)
		return jsonify(albumid=albumid, caption=caption, format=format, next=nextPicid, picid=picid, prev=prevPicid), 200
			
	elif request.method == 'PUT':
		try:
			albumid = request.get_json()["albumid"]
			caption = request.get_json()["caption"]
			format = request.get_json()["format"]
			next = request.get_json()["next"]
			prev = request.get_json()["prev"]
			cursor.execute("SELECT albumid, sequencenum FROM Contain WHERE picid = %s", [picid])
			aidseq = cursor.fetchone()
			albumidFromDB = aidseq[0]
			seqNumFromDB = aidseq[1]
			cursor.execute("SELECT format FROM Photo WHERE picid = %s", [picid])
			formatFromDB = cursor.fetchone()[0]
			prevFromDB, nextFromDB = getNeighbor(seqNumFromDB, picid)
			if albumidFromDB != albumid or formatFromDB != format or prevFromDB != prev or nextFromDB != next:
				errors.append({'message': "You can only update caption"})
				return jsonify(errors = errors), 403
			cursor.execute("UPDATE Contain SET caption = %s WHERE picid = %s", [caption, picid])
			conn.commit()
			return make_response(jsonify(albumid=albumid, caption=caption, format=format, next=nextPicid, picid=picid, prev=prevPicid), 200)
		except HTTPException:
			errors.append({'message': "You did not provide the necessary fields"})
			return jsonify(errors = errors), 422

			
			
			
			