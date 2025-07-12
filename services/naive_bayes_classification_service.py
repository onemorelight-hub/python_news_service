import joblib
import nltk
import string
from nltk.corpus import stopwords

nltk.download('stop_words')
stop_words = set(stopwords.words('english'))


# Load saved model components
model = joblib.load('./ai_models/naive_bayes/naive_bayes_model.pkl')
vectorizer = joblib.load('./ai_models/naive_bayes/tfidf_vectorizer.pkl')

def predict_category(text: str) -> str:
    text_processed = preprocess(text)  # if you have a preprocessing function
    X = vectorizer.transform([text_processed])
    X_dense = X.toarray()  # convert to dense
    prediction = model.predict(X_dense)
    return prediction[0]


def preprocess(text):
    text = str(text)  # just in case
    text = text.lower()
    text = ''.join(char for char in text if char not in string.punctuation)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)
