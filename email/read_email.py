import imaplib
import email
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASSWORD")

if user is None or password is None:
    print("Missing ENV variables")

imap_url = "imap.gmail.com"

my_mail = imaplib.IMAP4_SSL(imap_url)
my_mail.login(user,password)
my_mail.select("Inbox")

status, email_data = my_mail.search(None,"UNSEEN")
mail_id_list = email_data[0].split()

msgs=[]

for num in mail_id_list:
    typ, data = my_mail.fetch(num, "(RFC822)")
    msgs.append(data)
    

for msg in msgs[::-1]:
    for response_part in msg:
        if isinstance(response_part, tuple):
            my_msg = email.message_from_bytes(response_part[1])
            print("_____________________________________________")
            print("subj:", my_msg["subject"])
            print("from: ", my_msg["from"])
            print("body:")
            
            if my_msg.is_multipart():
                for part in my_msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        if body:
                            print(body.decode(errors="ignore"))
            else:
                body = my_msg.get_payload(decode=True)
                if body:
                    print(body.decode(errors="ignore"))
