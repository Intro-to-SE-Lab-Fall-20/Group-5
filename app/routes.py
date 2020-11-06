from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.forms import LoginForm, ComposeEmail, RegistrationForm, RegisterEmailForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Email, User, User_Email, get_accounts_count, get_accounts, get_account_by_id, get_account_by_email	
from app.smtp import sendemail

from app.email_reader import receive_emails, folder_list, check_connection

import pathlib
import os

from urllib.parse import unquote_plus


#UPLOAD_FOLDER = os.path.abspath('/Group-5-master/uploads/')
ALLOWED_EXTENSIONS = {'jpg','png','gif','txt','pdf','jpeg'}

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


#global Files=[]

@app.route('/inbox/', methods=['GET', 'POST'])
@app.route('/inbox/<path:email_account>/<path:folder>', methods=['GET', 'POST'])
#@app.route('/inbox/<path:folder>', methods=['GET', 'POST'])

@login_required   #Commented out till login is implemented
def inbox(email_account = "", folder = "" ):


	# Dummy info while users aren't set up


	accounts_count = get_accounts_count(current_user.id)
	print(accounts_count)



	if(accounts_count == 0 ):

		return redirect(url_for('registeremail'))

	else:
		if(email_account):
			account = get_account_by_email(current_user.id, unquote_plus(email_account))
		else:
			if(accounts_count == 1 ):
				#print("one email for user found")
				account = get_account_by_id(current_user.id)
			else:
				account = get_account_by_email(current_user.id, unquote_plus(current_user.preferred_email))
		
		if(folder == ""):
			if(current_user.preferred_folder):
				folder = current_user.preferred_folder
			else:
				#print("no prefrence for folder set")
				try:
					folder = folder_list(account.incoming_host, account.username, account.decrypt_password())[0]
				except:
					print("IMAP ERROR")
					folder = "INBOX"
		
		f = '"'+unquote_plus(folder)+'"'


		folders = folder_list(account.incoming_host, account.username, account.decrypt_password())
		emails = receive_emails(account.incoming_host, f, 15, account.username, account.decrypt_password())
			

		form = ComposeEmail()

		'''
		uploaded_file = request.files['file']
		if uploaded_file.filename != '':
			uploaded_file.save(uploaded_file.filename)
		'''
		if form.validate_on_submit():
			# lc.user_name and lc.password are in place to hide my testing email
			''''uploaded_file = request.files['file']
			if uploaded_file.filename != '':
				uploaded_file.save(uploaded_file.filename)'''
			#####  = open("filename", "rb") 
			email = Email(	sender=account.username,      
							reciever=form.reciever.data, 
							subject=form.subject.data,
							message=form.message.data,
							filename=form.filename.data,
							password=account.decrypt_password())

			'''
			uploaded_file = request.files['file']
			if uploaded_file.file != '':

				uploaded_file.save(uploaded_file.file)
				email.files = uploaded_file
			'''

			sendemail(account.outgoing_host, account.outgoing_port, email)
			flash('')
			return redirect(url_for('inbox'))
	

		return render_template('main.html', folders = folders,  emails = emails, form=form, email_account = account.username, current_folder = unquote_plus(folder))

@app.route('/notepath', methods=['GET','POST'])
def notepath():
	if request.method == 'POST':
		if request.form['submit_button'] == "Go to INBOX":
			return redirect(url_for('inbox'))
		elif request.form['submit_button'] == "Go to NOTES":
			return redirect(url_for('notesapp'))
	elif request.method == 'GET':
		return render_template('note.html')

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
		return redirect(url_for('notepath') )
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

		#return redirect("inbox")
		return redirect('notepath')

	return render_template('regsisterEmail.html', form = form)




@app.route('/', methods=['GET','POST'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for('inbox'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		
		
		#return redirect(url_for('inbox') )
		return redirect(url_for('notepath') )

	

	return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect("/")


@app.route('/addfile', methods=['GET','POST'])
def addfile():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(url_for('inbox'))
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file', filename=filename))
	"""
	uploaded_file = request.files['file']
	if uploaded_file.filename != '':
		uploaded_file.save(uploaded_file.filename)
		#email.files = uploaded_file
	"""
	return '''
	<!doctype html>
	<title>Upload new File</title>
	<h1>Upload new File</h1>
	<form method=post enctype=multipart/form-data>
		<input type=file name=file>
		<input type=submit value=Upload>
	</form>
	'''

	


