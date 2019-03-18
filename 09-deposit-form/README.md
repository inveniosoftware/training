# Tutorial 09 - Data models: build a simple deposit form

The goal of this tutorial is to learn how we can build a new simple form to be able to deposit new records. The `invenio-deposit` module is not in the scope of this exercise.

Jump to: [Step 1](#step-1) | [Step 2](#step-2) | [Step 3](#step-3) | [Step 4](#step-4) | [Step 5](#step-5) | [Step 6](#step-6) | [Step 7](#step-7) | [Step 8](#step-8) | [Step 9](#step-9)

We now have to enable users to deposit new records. For this exercise, we won't use what `invenio-records-rest` already provides out-of-the-box, but we will implement a custom view.
We will need:
* to render a simple form to create a record, where the user can input the value of each field
* a new view where to post the form, validate the input and create the new record
* a new view to display a success message or an error

## Step 1

Start from a clean and working instance:

```bash
$ ./start-from.sh 08-data-models-from-scratch
```

## Step 2

We are going to create a new module in our project which will contain all our files.
Let's create a new module folder: `my-site/my_site/deposit/`. When creating a new module, do not forget to add `__init__.py`:

`my-site/my_site/deposit/__init__.py`

```python
"""Deposit module."""
```

Then, we create the form, using [Flask-WTF](https://flask-wtf.readthedocs.io).

`my-site/my_site/deposit/forms.py`

```python
"""Simple deposit form module."""

from __future__ import absolute_import, print_function

from flask_wtf import FlaskForm
from wtforms import StringField, validators


class RecordForm(FlaskForm):
    """A simple deposit form."""

    title = StringField(
        'Title', [validators.DataRequired()]
    )
    contributor_name = StringField(
        'Name of the contributor', [validators.DataRequired()]
    )
```

## Step 3

We have to create a new view for the form. We will take advantage of the HTTP verbs `GET`, to render the form, and `POST`, to handle the submitted data.

`my-site/my_site/deposit/views.py`

```python
"""Views for deposit of records."""

from __future__ import absolute_import, print_function

from flask import Blueprint, redirect, render_template, url_for

from .forms import RecordForm
from .api import create_record


# define a new Flask Blueprint that is register under the url path /deposit
blueprint = Blueprint(
    'deposit',
    __name__,
    url_prefix='/deposit',
    template_folder='templates',
    static_folder='static',
)

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    """The create view."""
    form = RecordForm()
    # if the form is submitted and valid
    if form.validate_on_submit():
        # we creare one contributor object with the submitted name
        contributors = [dict(name=form.contributor_name.data)]
        # create the record
        create_record(
          dict(
            title=form.title.data,
            contributors=contributors
          )
        )
        # redirect to the success page
        return redirect(url_for('deposit.success'))
    return render_template('deposit/create.html', form=form)


@blueprint.route("/success")
def success():
    """The success view."""
    return render_template('deposit/success.html')
```

Templates creation: create a folder `templates` and a subfolder `deposit` (the name of the blueprint). Then, inside, two html files (our Jinja templates): `create.html` and `success.html`.

`my-site/my_site/deposit/templates/deposit/create.html`

```html
{%- extends config.BASE_TEMPLATE %}

{% macro errors(field) %}
  {% if field.errors %}
  <span class="help-block">
    <ul class=errors>
    {% for error in field.errors %}
      <li>{{ error }}</li>
    {% endfor %}
    </ul>
  {% endif %}
  </span>
{% endmacro %}

{% block page_body %}
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h2>Create record</h2>
      </div>
      <div class="col-md-offset-3 col-md-6 well">
        <form action="{{ url_for('deposit.create') }}" method="POST">
            <div class="form-group {{ 'has-error' if form.title.errors }}">
              <label for="title">{{ form.title.label }}</label>
              {{ form.title(class_="form-control")|safe }}
              {{ errors(form.title) }}
            </div>
            <div class="form-group {{ 'has-error' if form.contributor_name.errors }}">
              <label for="contributor_name">{{ form.contributor_name.label }}</label>
              {{ form.contributor_name(class_="form-control")|safe }}
              {{ errors(form.contributor_name) }}
            </div>
            {{ form.csrf_token }}
            {{ errors(form.csrf_token) }}
            <button type="submit" class="btn btn-default">Create</button>
        </form>
      </div>
    </div>
  </div>
{% endblock page_body %}
```

`my-site/my_site/deposit/templates/deposit/success.html`

```html
{%- extends config.BASE_TEMPLATE %}

{% block page_body %}
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <div class="alert alert-success">
          <b>Success!</b>
        </div>
        <a href="{{ url_for('deposit.create') }}" class="btn btn-warning">Create more</a>
      </div>
    </div>
  </div>
{% endblock page_body %}
```

### Step 6

We will now implement the `create_record` method: its responsabilities are to create the record in the database, mint a new persistent identifier and index it to make it searchable.

`my-site/my_site/deposit/api.py`

```python
"""Deposit APIs."""

from __future__ import absolute_import, print_function

import uuid

from flask import current_app
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore import current_pidstore
from invenio_records.api import Record


def create_record(data):
    """Create a record.

    :param dict data: The record data.
    """
    with db.session.begin_nested():
        # create uuid
        rec_uuid = uuid.uuid4()
        # create PID
        current_pidstore.minters['recid'](rec_uuid, data)
        # create record
        created_record = Record.create(data, id_=rec_uuid)
        # index the record
        RecordIndexer().index(created_record)
    db.session.commit()
```

### Step 7

Last step: add the new view in the app entrypoints. When the Invenio app will run, it will find the new blueprint and register its routes.

Add this in `my-site/setup.py`:

```diff
        'invenio_base.blueprints': [
            'my_site = my_site.theme.views:blueprint',
            'my_site_records = my_site.records.views:blueprint',
+           'deposit = my_site.deposit.views:blueprint',
        ],
        'invenio_config.module': [
            'my_site = my_site.config',
        ],
```

Finally, re-install the app to register the entrypoints:

```bash
$ pipenv run pip install -e .
```

## Step 9

Try it! Ensure `docker-compose` is running and reload the server (if not done already automatically):

```bash
$ ./scripts/server
$ firefox https://127.0.0.1/deposit/create
```

Now, create a record and verify it is indexed correctly:

```bash
$ firefox https://127.0.0.1:5000/api/records/?prettyprint=1
```

## What did we learn

- We have seen how to create a new view with templates
- We have built a new form with validation
- We learned how to create a record minting its PID and then index it
