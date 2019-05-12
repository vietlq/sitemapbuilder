"""Visits links within certain depth and certain (sub)domain."""

import requests
from .urlhtmlparser import UrlHtmlParser
from .urlhtmlparser import is_content_type_supported
from .urlhtmlparser import is_scheme_http_https


def is_url_content_type_http(url, fetcher=requests):
    """Send HEAD request and verify if the URL has valid Content-Type"""
    if not is_scheme_http_https(url):
        return False
    result = fetcher.head(url, allow_redirects=True, timeout=5)
    content_type_keys = [
        key for key in result.headers.keys()
        if key.strip().lower() == 'content-type']
    if not content_type_keys:
        return False
    return is_content_type_supported(result.headers[content_type_keys[0]])


def fetch_and_extract_links(url, fetcher=requests):
    """Fetch content of a HTML URL and extract hyper links from it"""
    if not is_url_content_type_http(url):
        return set()
    try:
        parser = UrlHtmlParser()
        response = fetcher.get(url, allow_redirects=True, timeout=5)
        html_content = response.text
        return parser.parse_html_with_url(html_content, response.url)
    except Exception:
        return set()
