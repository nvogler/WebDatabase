from datetime import datetime
from collections import namedtuple
from flask import *
import MySQLdb

#from database import db, get_pic_neighbors

db = MySQLdb.connect(host = 'localhost',
 user='root',
 passwd='root',
 db='group74pa1')

api = Blueprint('api', __name__, template_folder='views')

Pic = namedtuple('Pic', ['picid', 'format', 'date'])
Contain = namedtuple('Contain', ['albumid', 'picid', 'caption', 'sequencenum'])

def get_pic_neighbors(picid):
	cur = db.cursor()
	cur.execute("SELECT albumid, sequencenum FROM Contain WHERE picid=%s",[picid])
	albumid_current = cur.fetchone()
	albumid = albumid_current[0]
	current = albumid_current[1]
	cur.execute("SELECT max(sequencenum) FROM Contain WHERE albumid=%s", [albumid])
	maxsequence = cur.fetchone()[0]
	prevID = picid
	nextID = picid
	if maxsequence == current:
		cur.execute("SELECT picid FROM Contain WHERE sequencenum=%s",[current+1])
		nextID = cur.fetchone()[0]
	if current != '0':
		cur.execute("SELECT picid FROM Contain WHERE sequencenum=%s",[current-1])
		prevID = cur.fetchone()[0]
	return {"albumid":albumid,
			"prevID":prevID,
			"nextID":nextID}

def execute(query):
    cur = db.cursor()
    cur.execute(query)
    return cur.fetchall()

def update(query):
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    return cursor.lastrowid

def get_pic_by_id(picid):
	query = "SELECT picid, format, date FROM Photo WHERE picid='%s'" % (picid)
	results = execute(query)
	if len(results) > 0:
		print results[0]
		pic = Pic(*results[0])
		return pic
	else:
		raise RecordNotFound(resource_type='Pic', source={"pointer": "data/attributes/picid"})

def update_caption(picid, caption):
	query = "UPDATE Contain SET caption='%s' WHERE picid='%s'" % (caption, picid)
	try:
		update(query)
	except Exception as e:
		print e
		raise UpdateFailed(resource_type='Pic', source={"pointer": "data/attributes/picid",
														"pointer": "data/attributes/caption"})


def get_contain_by_picid(picid):
	query = "SELECT albumid, picid, caption, sequencenum FROM Contain WHERE picid='%s'" % (picid)
	results = execute(query)
	if len(results) > 0:
		contain = Contain(*results[0])
		return contain
	else:
		raise RecordNotFound(resource_type='Contain', source={"pointer": "data/attributes/picid"})


class JSONAPIException(Exception):

	def __init__(self, title, resource_type, message, status_code, source):
		self.status_code = status_code
		self.title = title
		self.resource_type = resource_type
		self.message = message
		self.status_code = status_code
		self.source = source
		super(JSONAPIException, self).__init__(self.to_json())

	def to_json(self):
		error = dict(status=self.status_code, title=self.title, source=self.source, detail=self.message) 
		return error

class RecordNotFound(JSONAPIException):

	def __init__(self, resource_type, source):
		super(RecordNotFound, self).__init__(title="Resource Not Found", resource_type=resource_type, 
			message="Resource not found for %s. Please verify you specified a valid id." % (resource_type),
			status_code=422, source=source)

class InsertFailed(JSONAPIException):

	def __init__(self, resource_type, source):
		super(InsertFailed, self).__init__(resource_type=resource_type, source=source, 
			title="Insert failed",
			message="Could not insert %s. Please verify correctness of your request." % (resource_type),
			status_code=422)

class UpdateFailed(JSONAPIException):

	def __init__(self, resource_type, source):
		super(UpdateFailed, self).__init__(resource_type=resource_type, source=source, 
			title="Update failed",
			message="Could not update %s. Please verify correctness of your request." % (resource_type),
			status_code=422)


class PicJSONAPI(object):

	def __init__(self, pic, contain):
		self.pic = pic
		self.contain = contain

	def attributes(self):
		albumid, prevID, nextID = get_pic_neighbors(self.pic.picid)
		attributes = {
			"picurl": "{}.{}".format(self.pic.picid, self.pic.format),
			"prevpicid": prevID,
			"nextpicid": nextID,
			"caption": self.contain.caption	
		}
		return attributes


	def relationships(self):
		relationships = {}

		if not relationships:
			return None

		return relationships

	def to_json(self):
		data = {
				"type": "pics",
				"id": self.pic.picid,
				"attributes": self.attributes()
			}

		relationships = self.relationships()
		if relationships is not None:
			data["relationships"] = relationships
		return { "data": data }

@api.route('/jsonapi/v1/pics/<picid>', methods=['GET'])
def pics(picid):
	print "asdfawersdf"
	try:
		pic = get_pic_by_id(picid)
		contain = get_contain_by_picid(picid)
	except RecordNotFound as e:
		response = json.jsonify(errors=[e.to_json()])
		response.status_code=404
		return response

	pic = PicJSONAPI(pic, contain)
	data = pic.to_json()
	return json.jsonify(**data)


@api.route('/jsonapi/v1/pics/<picid>', methods=['PATCH'])
def patch_caption(picid):
	try:
		data = request.get_json(force=True)["data"]
		caption = data["attributes"]["caption"]
		update_caption(picid, caption)
	except JSONAPIException as e:
		response = json.jsonify(errors=[e.to_json()])
		response.status_code = 422

	response = json.jsonify(data=data)
	response.status_code = 201
	return response


