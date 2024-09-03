import pdfplumber
import pytesseract
from PIL import Image
import io


def extract_text_and_images(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            print(f"--- Page {page_num + 1} ---")

            # get text
            text = page.extract_text()
            if text:
                print("Extracted text:")
                print(text)
            else:
                print("No text extracted directly.")

            # OCR
            images = page.images
            for i, img in enumerate(images):
                print(f"Image {i + 1}:")
                image = Image.open(io.BytesIO(img["stream"].get_data()))
                ocr_text = pytesseract.image_to_string(image)
                print(ocr_text)

            if not text and not images:
                print("No text or images found on this page.")


pdf_path = "../assets/pdf/monopoly.pdf"
extract_text_and_images(pdf_path)
