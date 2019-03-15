# Tutorial 8 - Record access management

The goal of this tutorial is to implement record access permissions in simple and complicated cases.


Prerequisites:
1. previous steps with owner field

2. at least two different users

```bash
my-site users create admin@test.ch -a --password=123456 # create admin user ID 1
my-site users create manager@test.ch -a --password=123456 # create admin user ID 2
my-site users create visitor@test.ch -a --password=123456 # create visitor user ID 3
```

2. at least two records

```bash
curl -k --header "Content-Type: application/json" --request POST --data '{"title":"My test record", "contributors": [{"name": "Doe, John"}], "owner": 1}' https://localhost:5000/api/records/?prettyprint=1

curl -k --header "Content-Type: application/json" --request POST --data '{"title":"Second test record", "contributors": [{"name": "Copernicus, Mikolaj"}], "owner": 2}' https://localhost:5000/api/records/?prettyprint=1
```


// TODO set those links

Jump to: [Step 1](#step-1) | [Step 2](#step-2) | [Step 3](#step-3) | [Step 4](#step-4)

## Step 1

Start from a clean and working instance:

```bash
$ cd 08-build-simple-deposit-form/
$ ./init.sh
```

### Use case:
Restrict the access to read, edit and delete action for the record only to it's owner.

1. We implement permission factory. The permission requires a need to be fulfilled by a user for a record. In this case we remember that:

```json
    "owner": {
      "type": "integer"
    },
``` 

so the permission factory requires an user to provide his ID as stored in the record in the `"owner"` field:

```python
from invenio_access import Permission
from flask_principal import UserNeed

def owner_permission_factory(record=None):
    """Permission factory with owner access to the record."""
    return Permission(UserNeed(record["owner"]))

```

2. We add the permission factory implemented to the configuration file to let the application know that this endpoint has a permission requirement (RUD)

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
+       read_permission_factory_imp=owner_permission_factory,
        update_permission_factory_imp=allow_all,
        delete_permission_factory_imp=allow_all,
        list_permission_factory_imp=allow_all
    ),
}
"""REST API for my-site."""
```

3. log 

4. visit `/api/records/<id>`

```json
{
"message": "You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.",
"status": 403
}
```

4. visit `/records/<id>`

Record still not protected!

5. Apply the permission factory for UI endpoints

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

Records are protected at their details pages. But if we visit `/search?page=1&size=20&q=` all the records are still visible in the search page. The same happens for REST API: `/api/records/`. In most of the cases we would like to hide the results from search if they are not owned by the current user.

1. We implement search filter - restriction for displaying this record in the search results only for it's owner

```python
from elasticsearch_dsl import Q
from flask_security import current_user


def owner_permission_filter():
    """Search filter with permission."""
    return [Q('match', owner=current_user.get_id())]

```

2. We implement search class which features the implemented filter 

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

3. We add the search class to the configuration

```diff

+from my_site.records.search import OwnerRecordsSearch

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
        create_permission_factory_imp=allow_all,
        read_permission_factory_imp=owner_permission_factory,
        update_permission_factory_imp=allow_all,
        delete_permission_factory_imp=allow_all,
        list_permission_factory_imp=allow_all
    ),
}
"""REST API for my-site."""
```

4. Go to the api search page `https://127.0.0.1:5000/api/records/` and check that if it displays only the records owned by current user

5. Go to UI search page `https://127.0.0.1:5000/search?page=1&size=20&q=` and check if it displays only the records owned by current user

## Step 3 - Create permissions

### Use case: restrict creation of the records only for authenticated users

1. Implement the permission factory

```python
# todo paste code here
```

2. Add the permission factory to the configuration of the records rest endpoints

```python
# todo paste conf code here
```

3. Perform POST request by using curl to test creation permission (as unauthenticated user)

```bash
add curl command for post/PUT
```

## Extras

### Group permission to edit

1. Create a record containing the structure similar to the on e visible below

```json
// todo paste example json access structure 
```

2. Create the permission factory per role

```python
# permission factory 
```
3. Add the permission factory to update_ config per rest endpoint
```python
# config code
```

### Explicit access per action type

1. Create a record containing the structure similar to the on e visible below

```json
// todo paste example json access structure 
```

2. Create the permission factory per role

```python
# permission factory 
```
3. Add the permission factory to update_ config per rest endpoint
```python
# config code
```


