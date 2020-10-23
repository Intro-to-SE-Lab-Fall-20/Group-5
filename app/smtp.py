import smtplib, ssl
from app.models import Email

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import html2text


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

		
		

		print("Created message")
		
		context = ssl.create_default_context()


		with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
			server.login(self.email_from, self.password)
			server.sendmail(self.email_from, self.email_to, message.as_string())
		

		print("SEnt?")

def sendemail(smtp_server, port, email):

	EmailThread(smtp_server, port, email).start()