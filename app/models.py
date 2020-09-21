


class email(sender, reciever, subject html):
	sender = sender
	reciever = reciever
	subject = subject
	body = body
	#html = html  Commented out until able to recieve emails

	def __repr__(self):
        return '<Email {}>'.format(self.subject)

	

