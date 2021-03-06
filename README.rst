A simple sitemap builder
========================

The sitemap builder traverses links from a website and constrains itself to
the given domain name. The final result will be a simple sitemap deduced
from the links visited. The crawler will accept & process only URLs with
http or https schemes.

Installation and usage
======================

To run the following command to install the tool:

.. code-block:: bash

    pip install -U sitemapbuilder

To run the sitemap builder:

.. code-block:: bash

    sitemapbuilder -u 'https://monzo.com' -o test_monzo.dot

Some websites have strong protection and the tool will not work for them:

.. code-block:: bash

    sitemapbuilder -u 'https://bloomberg.com' -o test_bloomberg.dot

Highlights
==========

#. Generate Graphviz `.dot` file showing directed links between pages. One can generate PNG/PDF and other image/document formats.
#. Have `configurable decay` (maximum depth) to avoid abuse.
#. Visit web link within the same hostname by default.
#. Use `5 threads` by default and times out after `10 seconds`.
#. Timeout after `5 seconds` when fetching a URL.
#. Handle timeout exceptions when querying a website.
#. Send a `HTTP HEAD` request and verify that `Content-Type` is `text/html` and `charset` is either `UTF-8` or `US-ASCII`.
#. Have a map of visited URLs to avoid revisiting them.
#. Follow HTTP redirects.

Upcoming features
=================
* Configure the number of threads and timeout via cmd args.
* Allow web links from all subdomains.
* Allow web links from a list of domains.
* Allow web links matching a pattern.
* Add an option for hierarchical sitemap instead of directed graph.
* Use PriorityQueue instead of Queue to process links with higher decay first.
* Fine-graned info, warn and error logging.
* Pass seed links from a file.
* Save to and resume from a DB/persistent data source.
* Faster concurrency and better performance with asyncio.
