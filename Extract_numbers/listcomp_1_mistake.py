"""
Extract phone numbers from screenshot into table
 https://github.com/UB-Mannheim/tesseract/wiki
 pip install tesseract
 pip install pytesseract

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

""" Deletion strings length less 6 symbol"""
list_numbers_1 = [x for x in text.split('\n') if len(x) >= 6]

""" Deleting a date:'+7991 240-17-86 28.10.2022' -> '+7991 240-17-86 '"""
list_numbers_2 = [re.sub(r'\d\d[.]\d\d[.]\d{4}', '', x) for x in list_numbers_1]

""" Removing spaces:'+7991 2401786 ' -> '+79912401786'"""
list_numbers_3 = [x.strip() for x in list_numbers_2]

""" Removing extra points:'+799981322.94' -> '+79998132294'"""
list_numbers_4 = [x.replace('.', '') for x in list_numbers_3]

""" Deletion strings length less 6 symbol """
list_numbers_5 = [x for x in list_numbers_4 if len(x) >= 6]
# 434068- Not a number but passed!!!
phone_numbers = '\n'.join(list_numbers_5)
with open('phone_numbers.xls', 'w') as file:
    file.write(phone_numbers)
with open('phone_numbers.txt', 'w') as file:
    file.write(phone_numbers)