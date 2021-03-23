'''
This code finds the similarity in text of different images. It calls upon 
an API provided by OCRSpace. Reads in four images (Original, and three
segmented images) and prints out their similarity to the original to 
the console. 

All code written is my own with the exception of the 'ocr_space_file' 
function which was taken from the second link. The first link directs
you to the OCRSpace's API page that allows you to signup and generate 
a key to use their API. 

1. https://ocr.space/OCRAPI
2. https://github.com/Zaargh/ocr.space_code_example/blob/master/ocrspace_example.py
'''

import requests
from difflib import SequenceMatcher

def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
  # Payload being sent to the API
  payload = {'isOverlayRequired': overlay,
              'apikey': api_key,
              'language': language,
              }
  with open(filename, 'rb') as f:
    # Sends post request with payload
    r = requests.post('https://api.ocr.space/parse/image',
                      files={filename: f},
                      data=payload,
                      )
  return r.json()

# Calls function to send post request given a filename and key
# Will return index out of range error if post request receives
# an error message. 
def getText(filename, key):
  jsonString = ocr_space_file(filename, False, key, 'eng')
  imageText = jsonString['ParsedResults'][0]['ParsedText']
  # Uncomment this to print to console output OCR result for image. 
  # print(imageText)
  return imageText

# Compares similarity of two texts using built in tool
def calculateSimilarity(text1, text2):
  return SequenceMatcher(None, text1, text2).ratio()*100

if __name__ == '__main__':
  # Personal key generated to send requests using api
  key = "f8711309b188957"
  # Image Filenames
  filenameOriginal = "../Images/Original/text_1.png"
  filenameNiblack = "../Images/Niblack/text_1.tif"
  filenamePhansalkar = "../Images/Phansalkar/text_1.tif"
  filenameSauvola = "../Images/Sauvola/text_1.tif"

  # This gets the text from the orginal image  
  originalImageText = getText(filenameOriginal, key)
  # Niblack Image:
  niblackImageText = getText(filenameNiblack, key)
  # Phansalkar Image:
  phansalkarImageText = getText(filenamePhansalkar, key)
  # Sauvola Image:
  sauvolaImageText = getText(filenameSauvola, key)

  # Compute similarity percentage of original image to segmented image
  niblackMetric = calculateSimilarity(originalImageText, niblackImageText)
  phansalkarMetric = calculateSimilarity(originalImageText, phansalkarImageText)
  sauvolaMetric = calculateSimilarity(originalImageText, sauvolaImageText)

  print("Text similarity compared to Original Image:\n")
  print("Niblack: ", niblackMetric)
  print("Phansalkar: ", phansalkarMetric)
  print("Sauvola: ", sauvolaMetric)