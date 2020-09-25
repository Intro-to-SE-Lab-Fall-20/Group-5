import smtplib, ssl
from app.models import Email



def sendemail(smtp_server, port, email):


	message = "From: <" + email.sender + "> \nTo: <" + email.reciever + "> \nSubject: " + email.subject + " \n" + email.message

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(email.sender, email.password)
		server.sendmail(email.sender, email.reciever, message)
