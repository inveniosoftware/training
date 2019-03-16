# Tutorial 08 - Data models: Build from scratch

In this session we will learn how to build a new data model from scratch. During that
process we will see how to create a new REST **module** for our model and provide functonalities
such as storing and searching.

Jump to: [Step 1](#step-1) | [Step 2](#step-2) | [Step 3](#step-3) | [Step 4](#step-4)

Any extra long description

## Step 1

Start from a clean and working instance:

```bash
$ cd 08-data-models-build-from-scratch/
$ ./init.sh
```

**Note**: In order to reduce the amount of code that we need to write we have prepared beforehand the module
structure in `/08-data-models-from-scratch/authors` folder in which will go through and uncomment the needed
code snippets to enable different functionalities and eventually build our module!

Run the below command to copy the module over:

```bash
$ ./bootstrap.sh
```

You should now see in your application folder a newly created `authors` folder which will be the module we will
develop through this tutorial.

## Create an `Authors` flask extension

First thing we need to do is to create an extension called `Authors` and register it in our `setup.py` so our Invenio application can know about it.

### Action steps

- Uncomment the code we find in the `my_site/authors/ext.py`
- Uncomment in the `setup.py` the following section:
  ```diff
   'invenio_base.api_apps': [
        'my_site = my_site.records:Mysite',
  - #   'authors = my_site.authors:Authors'
  +     'authors = my_site.authors:Authors'
  ]
  ```

  In that way we register our extension under Invenio API application.

## Internal representation: JSONSchema and ElasticSearch mappings

Now that we have our extension registered, we need to tell Invenio how the internal representation of our data model is. To do so we use [a JSONSchema](author_module/authors/jsonschemas/authors/author-v1.0.0.json) and [an ElasticSearch mapping](author_module/authors/mappings/v6/authors/author-v1.0.0.json): the former to validate the internal JSON format and the latter to tell ElasticSearch what shape our data model has so it can handle correctly its values.


### Action steps

- Uncomment the entrypoints in `setup.py`:

  ```diff
  - # 'invenio_jsonschemas.schemas': [
  - #     'my_site = my_site.records.jsonschemas',
  - #     'authors = my_site.authors.jsonschemas'
  - # ],
  - # 'invenio_search.mappings': [
  - #     'records = my_site.records.mappings',
  - #     'authors = my_site.authors.mappings'
  - # ],
  + 'invenio_jsonschemas.schemas': [
  +     'my_site = my_site.records.jsonschemas',
  +     'authors = my_site.authors.jsonschemas'
  + ],
  + 'invenio_search.mappings': [
  +     'records = my_site.records.mappings',
  +     'authors = my_site.authors.mappings'
  + ],
  ```

  By doing this we told Invenio to register our new schema and mapping.


## External representation: loaders and serializers

So far we have a new extension which defines how our data model is **stored** and **searchable**, but have not yet provided means to transform this data when its received or served by Invenio. To do so we will introduce two concepts: **loaders** whose responsibility is to transform incoming data to the internal format, and **serializers** which will be in charge of transforming the internal data to a different format, based on our needs.

### Action steps

- Uncomment the code inside `my_site/authors/marshmallow/json.py`, we use Marshmallow to define the format of the transformation, we will talk more about it in the next steps.


--------------


Create an authors folder and an authors JSONSchema:

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "http://localhost/schemas/authors/author-v1.0.0.json",
  "additionalProperties": false,
  "title": "My site v1.0.0",
  "type": "object",
  "properties": {
    "id": {
      "description": "Invenio record identifier (integer).",
      "type": "number"
    },
    "name": {
      "description": "Author name.",
      "type": "string"
    },
    "organization": {
      "description": "Organization the author belongs to.",
      "type": "string"
    }
  },
  "required": ["id", "name"]
}
```

Next, we will add the Marshmallow schema to `my_site/records/marshmallow/json.py` and add a new loader `my_site/records/loader/__init__.py` in order to validate the incoming data before storing it in the database.

```python
class AuthorMetadataSchemaV1(StrictKeysMixin):
    """Schema for the author metadata."""

    id = PersistentIdentifier()
    name = SanitizedUnicode(required=True)
    organization = SanitizedUnicode(required=True)
```

```diff
from __future__ import absolute_import, print_function

from invenio_records_rest.loaders.marshmallow import json_patch_loader, \
    marshmallow_loader

-from ..marshmallow import MetadataSchemaV1
+from ..marshmallow import MetadataSchemaV1, AuthorMetadataSchemaV1

#: JSON loader using Marshmallow for data validation.
json_v1 = marshmallow_loader(MetadataSchemaV1)
+author_v1 = marshmallow_loader(AuthorMetadataSchemaV1)

__all__ = (
    'json_v1',
+    'author_v1',
)
```

We will now create an ElasticSearch mapping to make the authors searchable:

```json
{
  "mappings": {
    "author-v1.0.0": {
      "date_detection": false,
      "numeric_detection": false,
      "properties": {
        "$schema": {
          "type": "text",
          "index": false
        },
        "id": {
          "type": "keyword"
        },
        "name": {
          "type": "keyword"
        },
        "organization": {
          "type": "keyword"
        },
        "_created": {
          "type": "date"
        },
        "_updated": {
          "type": "date"
        }
      }
    }
  }
}
```

Until now we managed to pave the way to create and search authors. Now we will create a Marshmallow schema in `my_site/records/marshmallow/json.py` for serializing and a new serializer in `my_site/records/serializers/__init__.py`:

```python
class AuthorSchemaV1(StrictKeysMixin):
    """Author schema."""

    metadata = fields.Nested(AuthorMetadataSchemaV1)
    created = fields.Str(dump_only=True)
    updated = fields.Str(dump_only=True)
    id = PersistentIdentifier()
```

```diff
"""Record serializers."""

from __future__ import absolute_import, print_function

from invenio_records_rest.serializers.json import JSONSerializer
from invenio_records_rest.serializers.response import record_responsify, \
    search_responsify

-from ..marshmallow import RecordSchemaV1
+from ..marshmallow import RecordSchemaV1, AuthorSchemaV1

# Serializers
# ===========
#: JSON serializer definition.
json_v1 = JSONSerializer(RecordSchemaV1, replace_refs=True)
+author_v1 = JSONSerializer(AuthorSchemaV1, replace_refs=True)

# Records-REST serializers
# ========================
#: JSON record serializer for individual records.
json_v1_response = record_responsify(json_v1, 'application/json')
#: JSON record serializer for search results.
json_v1_search = search_responsify(json_v1, 'application/json')
+#: JSON author serializer for individual authors.
+author_v1_response = record_responsify(author_v1, 'application/json')
+#: JSON author serializer for search results.
+author_v1_search = search_responsify(author_v1, 'application/json')

__all__ = (
    'json_v1',
    'json_v1_response',
    'json_v1_search',
+    'author_v1_response',
+    'author_v1_search',
)
```

## What did we learn

- TODO
