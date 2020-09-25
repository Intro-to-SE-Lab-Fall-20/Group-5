import smtplib, ssl
from app.models import Email

'''port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "HurleyIsTheBestDog@gmail.com"  # Enter your address
receiver_email = "haleyhagler@gmail.com"  # Enter receiver address
password = 'Hurley23'
message = """From: From Person <from@fromdomain.com>
To: To Person <haleyhagler@gmail.com>
Subject: SMTP e-mail test

This is a test e-mail message.

"""
'''

def sendemail(smtp_server, port, email):


	message = "From: <" + email.sender + "> \nTo: <" + email.reciever + "> \nSubject: " + email.subject + " \n" + email.message

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(email.sender, email.password)
		server.sendmail(email.sender, email.reciever, message)