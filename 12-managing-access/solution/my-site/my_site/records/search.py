from elasticsearch_dsl import Q
from flask_security import current_user
from invenio_search.api import DefaultFilter, RecordsSearch


def owner_permission_filter():
    """Search filter with permission."""
    return [Q('match', owner=current_user.get_id())]


class OwnerRecordsSearch(RecordsSearch):
    """Class providing permission search filter."""

    class Meta:
        index = 'records'
        default_filter = DefaultFilter(owner_permission_filter)
        doc_types = None
