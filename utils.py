import os
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/75.0.3770.142 '
    'Safari/537.36'
}


def is_image(url):
    try:
        r = requests.get(url, headers)
    except requests.RequestException:
        return False
    if r.status_code == requests.codes.ok:
        # return r.headers['content-type'] in ['image/jpeg', 'image/png']
        return r.headers['content-type'] in ['image/jpeg']
    return False


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_cover_img(url):
    soup = bs(requests.get(url).content, "html.parser")
    flag = False
    for img in soup.find_all("img"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        # if img_url is not short link, it will return img_url
        img_url = urljoin(url, img_url)
        if is_image(img_url):
            flag = True
            return img_url
    if flag == False:
        return 'https://miro.medium.com/max/3928/1*IPV5Wx-BoK1hpUKRrB-nlQ.png'