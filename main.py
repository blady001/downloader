from __future__ import unicode_literals
from models import Downloader

if __name__ == '__main__':
    print 'GitHub File Downloader 0.1'
    link = raw_input('Pass link to download: ')
    file_types = raw_input('\nPass type of files to download: '
                          '(use semicolon as separator e.g. "jpg;txt"): ')
    file_types = file_types.split(';')
    downloader = Downloader(link, file_types)
    downloader.download()
