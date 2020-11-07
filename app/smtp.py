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



def _make_mime(email):
	message = MIMEMultipart()
	message['Subject'] = email.subject
	message['From'] = email.sender
	message['To'] = email.reciever
	part1 = MIMEText(html2text.html2text(self.email), "plain")
	part2 = MIMEText(self.email, "html")

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
			return message

def sendemail(smtp_server, port, email):
	try:
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
			server.login(email.sender,email.password)
			message = _make_mime(email)
			server.sendmail(email.sender, email.reciever, message.as_string())
			logging.debug("Successfully sent email")
	except Exception as e:
		print(e)









