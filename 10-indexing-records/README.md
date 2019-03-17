# Tutorial 10 - Data models: modify records before indexing

The goal of this tutorial is to learn how to take advantage of ElasticSearch by manipulating records fields when indexing.

Jump to: [Step 1](#step-1) | [Step 2](#step-2) | [Step 3](#step-3)

Let's imagine that we now have a new use case: when retrieving a list of records from our REST endpoint, we would like to have an extra field for each record that counts the number of contributors. Moreover, we actually don't need the `keywords` field, so we can remove it.
For example, given the following record:

```json
{
  "id": 1,
  "title": "Invenio is awesome",
  "keywords": ["invenio", "CERN"],
  "contributors": [
    {
      "name": "Stark, Tony"
    },
    {
      "name": "Kent, Clark"
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
      "name": "Stark, Tony"
    },
    {
      "name": "Kent, Clark"
    }
  ],
  "contributors_count": 2
}
```

Let's see how to do it.

## Step 1

Start from a clean and working instance:

```bash
$ cd 10-indexing-records/
$ ./init.sh
```

## Step 2

We are going to take advantage of the `invenio-indexer` signal [before_record_index](https://github.com/inveniosoftware/invenio-indexer/blob/master/invenio_indexer/signals.py) to modify the record fields before indexing.
This signal [is called](https://github.com/inveniosoftware/invenio-indexer/blob/master/invenio_indexer/api.py#L305) every time and just before indexing a record.

Create a new file `indexer.py` and copy the following code:

`my-site/my_site/records/indexer.py`

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

`my-site/my_site/records/ext.py`

```diff
from __future__ import absolute_import, print_function

+from invenio_indexer.signals import before_record_index
+from .indexer import indexer_receiver
from . import config

...

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['my-site'] = self
+       before_record_index.connect(indexer_receiver, sender=app, weak=False)
```

Finally, let's change the ElasticSearch mappings to update the fields that we have changed.

`my-site/my_site/records/mappings/v6/records/record-v1.0.0.json`

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

## Step 3

The code is now ready and we can try it. Since we have changed the ElasticSearch mappings, we need to re-create them.

```bash
$ pipenv run pip install -e .
$ pipenv run invenio index destroy --force --yes-i-know
$ pipenv run invenio index init --force
$ pipenv run invenio index queue init purge
```

Let's re-index all records:

```bash
$ pipenv run invenio index reindex --pid-type recid --yes-i-know
$ pipenv run invenio index run
```

We can now create a new record, using the deposit of the previous exercise, and verify that in ElasticSearch we will can see the modified fields.

```bash
$ ./scripts/server
$ firefox http://127.0.0.1:9200/records/_search?pretty=true
```

Let's try to add a record with more contributors:

```bash
$ curl -k --header "Content-Type: application/json" \
    --request POST \
    --data '{"title": "Invenio is awesome", "contributors": [{"name": "Kent, Clark"}, {"name": "Wayne, Bruce"}, {"name": "Stark, Tony"}], "owner": 1}' \
    https://127.0.0.1:5000/api/records/?prettyprint=1
$ firefox http://127.0.0.1:9200/records/_search?pretty=true
```

The `contributors_count` field for the last created record should have value `3`.

## What did we learn

- We have seen how to connect to a signal
- We have learned how to modify data before indexing
- Finally, how to re-index all our records
