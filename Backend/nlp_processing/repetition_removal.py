def remove_repetitions(text):

    words = text.split()

    cleaned = []

    prev = None

    for w in words:

        if w.lower() != prev:
            cleaned.append(w)

        prev = w.lower()

    return " ".join(cleaned)