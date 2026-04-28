import os
import shutil
from pypdf import PdfReader

INPUT_FOLDER = "../generated/split&named"

PERIPHERAL_FOLDER = "../generated/peripheral"
BASEMENT_FOLDER = "../generated/basement"
CHITTOOR_FOLDER = "../generated/chittoor"
RANIPET_FOLDER = "../generated/ranipet"



def get_file_location(file_path):
    found_location = None

    reader = PdfReader(file_path)

    for page in reader.pages:

        def visitor(text, cm, tm, font_dict, font_size):
            nonlocal found_location

            if found_location:
                return

            x = tm[4]
            text_clean = text.strip()

            if not text_clean:
                return

            if 320.00 <= x <= 620:
                if "PERIPHERAL" in text_clean.upper():
                    found_location = "peripheral"
                    return

                if "BASEMENT AREA" in text_clean.upper():
                    found_location = "basement"
                    return

                if "CHITTOOR" in text_clean.upper():
                    found_location = "chittoor"
                    return

            if 15.00 <= x <= 300:
                if "RANIPET CAMP" in text_clean.upper():
                    found_location = "ranipet"
                    return

        page.extract_text(visitor_text=visitor)

        if found_location:
            break

    return found_location

def run():
    os.makedirs(PERIPHERAL_FOLDER, exist_ok=True)
    os.makedirs(BASEMENT_FOLDER, exist_ok=True)
    os.makedirs(CHITTOOR_FOLDER, exist_ok=True)
    os.makedirs(RANIPET_FOLDER, exist_ok=True)


    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(INPUT_FOLDER, filename)

            location = get_file_location(input_path)

            if location == "peripheral":
                output_path = os.path.join(PERIPHERAL_FOLDER, filename)
                shutil.move(input_path, output_path)
                print(f"Moved to peripheral: {filename}")

            elif location == "basement":
                output_path = os.path.join(BASEMENT_FOLDER, filename)
                shutil.move(input_path, output_path)
                print(f"Moved to basement: {filename}")

            elif location == "chittoor":
                output_path = os.path.join(CHITTOOR_FOLDER, filename)
                shutil.move(input_path, output_path)
                print(f"Moved to chittoor: {filename}")

            elif location == "ranipet":
                output_path = os.path.join(RANIPET_FOLDER, filename)
                shutil.move(input_path, output_path)
                print(f"Moved to ranipet: {filename}")
    
if __name__ == "__main__":
 run()