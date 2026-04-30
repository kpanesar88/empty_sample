import json
import os

# SAVING MODELS
import pickle

# CONVERTING NORMAL TEXT INTO NUMBERS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

TRAIN_PATH = "dataset/training_set.json"
TEST_PATH = "dataset/testing_set.json"

MODEL_DIR = "saved_model"
MODEL_PATH = os.path.join(MODEL_DIR, "email_classifier.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")

def load_database(filename):
    try:
        with open(filename, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {filename}")

train_data = load_database(TRAIN_PATH)
train_emails = train_data["emails"]

test_data = load_database(TEST_PATH)
test_emails = test_data["emails"]

def build_text_and_labels(emails):
    texts = []
    labels = []

    for email in emails:
        subject = email.get("subject", "")
        body = email.get("body", "")
        status = email.get("status", "")

        combined_text = f"{subject} {body}".strip()

        texts.append(combined_text)
        labels.append(status)

    return texts, labels


def save_pickle(obj, path):
    with open(path, "wb") as file:
        pickle.dump(obj, file)


X_train, y_train = build_text_and_labels(train_emails)
X_test, y_test = build_text_and_labels(test_emails)

print(f"Training emails: {len(X_train)}")
print(f"Testing emails: {len(X_test)}")

vectorizer = TfidfVectorizer(lowercase=True, stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

predictions = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy:.4f}")
print(classification_report(y_test, predictions))

os.makedirs(MODEL_DIR, exist_ok=True)
save_pickle(model, MODEL_PATH)
save_pickle(vectorizer, VECTORIZER_PATH)

print("Model saved.")
print("Vectorizer saved.")