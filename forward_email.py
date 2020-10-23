import smtplib, imaplib, email, string

imap_host = "imap.gmail.com"
imap_port = 993
smtp_host = "smtp.gmail.com"
smtp_port = 587
user = "potatomail.test@gmail.com"
passwd = "potato55"
msgid = "4"
from_addr = "potatomail.test@gmail.com"
to_addr = "poeslegacy@gmail.com"

# open IMAP connection and fetch message with id msgid
# store message data in email_data
client = imaplib.IMAP4(imap_host)
client.login(user, passwd)
client.select('INBOX')
status, data = client.fetch(msgid, "(RFC822)")
email_data = data[0][1]
client.close()
client.logout()

# create a Message instance from the email data
message = email.message_from_string(email_data)

# replace headers (could do other processing here)
message.replace_header("From", from_addr)
message.replace_header("To", to_addr)

# open authenticated SMTP connection and send message with
# specified envelope from and to addresses
smtp = smtplib.SMTP(smtp_host, smtp_port)
smtp.starttls()
smtp.login(user, passwd)
smtp.sendmail(from_addr, to_addr, message.as_string())
smtp.quit()

