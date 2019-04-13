from flask import Flask, render_template, g, request, session, redirect, url_for
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)



def get_current_user():
	current_user = None

	if 'user' in session:
		user = session['user']
		if user in ["gagan", "rakesh"]:
			current_user = user


		'''
		db = get_db()
		user_cur = db.execute('select id, name, password, expert, admin from users where name = ?',[user])
		user_result = user_cur.fetchone()
		'''


	return current_user



@app.route('/login', methods=["POST","GET"])
def login():
	user = get_current_user()
	usererror = None
	passworderror = None

	

	if request.method == "POST":
		name = request.form['name']
		password = request.form['password']
		
		if name in ["gagan", "rakesh"]:

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


	googleURL = "https://docs.google.com/forms/d/1uCDu6JzQXSm6bftqwtqsLEcnpASvUTlz-bGFUbucvNI"
	return render_template('exercise.html', user=user, exerciseID=exerciseID, googleURL=googleURL)


@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect(url_for('index'))



if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)