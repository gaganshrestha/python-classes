from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from database import app
from werkzeug.security import check_password_hash


db = SQLAlchemy(app)



class User(UserMixin, db.Model):

	__tablename__ = "users"

	user_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(45), nullable=False)
	password = db.Column(db.String(45), nullable=False)
	
	def check_password(self, password):
		return check_password_hash(self.password, password)


	def get_id(self):
		return self.name

	def add_user(_name, _password):
		new_user = User(name=_name,password=_password)
		db.session.add(new_user)
		db.session.commit()


class ChapterProgress(UserMixin, db.Model):

	__tablename__ = "chapter_progress"

	user_name = db.Column(db.String(45), primary_key=True, nullable=False)
	chapter_name = db.Column(db.String(45), nullable=False)

	def get_user(self):
		return self.user_name

	def get_chapter(self):
		return self.chapter_name

	def add_progress(_username, _chaptername):
		new_entry = ChapterProgress(user_name=_username, chapter_name=_chaptername)
		db.session.add(new_entry)
		db.session.commit()