import smtplib, ssl
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from app.models import Email

def sendemail(smtp_server, port, email):


	#message = "From: <" + email.sender + "> \nTo: <" + email.reciever + "> \nSubject: " + email.subject + " \n" + email.message
	
	
	message = MIMEMultipart()
	message['From'] = email.sender
	message['To'] = email.reciever
	message['Subject'] = email.subject
	message.attach(MIMEText(email.message))
	#message = MIMEText('<b>%s</b>' % (body), 'html')

	'''
	#for path in email.files:
	if email.files:
		part = MIMEBase('appplication', "octet-stream")
		with open(path, "rb") as file:
			part.set_payload(file.read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition','attachment; filename="{}"'.format(Path(path).name))
		
		message.attach(part)
	'''

	try:
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
			server.login(email.sender, email.password)
			server.sendmail(email.sender, email.reciever, message.as_string())
	
	except Exception as e:
		print(e)