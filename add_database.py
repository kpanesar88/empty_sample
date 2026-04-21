import json
from read_email import get_parsed_unread_emails

filename = "dataset/dataset.json"


def load_database(filename):
    with open(filename, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def save_database(data, filename):
    with open(filename, "w", encoding="utf-8") as database:
        json.dump(data, database, indent=4)


def get_next_id(data):
    if not data["emails"]:
        return 1
    return data["emails"][-1]["id"] + 1


def add_emails_to_database():
    data = load_database(filename)
    unread_emails = get_parsed_unread_emails()

    next_id = get_next_id(data)

    for email_info in unread_emails:
        new_email = {
            "id": next_id,
            "company": "",
            "job_title": "",
            "sender": email_info["sender"],
            "subject": email_info["subject"],
            "body": email_info["body"],
            "status": ""
        }

        data["emails"].append(new_email)
        next_id += 1

    save_database(data, filename)


add_emails_to_database()