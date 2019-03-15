from invenio_access import Permission, action_factory, authenticated_user
from flask_principal import UserNeed


create_records = action_factory("create-records")


def owner_permission_factory(record=None):
    """Permission factory with owner access."""
    return Permission(UserNeed(record["owner"]))


def authenticated_user_permission(record=None):
    """Return an object that evaluates if the current user is authenticated."""
    return Permission(authenticated_user)