import numpy as np
import cv2
from PIL import Image
import pytesseract
from pyzbar import pyzbar
import os
import json



"""
    @func qr_bar_code(image_name)
    @desc using pyzbar in exracting Qr/Bar code content [type and code ] from product 
    image and saving it into a json "Data" 
    @param {string} image_name
    @returns {JSON} Data
"""


def qr_bar_code(image_name):
    image = cv2.imread(image_name)
    barcodes = pyzbar.decode(image)
    data = { 'type': None, 'code': None }
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        # (x, y, w, h) = barcode.rect
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        data['type'] = barcodeType
        data['code'] = barcodeData    
    return data

"""
    @func OCR(image_name)
    @desc using pytessract to read letters and words in images and save them into text . 
    @param {string} image_name
    @returns {JSON} text
"""

def OCR(image_name):
    image = cv2.imread(image_name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    #exrtracting text content from images then removing it .
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    if len(text) == 0:
        text = None
    return text




"""
    @func preprocess_image(image_name)
    @desc preprocess_image is an interface fn to [qr_bar_code, OCR] collecting all content needed
    from the product image
    @param {string} image_name
    @returns {JSON}
"""

def preprocess_image(image_name):
    image_data = qr_bar_code(image_name)
    image_ocr = OCR(image_name)
    return { 'ocr': image_ocr, 'code': image_data['code'] }



# json_data = json.load(open('data.json'))
# image_data = readBarOrQrCodes("images/example_01.png")
# image_ocr = OCR("images/example_01.png")
# selectedItem = None
# query = "Select * From items where code={}".format(image_data['code'])
# for item in json_data:
#     if item['code'] == image_data['code']:
#         selectedItem = item
#         break

# print(preprocess_image("images/example_01.png"))
# print('QR Code Result:')
# print(image_data)
# print('OCR Result:')
# print(image_ocr)






