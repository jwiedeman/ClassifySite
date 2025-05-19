import sys
import csv
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup
try:
    from googletrans import Translator
    translator = Translator()
except Exception:
    translator = None


def load_training_data(path: str = "labels.csv") -> List[dict]:
    """Load existing labeled data for incremental heuristics."""
    if not Path(path).exists():
        return []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QRadioButton, QComboBox, QLineEdit,
    QMessageBox,
)
import io
from contextlib import redirect_stdout
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView


def fetch_html(url: str) -> tuple[str, str]:
    """Return page HTML and a simple availability status."""
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        response.raise_for_status()
        status = "redirect" if response.history else "ok"
        return response.text, status
    except Exception:
        return "", "unavailable"


def extract_text(html: str) -> str:
    """Return visible text from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    for elem in soup(["script", "style"]):
        elem.extract()
    return soup.get_text(separator=" ")


def translate_to_english(text: str, max_chars: int = 5000) -> str:
    """Translate text to English using Google Translate."""
    snippet = text[:max_chars]
    if translator is None:
        return snippet
    try:
        return translator.translate(snippet, dest="en").text
    except Exception:
        return snippet


CATEGORIES = [
    "Retail",
    "Restaurant",
    "Cafe",
    "Bar",
    "Grocery",
    "Fashion",
    "Electronics",
    "Home Services",
    "Professional Services",
    "Health & Wellness",
    "Medical",
    "Finance",
    "Travel & Tourism",
    "Hotel",
    "Real Estate",
    "Automotive",
    "Blog",
    "News",
    "Portfolio",
    "Forum",
    "Entertainment",
    "Education",
    "Government",
    "Non-profit",
    "Technology",
    "Other",
]


def simple_classify(html: str):
    """Very naive placeholder classification with expanded categories."""
    if not html:
        return {"business": False, "category": "Other", "tags": ""}
    text_content = extract_text(html)
    text = translate_to_english(text_content).lower()
    tokens = set(text.split())
    training_data = load_training_data()
    business = any(word in text for word in ["shop", "store", "buy", "service"])
    if any(word in text for word in ["restaurant", "menu", "dining", "food"]):
        category = "Restaurant"
    elif any(word in text for word in ["cafe", "coffee"]):
        category = "Cafe"
    elif any(word in text for word in ["bar", "pub", "brew"]):
        category = "Bar"
    elif any(word in text for word in ["grocery", "supermarket"]):
        category = "Grocery"
    elif any(word in text for word in ["fashion", "clothing", "apparel"]):
        category = "Fashion"
    elif any(word in text for word in ["electronics", "gadget"]):
        category = "Electronics"
    elif any(word in text for word in ["plumbing", "cleaning", "repair"]):
        category = "Home Services"
    elif any(word in text for word in ["consulting", "lawyer", "accounting"]):
        category = "Professional Services"
    elif any(word in text for word in ["health", "wellness", "fitness", "gym"]):
        category = "Health & Wellness"
    elif any(word in text for word in ["clinic", "hospital", "medical"]):
        category = "Medical"
    elif any(word in text for word in ["finance", "bank", "insurance"]):
        category = "Finance"
    elif any(word in text for word in ["travel", "tourism", "flight"]):
        category = "Travel & Tourism"
    elif any(word in text for word in ["hotel", "resort"]):
        category = "Hotel"
    elif any(word in text for word in ["real estate", "realtor", "property"]):
        category = "Real Estate"
    elif any(word in text for word in ["car", "automotive", "auto"]):
        category = "Automotive"
    elif any(word in text for word in ["shop", "store", "buy"]):
        category = "Retail"
    elif any(word in text for word in ["news", "article", "press"]):
        category = "News"
    elif any(word in text for word in ["portfolio", "resume", "cv"]):
        category = "Portfolio"
    elif "forum" in text or "community" in text:
        category = "Forum"
    elif any(word in text for word in ["game", "music", "movie"]):
        category = "Entertainment"
    elif any(word in text for word in ["school", "university", "course"]):
        category = "Education"
    elif any(word in text for word in ["gov", "government"]):
        category = "Government"
    elif any(word in text for word in ["non-profit", "donate", "charity"]):
        category = "Non-profit"
    elif any(word in text for word in ["tech", "software", "cloud"]):
        category = "Technology"
    elif "blog" in text:
        category = "Blog"
    else:
        category = "Other"

    # adjust category using prior labels
    category_scores = {}
    for row in training_data:
        cat = row.get("category", "")
        tags = row.get("tags", "")
        for token in tags.split(','):
            token = token.strip().lower()
            if token and token in tokens:
                category_scores[cat] = category_scores.get(cat, 0) + 1
    if category_scores:
        category = max(category_scores, key=category_scores.get)

    tags = []
    if "restaurant" in text or "menu" in text:
        tags.append("restaurant")
    if "cafe" in text:
        tags.append("cafe")
    if "bar" in text or "pub" in text:
        tags.append("bar")
    if "grocery" in text or "supermarket" in text:
        tags.append("grocery")
    if "fashion" in text or "clothing" in text:
        tags.append("fashion")
    if "electronics" in text:
        tags.append("electronics")
    if any(word in text for word in ["plumbing", "cleaning", "repair"]):
        tags.append("home services")
    if any(word in text for word in ["consulting", "lawyer", "accounting"]):
        tags.append("professional services")
    if any(word in text for word in ["health", "wellness", "fitness", "gym"]):
        tags.append("health")
    if "medical" in text or "clinic" in text:
        tags.append("medical")
    if any(word in text for word in ["finance", "bank", "insurance"]):
        tags.append("finance")
    if any(word in text for word in ["travel", "tourism", "flight"]):
        tags.append("travel")
    if "hotel" in text or "resort" in text:
        tags.append("hotel")
    if "real estate" in text or "realtor" in text:
        tags.append("real estate")
    if "car" in text or "auto" in text:
        tags.append("automotive")
    if "blog" in text:
        tags.append("blog")
    if "news" in text:
        tags.append("news")
    if "shop" in text:
        tags.append("shop")
    if "forum" in text:
        tags.append("forum")
    if "portfolio" in text:
        tags.append("portfolio")

    return {
        "business": business,
        "category": category,
        "tags": ",".join(tags),
    }


class MainWindow(QMainWindow):
    def __init__(self, urls: List[str]):
        super().__init__()
        self.urls = urls
        self.index = -1
        self.current_html = ""
        self.setWindowTitle("Site Classifier")

        self.web_view = QWebEngineView()

        self.url_label = QLabel("")
        self.pred_label = QLabel("")

        self.business_yes = QRadioButton("Business")
        self.business_no = QRadioButton("Personal")

        self.category_box = QComboBox()
        self.category_box.addItems(CATEGORIES)

        self.status_box = QComboBox()
        self.status_box.addItems(["ok", "redirect", "unavailable"])

        self.tags_edit = QLineEdit()

        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.next_site)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_current_record)

        train_btn = QPushButton("Train Model")
        train_btn.clicked.connect(self.train_model_ui)

        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.web_view)
        layout.addWidget(self.pred_label)
        layout.addWidget(self.business_yes)
        layout.addWidget(self.business_no)
        layout.addWidget(QLabel("Category"))
        layout.addWidget(self.category_box)
        layout.addWidget(QLabel("Status"))
        layout.addWidget(self.status_box)
        layout.addWidget(QLabel("Tags (comma separated)"))
        layout.addWidget(self.tags_edit)

        hlayout = QHBoxLayout()
        hlayout.addWidget(save_btn)
        hlayout.addWidget(train_btn)
        hlayout.addWidget(next_btn)
        layout.addLayout(hlayout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.resize(1000, 800)

        self.next_site()

    def closeEvent(self, event):
        # ensure current progress is saved when closing the window
        self.save_current_record()
        super().closeEvent(event)

    def next_site(self):
        # save current entry before moving on
        if self.index >= 0:
            self.save_current_record()

        self.index += 1
        if self.index >= len(self.urls):
            self.url_label.setText("Done!")
            self.pred_label.setText("")
            return
        url = self.urls[self.index]
        self.url_label.setText(url)
        # load via Google Translate for automatic English view
        translate_url = (
            f"https://translate.google.com/translate?sl=auto&tl=en&u={url}"
        )
        self.web_view.load(QUrl(translate_url))
        html, status = fetch_html(url)
        self.current_html = html
        self.status_box.setCurrentText(status)
        if status == "ok":
            pred = simple_classify(html)
            self.pred_label.setText(
                f"Predicted: {'Business' if pred['business'] else 'Personal'}, {pred['category']}"
            )
        else:
            pred = {"business": False, "category": "Other", "tags": ""}
            self.pred_label.setText(f"Site status: {status}")
        self.business_yes.setChecked(pred["business"])
        self.business_no.setChecked(not pred["business"])
        self.category_box.setCurrentText(pred["category"])
        self.tags_edit.setText(pred["tags"])

    def save_current_record(self):
        if self.index < 0 or self.index >= len(self.urls):
            return
        url = self.urls[self.index]
        data = {
            "url": url,
            "status": self.status_box.currentText(),
            "business": self.business_yes.isChecked(),
            "category": self.category_box.currentText(),
            "tags": self.tags_edit.text(),
        }
        file_exists = Path("labels.csv").exists()
        with open("labels.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

    def train_model_ui(self):
        from train_model import load_dataset, evaluate_heuristics, train_model as train_model_func
        try:
            data = load_dataset()
            if not data:
                QMessageBox.information(self, "Training", "No training data found in labels.csv")
                return
            buf = io.StringIO()
            with redirect_stdout(buf):
                evaluate_heuristics(data)
                train_model_func(data)
            QMessageBox.information(self, "Training Complete", buf.getvalue())
        except Exception as e:
            QMessageBox.critical(self, "Training Error", str(e))
def load_urls(path: str) -> List[str]:
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    urls = load_urls("urls.txt")
    window = MainWindow(urls)
    window.show()
    sys.exit(app.exec())
