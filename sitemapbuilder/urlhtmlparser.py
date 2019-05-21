"""Extract unique URLs from a given HTML content & hinted seed URL"""

import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

ERR_STR_BAD_SCHEME = "Bad scheme. Expected http(s)"
ERR_STR_UNSUPPORTED_CHARSET = \
    "Unsupported charset. Accepting only US-ASCII and UTF-8"
CONTENT_TYPE_RE_PAT = re.compile(r'^(text/html); charset=(.*)$')


def is_scheme_http_https(url):
    """Return True of the scheme is either http or https"""
    result = urlparse(url.lower())
    return result.scheme in ['http', 'https']


def is_charset_supported(charset):
    """Check if the charset is supported"""
    return charset.upper() in ['US-ASCII', 'UTF-8']


def split_content_type(content_type_str):
    """Split Content-Type string"""
    result = CONTENT_TYPE_RE_PAT.match(content_type_str)
    if result:
        return 'text/html', result.groups()[1]
    return None, None


def is_content_type_supported(content_type_str):
    """Validate Content-Type string"""
    content_type, charset = split_content_type(content_type_str)
    return content_type and charset \
        and (content_type == 'text/html') \
        and is_charset_supported(charset)


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
        return self.temp_urls

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            for tag_name, tag_val in attrs:
                if tag_name == 'href':
                    # Convert relative URL to absolute
                    new_url = urljoin(self.url, tag_val)
                    # NOTE: We do not handle fragments!!
                    new_url = new_url.split('#')[0]
                    if is_scheme_http_https(new_url):
                        self.temp_urls.add(new_url)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def error(self, message):
        raise NotImplementedError(
            "subclasses of UrlHtmlParser must override error()")
