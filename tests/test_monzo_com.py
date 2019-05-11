#!/usr/bin/env python3

"""Test sitemap builder against monzo.com"""

from html.parser import HTMLParser
from urllib.parse import urljoin


class UrlHtmlParser(HTMLParser):
    """HTML parser that extracts URLs from <A> tags"""

    def __init__(self):
        super().__init__()
        self.temp_urls = []
        self.url = None

    def parse_html_with_url(self, html_str, url):
        self.url = url
        super().feed(html_str)

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    temp_url = attr[1]
                    new_url = urljoin(self.url, temp_url)
                    self.temp_urls.append(new_url)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def error(self, message):
        raise NotImplementedError(
            "subclasses of UrlHtmlParser must override error()")


if __name__ == '__main__':
    parser = UrlHtmlParser()
    with open('tests/test_monzo_com.html', 'rb') as fh:
        monzo_com_html = fh.read().decode('utf-8')
    parser.parse_html_with_url(monzo_com_html, "https://monzo.com/")
    print(parser.temp_urls)
