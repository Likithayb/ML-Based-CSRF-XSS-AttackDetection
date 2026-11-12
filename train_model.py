from src.model import train

if __name__ == "__main__":
    metrics = train("data/demo_web_requests.csv")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print("Labels:", ", ".join(metrics["labels"]))
    print("Model saved to models/random_forest.joblib")
