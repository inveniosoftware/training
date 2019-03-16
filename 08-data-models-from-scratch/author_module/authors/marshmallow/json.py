# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from __future__ import absolute_import, print_function

from invenio_jsonschemas.proxies import current_jsonschemas
from invenio_records_rest.schemas import Nested, StrictKeysMixin
from invenio_records_rest.schemas.fields import DateString, \
    PersistentIdentifier, SanitizedUnicode
from marshmallow import fields, missing, validate


# class AuthorMetadataSchemaV1(StrictKeysMixin):
#     """Schema for the author metadata."""

#     id = PersistentIdentifier()
#     name = SanitizedUnicode(required=True)
#     organization = SanitizedUnicode(required=False)

# class AuthorSchemaV1(StrictKeysMixin):
#     """Author schema."""

#     metadata = fields.Nested(AuthorMetadataSchemaV1)
#     created = fields.Str(dump_only=True)
#     updated = fields.Str(dump_only=True)
#     id = PersistentIdentifier()
