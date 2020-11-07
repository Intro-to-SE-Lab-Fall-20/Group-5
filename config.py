import os

class Config(object):
	TESTING = True
	DEBUG = True
	FLASK_ENV = 'development'
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'guess-my-key'
	PYTHONPATH= "${PYTHONPATH}:" + os.getcwd()

