from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

# Load models safely
try:
    model = pickle.load(open("phishing_model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
except Exception as e:
    print(f"Error loading models: {e}")
    model = None
    vectorizer = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None or vectorizer is None:
        return jsonify({"error": "Model files are not loaded properly on the server."}), 500
        
    data = request.get_json()
    message = data.get("message", "")
    
    if not message.strip():
        return jsonify({"error": "Empty message provided."}), 400

    # Transform and Predict
    message_vector = vectorizer.transform([message])
    prediction = model.predict(message_vector)
    
    result = "phishing" if prediction[0] == 1 else "safe"
    
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
