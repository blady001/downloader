from __future__ import unicode_literals
from lxml import html
import mock
from unittest import TestCase
from models import GitHubLinkScarper


class FakeResponse(object):
        def __init__(self, text):
            self.text = text


class GitHubScarperTest(TestCase):

    def test_segregates_links(self):
        template = """
        <tr class="js-navigation-item">
            <td class="icon">
                <span class="octicon octicon-file-directory"></span>
            </td>
            <td class="content">
                <span>
                    <a href="/link/to/dir">DirLink</a>
                </span>
            </td>
        </tr>
        <tr class="js-navigation-item">
            <td class="icon">
                <span class="octicon octicon-file-text"></span>
            </td>
            <td class="content">
                <span>
                    <a href="/blob/link/to/file.jpg">FileLink</a>
                </span>
            </td>
        </tr>
        <tr class="js-navigation-item">
            <td class="icon">
                <span class="octicon octicon-file-text"></span>
            </td>
            <td class="content">
                <span>
                    <a href="/blob/link/to/file.png">FileLink</a>
                </span>
            </td>
        </tr>
        """
        rows = html.fromstring(template)
        self.assertEqual(len(rows), 3)
        scarper = GitHubLinkScarper('whatever', ('jpg', ))
        data = scarper.segregate_links(rows)
        self.assertEqual(len(data), 2)
        follow_links = data['follow_links']
        download_links = data['download_links']
        self.assertEqual(len(follow_links), 1)
        self.assertEqual(len(download_links), 1)
        self.assertIn('/link/to/dir', follow_links[0])
        self.assertIn('raw', download_links[0])
        self.assertNotIn('blob', download_links[0])
        self.assertIn('link/to/file.jpg', download_links[0])

    @mock.patch('models.requests.get')
    def test_retrieves_single_link_correctly(self, get_meth):
        template = """
        <body>
            <table>
                <tr class="js-navigation-item">
                    <td class="icon">
                        <span class="octicon octicon-file-text"></span>
                    </td>
                    <td class="content">
                        <span>
                            <a href="/blob/link/to/file.jpg">FileLink</a>
                        </span>
                    </td>
                </tr>
            </table>
        </body>
        """
        get_meth.return_value = FakeResponse(template)
        scarper = GitHubLinkScarper('whatever', ('jpg', ))
        results = scarper.collect_links()
        self.assertEqual(len(results), 1)
        link = results[0]
        self.assertIn('raw', link)
        self.assertNotIn('blob', link)

    @mock.patch('models.requests.get')
    def test_retrieves_multiple_link_correctly(self, get_meth):
        template = """
        <body>
            <table>
                <tr class="js-navigation-item">
                    <td class="icon">
                        <span class="octicon octicon-file-text"></span>
                    </td>
                    <td class="content">
                        <span>
                            <a href="/blob/link/to/file1.jpg">FileLink</a>
                        </span>
                    </td>
                </tr>
                <tr class="js-navigation-item">
                    <td class="icon">
                        <span class="octicon octicon-file-text"></span>
                    </td>
                    <td class="content">
                        <span>
                            <a href="/blob/link/to/file2.jpg">FileLink</a>
                        </span>
                    </td>
                </tr>
                <tr class="js-navigation-item">
                    <td class="icon">
                        <span class="octicon octicon-file-text"></span>
                    </td>
                    <td class="content">
                        <span>
                            <a href="/blob/link/to/file3.png">FileLink</a>
                        </span>
                    </td>
                </tr>
            </table>
        </body>
        """
        get_meth.return_value = FakeResponse(template)
        scarper = GitHubLinkScarper('whatever', ('jpg', ))
        results = scarper.collect_links()
        self.assertEqual(len(results), 2)
        files = ['file1.jpg', 'file2.jpg']
        for link in results:
            self.assertIn('raw', link)
            self.assertNotIn('blob', link)
            filename = link.split('/')[-1]
            self.assertIn(filename, files)

    @mock.patch('models.requests.get')
    def test_retrieves_all_files_if_no_specific_types_passed(self, get_meth):
        template = """
        <body>
            <table>
                <tr class="js-navigation-item">
                    <td class="icon">
                        <span class="octicon octicon-file-text"></span>
                    </td>
                    <td class="content">
                        <span>
                            <a href="/blob/link/to/file1.jpg">FileLink</a>
                        </span>
                    </td>
                </tr>
                <tr class="js-navigation-item">
                    <td class="icon">
                        <span class="octicon octicon-file-text"></span>
                    </td>
                    <td class="content">
                        <span>
                            <a href="/blob/link/to/file2.png">FileLink</a>
                        </span>
                    </td>
                </tr>
            </table>
        </body>
        """
        get_meth.return_value = FakeResponse(template)
        scarper = GitHubLinkScarper('whatever')
        results = scarper.collect_links()
        self.assertEqual(len(results), 2)
        files = ['file1.jpg', 'file2.png']
        for link in results:
            self.assertIn('raw', link)
            self.assertNotIn('blob', link)
            filename = link.split('/')[-1]
            self.assertIn(filename, files)
