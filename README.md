# ML-Based Detection and Analysis of CSRF and XSS Attacks

A Python/Streamlit academic project for detecting suspicious web requests using machine learning. The project is based on the methodology and analysis described in the accompanying paper: understanding attack characteristics, preprocessing HTTP-request features, feature extraction, Random Forest classification, evaluation with accuracy/precision/recall/F1-score, and real-time-style prediction.

## Project scope

- Detect three classes: `BENIGN`, `CSRF`, and `XSS`.
- Extract simple lexical/structural request features such as request method, URL length, parameter count, script indicators, CSRF-token indicators, special-character counts, and payload length.
- Train a Random Forest classifier.
- Show prediction, confidence, model metrics, and feature importance in a Streamlit dashboard.
- Provide a lightweight prediction interface for manually entered request data.

> **Important:** The supplied paper describes a research framework and contains result figures, but it does not provide the original dataset or source code. Therefore this repository is a clean, runnable reference implementation of the described workflow; it should not be represented as the authors' original source code or as reproducing the paper's exact numerical results.

## Folder structure

```text
CSRF_XSS_ML_GitHub_Repo/
├── app.py
├── train_model.py
├── requirements.txt
├── .gitignore
├── README.md
├── LICENSE
├── data/
│   └── demo_web_requests.csv
└── src/
    ├── __init__.py
    ├── features.py
    └── model.py
```

## Run locally

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

The browser will open the Streamlit dashboard.

## Dataset

`data/demo_web_requests.csv` is a small **demo dataset created for this repository** so that the application runs without the unavailable original research dataset. Replace it with your actual labelled HTTP-request dataset before using the project for academic evaluation.

Expected columns:

```text
method,url,headers,payload,label
```

Allowed labels:

```text
BENIGN
CSRF
XSS
```

## Methodology implemented

1. Understand attack characteristics.
2. Collect/prepare HTTP-request examples.
3. Extract lexical and structural features.
4. Split data into training and test sets.
5. Train Random Forest.
6. Evaluate using Accuracy, Precision, Recall and F1-score.
7. Use the trained model for interactive prediction.

## Security note

This project is intended for defensive security research and educational use. Do not test against systems you do not own or have explicit permission to assess.
