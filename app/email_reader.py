import imaplib
import email
from email.header import decode_header
import webbrowser
import os



def folder_list(server, username, password):
	imap = imaplib.IMAP4_SSL(server)
	# authenticate

	try:
		imap.login(username, password)
	except:
		print("Authenication Error")
		return []


	folders = imap.list()

	imap.logout()

	f = []

	for folder in folders[1]:
		if "\HasNoChildren" in folder.decode("utf-8").split(' "/" ')[0]:
			
			f.append(folder.decode("utf-8").split(' "/" ')[1].replace('"', ''))

	return f
	


def check_connection(server, username, password):
	imap = imaplib.IMAP4_SSL(server)
	# authenticate
	try:
		imap.login(username, password)
		imap.logout()
		return True

	except: 
		print("Authenication Error")
		return False

	

def receive_emails(server, inbox, N, username, password):
	# account credentials

	# create an IMAP4 class with SSL
	imap = imaplib.IMAP4_SSL(server)
	# authenticate

	try:
		imap.login(username, password)
		status, messages = imap.select(inbox)
		# number of top emails to fetch
		# total number of emails
		messages = int(messages[0])

		if messages < N:
			N = messages

		emails = []

		for i in range(messages, messages - N, -1):
			# fetch the email message by ID
			res, msg = imap.fetch(str(i), "(RFC822)")
			for response in msg:
				attachment = ""
				if isinstance(response, tuple):
					# parse a bytes email into a message object
					msg = email.message_from_bytes(response[1])
					
					# decode the email subject
					if(decode_header(msg["Subject"])[0][0]):
						subject = decode_header(msg["Subject"])[0][0]
					else:
						subject = "(none)"
					if isinstance(subject, bytes):
						# if it's a bytes, decode to str
						subject = subject.decode()
					# email sender
					from_ = msg.get("From")

					to_ = msg.get("To")
					
					# if the email message is multipart
					if msg.is_multipart():
						# iterate over email parts
						
						for part in msg.walk():
							# extract content type of email
							
							content_type = part.get_content_type()
							content_disposition = str(part.get("Content-Disposition"))
							
							if "attachment" in content_disposition:
								
								# download attachment
								filename = part.get_filename()
								print(filename)
								attachment = filename
								if filename:
									print("THIS ONE's got an email", subject)
									sanatized_subject = subject.rstrip().replace(" ", "_")
									if not os.path.isdir(sanatized_subject):

										# make a folder for this email (named after the subject)
										os.mkdir(sanatized_subject)

									filepath = os.path.join(sanatized_subject, filename)
									# download attachment and save it
									open(filepath, "wb").write(part.get_payload(decode=True))
							else:
								try:
									# get the email body
									body = part.get_payload(decode=True).decode()
								except:
									pass

					else:
						# extract content type of email
						content_type = msg.get_content_type()
						# get the email body
						body = msg.get_payload(decode=True).decode()
						if content_type == "text/html":
							# if it's HTML, create a new HTML file and open it in browser
							if not os.path.isdir(subject):
								# make a folder for this email (named after the subject)
								os.mkdir(subject)
							filename = f"{subject[:50]}.html"
							filepath = os.path.join(subject, filename)
							# write the file
							open(filepath, "w").write(body)
							# open in the default browser
							webbrowser.open(filepath)
						#print("=" * 100)
					
					emails.append({
						"sender": from_,
						"receiver": to_,
						"subject": subject,
						"body": body,
						"id": i, 
						"attachment": attachment
					})
		imap.close()
		imap.logout()
		return emails
	except: 
		print("Authenication Error")
		return []
