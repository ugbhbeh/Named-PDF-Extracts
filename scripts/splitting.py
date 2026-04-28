from pypdf import PdfReader, PdfWriter
import os

input_dir = "../input"
output_dir = "../generated/split&named"

os.makedirs(output_dir, exist_ok=True)


for filename in os.listdir(input_dir):
    if filename.lower().endswith(".pdf"):

        input_path = os.path.join(input_dir, filename)
        reader = PdfReader(input_path)

        base_name = os.path.splitext(filename)[0]

        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)

            output_path = os.path.join(
                output_dir,
                f"{base_name}_page_{i + 1}.pdf"
            )

            with open(output_path, "wb") as f:
                writer.write(f)

        print(f"Split: {filename}")