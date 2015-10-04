from __future__ import unicode_literals
import wget


def download_link(directory, url):
    filename = wget.download(url, out=directory)
    print 'Downloaded: %s' % filename
