"""Author resolver."""

from __future__ import absolute_import, print_function

import jsonresolver
from invenio_pidstore.resolver import Resolver
from invenio_records.api import Record


# the host corresponds to the config value for the key JSONSCHEMAS_HOST
@jsonresolver.route('/api/resolver/author/<authid>', host='my-site.com')
def record_jsonresolver(authid):
    """Resolve referenced author."""
    # Setup a resolver to retrive an author record given its id
    resolver = Resolver(pid_type='authid', object_type="rec", getter=Record.get_record)
    _, record = resolver.resolve(str(authid))
    # we could manipulate here the record and eventually add/remove fields
    del record['$schema']
    return record
