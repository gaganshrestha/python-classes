from flask import Flask,g
import sqlite3
import os




app = Flask(__name__)

#Settings for pythonanywhere MySQL DB
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="shresthagagan",
    password="mysql123",
    hostname="shresthagagan.mysql.pythonanywhere-services.com",
    databasename="shresthagagan$trainingdetails",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = os.urandom(24)



'''
app = Flask(__name__)

#Settings for local MySQL DB
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="mysql123",
    hostname="localhost",
    databasename="trainingdetails",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = os.urandom(24)
'''



'''
def connect_db():
	sql = sqlite3.connect('/Users/gaganshrestha/Projects/TrainingFramework/TrainingDetails.db')
	sql.row_factory = sqlite3.Row
	return sql

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db
'''

