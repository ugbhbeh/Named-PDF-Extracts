import os
import shutil
from pypdf import PdfReader

INPUT_FOLDER = "../generated/split&named"
PERIPHERAL_FOLDER = "../generated/peripheral"
A_STORE_FOLDER = "../generated/A-store"

TARGET = "PERIPHERAL"


def file_contains_target(file_path):
    X_MIN, X_MAX = 320.00, 620
    found = False

    reader = PdfReader(file_path)

    for page in reader.pages:

        def visitor(text, cm, tm, font_dict, font_size):
            nonlocal found

            if found:
                return

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
            break

    return found


os.makedirs(PERIPHERAL_FOLDER, exist_ok=True)
os.makedirs(A_STORE_FOLDER , exist_ok=True)


for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith(".pdf"):
        input_path = os.path.join(INPUT_FOLDER, filename)

        if file_contains_target(input_path):
            output_path = os.path.join(PERIPHERAL_FOLDER, filename)
            shutil.move(input_path, output_path)
            print(f"Moved to peripheral: {filename}")
        else:
            output_path = os.path.join(A_STORE_FOLDER , filename)
            shutil.move(input_path, output_path)
            print(f"Moved to non-peripheral: {filename}")