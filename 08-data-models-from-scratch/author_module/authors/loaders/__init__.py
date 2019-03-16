# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Loaders.

This file contains sample loaders that can be used to deserialize input data in
an application level data structure. The marshmallow_loader() method can be
parameterized with different schemas for the record metadata. In the provided
json_v1 instance, it uses the AuthorMetadataSchemaV1, defining the
PersistentIdentifier field.
"""

from __future__ import absolute_import, print_function

from invenio_records_rest.loaders.marshmallow import json_patch_loader, \
    marshmallow_loader

from ..marshmallow import AuthorMetadataSchemaV1

#: JSON loader using Marshmallow for data validation.
# json_v1 = marshmallow_loader(AuthorMetadataSchemaV1)

__all__ = (
    'json_v1',
)
