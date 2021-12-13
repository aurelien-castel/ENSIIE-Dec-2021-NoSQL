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
conn_mon = None
#conn_psq = psycopg2.connect(host="psql",database="postgres",user="postgres",password="postgres",port='5432')

def get_mongodb_connexion():
	global conn_mon
	if conn_mon is None:
		conn_mon = MongoClient('mongodb://mongo:mongo@mongo')
	return conn_mon

def redis_increment():
	r = RedisD.Redis(host='redis',port='6379',db=0)
	try:
		if r.ping():
			r.incr('compteur')
			return int(r.get('compteur'))
	except:
		return 0

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
		#get_neo4J_connexion().session().write_transaction(create_post_it, user, title, todo_date, description, importance)
		#app.logger.info("add post-it neo4j")
		print("123")
	elif databases[int(database_num)] == databases[2] :
		create_post_it_mongo(text)
		app.logger.info("add post-it mongo")
	else :
		#do some psql
		app.logger.info("NON add post-it psql")

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

def create_post_it(tx, userName, postItName, toDoDate, description, importance):
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

def create_post_it_mongo(text):
	conn_mon=get_mongodb_connexion()
	db=conn_mon.ToutDoux
	now = datetime.datetime.now()
	nowDate = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
	app.logger.info(nowDate)
	postit={"text": text, "creationDate": nowDate}
	app.logger.info(postit)
	db.PostIt.insert_one(postit)

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
