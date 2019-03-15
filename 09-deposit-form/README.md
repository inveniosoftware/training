# Tutorial 07 - Data models: build a simple deposit form

The goal of this tutorial is to learn how we can build a new simple form to be able to deposit new records. The `invenio-deposit` module is not in the scope of this exercise.

Jump to: [Step 1](#step-1) | [Step 2](#step-2) | [Step 3](#step-3) | [Step 4](#step-4)

We now have to allow users to deposit new records. For this exercise, we won't use what `invenio-records-rest` already provides out-of-the-box, but we will implement a custom view.
We will need:
* to render a simple form to create a record, where the user can input the value of each field
* a new view where to post the form, validate the input and create the new record
* a new view to display a success message or an error

## Step 1

Start from a clean and working instance:

```bash
$ cd 06-build-simple-deposit-form/
$ ./init.sh
```

## Step 2

We are going to create a new module in our project which will contain all our files.
Let's create a new folder: `my_site/deposit/`. Then, we create the form, using [Flask-WTF](https://flask-wtf.readthedocs.io). Create a new file `my_site/deposit/forms.py` and type:

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

We now have to create the view to render the form and to receive the posted date. Ideally, you would take advantage of the HTTP verbs `GET` and `POST` in the same view to distinguish the operations, but in this example we will split it in 2 different views to show a more complete example.

Let's create a new file in `my_site/deposit/views.py`:

```python
"""Views for deposit of records."""

from __future__ import absolute_import, print_function

from flask import Blueprint, redirect, render_template, request, url_for
from flask_babelex import gettext as _

from .forms import RecordForm
from .utils import create_record


# define a new Flask Blueprint that is register under the url path /deposit
deposit_blueprint = Blueprint(
    'my_site_deposit',
    __name__,
    url_prefix='/deposit',
    template_folder='templates',
    static_folder='static',
)


@deposit_blueprint.route("/")
def index():
    """Index view."""
    return render_template("my_site_deposit/index.html")


@deposit_blueprint.route('/create', methods=('GET', 'POST'))
def create():
    """The create view."""
    form = RecordForm()
    # if the form is submitted and valid
    if form.validate_on_submit():
        # create the record
        create_record(
          dict(
            title=form.title.data,
            contributor_name=form.contributor_name.data
          )
        )
        # redirect to the success page
        return redirect(url_for('my_site_deposit.success'))
    return render_template('my_site_deposit/create.html', form=form)


@deposit_blueprint.route("/success")
def success():
    """The success view."""
    return render_template('my_site_deposit/success.html')
```

Now, add the related templates:

// TODO complete me
`my_site/deposit/`

success view should have a link the list results
list results should have a link to create button

### Step 6

Create the `create_record` method: PID, record, indexing

### Step 7

Register blueprint in the entrypoints

## Step 8

Tests


## What did we learn

- Develop on Invenio
- Be happy!
- Understand something
