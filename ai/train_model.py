import pandas as pd
import os
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# Load training dataset
dataset_path = os.path.join("ai", "dataset.csv")
data = pd.read_csv(dataset_path)

# Separate email text and labels
X = data["text"]
y = data["label"]

# Convert email text into TF-IDF features
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

X_tfidf = vectorizer.fit_transform(X)

# Train Logistic Regression classifier
model = LogisticRegression(
    max_iter=1000
)

model.fit(X_tfidf, y)

# Save the trained model
model_path = os.path.join("ai", "phishing_model.pkl")

with open(model_path, "wb") as file:
    pickle.dump(model, file)

# Save the TF-IDF vectorizer
vectorizer_path = os.path.join("ai", "tfidf_vectorizer.pkl")

with open(vectorizer_path, "wb") as file:
    pickle.dump(vectorizer, file)

print("AI phishing detection model trained successfully.")
print(f"Training samples: {len(data)}")
print(f"Model saved to: {model_path}")
print(f"Vectorizer saved to: {vectorizer_path}")