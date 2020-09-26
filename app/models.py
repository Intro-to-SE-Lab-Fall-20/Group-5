


class Email:
	
	def __init__(self, sender, reciever, subject, message, i,  password): 
		self.sender = sender
		self.reciever = reciever
		self.subject = subject
		self.message = message
		self.password = password
		self.id = i
	#html = html  Commented out until able to recieve emails

	def __repr__(self):
		return '<Email {}>'.format(self.subject)

	

	def serialize(self):
		return { 
			"sender" : self.sender,
			'reciever': self.reciever,
			'subject': self.subject,
			'body': self.message,
			'id': self.id
		}