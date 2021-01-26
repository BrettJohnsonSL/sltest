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

if __name__ == '__main__':
	app.run(host='0.0.0.0',port='8888')
