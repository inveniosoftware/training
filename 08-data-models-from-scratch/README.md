# Tutorial 08 - Data models: Build from scratch

In this session we will learn how to build a new data model from scratch. During that
process we will see how to create a new REST **module** for our model and provide functionalities
such as storing and searching.

## Table of contents

- [Tutorial 08 - Data models: Build from scratch](#tutorial-08---data-models-build-from-scratch)
  - [Table of contents](#table-of-contents)
  - [Step 1: Bootstrap exercise](#step-1-bootstrap-exercise)
    - [1.1](#11)
    - [1.2](#12)
  - [Step 2: Create an `Authors` flask extension](#step-2-create-an-authors-flask-extension)
    - [Actions](#actions)
  - [Step 3: Internal representation: JSONSchema and Elasticsearch mappings](#step-3-internal-representation-jsonschema-and-elasticsearch-mappings)
    - [Actions](#actions-1)
  - [Step 4: External representation: loaders and serializers](#step-4-external-representation-loaders-and-serializers)
    - [Actions](#actions-2)
  - [Step 5: Data validation: Marshmallow](#step-5-data-validation-marshmallow)
    - [Actions](#actions-3)
  - [Step 6: Persistent identifiers](#step-6-persistent-identifiers)
    - [Actions](#actions-4)
  - [Step 7: Create an author](#step-7-create-an-author)
  - [What did we learn](#what-did-we-learn)

## Step 1: Bootstrap exercise

### 1.1

If you completed the previous tutorial, you can skip this step. If instead you would like to start from a clean state run the following commands:

```bash
cd ~/src/training/
./start-from.sh 07-data-models-new-field
```

### 1.2

**Note**: In order to reduce the amount of code that we need to write we have prepared beforehand the module structure in `/08-data-models-from-scratch/author_module` folder in which will go through and **uncomment** the needed code snippets to enable different functionalities and eventually build our module!

Run the below command to copy the module over:

```bash
./bootstrap.sh
```

You should now see in your application folder a newly created `authors` folder which will be the module we will develop through this tutorial.

## Step 2: Create an `Authors` flask extension

First thing we need to do is to create an extension called `Authors` and register it in our `setup.py` so our Invenio application can know about it.

### Actions

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

## Step 3: Internal representation: JSONSchema and Elasticsearch mappings

Now that we have our extension registered, we need to tell Invenio how the internal representation of our data model is. To do so, we use [a JSONSchema](author_module/my_site/authors/jsonschemas/authors/author-v1.0.0.json) and [an Elasticsearch mapping](author_module/my_site/authors/mappings/v7/authors/author-v1.0.0.json): the former to validate the internal JSON format and the latter to tell Elasticsearch what shape our data model has so it can handle correctly its values.

### Actions

- Uncomment the entrypoints in `setup.py`:

  ```diff
  'invenio_jsonschemas.schemas': [
        'my_site = my_site.records.jsonschemas',
  - #   'authors = my_site.authors.jsonschemas'
  +     'authors = my_site.authors.jsonschemas'
  ],
  'invenio_search.mappings': [
       'records = my_site.records.mappings',
  - #  'authors = my_site.authors.mappings'
  +    'authors = my_site.authors.mappings'
  ],
  ```

- Uncomment the following line from `my_site/authors/config.py`:

    ```diff
    - # search_index='authors',
    + search_index='authors',
    ```

By doing this we told Invenio to register our new schema and mapping. We are also defining the name of the Elasticsearch index which will be created to enable author search.

## Step 4: External representation: loaders and serializers

So far we have a new extension which defines how our data model is **stored** and **searchable**, but have not yet provided means to transform this data when it's received or served by Invenio. To do so, we will introduce two new concepts: **loaders** whose responsibility is to transform incoming data to the internal format, and **serializers** which will be in charge of transforming the internal data to a different format, based on our needs.

### Actions

For creating and registering our **loaders** we should:

- Uncomment the code in the `my_site/authors/loaders/__init__.py`
- Uncomment the following lines from `my_site/authors/config.py`.

  ```diff
  - # record_loaders={
  - #     'application/json': ('my_site.authors.loaders'
  - #                          ':json_v1'),
  - # },
  + record_loaders={
  +     'application/json': ('my_site.authors.loaders'
  +                          ':json_v1'),
  + },
  ```

For creating and registering the **record serializers** we should:

- Uncomment the `json_v1_response` variable in the `my_site/authors/serializers/__init__.py`
- Uncomment the following lines from `my_site/authors/config.py`.

  ```diff
  - # record_serializers={
  - #     'application/json': ('my_site.authors.serializers'
  - #                          ':json_v1_response'),
  - # },
  + record_serializers={
  +     'application/json': ('my_site.authors.serializers'
  +                          ':json_v1_response'),
  + },
  ```

For creating and registering the **search serializers** we should:

- Uncomment the `json_v1_search` variable in the `my_site/authors/serializers/__init__.py`
- Uncomment the following lines from `my_site/authors/config.py`.

  ```diff
  - # search_serializers={
  - #     'application/json': ('my_site.authors.serializers'
  - #                          ':json_v1_search'),
  - # },
  + search_serializers={
  +     'application/json': ('my_site.authors.serializers'
  +                          ':json_v1_search'),
  + },
  ```

During the first step, we registered our **loader** in the configuration of our new `authors` endpoint. Now every time we try to create a new author the loader is going to transform the incoming data to match the internal representation of an author document in our system.

In the upcoming steps, we created and registered our serializers. We split them into two categories: **Record serializers** and **Search serializers**. The first is used to **serialize** the internal representation of one specific record (e.g author) while the latter is transforming each record result of a search. They are capable of doing that by using again a `Marshmallow` schema which we will explain in detail in the next section.

## Step 5: Data validation: Marshmallow

In the previous section we have configured loaders and serializers but we also started to configure our first validation check by making reference to two Marshmallow schemas. These schemas will make sure that the data has the correct format both when it arrives to the system and when it is returned to the user.

### Actions

- Uncomment the code in the `my_site/authors/marshmallow/json.py`

Here we have added two classes which we made reference in the previous step, `AuthorMetadataSchemaV1` and `AuthorSchemaV1`. The first will take care of validating incoming author metadata and the second will take care of validating the author output format. Marshmallow is not mandatory, but highly recommended since it can do from simple validations to complex ones, for more information visit [Marshmallow documentation](https://marshmallow.readthedocs.io/en/2.x-line/).

## Step 6: Persistent identifiers

So far we have only cared about our content and its format, but we need to provide a way to retrieve our records. We are doing this by using PIDs, and the difference with normal IDs is that they do not change over time to avoid broken references.

Having identifiers which do not change over time adds certain complexity to the system. We need to have a way of generating new PIDs, which what we will reference as **minters** and we will also need a way of identifying the PID inside the record metadata, this is what **fetchers** do.

### Actions

- Uncomment the code in `my_site/authors/fetchers.py`
- Uncomment the code in `my_site/authors/minters.py`
- Uncomment the following lines from `my_site/authors/config.py`:

  ```diff
  pid_type='authid',
  - # pid_minter='authid',
  - # pid_fetcher='authid',
  + pid_minter='authid',
  + pid_fetcher='authid',
  default_endpoint_prefix=True,
  ```

- Uncomment the following lines from `my-site/setup.py`.

  ```diff
  - # 'invenio_pidstore.fetchers': [
  - #     'authid = my_site.authors.fetchers:author_pid_fetcher'
  - # ],
  - # 'invenio_pidstore.minters': [
  - #     'authid = my_site.authors.minters:author_pid_minter'
  - # ],
  + 'invenio_pidstore.fetchers': [
  +     'authid = my_site.authors.fetchers:author_pid_fetcher'
  + ],
  + 'invenio_pidstore.minters': [
  +     'authid = my_site.authors.minters:author_pid_minter'
  + ],
  ```

This is how we are registering our new minter and fetcher making them available.

**Important**: the value of the `pid_minter` and the `pid_fetcher` defined in `config.py` should match exactly with the entrypoint names defined in `setup.py`. Also, we should make sure that the `pid_type` value and the `RECORDS_REST_ENDPOINTS` endpoint key match exactly.

## Step 7: Create an author

In order to reflect our changes in the database and Elasticsearch but also to register our new entrypoints in Invenio we need to run the following commands:

```console
pipenv run pip install -e . # register entrypoints and update our applications code
./scripts/setup # reset DB and ES, create new index
./scripts/server # start invenio
```

We can now create new authors:

```bash
$ curl -k --header "Content-Type: application/json" \
    --request POST \
    --data '{"name":"John Doe"}' \
    https://127.0.0.1:5000/api/authors/\?prettyprint\=1
{
  "created": "2019-03-17T16:01:07.148176+00:00",
  "id": "1",
  "metadata": {
    "id": "1",
    "name": "John Doe"
  },
  "updated": "2019-03-17T16:01:07.148181+00:00"
}
```

Now we can search in the `/api/authors/` endpoint to see if our new author is there:

```bash
$ curl -k "https://127.0.0.1:5000/api/authors/?prettyprint=1"
{
  "aggregations": {
    "name": {
      "buckets": [
        {
          "doc_count": 1,
          "key": "John Doe"
        }
      ],
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0
    }
  },
  "hits": {
    "hits": [
      {
        "created": "2019-03-17T15:55:53.927754+00:00",
        "id": "1",
        "metadata": {
          "id": "1",
          "name": "John Doe"
        },
        "updated": "2019-03-17T15:55:53.927761+00:00"
      }
    ],
    "total": 1
  },
  "links": {
    "self": "https://127.0.0.1:5000/api/authors/?page=1&sort=mostrecent&size=10"
  }
}
```

If we want to retrieve the information about a specific author and we already know its `PID` then we can use the `/api/authors/<id>` endpoint:

```bash
$ curl -k "https://127.0.0.1:5000/api/authors/1?prettyprint=1"
{
  "created": "2019-03-17T15:55:53.927754+00:00",
  "id": "1",
  "metadata": {
    "id": "1",
    "name": "John Doe"
  },
  "updated": "2019-03-17T15:55:53.927761+00:00"
}
```

## What did we learn

- How to create a new Invenio module
- How to define a REST endpoints connected to our data model
- How to create Elasticsearch mappings
- How to create JSONSchemas
- How to define and use loaders and serializers
- How to use minters and fetchers to manipulate PIDs
