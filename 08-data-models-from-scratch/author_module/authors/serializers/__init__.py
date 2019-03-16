# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Record serializers."""

from __future__ import absolute_import, print_function

from invenio_records_rest.serializers.json import JSONSerializer
from invenio_records_rest.serializers.response import record_responsify, \
    search_responsify

from ..marshmallow import AuthorSchemaV1

# Serializers
# ===========

#: JSON serializer definition.
# json_v1 = JSONSerializer(AuthorSchemaV1, replace_refs=True)

# Records-REST serializers
# ========================

#: JSON record serializer for individual records.
# json_v1_response = record_responsify(json_v1, 'application/json')

#: JSON record serializer for search results.
# json_v1_search = search_responsify(json_v1, 'application/json')

__all__ = (
    'json_v1',
    'json_v1_response',
    'json_v1_search',
)
