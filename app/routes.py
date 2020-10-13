from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, ComposeEmail

from app.models import Email
from app.smtp import sendemail
from app.email_reader import receive_emails, folder_list

import app.login_credentials as lc

from urllib.parse import unquote_plus

@app.route('/inbox/', methods=['GET', 'POST'])
@app.route('/inbox/<path:folder>', methods=['GET', 'POST'])

#@login_required   #Commented out till login is implemented
def inbox(folder = "INBOX"):

	# Dummy info while users aren't set up
	user = {'username': lc.user_name}


	folders = folder_list("imap.gmail.com", lc.user_name, lc.password)

	emails = receive_emails("imap.gmail.com", '"'+unquote_plus(folder)+'"', 5, lc.user_name, lc.password)
	
	

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
		return redirect(url_for('inbox'))
	

	return render_template('main.html', folders = folders, user=user, emails = emails, form=form)




@app.route('/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('test'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/homepage/')
def logout():
	return render_template('logout_page.html')

@app.route('/test')
def test():
    user = {'username' : 'User'}
    return render_template('test.html', title = 'Home', user = user)
