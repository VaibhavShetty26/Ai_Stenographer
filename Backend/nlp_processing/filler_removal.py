import re

FILLERS = [
    "um","uh","umm","uhh","like","actually","basically","you know","i mean"
]

def remove_fillers(text):

    pattern = r'\b(' + '|'.join(FILLERS) + r')\b'

    text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    return re.sub(r'\s+', ' ', text).strip()