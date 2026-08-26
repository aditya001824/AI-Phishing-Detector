import argparse
import os
import pickle
import sys

MODEL_PATH = os.path.join(os.path.dirname(__file__), "phishing_model.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.pkl")


def load_artifacts():
    """Load serialized model and vectorizer artifacts."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(
            "Model artifacts (phishing_model.pkl, vectorizer.pkl) not found. "
            "Run 'python train_model.py' to generate them."
        )

    with open(MODEL_PATH, "rb") as f_model, open(VECTORIZER_PATH, "rb") as f_vec:
        model = pickle.load(f_model)
        vectorizer = pickle.load(f_vec)
    return model, vectorizer


def predict_message(text: str, model=None, vectorizer=None):
    """
    Predict if a text message is phishing or safe.
    
    Returns a dict with 'label' ('phishing' or 'safe'), 'is_phishing' bool, and 'confidence' float.
    """
    if not text or not text.strip():
        raise ValueError("Input message cannot be empty.")

    if model is None or vectorizer is None:
        model, vectorizer = load_artifacts()

    vector = vectorizer.transform([text])
    pred = model.predict(vector)[0]
    
    # Calculate probability if supported
    confidence = 1.0
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(vector)[0]
        confidence = float(probabilities[pred])

    label = "phishing" if pred == 1 else "safe"
    return {
        "result": label,
        "is_phishing": bool(pred == 1),
        "confidence": round(confidence, 4)
    }


def main():
    parser = argparse.ArgumentParser(
        description="AI Phishing Detector - Analyze text and emails for phishing indicators."
    )
    parser.add_argument(
        "-t", "--text", type=str, help="Text message or email snippet to analyze."
    )
    parser.add_argument(
        "-f", "--file", type=str, help="Path to a text file containing message to analyze."
    )
    args = parser.parse_args()

    try:
        model, vectorizer = load_artifacts()
    except Exception as e:
        print(f"[ERROR] Loading model failed: {e}", file=sys.stderr)
        sys.exit(1)

    if args.file:
        if not os.path.exists(args.file):
            print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    elif args.text:
        content = args.text
    else:
        try:
            content = input("Enter message to analyze: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            sys.exit(0)

    if not content.strip():
        print("[WARNING] No input provided.")
        sys.exit(1)

    result = predict_message(content, model, vectorizer)
    
    print("\n--- Analysis Result ---")
    if result["is_phishing"]:
        print("[ALERT] Status: PHISHING DETECTED")
        print(f"[INFO]  Confidence: {result['confidence'] * 100:.2f}%")
        print("[WARN]  Warning: Do not click any links or share sensitive credentials.")
    else:
        print("[OK]    Status: SAFE MESSAGE")
        print(f"[INFO]  Confidence: {result['confidence'] * 100:.2f}%")


if __name__ == "__main__":
    main()
