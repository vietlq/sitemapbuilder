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

# TODO: Add the following data structures
# 1. recorded - set of recorded links to avoid double fetching
# 2. message queue - new and unique links are added to the end of the queue
# 3. map<url, set<url>> - key is the original URL and value
# is set of URLs being pointed at from that URL
# 4. decay - passed recursively/tagged with url; stop visiting when decay = 0
# do not add to recorded if decay = 0; message queue should have decay;
# add to map even the target url has decay = 0
# 5. filter - only initial domain/hostname, make it as cmd arg
# 6. process in the sequence:
# 6.1. => init: (url, decay) mq
# 6.2. => acquire lock
# 6.3. => filter by decay > 0 and not in recorded
# 6.4. => process url
# 6.5. => update map
# 6.6. => filter urls
# 6.7. => push list of (url, decay - 1) into mq
# 6.8. => if the queue is empty, sleep 10s to wait for more items then return
