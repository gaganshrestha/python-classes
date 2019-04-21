from flask import Flask, render_template, g, request, session, redirect, url_for
import os
from database import get_db, connect_db
from database import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy



#app is created inside database.py so that app configuration can be done for database configurations
db = SQLAlchemy(app)

class Users(db.Model):
	__tablename__ = "users"

	user_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(45), nullable=false)
	password = db.Column(db.String(45), nullable=false)





@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()




def get_current_user():
	user_result = None

	if 'user' in session:
		user = session['user']
		
		db = get_db()
		user_cur = db.execute('select id, name, password from users where name = ?',[user])
		user_result = user_cur.fetchone()
		


	return user_result


@app.route('/register', methods=['POST','GET'])
def register():
	user = get_current_user()

	if request.method == 'POST':
		db = get_db()

		existing_user_cur = db.execute('select id from users where name = ?',[request.form['name']])
		existing_user = existing_user_cur.fetchone()
		if existing_user:
			return render_template('register.html', user=user, error='User already exists!!')


		hashed_password = generate_password_hash(request.form['password'], method='sha256')
		db.execute('insert into users (name, password, admin) values (?,?,?)',[request.form['name'], hashed_password,'0'])
		db.commit()

		session['user'] = request.form['name']
		return redirect( url_for('index'))

	return render_template('register.html', user=user)




@app.route('/login', methods=["POST","GET"])
def login():
	user = get_current_user()
	usererror = None
	passworderror = None

	

	if request.method == "POST":
		name = request.form['name']
		password = request.form['password']
		
		if name in ["Gagan", "Engramar", "Div", "Gitanjali", "Sarwar", "Paul", "Jen", "Hieu", "Tim", "Scott", "Geoff"]:

			if password == "python":
				session['user'] = name
				return redirect( url_for('homepage'))
			else:
				passworderror = "Incorrect password."
				
		else:
			usererror = "Incorrect username."

	return render_template('login.html', user=user, usererror=usererror, passworderror=passworderror)




@app.route('/')
def index():

	current_user = get_current_user()

	if current_user:
		return render_template('homepage.html', user=current_user)
	else:
		return render_template('login.html')






@app.route('/home')
def homepage():
	user = get_current_user()

	if not user:
		return redirect(url_for('login'))
	
	return render_template('homepage.html', user=user) 



@app.route('/chapter/<videoID>', methods=['GET'])
def displayVideo(videoID):
	user = get_current_user()

	if not user:
		return redirect(url_for('login'))


	return render_template('chapter.html', user=user, videoID=videoID)


@app.route('/exercise/<exerciseID>', methods=['GET'])
def displayExercise(exerciseID):
	user = get_current_user()

	if not user:
		return redirect(url_for('login'))


	googleURL = "href='https://docs.google.com/forms/d/1uCDu6JzQXSm6bftqwtqsLEcnpASvUTlz-bGFUbucvNI'"
	#googleURL=None
	return render_template('exercise.html', user=user, exerciseID=exerciseID, googleURL=googleURL)



@app.route('/submitExercise/<formID>', methods=['GET'])
def submitExercise(formID):
	user = get_current_user()

	if not user:
		return redirect(url_for('login'))


	googleURL = "https://docs.google.com/forms/d/e/" + formID + "/viewform?embedded=true"
	return render_template('submitForm.html', user=user, googleURL=googleURL)



@app.route('/prework', methods=['GET'])
def prework():
	user = get_current_user()

	if not user:
		return redirect(url_for('login'))


	return render_template('prework.html', user=user)



@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect(url_for('index'))



if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)