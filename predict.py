import os
import pickle

MODEL_PATH = os.path.join("saved_model", "email_classifier.pkl")
VECTORIZER_PATH = os.path.join("saved_model", "tfidf_vectorizer.pkl")


def load_pickle(path):
    with open(path, "rb") as file:
        return pickle.load(file)


def predict_email(subject, body):
    model = load_pickle(MODEL_PATH)
    vectorizer = load_pickle(VECTORIZER_PATH)

    combined_text = f"{subject} {body}".strip()
    text_vector = vectorizer.transform([combined_text])

    prediction = model.predict(text_vector)[0]
    return prediction


if __name__ == "__main__":
    subject = "Interview invitation for Software Developer Intern"
    body = "We would like to move you forward to the next stage. Please share your availability."

    result = predict_email(subject, body)
    print("Prediction:", result)