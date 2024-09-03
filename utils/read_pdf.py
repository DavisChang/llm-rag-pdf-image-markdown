# python3.9 readPDF.py

import pdfplumber
import io
from PIL import Image
import pytesseract


def extract_content_from_pdf(pdf_path):
    text_content = ""
    table_content = ""
    image_text_content = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text
            text = page.extract_text()
            if text:
                text_content += text + "\n"

            # Extract tables
            tables = page.extract_tables()
            if tables:
                for i, table in enumerate(tables):
                    table_content += f"Table {i+1} on page {page.page_number}:\n"
                    for row in table:
                        table_content += (
                            " | ".join(str(cell) if cell else "" for cell in row) + "\n"
                        )
                    table_content += "\n"

            # Extract images and perform OCR
            if page.images:
                for image in page.images:
                    try:
                        # Extract image bytes from the PDF using bbox
                        x0, y0, x1, y1 = (
                            image["x0"],
                            image["y0"],
                            image["x1"],
                            image["y1"],
                        )
                        cropped_image = page.within_bbox((x0, y0, x1, y1)).to_image()

                        # Convert the cropped image to PIL Image
                        img_bytes = cropped_image.original
                        im = Image.open(io.BytesIO(img_bytes))

                        # Perform OCR on the image
                        image_text = pytesseract.image_to_string(im)
                        image_text_content += (
                            f"Image on page {page.page_number}: {image_text}\n"
                        )
                    except Exception as e:
                        print(f"Error processing image on page {page.page_number}: {e}")

    return text_content, table_content, image_text_content


# Example usage
pdf_path = "../assets/pdf/monopoly.pdf"
text_content, table_content, image_text_content = extract_content_from_pdf(pdf_path)

print("Extracted text content:")
print(text_content)

print("\nExtracted table content:")
print(table_content)

print("\nExtracted text from images:")
print(image_text_content)
