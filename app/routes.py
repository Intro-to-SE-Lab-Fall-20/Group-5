from flask import render_template
from app import app



@app.route('/login/')
def welcome():
	return render_template('login_page.html')

@app.route('/')
@app.route('/email/')
#@login_required   #Commented out till login is implemented
def index():
	user = {'username': 'Miguel'}
    #email(sender, reciever, subject html):
	emails = [
        {
            'sender': 'haley@gmail.com',
            'reciever': 'test@email.com',
            'subject': 'Beautiful day in Portland!',
            'body': 'lalalallal!!',
            'id': 1
        },
        {
            'sender': 'Joe@yahoo.com',
            'reciever': 'test@email.com',
            'subject': 'Helloo!!',
            'body': 'lalalallal!!',
            'id': 2
        }
    ]
	return render_template('main.html', user=user, emails = emails)

@app.route('/homepage/')
def logout():
	return render_template('logout_page.html')




