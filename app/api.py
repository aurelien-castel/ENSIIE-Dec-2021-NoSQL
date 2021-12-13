from flask import Flask,render_template, request, redirect, url_for, session
import logging
import os
import datetime
import psycopg2
import uuid
from pymongo import MongoClient
from bson.objectid import ObjectId

# initialisation de l'application
app = Flask(__name__)
databases= {1: 'postgres', 2: 'mongodb'}
import time
time.sleep(5)
conn_mon = None
conn_psq = psycopg2.connect(host="psql",database="cookiepost",user="postgres",password="postgres",port='5432')
cursor_psq = conn_psq.cursor()

def get_mongodb_connexion():
	global conn_mon
	if conn_mon is None:
		conn_mon = MongoClient('mongodb://mongo:mongo@mongo')
	return conn_mon

@app.route('/')
def home():
    return redirect(url_for('form'))

@app.route('/form', methods = ['GET', 'POST'])
def form():
	return render_template("CookiePost.html")

@app.route('/submit', methods = ['POST'])
def submit():
	text = request.form["text"]
	database_num = request.form["database"]
	if databases[int(database_num)] == databases[1] :
		create_text_postgresql(text)
	elif databases[int(database_num)] == databases[2] :
		create_text_mongo(text)

	return redirect(url_for('form', name = "cookie"))

@app.route('/psql')
def postgres():
	try:		
		return {
		'psql': ['connexion:', 'OK']
		}
	except:
		return {
			'psql': ['fail']
		}

def create_text(tx, userName, postItName, toDoDate, description, importance):
    tx.run("Match(u:User {name : $userName})"
        "CREATE(p:PostIt {uuid : apoc.create.uuid(),"
			"name: $postItName,"
            "creationDate : date(),"
            "toDoDate : date($toDoDate),"
            "isDone : false,"
            "description : $description,"
			"importance : $importance})"
        "create (u)-[:haveToDo]->(p)", userName=userName, postItName=postItName, toDoDate=toDoDate, description=description, importance=importance)

def mongodbGetUser(name):
	conn_mon = get_mongodb_connexion()
	collection = conn_mon.ToutDoux 
	user = { "name" : name }
	collection.User.update(user,{ "$set" :user}, upsert=True)

def create_text_postgresql(text):
	try:
		cursor_psq.execute("INSERT INTO cookiepost (text, date) VALUES (%s, %s)", (text,date))
		conn_psq.commit()
		return "True"
	except:
		return "False"
	#now = datetime.datetime.now()
	#nowDate = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second)
	postit={"text": text}
	db.PostIt.insert_one(postit)

def create_text_mongo(text):
	conn_mon=get_mongodb_connexion()
	db=conn_mon.cookiepost
	#now = datetime.datetime.now()
	#nowDate = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
	cookie={"text": text}
	print(db.cookie.insert_one(cookie))
	print("################################################################################################")

@app.route('/mongo')
def mongo():
	try:
		client = MongoClient('mongodb://mongo:mongo@mongo')
		
		return {
		'mongo': ['connexion:', client.db_name.command('ping')]
		}
	except:
		return {
			'mongo': ['fail']
		}

# Lancement de l'application
if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(host='0.0.0.0', port=80, debug=True)
