from bs4 import BeautifulSoup
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import escpos.printer

def print_comic(name_of_comic, date='today'):
    img = get_comic_image(name_of_comic, date)
    # TODO resize images to fit?
    img.save('temp.png')
    printer = escpos.printer.Usb('todo')
    printer.text("Hello World\n")

def get_comic_image(name_of_comic, date):
    comic_image_url = None

    # get img link depending on comic and date chosen
    if name_of_comic is 'xkcd':
        comic_image_url = get_xkcd_comic_link(date)

    # get image data
    response = requests.get('http:' + comic_image_url)
    comic_image = Image.open(BytesIO(response.content))

    return comic_image

def get_xkcd_comic_link(date):
    base_url = 'https://xkcd.com/'

    if date is 'today':
        url = base_url
    else:
        #TODO implement getting different day
        url = base_url

    # get img link from website
    r = requests.get(url)
    data = r.text
    site_soup = BeautifulSoup(data, "lxml")
    div_soup = site_soup.find("div", {"id": "comic"})
    img_link = div_soup.find('img').get("src")

    return img_link