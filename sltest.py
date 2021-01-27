from flask_restful import Resource, Api
from flask import jsonify, send_from_directory, Flask, request 
from flask import render_template
from mysql.connector import connect, Error

import json
import mysql.connector


# Define a database connection and setup a cursor
db = mysql.connector.connect(user='sltest', password='sillypassword', host='127.0.0.1', database='sltest') 
mcursor = db.cursor()

# Setup the main Flask app and create routes
app = Flask(__name__, template_folder='.')
api = Api(app)



# Javascript dependencies
@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('js/', path)


# CSS 
@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('css/', path)


# jQuery uses /img/ sigh
@app.route('/img/<path:path>')
def send_img(path):
	return send_from_directory('img/', path)

# DataTables uses /images/ ..
@app.route('/images/<path:path>')
def send_images(path):
	return send_from_directory('images/', path)



# Route specific to marking a given to-do as "done" or completed
# does seem a bit redundant to /api/edit
@app.route('/api/edit/<id>/')
def edit_todo(id):
	task_id = id
	# request.args.get('id')
	verify_todo = check_todo(int(task_id))
	if verify_todo != int(task_id):
		json_return = {'error': 'No Such ID', 'task_id' : task_id}
		return jsonify(json_return)

	# Now we know that a task with that ID exists, we can action changes to due date/description or status
	action = request.args.get('action')
	print("Action = {}").format(action)
	if action == 'complete':
		querystring = """UPDATE todo set completed=1 where id=%s"""
		data = (verify_todo,)

	if action == 'update':	
		edit_name = request.args.get('name')
		edit_date = request.args.get('duedate')
		edit_desc = request.args.get('desc')

		if not edit_name:
			print("No name specified..")
			

	try:
		query = mcursor.execute(querystring,data)
		db.commit()
		print('Task {} Mark as complete?').format(task_id)
	except mysql.connector.Error as err:
		print("An error occured while trying to update record id#{}").format(task_id,err)

	return "OK"

@app.route('/api/delete/<id>')
def delete_todo(id):
	# task_id = request.args.get('id')
	result = 'warning'
	result_str = 'not yet implemented'
	json_return = [{result : result_str, 'task_id' : id }]
	return jsonify(json_return)

@app.route('/api/new')
def new_todo():
	task_name = request.args.get('name')
	task_desc = request.args.get('desc')
	task_due = request.args.get('due')

	temp_id = "test";

	if not task_name:
		result = 'fail'
		result_str = 'No Task Name was specified'

	if not task_desc:
		result = 'fail'
		result_str = 'No Description was given for this task'

	if not task_due:
		result = 'fail'
		result_str = 'No due date is set for this task.'
	else:
		print("Due date for this task is {}").format(task_due)

	json_return = [{result : result_str, 'task_id' : temp_id }]
	return json.dumps(json_return)

@app.route('/api/list')
@app.route('/api/list/<id>')
def list_todo(id = None):
	if not id:
		query = mcursor.execute("select id,name,description,DATE_FORMAT(due, '%d/%m/%Y') as due,completed from todo");
	else:
		query = mcursor.execute("select id,name,description,DATE_FORMAT(due, '%d/%m/%Y') as due,completed from todo where id=%s",(id,));

	row_headers=[x[0] for x in mcursor.description] 
	rval = mcursor.fetchall()
	# Don't cache the query results
	db.commit()
	json_data=[]
	for result in rval:
		json_data.append(dict(zip(row_headers,result)))
	return jsonify(json_data)
        

@app.route('/api/test1')
def test_return():
	return "Hello Tester"

# Default routing of /index.html
@app.route('/')
def welcome():
	return render_template('index.html')



# Query the DB for a given ID and return the same ID from the database if it exists, otherwise return 0 to indicate a lack of record with that ID
def check_todo(id):
	querystring = """SELECT id FROM todo WHERE id = %s"""
	try:
		query = mcursor.execute(querystring,(id,))
	except mysql.connector.Error as err:
        	print("Couldn't find a record with id#{}, error={}").format(task_id,err)

        rval = mcursor.fetchone()
	if not rval:
		return 0

        for result in rval:
        	return result


if __name__ == '__main__':
	app.run(host='0.0.0.0',port='8888')
