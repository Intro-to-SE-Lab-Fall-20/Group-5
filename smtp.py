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

ALLOWED_EXTENSIONS = {'jpg','png','gif','txt','pdf','jpeg'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def _get_attach_msg(path_1):
	cwd = Path.cwd()
	dirname, filename = os.path.split(os.path.abspath(path_1))
	original = os.path.abspath(path_1)
	target1 = os.path.abspath('uploads/')
	target = os.path.join(target1, filename)
	
	new_dirname, path_2 = os.path.split(os.path.abspath(target))

	
	ctype, encoding = mimetypes.guess_type(path_2)
	
	if ctype is None or encoding is not None:
		ctype = 'application/octet-stream'
	maintype, subtype = ctype.split('/', 1)
	
	if maintype == 'text':
		print("its a text file")
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
	message.add_header('Content-Disposition', 'attachment', filename=os.path.split('/')[-1])
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
	part1 = MIMEText(html2text.html2text(email.message), "plain")
	part2 = MIMEText(email.message, "html")

	message.attach(part1)
	message.attach(part2)
	if email.filename == '':
		return message
	else:
		UPLOAD_FOLDER = os.path.abspath('uploads/')
		file = request.files['filename']
		if file.filename == '':
			return message
		else:
			filename = secure_filename(file.filename)
			file.save(os.path.join(UPLOAD_FOLDER, filename))
			message.attach(_get_attach_msg(file.filename))
			print("Was an attachment added to message?")
			print("Lets mail this MIME!")
			return message

def sendemail(smtp_server, port, email):

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

