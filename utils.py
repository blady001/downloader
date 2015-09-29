from __future__ import unicode_literals
import requests
import shutil


# TODO: Cannot save text file, only images for now
def download_link(directory, link):
    resp = requests.get(link, stream=True)
    filename = link.split('/')[-1]
    path = directory + filename
    with open(path, 'wb') as f:
        shutil.copyfileobj(resp.raw, f)
    del resp
