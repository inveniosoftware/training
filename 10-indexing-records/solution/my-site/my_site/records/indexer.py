# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Record modification prior to indexing."""

from __future__ import absolute_import, print_function

def indexer_receiver(sender, json=None, record=None, index=None, doc_type=None):
    """Connect to before_record_index signal to transform record for ES.

    :param json: The dumped record dictionary which can be modified.
    :param record: The record being indexed.
    :param index: The index in which the record will be indexed.
    :param doc_type: The doc_type for the record.
    """

    # delete the `keywords` field before indexing
    if 'keywords' in json:
        del json['keywords']

    # count the number of contributors and add the new field
    contributors = json.get('contributors', [])
    json['contributors_count'] = len(contributors)
