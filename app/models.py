


class Email:
	
	def __init__(self, sender, reciever, subject, message, password): 
		self.sender = sender
		self.reciever = reciever
		self.subject = subject
		self.message = message
		self.password = password
	#html = html  Commented out until able to recieve emails

	def __repr__(self):
		return '<Email {}>'.format(self.subject)

	

