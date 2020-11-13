from flask import render_template, flash, redirect, url_for, request, session, send_from_directory
from app import app, db, limiter
from app.forms import LoginForm, ComposeEmail, RegistrationForm, RegisterEmailForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Email, User, User_Email, get_accounts_count, get_accounts, get_account_by_id, get_account_by_email
from app.smtp import sendemail

from app.email_reader import receive_emails, folder_list, check_connection
from pathlib import Path
import pathlib
import os

from urllib.parse import unquote_plus


#UPLOAD_FOLDER = os.path.abspath('/Group-5-master/uploads/')
ALLOWED_EXTENSIONS = {'jpg','png','gif','txt','pdf','jpeg'}

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/inbox/', methods=['GET', 'POST'])
@app.route('/inbox/<path:email_account>/<path:folder>', methods=['GET', 'POST'])
@login_required  
def inbox(email_account = "", folder = "" ):

	accounts_count = get_accounts_count(current_user.id)
	print(accounts_count)



	if(accounts_count == 0 ):

		return redirect(url_for('registeremail'))

	else:
		if(email_account):
			account = get_account_by_email(current_user.id, unquote_plus(email_account))
		else:
			if(accounts_count == 1 ):
				
				account = get_account_by_id(current_user.id)
			else:
				account = get_account_by_email(current_user.id, unquote_plus(current_user.preferred_email))
		
		if(folder == ""):
			if(current_user.preferred_folder):
				folder = current_user.preferred_folder
			else:
				
				try:
					folder = folder_list(account.incoming_host, account.username, account.decrypt_password())[0]
				except:
					
					folder = "INBOX"
		
		f = '"'+unquote_plus(folder)+'"'


		folders = folder_list(account.incoming_host, account.username, account.decrypt_password())
		emails = receive_emails(account.incoming_host, f, 15, account.username, account.decrypt_password())
		
		form = ComposeEmail()

		if form.validate_on_submit():
			email = Email(	sender=account.username,      
							reciever=form.reciever.data, 
							subject=form.subject.data,
							message=form.message.data,
							filename=form.filename.data,
							password=account.decrypt_password())

			

			sendemail(account.outgoing_host, account.outgoing_port, email)
			
			return redirect(url_for('inbox'))
	

		return render_template('main.html', folders = folders,  emails = emails, form=form, email_account = account.username, current_folder = unquote_plus(folder))

@app.route('/inbox/files/<path:subject>/<path:filename>')
def retrive_attatchment(subject, filename):
	full_filename = os.path.join(Path.cwd(), subject.replace(" ", "_"))
	print(full_filename)
	fp = open(os.path.join(full_filename, filename.replace(" ", "_")))
	return send_from_directory(full_filename, filename.replace(" ", "_"))

@app.route('/dashboard', methods=['GET'])
def dashboard():
	return render_template('dashboard.html')

@app.route('/notepad', methods=['GET','POST'])
def notepad():
	return render_template('notepad.html')

@app.route('/r', methods=['GET','POST'])
def register():
	
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		login_user(user, remember=False)

		#return redirect(url_for('inbox') )
		return redirect(url_for('dashboard') )
	return render_template('signup.html', title='Register', form=form)

@app.route('/account')
def account():


	print(get_accounts(current_user.id))
	accounts = get_accounts(current_user.id)

	return render_template('account.html', accounts = accounts)

	
@app.route('/regsisterEmail', methods=['GET','POST'])
def registeremail():
	form = RegisterEmailForm()
	if form.validate_on_submit() and check_connection(form.IHostName.data, form.email.data, form.password.data):
		email_account = User_Email(
			username 		= form.email.data, 
			user_id 		= current_user.id,
			incoming_host	= form.IHostName.data,
			outgoing_host 	= form.OHostName.data,
			incoming_port 	= form.IPortNum.data,
			outgoing_port 	= form.OPortNum.data )
		
		email_account.encrypt_password(form.password.data)


		db.session.add(email_account)
		db.session.commit()

		return redirect('dashbaord')

	return render_template('regsisterEmail.html', form = form)




@app.route('/', methods=['GET','POST'])
#@limiter.limit("100/day")
#@limiter.limit("10/hour")
@limiter.limit("3/minute")
def login():

	if current_user.is_authenticated:
		return redirect(url_for('dashboard'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		
		
		return redirect(url_for('dashboard') )

	

	return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect("/")

@app.errorhandler(429)
def ratelimit_handler(e):
	return render_template('429.html'), 429


