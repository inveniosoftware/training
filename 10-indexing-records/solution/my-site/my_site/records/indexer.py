"""Record modification prior to indexing."""

from __future__ import absolute_import, print_function


def indexer_receiver(
        sender,
        json=None,
        record=None,
        index=None,
        doc_type=None,
        arguments=None
):
    """Connect to before_record_index signal to transform record for ES.

    :param sender: The Flask application
    :param json: The dumped record dictionary which can be modified.
    :param record: The record being indexed.
    :param index: The index in which the record will be indexed.
    :param doc_type: The doc_type for the record.
    :param arguments: The arguments to pass to Elasticsearch for indexing.
    """
    # delete the `keywords` field before indexing
    if 'keywords' in json:
        del json['keywords']

    # count the number of contributors and add the new field
    contributors = json.get('contributors', [])
    json['contributors_count'] = len(contributors)
