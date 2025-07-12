### File: utils/tokenizers.py
import spacy
import string
import ssl


ssl._create_default_https_context = ssl._create_unverified_context


# Attempt to load spaCy model and download if missing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def remove_stopwords_and_lemmatize(text):
    doc = nlp(text.lower())
    return [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct and token.lemma_ not in string.punctuation
    ]
