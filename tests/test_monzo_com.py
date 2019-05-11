#!/usr/bin/env python3

"""Test sitemap builder against monzo.com"""

from html.parser import HTMLParser

#TODO: Use current location + <A:href> to get fully qualified URLs


class UrlHtmlParser(HTMLParser):
    """HTML parser that extracts URLs from <A> tags"""

    def __init__(self):
        super().__init__()
        self.temp_urls = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.temp_urls.append(attr[1])

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
    parser.feed(monzo_com_html)
    print(parser.temp_urls)
