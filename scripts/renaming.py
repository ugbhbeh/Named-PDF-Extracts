import os
import re
from pypdf import PdfReader

INPUT_FOLDER = "../generated/split&named"


def clean_filename(text):
    return re.sub(r'[<>:"/\\|?*]', '', text).strip()


def extract_data(file_path):
    PO_X_MIN, PO_X_MAX = 300, 340
    PO_Y_MIN, PO_Y_MAX = 690, 710

    NAME_X_MIN, NAME_X_MAX = 140, 200
    NAME_Y_MIN, NAME_Y_MAX = 490, 510

    po_number = None
    product_name = None

    reader = PdfReader(file_path)

    for page in reader.pages:

        def visitor(text, cm, tm, font_dict, font_size):
            nonlocal po_number, product_name

            x = tm[4]
            y = tm[5]
            text = text.strip()

            if not text:
                return

            if PO_X_MIN <= x <= PO_X_MAX and PO_Y_MIN <= y <= PO_Y_MAX:
                po_number = (po_number or "") + text

            if NAME_X_MIN <= x <= NAME_X_MAX and NAME_Y_MIN <= y <= NAME_Y_MAX:
                product_name = (product_name or "") + text

        page.extract_text(visitor_text=visitor)

        if po_number and product_name:
            break

    return po_number, product_name


def run():
    for filename in os.listdir(INPUT_FOLDER):
        if not filename.lower().endswith(".pdf"):
            continue

        old_path = os.path.join(INPUT_FOLDER, filename)

        try:
            po, name = extract_data(old_path)

            if not po or not name:
                print(f"Skipping (missing data): {filename}")
                continue

            safe_name = clean_filename(name)
            new_filename = f"{po}_{safe_name}.pdf"
            new_path = os.path.join(INPUT_FOLDER, new_filename)

            if os.path.exists(new_path):
                print(f"Skipping (already exists): {new_filename}")
                continue

            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")

        except Exception as e:
            print(f"Error with {filename}: {e}")


if __name__ == "__main__":
    run()