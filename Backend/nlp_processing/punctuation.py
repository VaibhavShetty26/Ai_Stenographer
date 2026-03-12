import re

def polish_text(text):

    text = re.sub(r"\bEveryone of\b", "Every one of", text)
    text = re.sub(r"\bBetween you and I\b", "Between you and me", text)

    text = re.sub(r"\s+([,.!?])", r"\1", text)

    sentences = re.split(r'(?<=[.!?]) +', text)

    sentences = [s.capitalize() for s in sentences]

    return " ".join(sentences)