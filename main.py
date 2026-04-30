import os
from dotenv import load_dotenv

from read_email import connect_to_email, get_unread_emails, fetch_email, extract_email_info
from predict import predict_email

load_dotenv()

user = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASSWORD")

if user is None or password is None:
    raise ValueError("Missing ENV variables")


def main():
    my_mail = connect_to_email(user, password)
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

        print("________________________________________")
        print("From:", sender)
        print("Subject:", subject)
        print("Prediction:", prediction)

        if prediction == "other":
            print("Ignored non-job-related email.")


if __name__ == "__main__":
    main()