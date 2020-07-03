"""
####################################################
# poster_downloader.py:
# simple script to download images and resize them
####################################################
"""
import os
import sys
import json
import time
import urllib.request
from PIL import Image

# posters_downloader.py home directory
dirname = os.path.dirname(__file__)
# Movies and Tv shows info
data_dict = {}
try:
    """try read info from file if present"""
    with open(os.path.join(dirname, 'trailers.json')) as f_obj:
            data_dict = json.load(f_obj)
except FileNotFoundError:
    pass


def download(path, url):
    """download image to specified file path from url"""
    if os.path.exists(path):        # if image not present locally
        return
    while True:
        try:
            """download image consecutively if connection keeps failing"""
            data = urllib.request.urlretrieve(url, path)
        except ConnectionResetError:
            time.sleep(1)
        except ConnectionError:
            print(sys.exc_info()[0], sys.exc_info()[1])
            return
        else:
            break
    image = Image.open(path)                            # open image
    image = image.resize((300, 450), Image.ANTIALIAS)   # resize image
    image.save(path)                                    # save image


def downloader(data_dict=data_dict):
    """Get url from data_dict and download image"""
    posters_dir = os.path.join(dirname, 'posters')
    try:
        """Check for posters dir; check if posters too large"""
        if len(os.listdir(posters_dir)) >= 500:
            os.rmdir(posters_dir)       # remove posters dir
            os.makedirs(posters_dir)    # recreate posters dir
    except FileNotFoundError:
        os.makedirs(posters_dir)        # recreate posters dir

    try:
        singles = [single               # movie or Tv show's details
                   for mtv in data_dict.values()
                   for genre in mtv.values() 
                   for single in genre]
    except AttributeError:
        return

    threads = []
    for single in singles:
        url = single['poster']          # poster url
        path = os.path.join(posters_dir, url.split('/')[-1])
        download(path, url)

if __name__ == '__main__':
    downloader()
