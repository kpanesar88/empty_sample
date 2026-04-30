import imaplib
import email
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASSWORD")

if user is None or password is None:
    raise ValueError("Missing ENV variables")


def connect_to_email(user, password):
    imap_url = "imap.gmail.com"
    my_mail = imaplib.IMAP4_SSL(imap_url)
    my_mail.login(user, password)
    my_mail.select("Inbox")
    return my_mail


def get_unread_emails(my_mail):
    status, email_data = my_mail.search(None, "UNSEEN")
    mail_id_list = email_data[0].split()
    return mail_id_list


def fetch_email(mail, email_id):
    typ, data = mail.fetch(email_id, "(RFC822)")
    return data


def extract_email_info(data):
    for response_part in data:
        if isinstance(response_part, tuple):
            my_msg = email.message_from_bytes(response_part[1])

            subject = my_msg["subject"]
            sender = my_msg["from"]
            body_text = ""

            if my_msg.is_multipart():
                for part in my_msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True)
                        if body:
                            body_text = body.decode(errors="ignore")
                            break
            else:
                body = my_msg.get_payload(decode=True)
                if body:
                    body_text = body.decode(errors="ignore")

            return {
                "subject": subject,
                "sender": sender,
                "body": body_text
            }

    return None