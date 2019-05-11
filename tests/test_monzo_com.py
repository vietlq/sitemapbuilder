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
        self.temp_urls = []
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
                        self.temp_urls.append(new_url)

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
    with open('tests/test_monzo_com.html', 'rb') as fh:
        monzo_com_html = fh.read().decode('utf-8')
    parser.parse_html_with_url(monzo_com_html, "https://monzo.com/")
    return parser.temp_urls


def test_parse_monzo_com():
    """Test URL extraction when parsing cached HTML file"""
    assert(parse_monzo_com() == ['https://monzo.com/', 'https://monzo.com/about', 'https://monzo.com/blog', 'https://monzo.com/community', 'https://monzo.com/help', 'https://monzo.com/download', 'https://monzo.com/business', 'https://app.adjust.com/ydi27sn?engagement_type=fallback_click', 'https://app.adjust.com/9mq4ox7?engagement_type=fallback_click', 'https://www.theguardian.com/technology/2017/dec/17/monzo-facebook-of-banking', 'https://www.telegraph.co.uk/personal-banking/current-accounts/monzo-atom-revolut-starling-everything-need-know-digital-banks/', 'https://www.thetimes.co.uk/article/tom-blomfield-the-man-who-made-monzo-g8z59dr8n', 'https://www.standard.co.uk/tech/monzo-prepaid-card-current-accounts-challenger-bank-a3805761.html', 'https://monzo.com/features/apple-pay', 'https://monzo.com/features/google-pay', 'https://monzo.com/features/travel', 'https://www.fscs.org.uk/', 'https://monzo.com/features/switch', 'https://monzo.com/features/overdrafts', 'https://app.adjust.com/ydi27sn?engagement_type=fallback_click', 'https://app.adjust.com/9mq4ox7?engagement_type=fallback_click', 'https://monzo.com/cdn-cgi/l/email-protection#e8808d8498a88587869287c68b8785', 'https://monzo.com/community', 'https://app.adjust.com/ydi27sn?engagement_type=fallback_click', 'https://app.adjust.com/9mq4ox7?engagement_type=fallback_click', 'https://monzo.com/about', 'https://monzo.com/blog', 'https://monzo.com/press', 'https://monzo.com/careers', 'https://web.monzo.com', 'https://monzo.com/community', 'https://monzo.com/community/making-monzo', 'https://monzo.com/transparency', 'https://monzo.com/blog/how-money-works', 'https://monzo.com/tone-of-voice', 'https://monzo.com/business', 'https://monzo.com/faq', 'https://monzo.com/legal/terms-and-conditions', 'https://monzo.com/legal/fscs-information', 'https://monzo.com/legal/privacy-policy', 'https://monzo.com/legal/cookie-policy', 'https://monzo.com/information-about-current-account-services', 'https://app.adjust.com/ydi27sn?engagement_type=fallback_click', 'https://app.adjust.com/9mq4ox7?engagement_type=fallback_click', 'https://twitter.com/monzo', 'https://www.instagram.com/monzo', 'https://www.facebook.com/monzobank', 'https://www.linkedin.com/company/monzo-bank', 'https://www.youtube.com/monzobank', 'https://monzo.com/cdn-cgi/l/email-protection#c6aea3aab686aba9a8bca9e8a5a9ab'])


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


if __name__ == '__main__':
    print(parse_monzo_com())
