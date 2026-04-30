import os
import json
from dotenv import load_dotenv

from read_email import connect_to_email, get_unread_emails, fetch_email, extract_email_info
from predict import predict_email
from matcher import match_email_to_sheet
from edit_sheet import update_application_status

load_dotenv(dotenv_path=".env")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if EMAIL_USER is None or EMAIL_PASSWORD is None:
    raise ValueError("Missing EMAIL_USER or EMAIL_PASSWORD in .env")

DATABASE_PATH = "dataset/dataset.json"


def load_database(path):
    if not os.path.exists(path):
        return {"emails": []}

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_database(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_next_id(database):
    emails = database.get("emails", [])
    if not emails:
        return 1
    return max(email_record.get("id", 0) for email_record in emails) + 1


def email_already_exists(database, subject, sender, body):
    for email_record in database.get("emails", []):
        if (
            email_record.get("subject", "") == subject
            and email_record.get("sender", "") == sender
            and email_record.get("body", "") == body
        ):
            return True
    return False


def save_processed_email(email_info, prediction, company, job_title):
    database = load_database(DATABASE_PATH)

    subject = email_info.get("subject", "")
    sender = email_info.get("sender", "")
    body = email_info.get("body", "")

    if email_already_exists(database, subject, sender, body):
        print("Email already exists in database. Skipping save.")
        return

    new_record = {
        "id": get_next_id(database),
        "company": company,
        "job_title": job_title,
        "sender": sender,
        "subject": subject,
        "body": body,
        "status": prediction
    }

    database["emails"].append(new_record)
    save_database(DATABASE_PATH, database)

    print(f"Saved email ID {new_record['id']} to database.")


def main():
    my_mail = connect_to_email(EMAIL_USER, EMAIL_PASSWORD)
    mail_ids = get_unread_emails(my_mail)

    if not mail_ids:
        print("No unread emails found.")
        return

    for email_id in mail_ids:
        data = fetch_email(my_mail, email_id)
        email_info = extract_email_info(data)

        if not email_info:
            continue

        subject = email_info.get("subject", "")
        sender = email_info.get("sender", "")
        body = email_info.get("body", "")

        prediction = predict_email(subject, body)
        company, job_title = match_email_to_sheet(subject, body)

        print("________________________________________")
        print("From:", sender)
        print("Subject:", subject)
        print("Prediction:", prediction)
        print("Company:", company if company else "[not found]")
        print("Job Title:", job_title if job_title else "[not found]")

        save_processed_email(email_info, prediction, company, job_title)

        if prediction == "other":
            print("Ignored non-job-related email.")
            continue

        if company and job_title:
            pretty_status = "Rejected" if prediction == "rejected" else "Next Step"
            update_application_status(company, job_title, pretty_status)
        else:
            print("Could not update sheet because company/job title was not found.")


if __name__ == "__main__":
    main()