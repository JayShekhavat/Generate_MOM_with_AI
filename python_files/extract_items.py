import spacy
from python_files.clean_text import cleaned_text

nlp = spacy.load("en_core_web_sm")


def extr_items(cleaned_texts):
    doc = nlp(cleaned_text)
    action_items = []
    for sent in doc.sents:
        if "will" in sent.text or "action" in sent.text.lower():
            action_items.append(sent.text)

    return action_items


# items = extr_items(cleaned_text)
# print(items)