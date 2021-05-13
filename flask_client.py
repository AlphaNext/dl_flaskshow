from __future__ import print_function
import requests
import json
import cv2
import sys

# addr example
addr = 'http://10.123.123.123:1001'   # need to replace your addr
test_url = addr + '/api/test'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type, 'Connection': 'close'}

#img = cv2.imread('lena.jpg')
img = cv2.imread(sys.argv[1])

# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)

# send http request with image and receive response
response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)

# decode response
print(json.loads(response.text))
