from nlp_processing.filler_removal import remove_fillers
from nlp_processing.repetition_removal import remove_repetitions
from grammar_model.grammar_corrector import correct_grammar


def clean_text(text: str):

    if not text:
        return ""

    # remove filler words
    text = remove_fillers(text)

    # remove repeated words
    text = remove_repetitions(text)

    # grammar correction
    text = correct_grammar(text)

    # basic formatting
    text = text.strip()

    if text:
        text = text[0].upper() + text[1:]

    return text