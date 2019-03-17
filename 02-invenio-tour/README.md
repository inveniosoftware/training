# Tutorial 02 - Tour of Invenio

In this tutorial, we will explore Invenio from a user's perspective. We will
see the different parts of the user interface, explore the REST API and create
and search for records.

## Step 1: Prerequisites

First ensure you have initialized your Invenio instance according to [the
previous tutorial](../01-getting-started), that you are running the
development server and that you have your browser open at the web application's
frontpage.

## Step 2: Register a user

First thing we need to do is register a user. Click on the "Sign-up" button, at
the top right of the page:

![](images/sign-up-button.png)

You will be redirected to the user registration form, where you should fill-in
an email address and password:

![](images/sign-up-form.png)

You will then be redirected to the frontpage, now being logged-in as the user
you registered. A verification email will be sent to the address you provided:

![](images/register-success.png)

**Note:** The email with the confifmration link is not actually being sent
since we are running a development server. You will see the body of the email
being output in the terminal logs of the web app.

## Step 3: Go through the account settings

Now that you have created a user, let's have a look at the available settings
pages for the user. If you click at your user's email address you will be
redirected to the User Profile page. Here you can set things like a username
or the full name of the user, or change the account's email address.

![](images/settings-profile.png)

On the left side of the page, you can see the other settings pages listed. The
"Change password", as you would expect is a page where you can change your
account's password:

![](images/settings-password.png)

The "Security" page is where you can see a list all of the logged-in sessions
for the account. You can see there information about the IP address, browser
and other information about each session. You can also force a "Logout" of an
active session, for security purposes:

![](images/settings-security.png)

Last, but not least, the "Applicatons" settings page, is where you can manage
access tokens used to authenticate your user for REST API access. This is also
the place where you can manage your own OAuth applications to implement
integrations with your Invenio instance:

![](images/settings-application.png)

## Step 4: Access the records REST API

Your new instance exposes a REST API for performing CRUD operations on records
(we will discuss in detail what a "record" is in later sessions).

Let's create a record with some minimal metadata by perfomring a POST request
to the `/api/records/` endpoint with a JSON payload:

```bash
$ curl -k --header "Content-Type: application/json" \
    --request POST \
    --data '{"title": "Some title", "contributors": [{"name": "Doe, John"}]}' \
    https://localhost:5000/api/records/?prettyprint=1

{
  "created": "2019-03-15T12:22:19.497592+00:00",
  "id": "1",
  "links": {"self": "https://localhost:5000/api/records/1"},
  "metadata": {
    "contributors": [{"name": "Doe, John"}],
    "id": "1",
    "title": "Some title"
  },
  "revision": 0,
  "updated": "2019-03-15T12:22:19.497596+00:00"
}
```

We can retrieve this newly created record by making a `GET /api/records/1`
request:

```bash
$ curl -k https://localhost:5000/api/records/1?prettyprint=1

{
  "created": "2019-03-15T12:22:19.497592+00:00",
  "id": "1",
  "links": {"self": "https://localhost:5000/api/records/1"},
  "metadata": {
    "contributors": [{"name": "Doe, John"}],
    "id": "1",
    "title": "Some title"
  },
  "revision": 0,
  "updated": "2019-03-15T12:22:19.497596+00:00"
}
```

We can search through all records by making a `GET /api/records/` request:

```bash
$ curl -k https://localhost:5000/api/records/?prettyprint=1

{
  "aggregations": {
    "keywords": {
      "buckets": [],
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0
    },
    "type": {
      "buckets": [],
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0
    }
  },
  "hits": {
    "hits": [
      {
        "created": "2019-03-15T12:22:19.497592+00:00",
        "id": "1",
        "links": {"self": "https://localhost:5000/api/records/1"},
        "metadata": {
          "contributors": [{"name": "Doe, John"}],
          "id": "1",
          "title": "Some title"
        },
        "revision": 0,
        "updated": "2019-03-15T12:22:19.497596+00:00"
      }
    ],
    "total": 1
  },
  "links": {
    "self": "https://localhost:5000/api/records/?page=1&sort=mostrecent&size=10"
  }
}
```

**Note:** By default this API doesn't require any authentication. We will
address this in later sessions.

## Step 5: Search and Record UI

Of the REST API is not the only way to display information on records. If you
navigate to the frontpage and click the search button you will go the
records search page:

![](./images/frontpage-search.png)

On the search page, besides the actual results, you can also see the total
number of results, paginate through them and sort by various options.

![](./images/search-page.png)

If you click on one of the record results you will be redirected to the
record's page, which at the moment displays in a very basic way the metadata:

![](./images/record-page.png)

## Step 6: Create an admin user through the CLI

Let's a crete a new user and give him admin permissions to the instance:

```bash
$ cd my-site
$ pipenv run invenio users create admin@invenio.org --password 123456 --active
{'email': 'admin@invenio.org', 'password': '****', 'active': True}
$ pipenv run invenio roles add admin@invenio.org admin
Role "admin - None" added to user "User <id=2, email=admin@invenio.org>" successfully.
```

## Step 7: Access the Admin Panel

If you now login as the newly created `admin@invenio.org` user with password
`123456`, a new "Administration" option will be visible in the user menu:

![](./images/admin-options.png)

If you click on it, you will be redirected to the Admin panel page, where you
can manage a variety of internal entities for your Invenio instance:

![](./images/admin-records.png)
![](./images/admin-users.png)
