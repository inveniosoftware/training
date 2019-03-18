# Tutorial 11 - Data models: link records using references

The goal of this tutorial is to learn how we can link records using references, with a technique similar to [JSON Reference](https://json-spec.readthedocs.io/reference.html).

### Table of Contents

- [Step 1: Bootstrap exercise](#step-1-bootstrap-exercise)
- [Step 2: Modify the record before indexing](#step-2-modify-the-record-before-indexing)
- [Step 3: Try it!](#step-3-try-it)
- [What did we learn](#what-did-we-learn)

In tutorial 08, we have learned how to create a new data model, the author record. It would be now very useful to link a record to his author so that, when using the REST APIs to return records, we can immediately return also the details of the author without performing any extra query.
For example, given the following record:

```json
{
  "id": 1,
  "title": "Invenio is awesome",
  "contributors": [
    {
      "name": "Kent, Clark"
    }
  ],
  "contributors_count": 1
}
```

and its author:

```json
{
  "id": 1,
  "name": "Goodman, Martin"
}
```

we would like that when we retrieve the record, the details of the author are automatically included in the each record:

```json
{
  "author": {
    "id": 1,
    "name": "Goodman, Martin"
  },
  "id": 1,
  "title": "Invenio is awesome",
  "contributors": [
    {
      "name": "Kent, Clark"
    }
  ],
  "contributors_count": 1
}
```

How do we do it?

1. In the record data model, we define a `$ref` attribute that is an URL pointing to the author record.
2. When indexing the record, Invenio will find the `$ref` record and use the URL to retrieve the referenced record.
3. The URL is a Flask route that we have to define and implement and it will be called by Invenio. This won't be a real HTTP call (see below for more explanations).
4. The indexed record will contain the replaced object instead of the `$ref` field.

Let's implement it.

## Step 1: Bootstrap exercise

If you completed the previous tutorial, you can skip this step. If instead you would like to start from a clean state run the following commands:

```bash
$ cd ~/src/training/
$ ./start-from.sh 10-indexing-records
```

## Step 2:

We need to create a reference (in a similar way as we would do using foreign keys in the SQL world) between record and author. Let's add a new `$ref` field in the record data model to reference the author.

`my-site/my_site/records/jsonschemas/records/record-v1.0.0.json`

```diff
  "type": "object",
  "properties": {
+   "author": {
+     "type": "object",
+     "properties": {
+       "$ref": {
+         "type": "string"
+       }
+     },
+     "required": ["$ref"]
+   },
    "title": {
      "description": "Record title.",
      "type": "string"
    },
```

Since we have changed the data model, we need to change the Elasticsearch mappings because you want to search records by author metadata.

`my-site/my_site/records/mappings/v6/records/record-v1.0.0.json`

```diff

+       "author": {
+         "type": "object",
+         "properties": {
+           "id": {
+             "type": "integer"
+           },
+           "name": {
+             "type": "text"
+           }
+         }
+       },
         "id": {
          "type": "keyword"
        },
```

## Step 3:

What will now happen is that when creating a new record, there will be a new `$ref` field with the URL to resolve the related author. For example, `$ref: https://my-site.com/api/resolver/author/1`.

When indexing, the `invenio-indexer` module will find the `$ref` field and, instead of calling the URL and performing the HTTP request, it will try to find if there is a Flask route registered with that URL. In that case, it will execute the method of the route itself and replace the `$ref` field with the output of the method. This method is a called `JSON resolver`.

Let's create a new file:

`my-site/my_site/records/jsonresolvers.py`

```python
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
```

## Step 4:

We need to add the JSON resolver method in the entrypoints.

`my-site/setup.py`

```diff
            'authors = my_site.authors.jsonschemas',
        ],
+       "invenio_records.jsonresolver": [
+           "author = my_site.records.jsonresolvers",
+       ],
        'invenio_search.mappings': [
            'records = my_site.records.mappings',
```

## Step 5:

We can now try to create an author and then a record with a reference to it. But first, since we have changed schema, mappings and entrypoints, let's re-install the app and re-init DB and Elasticsearch.

```bash
$ pipenv run pip install -e .
$ ./scripts/setup
$ ./scripts/server
```

Create a new author:

```bash
$ curl -k --header "Content-Type: application/json" \
    --request POST \
    --data '{"name": "Goodman, Martin"}' \
    "https://127.0.0.1:5000/api/authors/?prettyprint=1"
$ firefox http://127.0.0.1:9200/authors/_search?pretty=true
```

Create a new record. In the `$ref` field, we will put the route URL that we have defined in the JSON resolver method. To use the REST API, we would have to change the loaders, since the `author` field is not defined. Let's create the record using the CLI.

```bash
$ echo '{"author": { "$ref": "https://my-site.com/api/resolver/author/1" }, "title": "Invenio is awesome", "contributors": [{"name": "Kent, Clark"}], "owner": 1}' | pipenv run invenio records create --pid-minter recid
```

Let's re-index the newly create record so that the `$ref` attribute will be replaced:

```bash
$ pipenv run invenio index reindex --pid-type recid --yes-i-know
$ pipenv run invenio index run
```

Now, we can query Elasticsearch and verify that the author metadata are in the record.

```bash
$ firefox http://127.0.0.1:9200/records/_search?pretty=true
```

## Bonus

FIXME
Did you notice the `contributors_count` field in the author list of results? Can you guess why?

## A more complete explanation

# TODO complete me

`$ref` is an internal resolution of records references. As we usually don't expose foreign keys of our DB, it might be not a great idea to expose a field with an URL that has a meaning only in our instance. The URL contains a "fake" domain as host and it is meant to be used with JSON resolvers without performing a real HTTP call.
When using this technique, think about it in advance because the URL will be hardcoded in each record. If you have to change it, you will have most probably to perform un update of all your record.
Moreover, if you want to expose your records schema, it might not make sense to expose the `$ref` field. It is probably a good practice to always resolve `$ref` when exporting data as JSON or any other format.

`replace_refs` here description


To keep things simple, we will POST a new record with the right `$ref` URL.
In reality, we really recommend you to create your own record class and add the `author` field in the overridden `create` method, something like:

```python
class MyRecord(Record):

    _schema = "myrecords/myrecord-v1.0.0.json"

    @classmethod
    def create(cls, data, id_=None, **kwargs):
        """Create MyRecord record."""
        data["$schema"] = current_jsonschemas.path_to_url(cls._schema)
        data["author"] = {
            "$ref": "http://mysite.com/resolver/{}".format(data['author_id'])
        }
        return super(MyRecord, cls).create(data, id_=id_, **kwargs)
```

## What did we learn

- We have understood how Invenio uses JSON references
- We have seen how to create a reference between 2 records
- We have learned how to implement a JSON resolver
