import imaplib
import email
import os
import json
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASSWORD")

if user is None or password is None:
    raise ValueError("Missing ENV variables")

DATASET_PATH = "dataset/dataset.json"


def connect_to_email(user, password):
    imap_url = "imap.gmail.com"
    my_mail = imaplib.IMAP4_SSL(imap_url)
    my_mail.login(user, password)
    my_mail.select("Inbox")
    return my_mail


def get_unread_emails(my_mail):
    status, email_data = my_mail.search(None, "UNSEEN")
    if status != "OK":
        return []
    return email_data[0].split()


def fetch_email(mail, email_id):
    status, data = mail.fetch(email_id, "(RFC822)")
    if status != "OK":
        return None
    return data


def extract_email_info(data):
    if not data:
        return None

    for response_part in data:
        if isinstance(response_part, tuple):
            my_msg = email.message_from_bytes(response_part[1])

            subject = my_msg.get("subject", "")
            sender = my_msg.get("from", "")
            body_text = ""

            if my_msg.is_multipart():
                for part in my_msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition", ""))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True)
                        if body:
                            body_text = body.decode(errors="ignore").strip()
                            break
            else:
                body = my_msg.get_payload(decode=True)
                if body:
                    body_text = body.decode(errors="ignore").strip()

            return {
                "subject": subject,
                "sender": sender,
                "body": body_text
            }

    return None


def load_dataset(path):
    if not os.path.exists(path):
        return {"emails": []}

    with open(path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def save_dataset(path, data):
    with open(path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)


def get_next_id(dataset):
    emails = dataset.get("emails", [])
    if not emails:
        return 1
    return max(email["id"] for email in emails) + 1


def email_already_exists(dataset, subject, sender, body):
    for email_record in dataset.get("emails", []):
        if (
            email_record.get("subject", "") == subject
            and email_record.get("sender", "") == sender
            and email_record.get("body", "") == body
        ):
            return True
    return False


def add_email_to_dataset(email_info, dataset_path):
    dataset = load_dataset(dataset_path)

    if email_already_exists(
        dataset,
        email_info["subject"],
        email_info["sender"],
        email_info["body"]
    ):
        print("Email already exists in dataset. Skipping.")
        return

    new_email = {
        "id": get_next_id(dataset),
        "company": "",
        "job_title": "",
        "sender": email_info["sender"],
        "subject": email_info["subject"],
        "body": email_info["body"],
        "status": ""
    }

    dataset["emails"].append(new_email)
    save_dataset(dataset_path, dataset)

    print(f"Added email ID {new_email['id']} to dataset.")


if __name__ == "__main__":
    my_mail = connect_to_email(user, password)
    mail_ids = get_unread_emails(my_mail)

    if not mail_ids:
        print("No unread emails found.")
    else:
        for email_id in mail_ids:
            data = fetch_email(my_mail, email_id)
            email_info = extract_email_info(data)

            if email_info:
                print("________________________________________")
                print("From:", email_info["sender"])
                print("Subject:", email_info["subject"])
                print("Body:", email_info["body"])

                add_email_to_dataset(email_info, DATASET_PATH)