#!/usr/bin/env python3

"""Test UrlHtmlParser and related utility functions"""

import pytest
from sitemapbuilder import UrlHtmlParser
from sitemapbuilder.urlhtmlparser import is_scheme_http_https
from sitemapbuilder.urlhtmlparser import is_charset_supported
from sitemapbuilder.urlhtmlparser import is_content_type_supported


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


def test_is_charset_supported():
    """Test is_charset_supported"""
    assert is_charset_supported('us-ascii')
    assert is_charset_supported('utf-8')
    assert is_charset_supported('US-ASCII')
    assert is_charset_supported('UTF-8')
    assert not is_charset_supported('iso-646')
    assert not is_charset_supported('KOI8-R')


def test_is_content_type_supported():
    "Test is_content_type_supported"
    assert is_content_type_supported("text/html; charset=us-ascii")
    assert is_content_type_supported("text/html; charset=US-ASCII")
    assert is_content_type_supported("text/html; charset=utf-8")
    assert is_content_type_supported("text/html; charset=UTF-8")
    assert not is_content_type_supported("text/html")
    assert not is_content_type_supported("text/html; charset=iso-646")
    assert not is_content_type_supported("text/html; charset=KOI8-R")


if __name__ == '__main__':
    print(parse_monzo_com())
