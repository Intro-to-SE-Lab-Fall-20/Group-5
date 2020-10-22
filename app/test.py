import imaplib
import email
from email.header import decode_header
import webbrowser
import os



def folder_list(server, username, password):
	imap = imaplib.IMAP4_SSL(server)
	# authenticate
	imap.login(username, password)
	f = imap.list()

	folders = []

	for folder in f[1]:
		folders.append(folder.decode().split(' "/" ')[1])

	return folders



print(folder_list("imap.gmail.com", "hurleyisthebestdog@gmail.com", "JoeyIsDumb"))