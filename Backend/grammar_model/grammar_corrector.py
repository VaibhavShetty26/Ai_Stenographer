from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re

# Model name
MODEL_NAME = "prithivida/grammar_error_correcter_v1"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32
)

# Force CPU usage to avoid GPU / memory issues
device = torch.device("cpu")
model = model.to(device)


def clean_output(text):

    patterns = [
        r"grammar:",
        r"Improve the grammatical correctness.*?:",
        r"Correct grammatical errors.*?:"
    ]

    for p in patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE)

    return text.strip()


def correct_grammar(text: str):

    if not text or not text.strip():
        return ""

    try:

        prompt = "grammar: " + text

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            padding=True
        ).to(device)

        outputs = model.generate(
            **inputs,
            max_length=128
        )

        corrected = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        corrected = clean_output(corrected)

        return corrected

    except Exception as e:

        print("Grammar correction error:", e)

        return text