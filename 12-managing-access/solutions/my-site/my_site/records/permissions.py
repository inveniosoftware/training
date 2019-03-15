from invenio_access import Permission, action_factory
from flask_principal import UserNeed


create_records = action_factory("create-records")


def owner_permission_factory(record=None):
    """Permission factory with owner access."""
    return Permission(UserNeed(record["owner"]))
