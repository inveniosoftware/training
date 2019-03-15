from invenio_access import Permission, authenticated_user
from flask_principal import UserNeed, RoleNeed


def owner_permission_factory(record=None):
    """Permission factory with owner access."""
    return Permission(UserNeed(record["owner"]))


def authenticated_user_permission(record=None):
    """Return an object that evaluates if the current user is authenticated."""
    return Permission(authenticated_user)


def owner_manager_permission_factory(record=None):
    """Returns permission for managers group."""
    return Permission(UserNeed(record["owner"]), RoleNeed('managers'))
