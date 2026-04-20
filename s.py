# get coordinates for adress lines, compare to past, then split based of that, should be done after naming though.
import os
import re
from pypdf import PdfReader

INPUT_FOLDER = "output"


def clean_filename(text):
    return re.sub(r'[<>:"/\\|?*]', '', text).strip()

Store =  "PERIPHERAL PHARMACY STORE"


def extract_data(file_path):
    Ad_X_MIN, Ad_X_MAX = 320.00, 620
  
    Address = None

    reader = PdfReader(file_path)

    for page in reader.pages:

        def visitor(text, cm, tm, font_dict, font_size):
            nonlocal Address

            x = tm[4]
            y = tm[5]
            text = text.strip()

            if not text:
                return


        page.extract_text(visitor_text=visitor)

    print(Address)
    return Address
    


