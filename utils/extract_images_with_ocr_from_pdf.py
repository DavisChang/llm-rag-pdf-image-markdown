import pdfplumber
from PIL import Image
import pytesseract
import io


def extract_images_with_ocr(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for image in page.images:
                print("image:", image)
                try:
                    # Extract the image bounding box coordinates
                    x0, y0, x1, y1 = image["x0"], image["y0"], image["x1"], image["y1"]

                    # Crop the image using the bounding box
                    cropped_image = page.within_bbox((x0, y0, x1, y1)).to_image()

                    # Convert the cropped image to bytes
                    img_buffer = io.BytesIO()
                    cropped_image.save(img_buffer, format="PNG")
                    img_bytes = img_buffer.getvalue()

                    # Load the image with PIL
                    image_obj = Image.open(io.BytesIO(img_bytes))

                    # Perform OCR on the image
                    ocr_text = pytesseract.image_to_string(image_obj)
                    print(f"OCR Text on page {page.page_number}: {ocr_text}")

                except Exception as e:
                    print(f"Error processing image on page {page.page_number}: {e}")


# Example usage
pdf_path = "../assets/pdf/monopoly.pdf"
extract_images_with_ocr(pdf_path)
