from __future__ import unicode_literals
from models import Downloader

if __name__ == '__main__':
    print 'GitHub File Downloader 0.2'
    print "Please make sure that directory 'downloads' exists in a script's " \
          "directory"
    link = raw_input('Pass link to download: ')
    file_types = raw_input(
        '\nPass type of files to download (e.g. jpg;txt) or leave blank for '
        'any type: ')
    if file_types:
        file_types = file_types.split(';')
    else:
        file_types = list()
    downloader = Downloader(link, file_types)
    downloader.download()
    print '\nFinished downloading'
