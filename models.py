from __future__ import unicode_literals
from Queue import Queue
from threading import Thread
from lxml import html
import requests
from utils import download_link


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


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            directory, link = self.queue.get()
            download_link(directory, link)
            self.queue.task_done()


class Downloader(object):
    def __init__(self, initial_link, file_types,
                 link_scraper=GitHubLinkScarper):
        self.link_scraper = link_scraper(initial_link, file_types)

    def download(self):
        links = self.link_scraper.collect_links()
        queue = Queue()
        for x in range(2):
            worker = DownloadWorker(queue)
            worker.daemon = True
            worker.start()
        for link in links:
            queue.put(('downloads/', link))
        queue.join()
        print "Done"
