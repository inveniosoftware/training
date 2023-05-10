# Tutorial 07 - Data models: Adding a new field

The goal of this tutorial is to learn how to update your data model. We will show how you going to
update your [`JSONSchema`](https://json-schema.org/) to store a new field in the DB and your ES mapping so you can search for it.
Moreover, we will learn how [`Marshmallow`](https://marshmallow.readthedocs.io) schema can be used to validate your data.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Step 1: Bootstrap exercise](#step-1-bootstrap-exercise)
- [Step 2: Update the JSONSchema](#step-2-update-the-jsonschema)
- [Step 3: Update the Elasticsearch mapping](#step-3-update-the-elasticsearch-mapping)
- [Step 4: Update the Marshmallow schema](#step-4-update-the-marshmallow-schema)
- [Step 5: Create a new record including our new field](#step-5-create-a-new-record-including-our-new-field)
- [Step 6: Search for our new record](#step-6-search-for-our-new-record)
- [Step 7: Manipulate response using serializers](#step-7-manipulate-response-using-serializers)
- [What did we learn](#what-did-we-learn)

## Step 1: Bootstrap exercise

If you completed the previous tutorial, you can skip this step. If instead you would like to start from a clean state run the following commands:

```bash
cd ~/src/training/
./start-from.sh 05-customizing-invenio
```

## Step 2: Update the JSONSchema

Our use case: we have created our data model and we want to update it by adding a new field. Let's
call that field `owner` and it will be an integer (a User ID) that represents the owner of the corresponding record.

First thing we need to do is update our record schema in order to be able to store the new field in
the DB.

We edit the `my_site/records/jsonschemas/records/record-v1.0.0.json` file:

```diff
"properties": {
    "title": {
      "description": "Record title.",
      "type": "string"
    },
    "id": {
      "description": "Invenio record identifier (integer).",
      "type": "string"
    },
+   "owner": {
+     "type": "integer"
+   },
```

## Step 3: Update the Elasticsearch mapping

Now our system can validate and store our new field correctly in the DB. Now we want to enable search of a record by this new field. For this purpose, we need to update the mapping of our ES index in order to add our new field. By doing that we let ES know how to handle our new field(field type, searchable, analyzable, etc.).

So, in order to update the mapping we edit the `my_site/records/mappings/v7/records/record-v1.0.0.json` file:

```diff
      "properties": {
        "$schema": {
          "type": "text",
          "index": false
        },
        "title": {
          "type": "text",
          "copy_to": "suggest_title"
        },
        "suggest_title": {
          "type": "completion"
        },
        "id": {
          "type": "keyword"
        },
+       "owner": {
+         "type": "integer"
+       },
```

## Step 4: Update the Marshmallow schema

Next thing is to update our marshmallow schema in order to allow our new field to be validated by our loader. To
achieve that we edit the `my_site/records/marshmallow/json.py`:

```diff
class MetadataSchemaV1(StrictKeysMixin):
    """Schema for the record metadata."""

    id = PersistentIdentifier()
    title = SanitizedUnicode(required=True, validate=validate.Length(min=3))
    keywords = fields.List(SanitizedUnicode(), many=True)
    publication_date = DateString()
    contributors = Nested(ContributorSchemaV1, many=True, required=True)
+   owner = fields.Integer()
```

## Step 5: Create a new record including our new field

Now in order to **reflect our changes** in our system we will have to run the following command:

```bash
./scripts/setup
```

We have created and started a new DB and ES along with the updated schemas and mappings.

**Checkpoint 1**: At this point we are able to create a new record in our system that includes our new field. Let's do this!

**Note**: Make sure you have up and running our development server by running:

```bash
./scripts/server
```

Run the below command to create our new record:

```bash
curl -k --header "Content-Type: application/json" \
  --request POST \
  --data '{"title":"Some title", "contributors": [{"name": "Doe, John"}], "owner": "owner"}' \
  https://localhost:5000/api/records/?prettyprint=1
```

After executing the command you should see in your console the following output:

```json
{
  "status": 400,
  "message": "Validation error.",
  "errors": [
    {
      "field": "owner",
      "message": "Not a valid integer."
    }
  ]
}
```

It seems that our request wasn't successful. By checking again the error message we can see that in our request
the `owner` field has a `string` value rather than an `integer`. But who validated that?

If you remember we talked earlier about `loaders` and specifically we updated our `marshmallow` schema. But how is it related? To answer that let's talk about what is the responsibility of the `loaders`. Its purpose is to load the data received in the create a new record request, validate it using our `marshmallow` schema and transform it into our internal representation.

By having that in mind, when we did our request our loader used the marshmallow `MetadataSchemaV1` schema to validate the incoming data and noticed that the owner field isn't an integer as it was declared so it threw an error.

So now let's fix the data we sent before and create our record!

```bash
curl -k --header "Content-Type: application/json" \
  --request POST \
  --data '{"title":"Some title", "contributors": [{"name": "Doe, John"}], "owner": 1}' \
  https://localhost:5000/api/records/?prettyprint=1
```

Now you should see an output similar to the below:

```json
{
  "created": "2020-05-12T14:41:44.801477+00:00",
  "id": "1",
  "links": {
    "files": "https://localhost:5000/api/records/1/files",
    "self": "https://localhost:5000/api/records/1"
  },
  "metadata": {
    "$schema": "https://my-site.com/schemas/records/record-v1.0.0.json",
    "contributors": [
      {
        "name": "Doe, John"
      }
    ],
    "id": "1",
    "owner": 1,
    "title": "Some title"
  },
  "revision": 0,
  "updated": "2020-05-12T14:41:44.801484+00:00"
}
```

**Tip**: Save somewhere the `id` value of this response!

Our new record was successfully created!

## Step 6: Search for our new record

**Checkpoint 2**: At this point we have created our new record and we are able to search it. Let's do this!

**Note**: Make sure you have up and running our development server by running:

```bash
./scripts/server
```

Let's search now for our newly created record. Replace the `<id>` with the actual `id` of the
record we created in the previous step. Run the following command:

```bash
$ curl -k "https://localhost:5000/api/records/?q=owner:<id>"
{
  "aggregations": {...},
  "hits": {
    "hits": [
      {
        "created": "2019-03-13T10:39:57.345889+00:00",
        "id": "<id>",
        "links": {
          "self": "https://localhost:5000/api/records/2"
        },
        "metadata": {
          "contributors": [
            {
              "name": "Doe, John"
            }
          ],
          "id": "<id>",
          "owner": 1,
          "title": "Some title"
        },
        "revision": 0,
        "updated": "2019-03-13T10:39:57.345895+00:00"
      }
    ],
    "total": 1
  },
  "links": {
    "self": "https://localhost:5000/api/records/?page=1&sort=mostrecent&size=10"
  }
}
```

## Step 7: Manipulate response using serializers

Here you can see the data returned from the search regarding our record. The output of each result is controlled
by our `serializers`. These entities are responsible for getting the internal representation of our data and transforming
it into an output that the users of our system will see when they will use our API.

The `serializers` are also using a `Marshmallow` schema to validate the internal data and define which information should be returned. This means that if we want to hide some data and don't return every available information all we need to do is just
not define it in the `Marshmallow` schema.

For example, from the above output, we want to display only when the record was `updated` and not when was `created`. In order to
do that we need to update our `RecordSchemaV1` schema as below:

```diff
class RecordSchemaV1(StrictKeysMixin):
    """Record schema."""

    metadata = fields.Nested(MetadataSchemaV1)
-   created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = PersistentIdentifier()
```

Now, if we search again we will take the following result:

```bash
$ curl -k "https://localhost:5000/api/records/?q=owner:<id>"
{
  "aggregations": {...},
  "hits": {
    "hits": [
      {
        "id": "<id>",
        "links": {
          "self": "https://localhost:5000/api/records/2"
        },
        "metadata": {
          "contributors": [
            {
              "name": "Doe, John"
            }
          ],
          "id": "<id>",
          "title": "Some title"
        },
        "revision": 0,
        "updated": "2019-03-13T10:39:57.345895+00:00"
      },
      {...}
    ],
    "total": 1
  },
  "links": {
    "self": "https://localhost:5000/api/records/?page=1&sort=mostrecent&size=10"
  }
}
```

## What did we learn

- How to update the JSONSchema
- How to update a Elasticsearch mapping
- How to use Marshmallow schema along with loaders
- How to control your API responses with serializers
