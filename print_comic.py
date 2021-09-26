from bs4 import BeautifulSoup
from PIL import Image
from datetime import datetime as dt
import random
import string
import requests
from io import BytesIO
import escpos.printer
import math


def print_comic(img, temp_img_filename="temp.png"):
    # connect to printer
    printer = escpos.printer.Usb(0x0416, 0x5011, in_ep=0x81)
    printer.hw("RESET")

    maxwidth = 370.0

    # rotate image to better fit paper
    if img.size[0] > img.size[1]:
        img = img.rotate(270, expand=True)

    length = img.size[1]
    width = img.size[0]
    ratio = maxwidth / width

    new_length = math.floor(ratio * length)
    new_width = math.floor(ratio * width)

    new_size = int(new_width), int(new_length)

    img = img.resize(new_size)
    img.save(temp_img_filename)
    printer.image(temp_img_filename)

    # feed some space
    printer._raw(('\n').encode('UTF8'))
    printer._raw(('\n').encode('UTF8'))
    printer._raw(('\n').encode('UTF8'))


def get_comic_image(name_of_comic, date=""):
    comic_image_url = None

    # get img link depending on comic and date chosen
    if name_of_comic is 'xkcd':
        comic_image_url = get_xkcd_comic_link(date)
    elif name_of_comic is 'dilbert':
        comic_image_url = get_dilbert_comic_link(date)
    elif name_of_comic is 'calvin':
        comic_image_url = get_calvin_comic_link(date)
    elif name_of_comic is 'peanuts':
        comic_image_url = get_peanuts_comic_link(date)
    elif name_of_comic is 'overboard':
        comic_image_url = get_overboard_comic_link(date)
    elif name_of_comic is 'garfield':
        comic_image_url = get_garfield_comic_link(date)

    # get image data
    response = requests.get(comic_image_url)
    comic_image = Image.open(BytesIO(response.content))

    return comic_image.convert('RGB')


def get_xkcd_comic_link(date):
    if date is 'random':
        url = 'https://c.xkcd.com/random/comic/'
    else:
        url = 'https://xkcd.com/'

    # get img link from website
    r = requests.get(url)
    data = r.text
    site_soup = BeautifulSoup(data, "html5lib")
    div_soup = site_soup.find("div", {"id": "comic"})
    img_link = div_soup.find('img').get("src")

    return 'https:' + img_link


def get_dilbert_comic_link(date):
    if date is 'random':
        url = f'https://dilbert.com/search_results?terms={random.choice(string.ascii_letters)}'
    else:
        url = 'https://dilbert.com/'

    # get img link from website
    r = requests.get(url)
    data = r.text
    site_soup = BeautifulSoup(data, "html5lib")
    div_soup = site_soup.find("a", {"class": "img-comic-link"})
    img_link = div_soup.find('img').get("src")

    return img_link


def get_calvin_comic_link(date):
    if date is 'random':
        url = 'https://www.gocomics.com/random/calvinandhobbes'
    else:
        url = f'https://www.gocomics.com/calvinandhobbes/{dt.today().strftime("%Y/%m/%d")}'

    # get img link from website
    r = requests.get(url)
    data = r.text
    site_soup = BeautifulSoup(data, "html5lib")
    div_soup = site_soup.find("div", {"class": "comic__container"})
    picture_soup = div_soup.find('picture', {"class": "item-comic-image"})
    img_link = picture_soup.find('img', {"class": "lazyload img-fluid"}).get("src")

    return img_link


def get_peanuts_comic_link(date):
    if date is 'random':
        url = 'https://www.gocomics.com/random/peanuts'
    else:
        url = f'https://www.gocomics.com/peanuts/{dt.today().strftime("%Y/%m/%d")}'

    # get img link from website
    r = requests.get(url)
    data = r.text
    site_soup = BeautifulSoup(data, "html5lib")
    div_soup = site_soup.find("div", {"class": "comic__container"})
    picture_soup = div_soup.find('picture', {"class": "item-comic-image"})
    img_link = picture_soup.find('img', {"class": "lazyload img-fluid"}).get("src")

    return img_link


def get_overboard_comic_link(date):
    if date is 'random':
        url = 'https://www.gocomics.com/random/overboard'
    else:
        url = f'https://www.gocomics.com/overboard/{dt.today().strftime("%Y/%m/%d")}'

    # get img link from website
    r = requests.get(url)
    data = r.text
    site_soup = BeautifulSoup(data, "html5lib")
    div_soup = site_soup.find("div", {"class": "comic__container"})
    picture_soup = div_soup.find('picture', {"class": "item-comic-image"})
    img_link = picture_soup.find('img', {"class": "lazyload img-fluid"}).get("src")

    return img_link

def get_garfield_comic_link(date):
    if date is 'random':
        url = 'https://www.gocomics.com/random/garfield'
    else:
        url = f'https://www.gocomics.com/garfield/{dt.today().strftime("%Y/%m/%d")}'

    # get img link from website
    r = requests.get(url)
    data = r.text
    site_soup = BeautifulSoup(data, "html5lib")
    div_soup = site_soup.find("div", {"class": "comic__container"})
    picture_soup = div_soup.find('picture', {"class": "item-comic-image"})
    img_link = picture_soup.find('img', {"class": "lazyload img-fluid"}).get("src")

    return img_link
