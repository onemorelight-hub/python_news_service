import spacy.cli


def download_model():
    spacy.cli.download("en_core_web_sm")
