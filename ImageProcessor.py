# image_processor.py
import os
import cv2
import pytesseract

# Set the Tesseract command path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\hp\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

class ImageProcessor:

    def process_images(self, files):
        processed_images = []
        for file in files:
            if os.path.isfile(file):
                image = cv2.imread(file)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                processed_image = self.process_image(image)
                processed_images.append(processed_image)
        return processed_images

    def process_image(self, image):
        boxes = pytesseract.image_to_data(image)

        for x, b in enumerate(boxes.splitlines()):
            if x != 0:
                b = b.split()
                if len(b) == 12:
                    x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    cv2.putText(image, b[11], (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (60, 60, 255), 1)

        return image