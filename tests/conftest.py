import pytest
from app.models import Email, User, User_Email

@pytest.fixture(scope='module')
def new_user():
	user = User(username='hurleyisthebestdog@gmail.com')
	user.set_password('I<3tReaTS')
	return user

@pytest.fixture(scope='module')
def new_email():
	email = User_Email(
		username 		= 'hurleyisthebestdog@gmail.com',
		user_id 		= 5,
		incoming_host	= "imap.gmail.com",
		outgoing_host 	= "smtp.gmail.com",
		incoming_port 	= 993,
		outgoing_port 	= 465 )


	email.encrypt_password('I<3tReaTS')
	return email

