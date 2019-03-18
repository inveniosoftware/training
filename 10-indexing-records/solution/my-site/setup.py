# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Invenio digital library framework."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('my_site', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='my-site',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='my-site Invenio',
    license='MIT',
    author='CERN',
    author_email='info@my-site.com',
    url='https://github.com/my-site/my-site',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'my-site = invenio_app.cli:cli',
        ],
        'invenio_base.apps': [
            'my_site_records = my_site.records:Mysite',
        ],
        'invenio_base.blueprints': [
            'my_site = my_site.theme.views:blueprint',
            'my_site_records = my_site.records.views:blueprint',
            'my_site_deposit = my_site.deposit.views:blueprint',
        ],
        'invenio_assets.webpack': [
            'my_site_theme = my_site.theme.webpack:theme',
        ],
        'invenio_config.module': [
            'my_site = my_site.config',
        ],
        'invenio_i18n.translations': [
            'messages = my_site',
        ],
        'invenio_base.api_apps': [
            'my_site = my_site.records:Mysite',
            'authors = my_site.authors:Authors',
        ],
        'invenio_pidstore.fetchers': [
            'authid = my_site.authors.fetchers:author_pid_fetcher',
        ],
        'invenio_pidstore.minters': [
            'authid = my_site.authors.minters:author_pid_minter',
        ],
        'invenio_jsonschemas.schemas': [
            'my_site = my_site.records.jsonschemas',
            'authors = my_site.authors.jsonschemas',
        ],
        'invenio_search.mappings': [
            'records = my_site.records.mappings',
            'authors = my_site.authors.mappings',
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
    ],
)
