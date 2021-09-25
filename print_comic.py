from bs4 import BeautifulSoup
from PIL import Image
import requests
from io import BytesIO
import escpos.printer
import math


def print_comic(name_of_comic, date='today'):
    # connect to printer
    printer = escpos.printer.Usb(0x0416, 0x5011, in_ep=0x81)
    printer.hw("RESET")

    # get comic image
    temp_img_filename = "temp.png"
    img = get_comic_image(name_of_comic, date)

    maxwidth = 380.0
    maxlength = 200

    # format image
    if (img.size[0] / img.size[1]) > 1.5:
        img = img.rotate(270, expand=True)

    length = img.size[1]
    width = img.size[0]
    ratio = maxwidth / width

    new_length = math.floor(ratio * length)
    new_width = math.floor(ratio * width)

    new_size = int(new_width), int(new_length)

    img = img.resize(new_size)
    img.save(temp_img_filename)
    # print image in slices
    num_of_slices = int(math.floor(img.size[1] / maxlength))
    for i in range(num_of_slices):
        x = i * maxlength
        y = (i + 1) * maxlength
        temp_img = img.crop((0, x, img.size[0], y))
        temp_img.save(temp_img_filename)
        printer.image(temp_img_filename)

    # feed some space
    printer._raw(('\n').encode('UTF8'))
    printer._raw(('\n').encode('UTF8'))
    printer._raw(('\n').encode('UTF8'))


def get_comic_image(name_of_comic, date):
    comic_image_url = None

    # get img link depending on comic and date chosen
    if name_of_comic is 'xkcd':
        comic_image_url = get_xkcd_comic_link(date)
    elif name_of_comic is 'dilbert':
        comic_image_url = get_dilbert_comic_link(date)
    elif name_of_comic is 'cyanide':
        comic_image_url = get_cyanide_comic_link(date)
    elif name_of_comic is 'calvin':
        comic_image_url = get_calvin_comic_link(date)
    elif name_of_comic is 'overboard':
        comic_image_url = get_overboard_comic_link(date)

    # get image data
    response = requests.get(comic_image_url)
    comic_image = Image.open(BytesIO(response.content))

    return comic_image.convert('RGB')


def get_xkcd_comic_link(date):
    base_url = 'https://xkcd.com/'

    if date is 'random':
        url = 'https://c.xkcd.com/random/comic/'
    else:
        url = base_url

    # get img link from website
    r = requests.get(url)
    data = r.text
    site_soup = BeautifulSoup(data, "html5lib")
    div_soup = site_soup.find("div", {"id": "comic"})
    img_link = div_soup.find('img').get("src")

    return 'https:' + img_link


def get_dilbert_comic_link(date):
    base_url = 'https://dilbert.com/'

    if date is 'random':
        url = 'https://dilbert.com/search_results?terms=Random'
    else:
        url = base_url

    # get img link from website
    r = requests.get(url)
    data = r.text
    site_soup = BeautifulSoup(data, "html5lib")
    div_soup = site_soup.find("a", {"class": "img-comic-link"})
    img_link = div_soup.find('img').get("src")
    # print img_link

    if date is 'random':
        return img_link
    else:
        return 'https:' + img_link


def get_cyanide_comic_link(date):
    base_url = 'https://explosm.net/comics/latest'

    if date is 'random':
        url = 'https://explosm.net/comics/random'
    else:
        url = base_url

    # get img link from website
    r = requests.get(url)
    data = r.text
    site_soup = BeautifulSoup(data, "html5lib")
    img_link = site_soup.find('img', {"id": "main-comic"}).get("src")
    # print img_link

    return 'https:' + img_link


def get_calvin_comic_link(date):
    base_url = 'https://www.gocomics.com/calvinandhobbes'

    if date is 'random':
        url = 'https://www.gocomics.com/random/calvinandhobbes'
    else:
        url = base_url

    # get img link from website
    r = requests.get(url)
    data = r.text
    site_soup = BeautifulSoup(data, "html5lib")
    div_soup = site_soup.find("div", {"class": "card"})
    img_link = div_soup.find('img', {"class": "img-fluid"}).get("src")
    # print img_link

    return 'https:' + img_link


def get_overboard_comic_link(date):
    base_url = 'https://www.gocomics.com/overboard'

    if date is 'random':
        url = 'https://www.gocomics.com/random/overboard'
    else:
        url = base_url

    # get img link from website
    r = requests.get(url)
    data = r.text
    site_soup = BeautifulSoup(data, "html5lib")
    div_soup = site_soup.find("div", {"class": "card"})
    img_link = div_soup.find('img', {"class": "img-fluid"}).get("src")
    # print img_link

    return 'https:' + img_link
