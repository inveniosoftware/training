# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Author Api."""

from __future__ import absolute_import, print_function

from __future__ import absolute_import, print_function

from flask import current_app
from invenio_jsonschemas import current_jsonschemas
from invenio_records.api import Record



class AuthorRecord(Record):
    """Author record class."""

    @classmethod
    def create(cls, data, id_=None, **kwargs):
        """Create Author record."""
        data["$schema"] = current_jsonschemas.path_to_url('authors/author-v1.0.0.json')
        return super(AuthorRecord, cls).create(data, id_=id_, **kwargs)
