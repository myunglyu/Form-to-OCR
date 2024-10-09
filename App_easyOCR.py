import easyocr
import cv2

# Load the image
image_path = 'test4.jpg'
image = cv2.imread(image_path)

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Perform OCR on the image
results = reader.readtext(image)

# extract text from the OCR
extracted_text = [text for (_, text, _) in results]
full_text = ' '.join(extracted_text)

# Output text
print(full_text)