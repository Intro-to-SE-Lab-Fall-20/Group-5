from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, ComposeEmail

from app.models import Email
from app.smtp import sendemail

import app.login_credentials as lc

@app.route('/email/', methods=['GET', 'POST'])
#@login_required   #Commented out till login is implemented
def index():

	# Dummy info while users aren't set up
	user = {'username': 'Miguel'}

	# Dummy emails while email retrival isn't working
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

	form = ComposeEmail()

	if form.validate_on_submit():

		# lc.user_name and lc.password are in place to hide my testing email
		email = Email(	sender=lc.user_name,      
						reciever=form.reciever.data, 
						subject=form.subject.data,
						message=form.message.data,
						password=lc.password)


		sendemail("smtp.gmail.com", 465, email)
		
		flash('')
		return redirect(url_for('index'))
	

	return render_template('main.html', user=user, emails = emails, form=form)

@app.route('/homepage/')
def logout():
	return render_template('logout_page.html')

@app.route('/test')
def test():
    user = {'username' : 'User'}
    return render_template('test.html', title = 'Home', user = user)

@app.route('/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('test'))
    return render_template('login.html', title='Sign In', form=form)
