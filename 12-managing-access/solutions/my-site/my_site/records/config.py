# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

from invenio_indexer.api import RecordIndexer
from invenio_records_rest.facets import terms_filter
from invenio_records_rest.utils import allow_all, check_elasticsearch
from invenio_search import RecordsSearch

from my_site.records.permissions import owner_permission_factory
from my_site.records.search import OwnerRecordsSearch


def _(x):
    """Identity function for string extraction."""
    return x


RECORDS_REST_ENDPOINTS = {
    'recid': dict(
        pid_type='recid',
        pid_minter='recid',
        pid_fetcher='recid',
        default_endpoint_prefix=True,
        search_class=OwnerRecordsSearch,
        indexer_class=RecordIndexer,
        search_index='records',
        search_type=None,
        record_serializers={
            'application/json': ('my_site.records.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('my_site.records.serializers'
                                 ':json_v1_search'),
        },
        record_loaders={
            'application/json': ('my_site.records.loaders'
                                 ':json_v1'),
        },
        list_route='/records/',
        item_route='/records/<pid(recid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=allow_all,
        read_permission_factory_imp=owner_permission_factory,
        update_permission_factory_imp=allow_all,
        delete_permission_factory_imp=allow_all,
        list_permission_factory_imp=allow_all
    ),
}
"""REST API for my-site."""

RECORDS_UI_ENDPOINTS = {
    'recid': {
        'pid_type': 'recid',
        'route': '/records/<pid_value>',
        'template': 'records/record.html',
        'permission_factory_imp': 'my_site.records.permissions:'
                                  'owner_permission_factory',
    },
}
"""Records UI for my-site."""

SEARCH_UI_JSTEMPLATE_RESULTS = 'templates/records/results.html'
"""Result list template."""

PIDSTORE_RECID_FIELD = 'id'

MY_SITE_ENDPOINTS_ENABLED = True
"""Enable/disable automatic endpoint registration."""


RECORDS_REST_FACETS = dict(
    records=dict(
        aggs=dict(
            type=dict(terms=dict(field='type')),
            keywords=dict(terms=dict(field='keywords'))
        ),
        post_filters=dict(
            type=terms_filter('type'),
            keywords=terms_filter('keywords'),
        )
    )
)
"""Introduce searching facets."""


RECORDS_REST_SORT_OPTIONS = dict(
    records=dict(
        bestmatch=dict(
            title=_('Best match'),
            fields=['_score'],
            default_order='desc',
            order=1,
        ),
        mostrecent=dict(
            title=_('Most recent'),
            fields=['-_created'],
            default_order='asc',
            order=2,
        ),
    )
)
"""Setup sorting options."""


RECORDS_REST_DEFAULT_SORT = dict(
    records=dict(
        query='bestmatch',
        noquery='mostrecent',
    )
)
"""Set default sorting options."""
