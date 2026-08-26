from flask import Flask, render_template, request, jsonify
from detector import predict_message, load_artifacts

app = Flask(__name__)

# Load models safely on startup
try:
    model, vectorizer = load_artifacts()
except Exception as e:
    print(f"Warning: Model artifacts could not be loaded: {e}")
    model = None
    vectorizer = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None and vectorizer is not None
    })


@app.route("/predict", methods=["POST"])
def predict():
    if model is None or vectorizer is None:
        return jsonify({"error": "Model files are not loaded properly on the server."}), 500

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field in JSON payload."}), 400

    message = data.get("message", "")
    if not message.strip():
        return jsonify({"error": "Empty message provided."}), 400

    try:
        result = predict_message(message, model, vectorizer)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
