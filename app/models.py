
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash

from dotenv import load_dotenv
from cryptography.fernet import Fernet

import base64
import os

load_dotenv()


class User(UserMixin, db.Model):
	""" User Model """
	__tablename__ = "appuser_a"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(64), unique=True, nullable=False)
	
	password = db.Column(db.String(128), nullable=False)

	preferred_email = db.Column(db.String(64), nullable=True)
	preferred_folder = db.Column(db.String(64), nullable=True)

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))


class User_Email(UserMixin, db.Model):
	""" Email modle with relationship with users """
	__tablename__ = "email_info"
	
	username = db.Column(db.String(64), primary_key=True, unique=True, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('appuser_a.id'))
	password = db.Column(db.String(400))
	incoming_host = db.Column(db.String(64))
	outgoing_host = db.Column(db.String(64))
	incoming_port = db.Column(db.Integer)
	outgoing_port = db.Column(db.Integer)

	def encrypt_password(self, password):
		key = os.getenv("EKEY").encode()
		
		f = Fernet(key)
		self.password = f.encrypt(password.encode()).decode()

	def decrypt_password(self):
		key = os.getenv("EKEY").encode()
		fe = Fernet(key)

		return fe.decrypt(self.password.encode()).decode()
		

def get_accounts_count(id):
	return User_Email.query.filter_by(user_id=id).count()

def get_accounts(id):
	return User_Email.query.filter_by(user_id=id).all()

def get_account_by_id(id):
	return User_Email.query.filter_by(user_id=id).first()

def get_account_by_email(id, email):
	return User_Email.query.filter_by(user_id=id, username=email).first()



class Email:
	
	def __init__(self, sender, reciever, subject, message, password, filename): 
		self.sender = sender
		self.reciever = reciever
		self.subject = subject
		self.message = message
		self.password = password
		self.filename = filename
	#html = html  Commented out until able to recieve emails

	def __repr__(self):
		return '<Email {}>'.format(self.subject)

	

