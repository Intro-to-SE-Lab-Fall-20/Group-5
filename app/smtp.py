from flask import request, jsonify, flash
import smtplib, ssl
from pathlib import Path
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.header import Header
import os
import mimetypes
import datetime
import logging
import shutil
from app.models import Email
from werkzeug.utils import secure_filename


import html2text

#UPLOAD_FOLDER = os.path.abspath('/Group-5-master/uploads/')
ALLOWED_EXTENSIONS = {'jpg','png','gif','txt','pdf','jpeg'}

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def _get_attach_msg(path_1):
	print("Lets add an attachment")
	'''
	if not os.path.isfile(path_1):
		print("There was no attachment")
		return
	'''
	cwd = Path.cwd()
	print("Split path")
	dirname, filename = os.path.split(os.path.abspath(path_1))
	#filepath = email.files
	print("Find original path")
	original = os.path.abspath(path_1)
	print("Make target path")
	target1 = os.path.abspath('uploads/')
	target = os.path.join(target1, filename)
	print("Copy to new path")

	'''
	with open(original,'rb') as f1:
		print("Opened the original path")
		with open(target,'wb') as f2:
			print("Opened the target path")
			copyfileobj(f1,f2,length=16*1024)
			print("Copied the file object")
	'''
	#new_dirname, path_2 = os.path.split(os.path.abspath(path_1))
	new_dirname, path_2 = os.path.split(os.path.abspath(target))

	print("There was an attachment")
	ctype, encoding = mimetypes.guess_type(path_2)
	print("lets guess the type")
	if ctype is None or encoding is not None:
		ctype = 'application/octet-stream'
	maintype, subtype = ctype.split('/', 1)
	print("lets read the maintype")
	if maintype == 'text':
		print("its a text file")
		#fp = open(path_2)
		fp = open(target)
		message = MIMEText(fp.read(), _subtype=subtype)
		fp.close()
	elif maintype == 'image':
		print("its an image")
		#fp = open(path_2,'rb')
		fp = open(target,'rb')
		message = MIMEImage(fp.read(), _subtype=subtype)
		fp.close()
	elif maintype == 'audio':
		print("its an audio file")
		#fp = open(path_2,'rb')
		fp = open(target,'rb')
		message.MIMEAudio(fp.read(), _subtype=subtype)
		fp.close()
	else:
		print("its a different type file")
		#fp = open(path_2,'rb')
		fp = open(target,'rb')
		message = MIMEBase(maintype, subtype)
		message.set_payload(fp.read())
		fp.close()
		encoders.encode_base64(message)
	print("Lets add a header")
	message.add_header('Content-Disposition', 'attachment', filename=os.path.split('/')[-1])
	print("Return attachment")
	return message

def copyfileobj(fsrc, fdst, length=16*1024):
    """copy data from file-like object fsrc to file-like object fdst"""
    while 1:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)

def _make_mime(email):
	print("Do you wanna build a MIME?")
	message = MIMEMultipart()
	message['Subject'] = email.subject
	message['From'] = email.sender
	message['To'] = email.reciever
	print("Cmon lets go and play!")
	message.preamble = 'This is a PotatoMail preamble, killlll mmeeeeeeee!!!\n'
	print("I never see you anymore")
	message.attach(MIMEText(email.message,'plain'))
	print("Cmon out the door")
	#file_path = email.filename
	#filename = email.filename

	if email.filename == '':
		return message
	else:
		#UPLOAD_FOLDER = os.path.abspath('uploads/')
		UPLOAD_FOLDER = os.path.abspath('uploads/')
		#UPLOAD_FOLDER = Path.cwd()
		file = request.files['filename']
		if file.filename == '':
			return message
		else:
			filename = secure_filename(file.filename)
			#file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			file.save(os.path.join(UPLOAD_FOLDER, filename))
			
			#message.attach(MIMEText(_get_attach_msg(file_path)))
			#message.attach(_get_attach_msg(file_path))
			#message.attach(_get_attach_msg(filename))
			#message.attach(_get_attach_msg(file))
			#message.attach(_get_attach_msg(file.filename))
			#message.attach(file.filename)
			message.attach(_get_attach_msg(file.filename))
			print("Was an attachment added to message?")
			print("Lets mail this MIME!")
			return message



from threading import Thread

class EmailThread(Thread):
	def __init__(self, smtp_server, port, email):
		self.email_to = email.reciever
		self.email_from = email.sender
		self.email = email.message
		self.subject = email.subject
		self.port = port
		self.smtp_server = smtp_server
		self.password = email.password
		#self.file = email.file
		#self.filename = email.filename
		Thread.__init__(self)

	def run (self):

		message = MIMEMultipart("alternative")
		
		message["Subject"] = self.subject
		message["From"] = self.email_from
		message["To"] = self.email_to

		part1 = MIMEText(html2text.html2text(self.email), "plain")
		part2 = MIMEText(self.email, "html")

		message.attach(part1)
		message.attach(part2)

		
		
'''
		print("Created message")
		
		context = ssl.create_default_context()


		with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
			server.login(self.email_from, self.password)
			server.sendmail(self.email_from, self.email_to, message.as_string())
		

		print("SEnt?")

def sendemail(smtp_server, port, email):

	EmailThread(smtp_server, port, email).start()
 
'''


	try:
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
			server.login(email.sender,email.password)
			print("Attempting to make MIME")
			message = _make_mime(email)
			print("Did MIME get made?")
			server.sendmail(email.sender, email.reciever, message.as_string())
			logging.debug("Successfully sent email")
	except Exception as e:
		print(e)

