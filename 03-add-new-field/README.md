# Tutorial 03 - Data models: Adding a new field

The goal of this tutorial is to learn how to update your datamodel. We will show how you going to
update your [`JSONSchema`](https://json-schema.org/) to store the new field in the DB and your ES mapping so you can index it.
Moreover we will learn how [`Marshmallow`](https://marshmallow.readthedocs.io) schema can be used to validate your data.

If you have a lot of steps, add some shortcuts

[Step 1](#step-1) | [Step 2](#step-2) | [Step 3](#step-3) | [Step 4](#step-4)

## Step 1

Start from a clean and working instance:

```bash
$ cd 03-add-new-field/
$ ./init.sh
```

## Step 2

Our use case: we have created our data model and we want to update it by adding a new field. Let's
call that field `owner` and it will be an integer that represents the owner of the corresponding
record.

First thing we need to do is update our record schema in order to be able to store the new field in
the DB.

We edit the `jsonschemas/records/record-v10.0.json` file:

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

Now our system can validate and store our new field correctly in the DB. Now we want to enable search of a record by this new field. For this purpose we need to update the mapping of our ES index in order to add our new field. By doing that we let ES know how to handle our new field(field type, searchable, analyzable, etc.).

So, in order to update the mapping we edit the `/mappings/v6/records/record-v10.0.json` file:

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

Now in order to **reflect our changes** in our system we will have to run the `setup` script. With that we start fresh our DB and ES along with the updated information about schemas and mappings.


Checkpoint: At this point we are able to create a new record in our system that includes our new field. Let's do this!

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
