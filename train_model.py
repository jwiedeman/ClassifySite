import csv
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import joblib

from app import fetch_html, extract_text, simple_classify, translate_to_english


def load_dataset(labels_path: str = "labels.csv"):
    """Load labeled sites and fetch their text."""
    if not Path(labels_path).exists():
        raise FileNotFoundError(f"{labels_path} not found")

    records = []
    with open(labels_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("status") != "ok":
                continue
            url = row["url"]
            html, status = fetch_html(url)
            if status != "ok" or not html:
                continue
            text = translate_to_english(extract_text(html))
            records.append({"text": text, "category": row["category"], "url": url})
    return records


def evaluate_heuristics(records):
    """Evaluate simple heuristics on the dataset."""
    gold, preds = [], []
    for rec in records:
        html, _ = fetch_html(rec["url"])
        pred = simple_classify(html)["category"] if html else "Other"
        gold.append(rec["category"])
        preds.append(pred)
    print("Heuristic accuracy:", accuracy_score(gold, preds))
    print(classification_report(gold, preds))


def train_model(records):
    texts = [r["text"] for r in records]
    labels = [r["category"] for r in records]
    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(texts)
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42
    )
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    print("Model accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))
    joblib.dump({"vectorizer": vectorizer, "model": clf}, "model.pkl")
    print("Model saved to model.pkl")


if __name__ == "__main__":
    data = load_dataset()
    if not data:
        print("No training data found in labels.csv")
    else:
        print("Evaluating heuristics on dataset...")
        evaluate_heuristics(data)
        print("\nTraining logistic regression model...")
        train_model(data)
