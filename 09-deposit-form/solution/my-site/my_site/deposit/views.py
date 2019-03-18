"""Views for deposit of records."""

from __future__ import absolute_import, print_function

from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required
from flask_security import current_user

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
@login_required
def create():
    """The create view."""
    form = RecordForm()
    # if the form is submitted and valid
    if form.validate_on_submit():
        # we creare one contributor object with the submitted name
        contributors = [dict(name=form.contributor_name.data)]
        # set the owner as the current logged in user
        owner = int(current_user.get_id())
        # create the record
        create_record(
          dict(
            title=form.title.data,
            contributors=contributors,
            owner=owner,
          )
        )
        # redirect to the success page
        return redirect(url_for('deposit.success'))
    return render_template('deposit/create.html', form=form)


@blueprint.route("/success")
@login_required
def success():
    """The success view."""
    return render_template('deposit/success.html')
