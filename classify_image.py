try:
    from PIL import Image
except ImportError:
    import Image
import os
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
if os.path.exists(r'S:\IAMGE BACK\Screenshots\Screenshot_2020-01-02-22-28-41-424_com.tinder.jpg'):
    print("File is reachable ")
print(pytesseract.image_to_string(Image.open(r'S:\IAMGE BACK\Screenshots\Screenshot_2020-02-04-15-11-02-661_com.google.android.youtube.jpg')))