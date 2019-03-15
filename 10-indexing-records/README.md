# Tutorial 10 - Data models: modify records before indexing

The goal of this tutorial is to learn how to take advantage of ElasticSearch to index records in a format that can be more adapted to our needs.

Jump to: [Step 1](#step-1) | [Step 2](#step-2) | [Step 3](#step-3) | [Step 4](#step-4)

Let's say that we now have a new use case: when retrieving a list of records, we would like to have an extra field for each record that counts the number of contributors. Moreover, we actually don't need the `keywords`, so we can remove them.
For example, given the following record:

```json
{
  "id": 1,
  "title": "Invenio is awesome",
  "keywords": ["invenio", "CERN"],
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

it would be handy to have an extra field `contributors_count` that has value `2` and skip the `keywords` field, like this:

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
  ],
  "contributors_count": 2
}
```

Let's see how to do it.

## Step 1

Start from a clean and working instance:

```bash
$ cd 05-linking-records-index/
$ ./init.sh
```

## Step 2

We are going to take advantage of the `invenio-indexer` signal [before_record_index](https://github.com/inveniosoftware/invenio-indexer/blob/master/invenio_indexer/signals.py) to modify the record before indexing.
This signal [is called](https://github.com/inveniosoftware/invenio-indexer/blob/master/invenio_indexer/api.py#L305) every time and just before indexing a record.

Create a new file `indexer.py` and copy the following code:

`my_site/indexer.py`

```python
"""Record modification prior to indexing."""

from __future__ import absolute_import, print_function

def indexer_receiver(sender, json=None, record=None, index=None, doc_type=None):
    """Connect to before_record_index signal to transform record for ES.

    :param json: The dumped record dictionary which can be modified.
    :param record: The record being indexed.
    :param index: The index in which the record will be indexed.
    :param doc_type: The doc_type for the record.
    """

    # delete the `keywords` field before indexing
    if 'keywords' in json:
        del json['keywords']

    # count the number of contributors and add the new field
    contributors = json.get('contributors', [])
    json['contributors_count'] = len(contributors)
```

Now we need to register the signal in our Invenio instance. Change the `ext.py` to connect the signal.

`my_site/ext.py`

```diff
from __future__ import absolute_import, print_function

+from invenio_indexer.signals import before_record_index
+from .indexer import indexer_receiver
from . import config


class Mysite(object):
    """My site extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)
+       self.register_signals()
+
+    def register_signals(self):
+        """Register signals."""
+       before_record_index.connect(indexer_receiver, sender=app, weak=False)
+
```

Finally, let's change the ElasticSearch mappings to update the fields that we have changed.

`my_site/records/mappings/v6/records/record-v1.0.0.json`

```diff
         "id": {
          "type": "keyword"
        },
-       "keywords": {
-         "type": "keyword"
-       },
        "publication_date": {
          "type": "date",
          "format": "date"
        },
+       "contributors_count": {
+         "type": "short"
+       },
        "contributors": {
          "type": "object",
          "properties": {
```

// TODO: change serializers?

## Step 3

The code is now ready and we can try it (we will write a few tests later on). We need to re-index:

```bash
$ invenio index reindex --pid-type recid --yes-i-know
$ invenio index run
$ ./script/server
$ firefox https://127.0.0.1:5000/api/records/
```

## Step 4

// TODO: add tests

## What did we learn

- We have seen how to connect to a signal
- We have learned how to modify data before indexing
- Finally, how to re-index all our records
