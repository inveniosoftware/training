"""Deposit APIs."""

from __future__ import absolute_import, print_function

import uuid

from flask import current_app
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore import current_pidstore
from invenio_records.api import Record


def create_record(data):
    """Create a record.

    :param dict data: The record data.
    """
    with db.session.begin_nested():
        # create uuid
        rec_uuid = uuid.uuid4()
        # create PID
        current_pidstore.minters['recid'](rec_uuid, data)
        # create record
        created_record = Record.create(data, id_=rec_uuid)
        # index the record
        RecordIndexer().index(created_record)
    db.session.commit()
