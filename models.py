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

