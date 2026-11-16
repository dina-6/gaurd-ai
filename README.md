# 🛡️ PhishGuard AI — Explainable Phishing URL Detector

A portfolio-ready AI/ML project that analyses the **structure of a URL** and predicts whether it resembles a phishing link. It combines a scikit-learn classifier with human-readable warning indicators and a Streamlit interface.

> **Important:** This is an educational prototype, not a production security product. It does not visit URLs, inspect page content, or guarantee that a website is safe. The included sample dataset is illustrative and far too small for reliable real-world predictions.

## Features

- URL feature engineering (length, symbols, IP host, subdomains, punycode, suspicious words, etc.)
- Random Forest classification with class balancing
- Train/test split and evaluation report
- Streamlit web interface
- Human-readable URL warning indicators
- Unit tests
- Bring your own labelled URL dataset

## Project structure

```text
PhishGuard-AI/
├── app.py
├── train.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_urls.csv
├── models/                 # trained model is generated here
├── src/
│   ├── __init__.py
│   ├── features.py
│   └── model.py
└── tests/
    └── test_features.py
```

## 1. Run locally

Python 3.10 or newer is recommended.

```bash
git clone https://github.com/YOUR-USERNAME/PhishGuard-AI.git
cd PhishGuard-AI

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python train.py
streamlit run app.py
```

Open the local Streamlit URL shown in your terminal.

## 2. Use a better dataset

The included `data/sample_urls.csv` only checks that the pipeline runs. For meaningful evaluation, obtain a legally usable, well-labelled dataset from a reputable source (for example, the UCI Machine Learning Repository or a research dataset with a clear licence).

Prepare a CSV with exactly these columns:

```csv
url,label
https://www.example.org,0
http://suspicious-example.test/login,1
```

- `0` = legitimate
- `1` = phishing

Then train with:

```bash
python train.py --data path/to/your_dataset.csv
```

Use a dataset with many diverse URLs, check for duplicates and label quality, and avoid mixing near-duplicate URLs across train and test sets. For stronger research, use a time-based or domain-grouped split and report precision, recall, F1-score, and confusion matrix—not accuracy alone.

## 3. Run tests

```bash
pytest -q
```

## How it works

1. User enters a URL.
2. The feature extractor converts the URL into numeric signals.
3. A trained Random Forest classifier estimates the class.
4. The interface displays the prediction, estimated phishing score, and interpretable warning clues.

### ML features

Examples include URL length, hostname length, number of dots/hyphens, `@` and `?` counts, digit count, IP-address host, number of subdomains, punycode presence, HTTPS scheme, and suspicious keyword count.

## Model evaluation

`train.py` prints a hold-out classification report and confusion matrix. Do not claim high performance from the sample file. Re-train and report results from a properly sourced, sufficiently large dataset before presenting this as a research result.

## Suggested future improvements

- Add domain age and DNS/WHOIS signals from trusted sources (with rate limits and privacy safeguards).
- Compare Logistic Regression, Random Forest, and Gradient Boosting.
- Add SHAP explanations.
- Add a browser extension only after robust validation.
- Add a dataset card describing source, licence, class balance, and limitations.

## Tech stack

Python • Pandas • scikit-learn • Streamlit • pytest

## Responsible-use note

A URL classifier can make false positives and false negatives. Never use its output as the only basis for a security decision. Do not submit private, internal, or sensitive URLs to public demos.
