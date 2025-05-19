# ClassifySite

A simple desktop app that loads a list of URLs, shows the page in an embedded browser, and helps you classify the site. Results are stored locally for future model training.

## Usage

1. Install dependencies (make sure your PySide6 installation includes the WebEngine module):
   ```bash
   pip install -r requirements.txt
   ```
2. Put URLs to classify in `urls.txt` (one per line).
3. Run the application:
   ```bash
   python app.py
   ```

The application will try to guess whether a site is a business, its category, and content tags using a simple heuristic. You can correct the predictions and save the labels to `labels.csv`. The category drop-down now contains several common categories so you can quickly approve or adjust the guess.

**Note:** The classification logic is a placeholder. Integrate your preferred LLM or machine learning model for better results.
