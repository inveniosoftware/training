# Tutorial 03 - Data models: Adding a new field

The goal of this tutorial is to learn how to update your datamodel. We will show how you going to
update your [`JSONSchema`](https://json-schema.org/) to store a new field in the DB and your ES mapping so you can search for it.
Moreover we will learn how [`Marshmallow`](https://marshmallow.readthedocs.io) schema can be used to validate your data.

Table of contents:
- [Bootstrap exercise](#Bootstrap-exercise)
- [Update the JSONSchema](#Update-the-JSONSchema)
- [Update the Elasticsearch mapping](#Update-the-Elasticsearch-mapping)
- [Update the Marshmallow schema](#Update-the-Marshmallow-schema)
- [Create a new record including our new field](#Create-a-new-record-including-our-new-field)
- [Search for our new record](#Search-for-our-new-record)
- [Manipulate response using serializers](#Manipulate-response-using-serializers)

## Bootstrap exercise

Start from a clean and working instance:

```bash
$ cd 03-add-new-field/
$ ./init.sh
```

## Update the JSONSchema

Our use case: we have created our data model and we want to update it by adding a new field. Let's
call that field `owner` and it will be an integer that represents the owner of the corresponding
record.

First thing we need to do is update our record schema in order to be able to store the new field in
the DB.

We edit the `jsonschemas/records/record-v1.0.0.json` file:

```diff
"properties": {
    "title": {
      "description": "Record title.",
      "type": "string"
    },
    "id": {
      "description": "Invenio record identifier (integer).",
      "type": "number"
    },
+   "owner": {
+     "type": "integer"
+   },
```

## Update the Elasticsearch mapping

Now our system can validate and store our new field correctly in the DB. Now we want to enable search of a record by this new field. For this purpose we need to update the mapping of our ES index in order to add our new field. By doing that we let ES know how to handle our new field(field type, searchable, analyzable, etc.).

So, in order to update the mapping we edit the `/mappings/v6/records/record-v1.0.0.json` file:

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
+         "type": "keyword"
+       },
```

## Update the Marshmallow schema
Next thing is to update our marshmallow schema in order to allow our new field to be validated by our loader. To
achieve that we edit the `marshmallow/json.py`:

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

## Create a new record including our new field

Now in order to **reflect our changes** in our system we will have to run the `/scripts/setup` script. With that we start fresh our DB and ES along with the updated information about schemas and mappings.


**Checkpoint 1**: At this point we are able to create a new record in our system that includes our new field. Let's do this!

**Note**: Make sure you have up and running our development server by running the `/scripts/server` script.

Run the below command to create our new record:

```bash
$ curl -k --header "Content-Type: application/json" \
    --request POST \
    --data '{"title":"Some title", "contributors": [{"name": "Doe, John"}], "owner": "owner"}' \
    https://localhost:5000/api/records/?prettyprint=1
```

After executing the command you should see in your console the following output:

```json
{"status": 400, "message": "Validation error.", "errors": [{"field": "owner", "message": "Not a valid integer."}]}
```

It seems that our request wasn't successfull. By checking again the error message we can see that in our request
the `owner` field has a `string` value rather than an `integer`. But who validated that?

If you remember we talked earlier about `loaders` and specifically we updated our `marshmallow` schema. But how are these related? To answer that let's talk about what is the responsibility of the `loaders`. It's purpose is to load the data which is passed when doing a request to create a new record, validate them by using our `marshmallow` schema and transform them in our internal representation.

By having that in mind, before when we did our request our loader used the marshmallow `MetadataSchemaV1` schema to validate the incoming data and noticed that the owner field isn't an integer as it was declared so it threw an error.

So now let's fix the data we sent before and create our record!

```bash
$ curl -k --header "Content-Type: application/json" \
    --request POST \
    --data '{"title":"Some title", "contributors": [{"name": "Doe, John"}], "owner": 1}' \
    https://localhost:5000/api/records/?prettyprint=1
```

Now you should see an output similar to the below:

```json
{
  "created": "2019-03-13T10:39:57.345889+00:00",
  "id": "2",
  "links": {
    "self": "https://localhost:5000/api/records/2"
  },
  "metadata": {
    "contributors": [
      {
        "name": "Doe, John"
      }
    ],
    "id": "2",
    "owner": 1,
    "title": "Some title"
  },
  "revision": 0,
  "updated": "2019-03-13T10:39:57.345895+00:00"
}
```
**Tip**: Save somewhere the `id` value of this value!

Our new record was successfully created!

## Search for our new record

**Checkpoint 2**: At this point we have created our new record and we are able to search it. Let's do this!

**Note**: Make sure you have up and running our development server by running the `/scripts/server` script.

Let's search now for our newly created record in `https://localhost:5000/api/records/`. Having the `id` of the
record we had created in the previous step we can search in the page for our record.


```json
{
  "aggregations": {...},
  "hits": {
    "hits": [
      {
        "created": "2019-03-13T10:39:57.345889+00:00",
        "id": "2",
        "links": {
          "self": "https://localhost:5000/api/records/2"
        },
        "metadata": {
          "contributors": [
            {
              "name": "Doe, John"
            }
          ],
          "id": "2",
          "owner": 1,
          "title": "Some title"
        },
        "revision": 0,
        "updated": "2019-03-13T10:39:57.345895+00:00"
      },
      {...}
    ],
    "total": 2
  },
  "links": {
    "self": "https://localhost:5000/api/records/?page=1&sort=mostrecent&size=10"
  }
}
```

## Manipulate response using serializers

Here you can see the data returned from the search regarding our record. The output of each result is controlled
by our `serializers`. These entities are responsible for getting the internal representation of our data and transform
it in an output that the users of our system will see when they will use our api.

The `serializers` are using also a `Marshmallow` schema to validate the internal data and define which information should be returned. This means that if we want to hide some data and don't return every available information all we need to do is just
not define it in the `Marshmallow` schema.

For example, from the above output we want to display only when the record was `updated` and not when was `created`. In order to
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

Then now if search again we will take the following result:

```json
{
  "aggregations": {...},
  "hits": {
    "hits": [
      {
        "id": "2",
        "links": {
          "self": "https://localhost:5000/api/records/2"
        },
        "metadata": {
          "contributors": [
            {
              "name": "Doe, John"
            }
          ],
          "id": "2",
          "title": "Some title"
        },
        "revision": 0,
        "updated": "2019-03-13T10:39:57.345895+00:00"
      },
      {...}
    ],
    "total": 2
  },
  "links": {
    "self": "https://localhost:5000/api/records/?page=1&sort=mostrecent&size=10"
  }
}
```
