# Tutorial 07 - Data models: link records using references

The goal of this tutorial is to learn how we can link records using references, with a technique similar to [JSON Reference](https://json-spec.readthedocs.io/reference.html).

Jump to: [Step 1](#step-1) | [Step 2](#step-2) | [Step 3](#step-3) | [Step 4](#step-4)

//TODO: fix link
In tutorial 0X, we have learned how to create a new data model, the author record. It would be now very useful to link a record to his author so that, when using the REST APIs to return records, we can immediately return also the details of the author without performing any extra query.
For example, given the following record:

```json
{
  "id": 1,
  "title": "Invenio is awesome",
  "contributors": [
    {
      "name": "Nicola Tarocco",
      "affiliations": ["CERN"],
      "email": "myemail@noreply.org",
    },
    {
      "name": "Spaghetti Code",
      "affiliations": ["CERN"],
      "email": "myemail@noreply.org",
    }
  ]
}
```

and the following author:

```json
{
  "id": 1,
  "firstname": "Nicola",
  "lastname": "Tarocco"
}
```

we would like to retrieve the record with the details of his author, in a similar way as a JOIN in the SQL world:

// TODO: fix fields for author
```json
{
  "author": {
    "id": 1,
    "firstname": "Nicola",
    "lastname": "Tarocco"
  },
  "id": 1,
  "title": "Invenio is awesome",
  "contributors": [
    {
      "name": "Nicola Tarocco",
      "affiliations": ["CERN"],
      "email": "myemail@noreply.org",
    },
    {
      "name": "Spaghetti Code",
      "affiliations": ["CERN"],
      "email": "myemail@noreply.org",
    }
  ],
}
```

Let's see how to do it.

## Step 1

Start from a clean and working instance:

```bash
$ cd 06-linking-records-reference/
$ ./init.sh
```

## Step 2

We need to add a new `$ref` field in the record data model to reference the author. Let's change it.

`my_site/records/jsonschemas/records/record-v1.0.0.json`

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
+     "required": [
+       "$ref"
+     ]
+   },
    "title": {
      "description": "Record title.",
      "type": "string"
    },
```

Since we have changed the data model, we need to change the ElasticSearch mappings.

`my_site/records/mappings/v6/records/record-v1.0.0.json`

```diff
+       "author": {
+         "type": "object",
+         "properties": {
+           "$ref": {
+             "type": "object",
+             "properties": {
+               TODO: add here
+             }
+           }
+         }
+       },
         "id": {
          "type": "keyword"
        },
```

// TODO: change serializers?

Now, let's modify our record

## Step 3

The

## Step 4

Re-index

## Step 5

Tests


## What did we learn

- Develop on Invenio
- Be happy!
- Understand something
