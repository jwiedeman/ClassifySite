import sys
import csv
from pathlib import Path
from typing import List

import requests
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QRadioButton, QComboBox, QLineEdit
)


def fetch_html(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception:
        return ""


def simple_classify(html: str):
    """Very naive placeholder classification."""
    text = html.lower()
    business = any(word in text for word in ["shop", "store", "buy"])
    category = "Retail" if "shop" in text else "Other"
    tags = []
    if "blog" in text:
        tags.append("blog")
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

        self.url_label = QLabel("")
        self.pred_label = QLabel("")

        self.business_yes = QRadioButton("Business")
        self.business_no = QRadioButton("Personal")

        self.category_box = QComboBox()
        self.category_box.addItems(["Retail", "Blog", "Other"])

        self.tags_edit = QLineEdit()

        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.next_site)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_current)

        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.pred_label)
        layout.addWidget(self.business_yes)
        layout.addWidget(self.business_no)
        layout.addWidget(QLabel("Category"))
        layout.addWidget(self.category_box)
        layout.addWidget(QLabel("Tags (comma separated)"))
        layout.addWidget(self.tags_edit)

        hlayout = QHBoxLayout()
        hlayout.addWidget(save_btn)
        hlayout.addWidget(next_btn)
        layout.addLayout(hlayout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.next_site()

    def next_site(self):
        self.index += 1
        if self.index >= len(self.urls):
            self.url_label.setText("Done!")
            self.pred_label.setText("")
            return
        url = self.urls[self.index]
        self.url_label.setText(url)
        html = fetch_html(url)
        self.current_html = html
        pred = simple_classify(html)
        self.business_yes.setChecked(pred["business"])
        self.business_no.setChecked(not pred["business"])
        self.category_box.setCurrentText(pred["category"])
        self.tags_edit.setText(pred["tags"])
        self.pred_label.setText(
            f"Predicted: {'Business' if pred['business'] else 'Personal'}, {pred['category']}"
        )

    def save_current(self):
        if self.index >= len(self.urls):
            return
        url = self.urls[self.index]
        data = {
            "url": url,
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
        self.next_site()


def load_urls(path: str) -> List[str]:
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    urls = load_urls("urls.txt")
    window = MainWindow(urls)
    window.show()
    sys.exit(app.exec())
