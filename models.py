from __future__ import unicode_literals
from lxml import html
import requests


class GitHubLinkScarper(object):
    DOMAIN_BASE = 'https://github.com'
    ROW_TEMPLATE = '//tr[@class="js-navigation-item"]'
    DIR_CLASS = 'octicon octicon-file-directory'
    FILE_CLASS = 'octicon octicon-file-text'

    def __init__(self, initial_link, file_types):
        self.initial_link = initial_link
        self.file_types = file_types
        self.download_links = list()

    def collect_links(self):
        self.fill_download_links()
        return self.download_links

    def fill_download_links(self, link=None):
        link = link if link else self.initial_link
        page = requests.get(link)
        tree = html.fromstring(page.text)
        rows = tree.xpath(self.ROW_TEMPLATE)
        if rows:
            data = self.segregate_links(rows)
            self.download_links += data['download_links']
            if data['follow_links']:
                for l in data['follow_links']:
                    self.fill_download_links(link=l)

    def segregate_links(self, rows):
        data = {'follow_links': list(), 'download_links': list()}
        for row in rows:
            class_ = row[0][0].get('class')
            if class_ == self.DIR_CLASS:
                link = row[1][0][0].get('href')
                link = self.DOMAIN_BASE + link
                data['follow_links'].append(link)
            elif class_ == self.FILE_CLASS:
                link = row[1][0][0].get('href')
                parts = link.split('/')
                last = parts[-1].split('.')[-1]
                if last in self.file_types:
                    link = link.replace('blob', 'raw')
                    link = self.DOMAIN_BASE + link
                    data['download_links'].append(link)
        return data


class Downloader(object):

    def __init__(self, initial_link, file_type, link_scraper=GitHubLinkScarper):
        self.file_type = file_type
        self.link_scraper = link_scraper(initial_link)

    def download(self):
        links = self.link_scraper.collect_links()

