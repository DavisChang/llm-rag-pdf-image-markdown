from PIL import Image
import pytesseract

# Load the image
image_path = "../assets/images/TABLE4-3.png"  # Replace with the path to your image file
image = Image.open(image_path)

# Perform OCR to extract text from the image
extracted_text = pytesseract.image_to_string(image)

print("Extracted Text:\n")
print(extracted_text)
