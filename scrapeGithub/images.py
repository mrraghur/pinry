from typing import Mapping
from urllib import response
import requests
from PIL import Image
import validators
from cairosvg import svg2png
import pdb
from PIL import Image as PILImage
import requests, cv2
from urllib.error import HTTPError

def getDimensions(url):
    check = validators.url(url)
    if check == True:
        try:
            img_data = requests.get(url).content #Download image data and save to output
            errorMessage = [b'Error Fetching Resource',b'Not Found\n',b'Error Fetching Resource\n',b'Cannot proxy the given URL\n']
            if img_data in errorMessage:
                return

            with open('output', 'wb') as handler:
                handler.write(img_data)
                handler.close()

            if b'<svg' in img_data:
                imageType = 'svg'
                svg2png(bytestring=img_data,write_to='output')
                # Convert svg to png

            dims = Image.open('output').size
            return dims

        except Exception as e:
            pdb.set_trace()

def checkIsLogo(url,model):
    check = validators.url(url)
    if check == True:
        try:
            errorMessage = [b'Error Fetching Resource',
            b'Not Found\n',
            b'Error Fetching Resource\n',
            b'Cannot proxy the given URL\n',
            b'Invalid upstream response (429)\n'
            ]
            response = requests.get(url)
            img_data = response.content #Download image data and save to output
            if img_data in errorMessage:
                raise HTTPError(response.url,response.status_code,response.content,response.headers,None)

            path = '/tmp/output'
            if img_data[:4] == b'<svg' or img_data[:5] == b'<?xml':
                svg2png(bytestring=img_data,write_to=path)
            elif img_data[:3] == b'GIF':
                return 'screenshot'
            else:
                tempImage = open(path,'wb')
                tempImage.write(img_data)
                tempImage.close()
            image = cv2.imread(path)

            img_height,img_width = 224,224
            resized_image = cv2.resize(image, (img_height,img_width)).reshape(1,img_height,img_width,3)

            y = model.predict(resized_image)
            if y[0][0] > 0.5:
                return 0
            return 1

        except Exception as e:
            pdb.set_trace()
