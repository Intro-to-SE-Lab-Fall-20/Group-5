from flask import render_template
from app import app

@app.route('/')
def index():
	return render_template('login_page.html')

@app.route('/homepage')
def homepage():
	return render_template('logout_page.html')




