# A simple sitemap builder

The sitemap builder traverses links from a website and constrains itself to the given domain name. The final result will be a simple sitemap deduced from the links visited. The crawler will accept & process only URLs with `http` or `https` schemes.

To run the following command to install the tool: `pip install -U sitemapbuilder`

To run the sitemap builder: `sitemapbuilder -u 'https://monzo.com' -o test_monzo.dot`

Instead of printing the sitemap in XML format like [https://vietlq.github.io/sitemap.xml](https://vietlq.github.io/sitemap.xml), I decided to generate Graphviz .dot file, which can be used to generate PNG/PDF and other image/document formats.

The tool uses 5 threads by default and times out after 10 seconds.

There are safety features built-in:

1. Handle exceptions when querying a website
2. Check for HEAD and verify that content-type is `text/html` and charset is either UTF-8 or US-ASCII
3. Have decay (maximum depth) to avoid abuse
4. Have a map of visited URLs to avoid revisiting them
