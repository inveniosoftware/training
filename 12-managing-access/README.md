# Tutorial 12 - Record access management

## Table of contents
- [Step 1 - Allow for access only from the owner](#step-1---allow-for-access-only-from-the-owner)
- [Step 2 - search filter](#step-2---search-filter)
- [Step 3 - Create permissions](#step-3---create-permissions)
- [Extras - Additional excersises](#extras)

The goal of this tutorial is to implement record access permissions in simple and complicated cases.

Prerequisites:
1. previous steps with owner field

2. at least two different users

```commandline
my-site users create admin@test.ch -a --password=123456 # create admin user ID 1
my-site users create manager@test.ch -a --password=123456 # create admin user ID 2
my-site users create visitor@test.ch -a --password=123456 # create visitor user ID 3
```

2. at least two records

```commandline
curl -k --header "Content-Type: application/json" --request POST --data '{"title":"My test record", "contributors": [{"name": "Doe, John"}], "owner": 1}' https://localhost:5000/api/records/?prettyprint=1

curl -k --header "Content-Type: application/json" --request POST --data '{"title":"Second test record", "contributors": [{"name": "Copernicus, Mikolaj"}], "owner": 2}' https://localhost:5000/api/records/?prettyprint=1
```


## Step 1 - Allow for access only from the owner

### Use case:
Restrict the access to read, edit and delete action for the record only to its owner.

1. We implement the permission factory. The permission requires a need to be fulfilled by a user for a record. In this case we remember that:

```json
    "owner": {
      "type": "integer"
    },
```

so the permission factory requires users to provide their ID as stored in the the `"owner"` field of the record.
Add the following `my_site/records/permissions.py` file:

```python
from invenio_access import Permission
from flask_principal import UserNeed

def owner_permission_factory(record=None):
    """Permission factory with owner access to the record."""
    return Permission(UserNeed(record["owner"]))

```

2. We use the permission factory in the configuration file to let the application know that this endpoint has a permission requirement (RUD). Edit `my_site/records/config.py`:

```diff
+from my_site.records.permissions import owner_permission_factory

RECORDS_REST_ENDPOINTS = {
    'recid': dict(
        pid_type='recid',
        pid_minter='recid',
        pid_fetcher='recid',
        default_endpoint_prefix=True,
        search_class=RecordsSearch,
        indexer_class=RecordIndexer,
        search_index='records',
        search_type=None,
        record_serializers={
            'application/json': ('my_site.records.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('my_site.records.serializers'
                                 ':json_v1_search'),
        },
        record_loaders={
            'application/json': ('my_site.records.loaders'
                                 ':json_v1'),
        },
        list_route='/records/',
        item_route='/records/<pid(recid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=allow_all,
-       read_permission_factory_imp=check_elasticsearch,
-       update_permission_factory_imp=allow_all,
-       delete_permission_factory_imp=allow_all,
+       read_permission_factory_imp=owner_permission_factory,
+       update_permission_factory_imp=owner_permission_factory,
+       delete_permission_factory_imp=owner_permission_factory,
        list_permission_factory_imp=allow_all
    ),
}
"""REST API for my-site."""
```

3. log in as manager user

4. visit `/api/records/<id>` (first record)

```json
{
"message": "You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.",
"status": 403
}
```

4. visit `/records/<id>`

Record still not protected!

5. Set permission factory also for UI endpoints in `my_site/records/config.py`:
```diff
RECORDS_UI_ENDPOINTS = {
    'recid': {
        'pid_type': 'recid',
        'route': '/records/<pid_value>',
        'template': 'records/record.html',
+       'permission_factory_imp': 'my_site.records.permissions:owner_permission_factory',
    },
}
"""Records UI for my-site."""
```

6. visit `/records/<id>`


## Step 2 - search filter

The details pages of records are now protected. But if we visit `/search?page=1&size=20&q=`, all the records are still visible in the search page. The same is true for the REST API: `/api/records/`. We would like to hide the results from search if they are not owned by the current user.

1. We implement a search filter that will display records in the search results only to their owner.
Let' s create `my_site/records/search.py`:

```python
from elasticsearch_dsl import Q
from flask_security import current_user


def owner_permission_filter():
    """Search filter with permission."""
    return [Q('match', owner=current_user.get_id())]

```

2. We implement a search class that uses the implemented filter (also in `search.py`).

```diff
from elasticsearch_dsl import Q
from flask_security import current_user
+from invenio_search.api import DefaultFilter, RecordsSearch


def owner_permission_filter():
    """Search filter with permission."""
    return [Q('match', owner=current_user.get_id())]


+class OwnerRecordsSearch(RecordsSearch):
+    """Class providing permission search filter."""
+
+    class Meta:
+        index = 'records'
+        default_filter = DefaultFilter(owner_permission_filter)
+        doc_types = None

```

3. We add the search class to the configuration in `my_site/records/config.py`:

```diff

+from my_site.records.search import OwnerRecordsSearch

RECORDS_REST_ENDPOINTS = {
    'recid': dict(
        pid_type='recid',
        pid_minter='recid',
        pid_fetcher='recid',
        default_endpoint_prefix=True,
+       search_class=OwnerRecordsSearch,
        indexer_class=RecordIndexer,
        search_index='records',
        search_type=None,
        record_serializers={
            'application/json': ('my_site.records.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('my_site.records.serializers'
                                 ':json_v1_search'),
        },
        record_loaders={
            'application/json': ('my_site.records.loaders'
                                 ':json_v1'),
        },
        list_route='/records/',
        item_route='/records/<pid(recid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=allow_all,
        read_permission_factory_imp=owner_permission_factory,
        update_permission_factory_imp=owner_permission_factory,
        delete_permission_factory_imp=owner_permission_factory,
        list_permission_factory_imp=allow_all
    ),
}
"""REST API for my-site."""
```

4. Go to the api search page `https://127.0.0.1:5000/api/records/` and check that it displays only the records owned by the current user

5. Go to the UI search page `https://127.0.0.1:5000/search?page=1&size=20&q=` and check that it displays only the records owned by the current user

## Step 3 - Create permissions

### Use case: restrict creation of records to authenticated users

1. Implement the permission factory in `my_site/records/permissions.py` 

```python
from invenio_access import Permission, authenticated_user

def authenticated_user_permission(record=None):
    """Return an object that evaluates if the current user is authenticated."""
    return Permission(authenticated_user)

```

2. Add the permission factory to the configuration of the records REST endpoints
in `my_site/records/config.py`

```diff
-from my_site.records.permissions import owner_permission_factory
+from my_site.records.permissions import owner_permission_factory, \
+   authenticated_user_permission

RECORDS_REST_ENDPOINTS = {
    'recid': dict(
        pid_type='recid',
        pid_minter='recid',
        pid_fetcher='recid',
        default_endpoint_prefix=True,
        search_class=OwnerRecordsSearch,
        indexer_class=RecordIndexer,
        search_index='records',
        search_type=None,
        record_serializers={
            'application/json': ('my_site.records.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('my_site.records.serializers'
                                 ':json_v1_search'),
        },
        record_loaders={
            'application/json': ('my_site.records.loaders'
                                 ':json_v1'),
        },
        list_route='/records/',
        item_route='/records/<pid(recid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
-       create_permission_factory_imp=allow_all
+       create_permission_factory_imp=authenticated_user_permission,

```

3. Perform a POST request by using curl to test permission to create records as an unauthenticated user (should fail)

```commandline
curl -k --header "Content-Type: application/json" --request POST --data '{"title":"Second test record", "contributors": [{"name": "Copernicus, Mikolaj"}], "owner": 2}' https://localhost:5000/api/records/?prettyprint=1
```

## Extras

### Group permission to edit

Use case: We would like to allow our site's managers to edit and delete records

```
 NOTE: we have existing records already, we would not like to add the group access one by one to each record.
 ```

1. Create a managers role (group)

```commandline
(my-site)$ my-site roles create managers
```

2. Connect manager user with created role

```commandline
(my-site)$ my-site roles add manager@test.ch managers
```

3. Create the permission factory for role and owner

```python
from invenio_access import Permission
from flask_principal import UserNeed, RoleNeed


def owner_manager_permission_factory(record=None):
    """Returns permission for managers group."""
    return Permission(UserNeed(record["owner"]), RoleNeed('managers'))

```
4. Implement search filter for role and owner
```python
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

```

5. Update the configuration file with your new filter and factory

```python
from my_site.records.permissions import owner_permission_factory, \
    authenticated_user_permission, owner_manager_permission_factory
from my_site.records.search import OwnerManagerRecordsSearch

RECORDS_REST_ENDPOINTS = {
    'recid': dict(
        pid_type='recid',
        pid_minter='recid',
        pid_fetcher='recid',
        default_endpoint_prefix=True,
        search_class=OwnerManagerRecordsSearch,
        indexer_class=RecordIndexer,
        search_index='records',
        search_type=None,
        record_serializers={
            'application/json': ('my_site.records.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('my_site.records.serializers'
                                 ':json_v1_search'),
        },
        record_loaders={
            'application/json': ('my_site.records.loaders'
                                 ':json_v1'),
        },
        list_route='/records/',
        item_route='/records/<pid(recid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=authenticated_user_permission,
        read_permission_factory_imp=owner_manager_permission_factory,
        update_permission_factory_imp=owner_manager_permission_factory,
        delete_permission_factory_imp=owner_manager_permission_factory,
        list_permission_factory_imp=allow_all
    ),
}
"""REST API for my-site."""
```

6. Visit `https://127.0.0.1:5000/search?page=1&size=20&q=` and `https://127.0.0.1:5000/api/records/` as manager user and check if all the records are listed.


### Explicit access per action type - additional excersize

1. Implement access management for the record having in mind the structure below

```json
{
    "_access": {
        "read": {
            "systemroles": ["campus_user"]
        },
        "update": {
            "users": [1],
            "roles": ["curators"]
        }
    }
}
```


