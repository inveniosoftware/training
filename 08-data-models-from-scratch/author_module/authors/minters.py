# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
# Copyright (C) 2018 RERO.
#
# Invenio-Circulation is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Circulation minters."""

from .providers import AuthorIdProvider

# Uncomment me

# def author_pid_minter(record_uuid, data):
#     """Mint loan identifiers."""
#     assert 'id' not in data
#     provider = AuthorIdProvider.create(
#         object_type='rec',
#         object_uuid=record_uuid,
#     )
#     data['id'] = provider.pid.pid_value
#     return provider.pid
