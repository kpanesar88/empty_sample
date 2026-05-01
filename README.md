# Job Application Email Classifier

## About
An AI-powered Python workflow that reads unread emails, classifies them as **rejected**, **next step**, or **other**, and updates a job application tracker automatically.

## Overview
This project was built to reduce the manual work of checking job-related emails and updating an application spreadsheet. It combines email parsing, machine learning, keyword matching, and spreadsheet automation into one pipeline.

The system:
- reads unread emails from Gmail
- extracts the sender, subject, and body
- classifies each email as `rejected`, `next_step`, or `other`
- matches the email to an application entry
- updates the corresponding Google Sheets status field
- stores processed emails in a local JSON database

## Features
- Gmail unread email parsing with IMAP
- text classification using TF-IDF + Logistic Regression
- three-class prediction:
  - `rejected`
  - `next_step`
  - `other`
- Google Sheets status updates
- automatic status cell coloring
- local processed-email logging in `database.json`
- training and testing on synthetic labeled datasets

## Tech Stack
- **Python**
- **scikit-learn**
- **TF-IDF Vectorizer**
- **Logistic Regression**
- **IMAP / imaplib**
- **Google Sheets API**
- **gspread**
- **python-dotenv**
- **JSON**
- **pickle**

## Project Structure
- `train_model.py` — trains and saves the classifier
- `predict.py` — loads the trained model and predicts email status
- `read_email.py` — reads unread emails and extracts content
- `matcher.py` — matches email content to spreadsheet company/job title rows
- `edit_sheet.py` — updates Google Sheets status cells
- `main.py` — connects the full pipeline
- `dataset/` — training and testing datasets
- `database/` — processed email log
- `saved_model/` — saved classifier and vectorizer

## Pipeline
1. Fetch unread emails from Gmail
2. Parse each email into subject, sender, and body
3. Use the trained model to classify the email
4. Ignore emails classified as `other`
5. Match company and job title to the spreadsheet
6. Update the application status in Google Sheets
7. Save the processed email to the local database

## Model Training
The model is trained using labeled datasets of job-related emails and non-actionable emails. It uses:
- **TF-IDF** to convert email text into numeric features
- **Logistic Regression** to classify the email outcome

## Notes
- `.env` and `credentials.json` are not included in the repository
- synthetic datasets were used for initial model training/testing
- live email processing uses unread inbox messages only
