"""Extract unique URLs from a given HTML content & hinted seed URL"""

from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

ERR_STR_BAD_SCHEME = "Bad scheme. Expected http(s)"


def is_scheme_http_https(url):
    """Return True of the scheme is either http or https"""
    result = urlparse(url.lower())
    return result.scheme in ['http', 'https']


class UrlHtmlParser(HTMLParser):
    """HTML parser that extracts URLs from <A> tags"""

    def __init__(self):
        super().__init__()
        self.temp_urls = set()
        self.url = None

    def parse_html_with_url(self, html_str, url):
        """Parse HTML and URL is given as a hint for building fully
        qualified URLs from hyper-links."""
        if not is_scheme_http_https(url):
            raise Exception(ERR_STR_BAD_SCHEME)
        self.url = url
        super().feed(html_str)

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            for tag_name, tag_val in attrs:
                if tag_name == 'href':
                    new_url = urljoin(self.url, tag_val)
                    if is_scheme_http_https(new_url):
                        self.temp_urls.add(new_url)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def error(self, message):
        raise NotImplementedError(
            "subclasses of UrlHtmlParser must override error()")