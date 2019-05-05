from flask import Flask, render_template, g, request, session, redirect, url_for
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from models import *
import os
from database import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



#app is created inside database.py so that app configuration can be done for database configurations
db = SQLAlchemy(app)
migrate = Migrate(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.filter_by(name=user_id).first()



def get_progress(user):
	total = ChapterProgress.query.filter_by(user_name=user).count()
	complete = round((total/47)*100)
	return complete



@app.route('/register', methods=['POST','GET'])
def register():
	
	if request.method == 'POST':

		user = load_user(request.form['name'])

		if user:
			return render_template('register.html', error='User already exists!!')


		hashed_password = generate_password_hash(request.form['password'], method='sha256')
		User.add_user(request.form['name'],hashed_password)
		
		user = load_user(request.form['name'])
		login_user(user)
		return redirect(url_for('index'))

	return render_template('register.html')





@app.route('/login', methods=["POST","GET"])
def login():
	
	usererror = None
	passworderror = None

	

	if request.method == "POST":
		name = request.form['name']
		password = request.form['password']
		
		
		user = load_user(name)

		if user:

			if user.check_password(password):
				login_user(user)
				#session['user'] = name
				return redirect(url_for('homepage'))
			else:
				passworderror = "Incorrect password."
				
		else:
			usererror = "Incorrect username."

	return render_template('login.html', usererror=usererror, passworderror=passworderror)




@app.route('/')
def index():

	
	if not current_user.is_authenticated:

		return redirect(url_for('login'))	

	return render_template('homepage.html', user=current_user.name)
	
	



@app.route('/home')
@login_required
def homepage():
	
	if not current_user.is_authenticated:

		return redirect(url_for('login'))
	
	return render_template('homepage.html', user=current_user.name) 





@app.route('/chapter/<videoID>/<chapter_name>', methods=['GET'])
@login_required
def displayVideo(videoID, chapter_name):
	

	if not current_user.is_authenticated:
		return redirect(url_for('login'))


	exists = ChapterProgress.query.filter_by(user_name=current_user.name,chapter_name=chapter_name).first()	
	#exists = db.session.query(ChapterProgress.user_name).filter_by(user_name == current_user.name, chapter_name == chapter_name).scalar() 

	if not exists:
		ChapterProgress.add_progress(current_user.name,chapter_name)

	progress = get_progress(current_user.name)

	return render_template('chapter.html', user=current_user.name, videoID=videoID, progress=progress)





@app.route('/exercise/<exerciseID>/<chapter>/<chapter_name>', methods=['GET'])
@login_required
def displayExercise(exerciseID, chapter, chapter_name):
	

	if not current_user.is_authenticated:
		return redirect(url_for('login'))


	exists = ChapterProgress.query.filter_by(user_name=current_user.name,chapter_name=chapter_name).first()	
	#exists = db.session.query(ChapterProgress.user_name).filter_by(user_name == current_user.name, chapter_name == chapter_name).scalar() 

	if not exists:
		ChapterProgress.add_progress(current_user.name,chapter_name)

	progress = get_progress(current_user.name)

	
	return render_template('exercise.html', user=current_user.name, exerciseID=exerciseID, chapter=chapter, progress=progress)






@app.route('/submitExercise/<formID>/<chapter>/<chapter_name>', methods=['GET'])
@login_required
def submitExercise(formID, chapter, chapter_name):
	
	if not current_user.is_authenticated:
		return redirect(url_for('login'))


	exists = ChapterProgress.query.filter_by(user_name=current_user.name,chapter_name=chapter_name).first()	
	#exists = db.session.query(ChapterProgress.user_name).filter_by(user_name == current_user.name, chapter_name == chapter_name).scalar() 

	if not exists:
		ChapterProgress.add_progress(current_user.name,chapter_name)

	progress = get_progress(current_user.name)


	googleURL = "https://docs.google.com/forms/d/e/" + formID + "/viewform?embedded=true"
	return render_template('submitForm.html', user=current_user.name, googleURL=googleURL, chapter=chapter, progress=progress)






@app.route('/prework/<chapter_name>', methods=['GET'])
@login_required
def prework(chapter_name):
	

	if not current_user.is_authenticated:
		return redirect(url_for('login'))


	exists = ChapterProgress.query.filter_by(user_name=current_user.name,chapter_name=chapter_name).first()	
	#exists = db.session.query(ChapterProgress.user_name).filter_by(user_name == current_user.name, chapter_name == chapter_name).scalar() 

	if not exists:
		ChapterProgress.add_progress(current_user.name,chapter_name)

	progress = get_progress(current_user.name)


	return render_template('prework.html', user=current_user.name, progress=progress)






@app.route('/logout')
@login_required
def logout():

	logout_user()
	
	return redirect(url_for('index'))





if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)