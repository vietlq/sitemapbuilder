"""Visits links within certain depth and certain (sub)domain."""

import ipaddress
import logging
import time
from threading import Thread, Lock
import queue
import socket
from urllib.parse import urlparse
import requests
import urllib3
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
    try:
        if not is_url_content_type_http(url):
            return set()
        # Fetch & extract links of content-type is supported
        parser = UrlHtmlParser()
        response = fetcher.get(url, allow_redirects=True, timeout=5)
        html_content = response.text
        return parser.parse_html_with_url(html_content, response.url)
    except (socket.timeout,
            urllib3.exceptions.ReadTimeoutError,
            requests.exceptions.ReadTimeout):
        msg = "Timed out when requesting URL [%s]" % response.url
        logging.getLogger("LinkVisitor").warning(msg)
        return set()
    except Exception:
        return set()

# NOTE: The following data structures are used:
# 1. recorded - set of recorded links to avoid double fetching
# 2. message queue - new and unique links are added to the end of the queue
# 3. map<url, set<url>> - key is the original URL and value
# is set of URLs being pointed at from that URL
# 4. decay - passed recursively/tagged with url; stop visiting when decay = 0
# do not add to recorded if decay = 0; message queue should have decay;
# add to map even the target url has decay = 0
# 5. filter - only initial domain/hostname, make it as cmd arg
# NOTE: Sitemap builder is running the algo:
# 1. => init: (url, decay) mq
# 2. => acquire lock
# 3. => filter by decay > 0 and not in recorded
# 4. => process url
# 5. => update map
# 6. => filter urls by recorded, domain name
# 7. => push list of (url, decay - 1) into mq
# 8. => if the queue is empty, sleep 10s to wait for more items then return


class SameHostnameFilter():
    """Only passes URLs with the same predefined hostname"""
    def __init__(self, seed_url):
        self.seed_url = seed_url
        hostname = str(urlparse(seed_url).hostname)
        try:
            _ = ipaddress.ip_address(hostname)
            self.hostnames = [hostname]
        except ValueError:
            if hostname.startswith('www.'):
                self.hostnames = [hostname, hostname[4:]]
            else:
                parts = hostname.split('.')
                self.hostnames = [hostname]
                if len(parts) == 2:
                    self.hostnames.append('www.%s' % hostname)

    def validate(self, url):
        """Validate if URL matches given hostname"""
        hostname = str(urlparse(url).hostname)
        return hostname in self.hostnames


class LinkVisitor():
    """Encapsulates link visiting crawler"""
    def __init__(self, seed_url, decay, domain_filter, num_workers=5,
                 retries_per_worker=10):
        assert num_workers > 0
        assert retries_per_worker > 1
        self.seed_url = seed_url
        self.decay = decay
        self.domain_filter = domain_filter
        self.num_workers = num_workers
        self.recorded = dict()
        self.sitemap = dict()
        self.queue = queue.Queue()
        self.max_retries = num_workers * retries_per_worker
        self.should_do = True
        self.retries = self.max_retries
        self.threads = []
        self.mutex = Lock()

    def do_work(self, *args, **kwargs):
        """Worked thread function"""
        while self.should_do and self.retries > 0:
            self.mutex.acquire()
            if self.queue.empty():
                self.retries -= 1
                print("empty queue; retries left: %d" % self.retries)
                self.mutex.release()
                time.sleep(1)
                continue
            self.retries = self.max_retries
            url, decay = self.queue.get()
            print("processing URL [%s] with [decay=%d]" % (url, decay))
            if decay < 1:
                print("skipped URL [%s] with low [decay=%d]" % (url, decay))
                self.mutex.release()
                continue
            # If a new URL detected, add it
            # If the same URL has new higher decay, add it
            if (url not in self.recorded) or \
               (url in self.recorded and self.recorded[url] < decay):
                self.recorded[url] = decay
                tmp_next_links = fetch_and_extract_links(url)
                next_links = []
                for link in tmp_next_links:
                    if self.domain_filter.validate(link):
                        next_links.append(link)
                    else:
                        print("skipped URL [%s]" % link)
                # Now update the calling map between links
                if url in self.sitemap:
                    for link in next_links:
                        self.sitemap[url].add(link)
                else:
                    self.sitemap[url] = set(next_links)
                # Avoid adding links with decay <= 0
                if decay > 1:
                    for link in next_links:
                        link_tuple = (link, decay - 1)
                        self.queue.put(link_tuple)
                        print("added URL [%s] with [decay=%d]" % link_tuple)
            self.mutex.release()

    def start(self):
        """Create threads, add seed url to start the process"""
        # Add seed URL to the queue
        self.mutex.acquire()
        self.queue.put((self.seed_url, self.decay))
        self.mutex.release()
        # Create the threads
        self.threads = []
        for _ in range(self.num_workers):
            worker_thread = Thread(target=self.do_work, args=(self,))
            worker_thread.start()
            self.threads.append(worker_thread)
        # Wait for the threads to finish
        for worker_thread in self.threads:
            worker_thread.join()

    def stop(self):
        """Stop processing the queue, but allow in-progress items to finish"""
        self.mutex.acquire()
        self.should_do = False
        self.mutex.release()
