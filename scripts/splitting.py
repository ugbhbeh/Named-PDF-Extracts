from pypdf import PdfReader, PdfWriter
import os

input_pdf = "../input/input.pdf"
output_dir = "../generated/split&named"

os.makedirs(output_dir, exist_ok=True)

reader = PdfReader(input_pdf)

for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)

    output_path = os.path.join(output_dir, f"page_{i + 1}.pdf")

    with open(output_path, "wb") as f:
        writer.write(f)