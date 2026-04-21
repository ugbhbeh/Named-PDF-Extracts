from pypdf import PdfReader

reader = PdfReader("input/input.pdf")

for page_num, page in enumerate(reader.pages):
    print(f"\n--- PAGE {page_num + 1} ---")

    def visitor(text, cm, tm, font_dict, font_size):
        x = tm[4]
        y = tm[5]
        text = text.strip()

        if text:  
            print(f"({x:.2f}, {y:.2f}) -> {text}")

    page.extract_text(visitor_text=visitor)