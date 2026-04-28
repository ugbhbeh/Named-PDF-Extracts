import os
import csv
import shutil
from collections import defaultdict
from pypdf import PdfReader

INPUT_FOLDER = "../generated/split&named"
OUTPUT_BASE = "../generated"
CONFIG_FILE = "../reference/locations.csv"


def load_rules():
    rules = defaultdict(list)

    with open(CONFIG_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            folder = row["folder"]
            x = float(row["x"])
            y = float(row["y"])
            text = row["text"]

            rules[folder].append(((x, y), text))

    return rules


LOCATION_RULES = load_rules()


def detect_location(file_path):
    reader = PdfReader(file_path)
    found = {folder: set() for folder in LOCATION_RULES}

    for page in reader.pages:

        def visitor(text, cm, tm, font_dict, font_size):
            x = tm[4]
            y = tm[5]
            text_clean = text.strip()

            if not text_clean:
                return

            for folder_name, rules in LOCATION_RULES.items():
                for (target_x, target_y), expected_text in rules:
                    if x == target_x and y == target_y:
                        if expected_text.lower() in text_clean.lower():
                            found[folder_name].add(expected_text)

        page.extract_text(visitor_text=visitor)

    for folder_name, rules in LOCATION_RULES.items():
        required = {text for _, text in rules}
        if required.issubset(found[folder_name]):
            return folder_name

    return "Unmatched"


for folder in LOCATION_RULES:
    os.makedirs(os.path.join(OUTPUT_BASE, folder), exist_ok=True)

os.makedirs(os.path.join(OUTPUT_BASE, "Unmatched"), exist_ok=True)


for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith(".pdf"):
        input_path = os.path.join(INPUT_FOLDER, filename)

        folder_name = detect_location(input_path)

        output_path = os.path.join(OUTPUT_BASE, folder_name, filename)
        shutil.move(input_path, output_path)

        print(f"Moved {filename} -> {folder_name}")