import fitz  # PyMuPDF
from PIL import Image
import io
import tiktoken


def calculate_pdf_metrics(pdf_path):
    # use encoding compatible with GPT-3.5-turbo.
    encoding = tiktoken.get_encoding("cl100k_base")
    total_tokens = 0
    total_image_pixels = 0

    # open PDF file
    doc = fitz.open(pdf_path)

    for page in doc:
        # get text
        text = page.get_text()
        total_tokens += len(encoding.encode(text))  # token

        # get page image
        images = page.get_images(full=True)
        for img in images:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_data = base_image["image"]

            # use PIL
            image = Image.open(io.BytesIO(image_data))
            width, height = image.size
            total_image_pixels += width * height

    return total_tokens, total_image_pixels


pdfs = [
    "../assets/pdf/monopoly.pdf",
]

# example
total_tokens = 0
total_pixels = 0
for pdf_path in pdfs:
    tokens, image_pixels = calculate_pdf_metrics(pdf_path)
    total_tokens += tokens
    total_pixels += image_pixels
    print(f"PDF: {pdf_path}")
    print(f"file Tokens: {tokens}")
    print(f"file Image Pixels: {image_pixels}")

print(f"Total Tokens: {total_tokens}")
print(f"Total Image Pixels: {total_pixels}")
