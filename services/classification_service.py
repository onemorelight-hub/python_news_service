import joblib

# Load saved model components
model = joblib.load('./ai_models/logistic_model.pkl')
vectorizer = joblib.load('./ai_models/tfidf_vectorizer.pkl')
label_encoder = joblib.load('./ai_models/label_encoder.pkl')


def predict_category(text: str) -> str:
    # Transform input text
    text_vector = vectorizer.transform([text])

    # Predict label
    pred_label = model.predict(text_vector)[0]

    # Decode label to category name
    category = label_encoder.inverse_transform([pred_label])[0]
    return category
