import argparse
from src.model import train_model

parser = argparse.ArgumentParser(description="Train the PhishGuard URL classifier.")
parser.add_argument("--data", default="data/sample_urls.csv", help="CSV with url,label columns")
args = parser.parse_args()

metrics = train_model(args.data)
print(f"Model saved to models/phishguard.joblib")
print(f"Hold-out accuracy: {metrics['accuracy']:.3f} (test rows: {metrics['test_size']})")
print("Classification report:\n", metrics["report"])
print("Confusion matrix [ [TN, FP], [FN, TP] ]:\n", metrics["confusion_matrix"])
print("\nNote: metrics from the tiny sample dataset are only a pipeline check, not evidence of real-world performance.")
