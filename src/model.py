from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from .features import extract_features

MODEL_PATH = Path("models/phishguard.joblib")

def train_model(csv_path: str, model_path: Path = MODEL_PATH):
    data = pd.read_csv(csv_path)
    if not {"url", "label"}.issubset(data.columns):
        raise ValueError("CSV must contain 'url' and 'label' columns.")
    data = data.dropna(subset=["url", "label"]).copy()
    data["label"] = data["label"].astype(int)
    if not set(data["label"].unique()).issubset({0, 1}) or data["label"].nunique() != 2:
        raise ValueError("Labels must contain both classes: 0=legitimate, 1=phishing.")
    X = pd.DataFrame([extract_features(u) for u in data["url"]])
    y = data["label"]
    if len(data) < 10:
        raise ValueError("Please provide at least 10 labelled URLs for a basic train/test split.")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    model = Pipeline([
        ("scale", StandardScaler()),
        ("classifier", RandomForestClassifier(
            n_estimators=300, class_weight="balanced", random_state=42,
            min_samples_leaf=1
        ))
    ])
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "feature_names": list(X.columns)}, model_path)
    return {
        "accuracy": accuracy_score(y_test, pred),
        "report": classification_report(y_test, pred, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        "test_size": len(y_test),
    }

def load_model(model_path: Path = MODEL_PATH):
    if not model_path.exists():
        raise FileNotFoundError("Model not found. Run: python train.py")
    return joblib.load(model_path)
