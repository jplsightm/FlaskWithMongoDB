from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os
import logging

if os.name == 'nt':
    LOG_NAME = 'C:\\temp\\data_stream.log'
else:
	LOG_NAME='/var/log/data_stream.log'

FORMAT = '%(levelname)s:%(name)s: - - [%(asctime)s] - - %(message)s -'
logging.basicConfig(filename=LOG_NAME, level=logging.INFO, format=FORMAT)
logger = logging.getLogger('Task Tracker Web')

app = Flask(__name__)
title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.mymongodb    #Select the database
todos = db.todo #Select the collection name

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/list")
def lists ():
	#Display the all Tasks
	try:
		todos_l, td_count = todos.find(), todos.find()
		logger.info('Found {} todos'.format(td_count.count()))
	except Exception as e:
		logger.info('todos collection unavailable: {}'.format(e))
		todos_1={}

	a1="active"
	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/")
@app.route("/uncompleted")
def tasks ():
	#Display the Uncompleted Tasks
	
	try:
		todos_l, td_count = todos.find({"done":"no"}), todos.find({"done":"no"})
		logger.info('Found {} incomplete tasks'.format(td_count.count()))
	except Exception as e:
		logger.info('todos collection unavailable: {}'.format(e))
		todos_1={}

	a2="active"
	return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)


@app.route("/completed")
def completed ():
	#Display the Completed Tasks
	
	try:
		todos_l, td_count = todos.find({"done":"yes"}), todos.find({"done":"yes"})
		logger.info('Found {} completed tasks'.format(td_count.count()))
	except Exception as e:
		logger.info('todos collection unavailable: {}'.format(e))
		todos_1={}
	a3="active"
	return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)

@app.route("/done")
def done ():
	#Done-or-not ICON
	

	try:
		_id=request.values.get("_id")
		task=todos.find({"_id":ObjectId(_id)})
		if(task[0]["done"]=="yes"):
			todos.update({"_id":ObjectId(_id)}, {"$set": {"done":"no"}})
			logger.info('{} task set to not done'.format(_id))
		else:
			todos.update({"_id":ObjectId(_id)}, {"$set": {"done":"yes"}})
			logger.info('{} task set to done'.format(_id))
	except Exception as e:
		logger.info('todos collection unavailable: {}'.format(e))
		todos_1={}

	redir=redirect_url()	

	return redirect(redir)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	try:
		todos.insert({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
		logger.info('Created a new todo task')
	except Exception as e:
		logger.info('todos collection unavailable: {}'.format(e))

	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	
	try:
		_id=request.values.get("_id")
		todos.remove({"_id":ObjectId(_id)})
		logger.info('{} removed from task list'.format(_id))
	except Exception as e:
		logger.info('todos collection unavailable: {}'.format(e))

	return redirect("/")

@app.route("/update")
def update ():
	_id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(_id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	id=request.values.get("_id")
	todos.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})
	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = todos.find({refer:ObjectId(key)})
	else:
		todos_l = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

if __name__ == "__main__":

    app.run()
