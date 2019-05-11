#!/usr/bin/env python3

"""Test sitemap builder against monzo.com"""

from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import pytest

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


def parse_monzo_com():
    """Parse static HTML that was retrieved from https://monzo.com"""
    parser = UrlHtmlParser()
    with open('tests/test_monzo_com.html', 'rb') as file_handle:
        monzo_com_html = file_handle.read().decode('utf-8')
    parser.parse_html_with_url(monzo_com_html, "https://monzo.com/")
    return parser.temp_urls


def test_parse_monzo_com():
    """Test URL extraction when parsing cached HTML file"""
    with open('tests/test_monzo_com_links.txt', 'r') as file_handle:
        expected_links = [line.strip() for line in file_handle.readlines()]
    assert parse_monzo_com() == set(expected_links)


def test_is_scheme_http_https():
    """Test is_scheme_http_https"""
    assert not is_scheme_http_https('ftps://monzo.com/')
    assert not is_scheme_http_https('ftp://monzo.com/')
    assert not is_scheme_http_https('monzo.com')
    assert is_scheme_http_https('https://monzo.com/')
    assert is_scheme_http_https('http://monzo.com/')


def test_bad_scheme():
    """Test parser against bad schemes (not http or https)"""
    parser = UrlHtmlParser()
    a_ftps_monzo = '''<a href="ftps://monzo.com/up/">some FTP</a>'''
    parser.parse_html_with_url(a_ftps_monzo, "https://monzo.com/")
    with pytest.raises(Exception):
        parser.parse_html_with_url(a_ftps_monzo, "ftps://monzo.com/")


def test_skip_non_http_https():
    """Test that the parser skips http or https links"""
    parser = UrlHtmlParser()
    # Test against fpts:
    a_ftps_monzo = '''<a href="ftps://monzo.com/up/">some FTP</a>'''
    parser.parse_html_with_url(a_ftps_monzo, "https://monzo.com/")
    assert parser.temp_urls == set()
    # Test against mailto:
    a_mailto_monzo = '''<a href="mailto:callme@maybe.com">Call me maybe</a>'''
    parser.parse_html_with_url(a_mailto_monzo, "https://monzo.com/")
    assert parser.temp_urls == set()
    # Test against http:
    a_http_monzo = '''<a href="http://monzo.com">Monzo</a>'''
    parser.parse_html_with_url(a_http_monzo, "https://monzo.com/")
    assert parser.temp_urls == {'http://monzo.com'}
    # Test against https:
    a_https_monzo = '<a href="https://github.com/vietlq/">Viet\'s GitHub</a>'
    parser.parse_html_with_url(a_https_monzo, "https://monzo.com/")
    assert parser.temp_urls == {
        'http://monzo.com',
        'https://github.com/vietlq/'}


def test_no_duplicated_urls():
    """Test that the parser does not produce duplicated URLs"""
    parser = UrlHtmlParser()
    a_http_monzo = '''
    <a style="display: none;" href="https://monzo.com/business">Monzo</a>
    <a id="again" href="https://monzo.com/business">Again</a>
    <a class="perfect" href="https://monzo.com/business">More</a>
    <a href="https://monzo.com/business">Even more</a>
    <a href="https://monzo.com/business">Yeah, one more time</a>
    '''
    parser.parse_html_with_url(a_http_monzo, "https://monzo.com/")
    assert parser.temp_urls == {'https://monzo.com/business'}


if __name__ == '__main__':
    print(parse_monzo_com())
