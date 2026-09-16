import pickle


# Load trained model and vectorizer
with open("ai/phishing_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("ai/tfidf_vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)


# Test emails
test_emails = [
    "Urgent! Your account has been suspended. Click the link immediately to verify your account.",
    "Please review the project report before tomorrow's meeting."
]


# Convert emails into TF-IDF features
email_features = vectorizer.transform(test_emails)

# Make predictions
predictions = model.predict(email_features)


# Display results
for email, prediction in zip(test_emails, predictions):
    print("\nEmail:")
    print(email)
    print("Prediction:", prediction)