import os
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv(dotenv_path=".env")

SHEET_ID = os.getenv("SHEET_ID")
if not SHEET_ID:
    raise ValueError("Missing SHEET_ID in .env")

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

spreadsheet = client.open_by_key(SHEET_ID)
worksheet = spreadsheet.sheet1


def normalize(text):
    return str(text).strip().lower()


def get_sheet_records():
    return worksheet.get_all_records()


def match_email_to_sheet(subject, body):
    email_text = normalize(f"{subject} {body}")
    records = get_sheet_records()

    best_match = None
    best_score = -1

    for row in records:
        company = row.get("COMPANY", "")
        job_title = row.get("JOB TITLE", "")

        company_norm = normalize(company)
        job_title_norm = normalize(job_title)

        score = 0

        if company_norm and company_norm in email_text:
            score += 1

        if job_title_norm and job_title_norm in email_text:
            score += 1

        if score > best_score:
            best_score = score
            best_match = (company, job_title)

    if best_score <= 0:
        return "", ""

    return best_match