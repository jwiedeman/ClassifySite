# ClassifySite

A simple desktop app that loads a list of URLs, shows the page in an embedded browser, and helps you classify the site. Results are stored locally for future model training.
Pages are automatically translated to English using Google Translate (if available) so you can work with foreign language sites.
Each time you move to the next site your selections are saved automatically, letting you quit at any time without losing progress.

## Usage

1. Install dependencies (make sure your PySide6 installation includes the WebEngine module). Translation is optional, so failures to install `googletrans` on newer Python versions are safe to ignore:
   ```bash
   pip install -r requirements.txt
   ```
2. Put URLs to classify in `urls.txt` (one per line).
3. Run the application:
   ```bash
   python app.py
   ```

The application will try to guess whether a site is a business, its category, and content tags using a simple heuristic. You can correct the predictions and save the labels to `labels.csv`. The category drop-down now contains many common business types. Previous labels are loaded on each step to refine future predictions as you work.

Each record also stores a simple **status** flag (`ok`, `redirect`, or `unavailable`) so you can mark pages that fail to load or immediately redirect.

**Note:** The classification logic is a placeholder. Integrate your preferred LLM or machine learning model for better results.

## Training a model

After labeling some sites you can train a simple text classifier and compare it
with the built-in heuristic. Training can be initiated directly from the
application by clicking **"Train Model"**. Results are shown in a pop up dialog
and the trained model is written to `model.pkl`.

Once a model is saved you can load it in the application by clicking
**"Load Model"**. When loaded, the predicted category will come from the
trained model instead of the heuristic so you can iteratively refine the
classifier as you label more data.

If you prefer running from the command line you can still execute the script:

```bash
python train_model.py
```
