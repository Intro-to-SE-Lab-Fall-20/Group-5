def test_new_user(new_user):
	assert new_user.username == 'hurleyisthebestdog@gmail.com'
	assert new_user.password != 'I<3tReaTS'
	


def new_email(new_email):
	assert new_email.username == "hurleyisthebestdog@gmail.com"
	assert new_email.password != "I<3tReaTS"
	assert new_email.decrypt_password() == 'I<3tReaTS'
	assert new_email.incoming_host == "imap.gmail.com"
	assert new_email.outgoing_host == "smtp.gmail.com"
	assert new_email.incoming_port == 993
	assert new_email.outgoing_port == 465