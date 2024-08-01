import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_config = r'--psm 6 digits'


def get_number_from_image(img):
    img = Image.open(img)
    number = pytesseract.image_to_string(
        img, config=custom_config).strip()
    return int(number) if number else 0


if __name__ == '__main__':
    print(get_number_from_image('roi_14.jpg'))
