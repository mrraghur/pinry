import urllib.request, requests
from urllib.parse import urlparse
from PIL import Image
import validators
from cairosvg import svg2png
import imghdr
import pdb

def getDimensions(url):
    check = validators.url(url)
    if check == True:
        try:
            img_data = requests.get(url).content #Download image data and save to output
            errorMessage = [b'Error Fetching Resource',b'Not Found\n',b'Error Fetching Resource\n',b'Cannot proxy the given URL\n']
            if img_data in errorMessage:
                return (0,0)

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
