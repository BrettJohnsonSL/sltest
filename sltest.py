from flask_restful import Resource, Api
from flask import jsonify, send_from_directory, Flask, request 
from flask import render_template
from mysql.connector import connect, Error
from json import dumps
import json

import mysql.connector

db = mysql.connector.connect(user='sltest', password='sillypassword', host='127.0.0.1', database='sltest') 
mcursor = db.cursor()

app = Flask(__name__, template_folder='.')
api = Api(app)


@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('js/', path)

@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('css/', path)

@app.route('/img/<path:path>')
def send_img(path):
	return send_from_directory('img/', path)

@app.route('/images/<path:path>')
def send_images(path):
	return send_from_directory('images/', path)

@app.route('/api/complete')
def complete_todo():
	task_id = int(request.args.get('id'))
	verify_todo = check_todo(int(task_id))
	if verify_todo != task_id: 
		return 'No Such ID {}'.format(verify_todo)
	app.logger.info('Task ',task_id, 'Mark as complete?')
	return "OK"

@app.route('/api/delete')
def delete_todo():
	task_id = request.args.get('id')
	app.logger.info('Task ',task_id, ' Deleted?')
	return "OK"

@app.route('/api/new')
def new_todo():
	task_name = request.args.get('name')
	task_desc = request.args.get('desc')
	task_due = request.args.get('due')
	app.logger.info('Task ',task_id, ' created')
	return "OK"

@app.route('/api/list_todo')
def list_todo():
	query = mcursor.execute("select * from todo");
	row_headers=[x[0] for x in mcursor.description] 
	rval = mcursor.fetchall()
	json_data=[]
	for result in rval:
		json_data.append(dict(zip(row_headers,result)))
	return jsonify(json_data)
        
@app.route('/')
def welcome():
	return render_template('index.html')


def check_todo(id):
	querystring = """SELECT id FROM todo WHERE id = %s"""
	query = mcursor.execute(querystring,(id,))
        rval = mcursor.fetchone()
        for result in rval:
        	return result


if __name__ == '__main__':
	app.run(host='0.0.0.0',port='8888')
