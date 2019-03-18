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

from .api import AuthorRecord

def _(x):
    """Identity function for string extraction."""
    return x

RECORDS_REST_ENDPOINTS = {
    'authid': dict(
        pid_type='authid',
#        pid_minter='authid',
#        pid_fetcher='authid',
        default_endpoint_prefix=True,
        record_class=AuthorRecord,
        search_class=RecordsSearch,
        indexer_class=RecordIndexer,
#        search_index='authors',
        search_type=None,
        # record_serializers={
        #     'application/json': ('my_site.authors.serializers'
        #                          ':json_v1_response'),
        # },
        # search_serializers={
        #     'application/json': ('my_site.authors.serializers'
        #                          ':json_v1_search'),
        # },
        # record_loaders={
        #     'application/json': ('my_site.authors.loaders'
        #                          ':json_v1'),
        # },
        list_route='/authors/',
        item_route='/authors/<pid(authid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=allow_all,
        read_permission_factory_imp=check_elasticsearch,
        update_permission_factory_imp=allow_all,
        delete_permission_factory_imp=allow_all,
        list_permission_factory_imp=allow_all
    ),
}
"""REST API for my-site."""


RECORDS_REST_SORT_OPTIONS = dict(
    authors=dict(
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
    authors=dict(
        query='bestmatch',
        noquery='mostrecent',
    )
)
"""Set default sorting options."""
