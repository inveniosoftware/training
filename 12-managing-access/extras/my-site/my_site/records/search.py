from elasticsearch_dsl import Q
from flask_security import current_user
from invenio_search.api import DefaultFilter, RecordsSearch


def owner_manager_permission_filter():
    """Search filter with permission."""
    if current_user.has_role('managers'):
        return [Q(name_or_query='match_all')]
    else:
        return [Q('match', owner=current_user.get_id())]


class OwnerManagerRecordsSearch(RecordsSearch):
    """Class providing permission search filter."""

    class Meta:
        index = 'records'
        default_filter = DefaultFilter(owner_manager_permission_filter)
        doc_types = None
