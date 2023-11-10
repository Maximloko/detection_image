"""
Extract phone numbers from screenshot into table
 https://github.com/UB-Mannheim/tesseract/wiki
 pip install tesseract
 pip install pytesseract
phone numbers: '\+7\d{10}', '\+9\d{11}', '3\d{5}'

 """
import pytesseract
from PIL import Image
import re

# path to tesseract.exe - Necessarily!
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
img = Image.open('Screenshot.jpg')
custom_config = r'digits --oem 1 --psm 7 -c tessedit_char_whitelist=+.0123456789'

""" Detection only digits and dot """
text = pytesseract.image_to_string(img, config=custom_config)
with open('raw recognition.txt', 'w') as file:
    file.write(text)
""" The date “3х.хх.хххх” begins with “3”, so we delete the dates:'+7991 240-17-86 30.09.2022' ->'+7991 240-17-86 ' '"""
without_dates = re.sub(r'\d\d[.]\d\d[.]\d{4}', '', text)

""" Removing extra points:'+799981322.94' -> '+79998132294'"""
without_extra_points = without_dates.replace('.', '')


def recognize_with_listcomp(without_extra_points: str):
    """
    434068, +799162322802, +792517367692, +799440481690, 72250917- Not a number but passed!!!
    195 numbers found.
    Removing spaces:'+79912401786 ' -> '+79912401786'"""
    without_extra_spaces = [line.strip() for line in without_extra_points.split('\n')]

    """ Deletion strings length less 6 symbol """
    set_numbers = {line for line in without_extra_spaces if len(line) >= 6}
    phone_numbers = '\n'.join(set_numbers)
    with open('phone_numbers_listcomp.xls', 'w') as f:
        f.write(phone_numbers)
    with open('phone_numbers_listcomp.txt', 'w') as f:
        f.write(phone_numbers)


def recognize_with_regex(without_extra_points: str):
    """
    189 numbers found.
    Errors are possible with short numbers if the line starts with "3"
    For this function, it was possible not to recognize the points and, accordingly, not to delete the dates.
    """

    all_numbers = re.findall(r'\+7\d{10}|\+9\d{11}|\n3\d{5}', without_extra_points)
    no_duplicates = set(all_numbers)
    with_extra_new_line = '\n'.join(no_duplicates)
    phone_numbers_regex = with_extra_new_line.replace('\n\n', '\n')
    with open('phone_numbers_regex.txt', 'w') as f:
        f.write(phone_numbers_regex)
    with open('phone_numbers_regex.xls', 'w') as f:
        f.write(phone_numbers_regex)


if __name__ == '__main__':
    recognize_with_listcomp(without_extra_points)
    recognize_with_regex(without_extra_points)
