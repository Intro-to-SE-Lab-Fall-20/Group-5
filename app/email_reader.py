import imaplib
import email
from email.header import decode_header
import webbrowser
import os



def folder_list(server, username, password):
	imap = imaplib.IMAP4_SSL(server)
	# authenticate
	imap.login(username, password)
	folders = imap.list()

	f = []

	for folder in folders[1]:
		f.append(folder.decode("utf-8").split(' "/" ')[1].replace('"', ''))

	return f

def receive_emails(server, inbox, N, username, password):
	# account credentials


	# create an IMAP4 class with SSL
	imap = imaplib.IMAP4_SSL(server)
	# authenticate
	imap.login(username, password)
	
	status, messages = imap.select(inbox)
	# number of top emails to fetch

	print(messages)

	# total number of emails
	messages = int(messages[0])

	if messages < N:
		N = messages

	emails = []

	for i in range(messages, messages - N, -1):
		# fetch the email message by ID
		res, msg = imap.fetch(str(i), "(RFC822)")
		for response in msg:

			if isinstance(response, tuple):
				# parse a bytes email into a message object
				msg = email.message_from_bytes(response[1])
				print(msg)
				# decode the email subject
				subject = decode_header(msg["Subject"])[0][0]
				if isinstance(subject, bytes):
					# if it's a bytes, decode to str
					subject = subject.decode()
				# email sender
				from_ = msg.get("From")

				to_ = msg.get("To")
				#print("Subject:", subject)
				print("***From:", from_)
				print("***To:", to_)
				# if the email message is multipart
				if msg.is_multipart():
					# iterate over email parts
					for part in msg.walk():
						# extract content type of email
						content_type = part.get_content_type()
						content_disposition = str(part.get("Content-Disposition"))
						try:
							# get the email body
							body = part.get_payload(decode=True).decode()
						except:
							pass
						if "attachment" in content_disposition:
							# download attachment
							filename = part.get_filename()
							if filename:
								if not os.path.isdir(subject):
									# make a folder for this email (named after the subject)
									os.mkdir(subject)
								filepath = os.path.join(subject, filename)
								# download attachment and save it
								open(filepath, "wb").write(part.get_payload(decode=True))
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
				print("+++From:", from_)
				print("+++To:", to_)
				emails.append({
					"sender": from_,
					"receiver": to_,
					"subject": subject,
					"body": body,
					"id": i
				})
	imap.close()
	imap.logout()
	return emails