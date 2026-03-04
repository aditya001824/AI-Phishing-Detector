import pickle

model = pickle.load(open("phishing_model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

message = input("Enter email message: ")

message_vector = vectorizer.transform([message])

prediction = model.predict(message_vector)

if prediction[0] == 1:
    print("⚠️ Phishing message detected")
else:
    print("✅ Safe message")
