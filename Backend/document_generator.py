import os
from datetime import datetime


def generate_document(text, filename="stenographer_output.txt"):
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Professional Document\n")
        f.write("=====================\n\n")
        f.write(f"Generated on: {datetime.now()}\n\n")
        f.write(text + "\n")

    return file_path
