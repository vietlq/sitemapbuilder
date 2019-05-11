#!/usr/bin/env python3

from html.parser import HTMLParser

class UrlHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.temp_urls = []

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        print("The attributes: ", attrs)
        if tag.lower() == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    #print(attr[1])
                    #yield attr[1]
                    self.temp_urls.append(attr[1])

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

parser = UrlHtmlParser()
with open('tests/test_monzo_com.html', 'rb') as fh:
    monzo_com_html = fh.read().decode('utf-8')
parser.feed(monzo_com_html)
print(parser.temp_urls)
