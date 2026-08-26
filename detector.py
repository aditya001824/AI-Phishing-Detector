import argparse
import os
import pickle
import sys
from heuristics import analyze_heuristics

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
    Perform hybrid ML + Heuristic prediction on a given text message.
    """
    if not text or not text.strip():
        raise ValueError("Input message cannot be empty.")

    if model is None or vectorizer is None:
        model, vectorizer = load_artifacts()

    # 1. Machine Learning Prediction
    vector = vectorizer.transform([text])
    pred = model.predict(vector)[0]
    
    confidence = 1.0
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(vector)[0]
        confidence = float(probabilities[pred])

    # 2. Heuristic Risk Analysis
    heuristic_results = analyze_heuristics(text)

    # Hybrid escalation: If heuristics detect critical danger (e.g. IP address URL + high urgency)
    is_phishing = bool(pred == 1)
    if not is_phishing and heuristic_results["heuristic_score"] >= 65:
        # Heuristic override for high risk signatures
        is_phishing = True
        label = "phishing"
    else:
        label = "phishing" if is_phishing else "safe"

    return {
        "result": label,
        "is_phishing": is_phishing,
        "confidence": round(confidence, 4),
        "heuristic_score": heuristic_results["heuristic_score"],
        "risk_level": heuristic_results["risk_level"],
        "flags": heuristic_results["flags"],
        "url_analysis": heuristic_results["url_analysis"]
    }


def main():
    parser = argparse.ArgumentParser(
        description="AI Phishing Detector - Hybrid ML & Heuristic Analysis."
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
    
    print("\n" + "=" * 45)
    print("           ANALYSIS REPORT           ")
    print("=" * 45)
    if result["is_phishing"]:
        print("[STATUS]     🚨 PHISHING DETECTED")
    else:
        print("[STATUS]     ✅ SAFE MESSAGE")

    print(f"[CONFIDENCE] {result['confidence'] * 100:.2f}%")
    print(f"[RISK LEVEL] {result['risk_level']} (Score: {result['heuristic_score']}/100)")
    
    if result["flags"]:
        print("\n[KEY RISK INDICATORS]")
        for flag in result["flags"]:
            print(f"  - {flag}")

    if result["url_analysis"]["url_count"] > 0:
        print(f"\n[URL SCAN]   Found {result['url_analysis']['url_count']} link(s)")

    print("=" * 45)


if __name__ == "__main__":
    main()
