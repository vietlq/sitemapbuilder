#!/usr/bin/env python

# Read https://github.com/django-extensions/django-extensions/issues/92
# Read: http://setuptools.readthedocs.io/en/latest/setuptools.html
# Look for find_packages, packages, package_dir

from setuptools import setup, find_packages
import codecs

with codecs.open('README.rst', 'r', 'utf-8') as fd:
    long_description = fd.read()

# TODO: Simplify & unify versioning
pkg_version = '0.0.5'

setup(
    name='sitemapbuilder',
    version=pkg_version,
    description='Simple sitemap builder',
    long_description=long_description,
    author='Viet Le',
    author_email='vietlq85@gmail.com',
    url='https://github.com/vietlq/sitemapbuilder',
    install_requires=['requests'],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    scripts=['tools/sitemapbuilder'],
    keywords=['sitemapbuilder sitemap builder http'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ])
