import os
import shutil
from pypdf import PdfReader

INPUT_FOLDER = "output"
OUTPUT_FOLDER = "peripheral"

TARGET = "PERIPHERAL"


def file_contains_target(file_path):
    X_MIN, X_MAX = 320.00, 620
    found = False

    reader = PdfReader(file_path)

    for page in reader.pages:

        def visitor(text, cm, tm, font_dict, font_size):
            nonlocal found

            if found:
                return  # stop extra work once found

            x = tm[4]
            text_clean = text.strip()

            if not text_clean:
                return

            if not (X_MIN <= x <= X_MAX):
                return

            if TARGET.lower() in text_clean.lower():
                found = True

        page.extract_text(visitor_text=visitor)

        if found:
            break  # stop scanning more pages

    return found


# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# Process all PDFs
for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith(".pdf"):
        input_path = os.path.join(INPUT_FOLDER, filename)

        if file_contains_target(input_path):
            output_path = os.path.join(OUTPUT_FOLDER, filename)
            shutil.copy(input_path, output_path)
            print(f"Copied: {filename}")