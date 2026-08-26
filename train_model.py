import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset", "phishing_email.csv")
MODEL_OUT = os.path.join(os.path.dirname(__file__), "phishing_model.pkl")
VECTORIZER_OUT = os.path.join(os.path.dirname(__file__), "vectorizer.pkl")


def train_and_save_model():
    print("=" * 50)
    print("Training AI Phishing Detector Model")
    print("=" * 50)

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

    print(f"Loading dataset from: {DATASET_PATH}")
    data = pd.read_csv(DATASET_PATH, sep="\t", names=["label", "message"])
    print(f"Dataset Shape: {data.shape[0]} rows, {data.shape[1]} columns")

    # Map labels: ham (safe) -> 0, spam/phishing -> 1
    data["label"] = data["label"].map({"ham": 0, "spam": 1})
    data.dropna(subset=["message", "label"], inplace=True)

    X = data["message"]
    y = data["label"]

    print("Vectorizing text using TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000, stop_words="english", ngram_range=(1, 2))
    X_vec = vectorizer.fit_transform(X)

    print("Splitting data into 80% train and 20% test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vec, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training Logistic Regression classifier...")
    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(X_train, y_train)

    # Evaluate
    print("\n--- Model Evaluation Metrics ---")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc * 100:.2f}%\n")
    print("Detailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Safe (Ham)", "Phishing (Spam)"]))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Save artifacts
    print(f"\nSaving model to {MODEL_OUT}...")
    with open(MODEL_OUT, "wb") as f_model:
        pickle.dump(model, f_model)

    print(f"Saving vectorizer to {VECTORIZER_OUT}...")
    with open(VECTORIZER_OUT, "wb") as f_vec:
        pickle.dump(vectorizer, f_vec)

    print("Model training completed successfully!")


if __name__ == "__main__":
    train_and_save_model()
