# Tutorial 02 - Tour of Invenio

In this tutorial, we will explore Invenio from a user's perspective. We will
see the different parts of the user interface, explore the REST API and create
and search for records.

## Table of Contents

- [Step 1: Prerequisites](#step-1-prerequisites)
- [Step 2: Register a user](#step-2-register-a-user)
- [Step 3: Go through the account settings](#step-3-go-through-the-account-settings)
- [Step 4: Access the records REST API](#step-4-access-the-records-rest-api)
- [Step 5: Search and Record UI](#step-5-search-and-record-ui)
- [Step 6: Create an admin user through the CLI](#step-6-create-an-admin-user-through-the-cli)
- [Step 7: Access the Admin Panel](#step-7-access-the-admin-panel)
- [Step 8: Access the OAI-PMH endpoint](#step-8-access-the-oai-pmh-endpoint)
- [What did we learn](#what-did-we-learn)

## Step 1: Prerequisites

First ensure you have initialized your Invenio instance according to [the
previous tutorial](../01-getting-started), that you are running the
development server and that you have your browser open at the web application's
front page.

## Step 2: Register a user

First thing we need to do is register a user. Click on the "Sign-up" button, at
the top right of the page:

![Sign up button](images/sign-up-button.png)

You will be redirected to the user registration form, where you should fill-in
an email address and password:

![Sign up form](images/sign-up-form.png)

You will then be redirected to the front page, now being logged-in as the user
you registered. A verification email will be sent to the address you provided:

![Successful registration page](images/register-success.png)

**Note:** The email with the confirmation link is not actually being sent
since we are running a development server. You will see the body of the email
being output in the terminal logs of the web app.

## Step 3: Go through the account settings

Now that you have created a user, let's have a look at the available settings
pages for the user. If you click at your user's email address you will be
redirected to the User Profile page. Here you can set things like a username
or the full name of the user, or change the account's email address.

![Settings page, profile tab](images/settings-profile.png)

On the left side of the page, you can see the other settings pages listed. The
Change password, as you would expect is a page where you can change your
account's password:

![Settings page, change password tab](images/settings-password.png)

The "Security" page is where you can see a list all of the logged-in sessions
for the account. You can see there information about the IP address, browser
and other information about each session. You can also force a "Logout" of an
active session, for security purposes:

![Settings page, security tab](images/settings-security.png)

Last, but not least, the "Applications" settings page, is where you can manage
access tokens used to authenticate your user for REST API access. This is also
the place where you can manage your own OAuth applications to implement
integrations with your Invenio instance:

![Settings page, applications tab](images/settings-application.png)

## Step 4: Access the records REST API

Your new instance exposes a REST API for performing CRUD operations on records
(we will discuss in detail what a "record" is in later sessions).

Let's create a record with some minimal metadata by performing a POST request
to the `/api/records/` endpoint with a JSON payload:

```bash
$ curl -k --header "Content-Type: application/json" \
    --request POST \
    --data '{"title": "Some title", "contributors": [{"name": "Doe, John"}]}' \
    https://localhost:5000/api/records/?prettyprint=1
{
  "created": "2020-05-12T00:28:31.140277+00:00",
  "id": "1",
  "links": {
    "files": "https://localhost:5000/api/records/1/files",
    "self": "https://localhost:5000/api/records/1"
  },
  "metadata": {
    "contributors": [
      {
        "name": "Doe, John"
      }
    ],
    "id": "1",
    "title": "Some title"
  },
  "revision": 0,
  "updated": "2020-05-12T00:28:31.140284+00:00"
}
```

We can retrieve this newly created record by making a `GET /api/records/1`
request:

```bash
$ curl -k https://localhost:5000/api/records/1?prettyprint=1
{
  "created": "2020-05-12T00:28:31.140277+00:00",
  "id": "1",
  "links": {
    "files": "https://localhost:5000/api/records/1/files",
    "self": "https://localhost:5000/api/records/1"
  },
  "metadata": {
    "contributors": [
      {
        "name": "Doe, John"
      }
    ],
    "id": "1",
    "title": "Some title"
  },
  "revision": 0,
  "updated": "2020-05-12T00:28:31.140284+00:00"
}%
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
        "created": "2020-05-12T00:28:31.140277+00:00",
        "id": "1",
        "links": {
          "files": "https://localhost:5000/api/records/1/files",
          "self": "https://localhost:5000/api/records/1"
        },
        "metadata": {
          "contributors": [
            {
              "name": "Doe, John"
            }
          ],
          "id": "1",
          "title": "Some title"
        },
        "revision": 0,
        "updated": "2020-05-12T00:28:31.140284+00:00"
      }
    ],
    "total": 1
  },
  "links": {
    "self": "https://localhost:5000/api/records/?sort=mostrecent&size=10&page=1"
  }
}
```

**Note:** By default this API doesn't require any authentication. We will
address this in later sessions.

## Step 5: Search and Record UI

The REST API is not the only way to display information on records. If you
navigate to the front page and click the search button you will go the
records search page:

![Front page search bar](./images/frontpage-search.png)

On the search page, besides the actual results, you can also see the total
number of results, paginate through them and sort by various options.

![Search page](./images/search-page.png)

Let's create some more records, to demonstrate the querying capabilities:

![Search page with result list](./images/search-more-records.png)

Let's say, we want to get all of the records written by "Smith" we could
naively type `Smith` in the search box, but that would give us all records that
contain the text "Smith" in any of their fields (even the title):

![Search query](./images/search-query.png)

To refine our results we can search on a specific field by searching for
something like `contributors.name:Smith`:

![Search query fields](./images/search-field-query.png)

If you click on any of the record results you will be redirected to the
record's page, which at the moment displays in a very basic way the metadata:

![Result record page](./images/record-page.png)

## Step 6: Create an admin user through the CLI

Let's a crete a new user and give them admin permissions to the instance:

```bash
$ cd my-site
$ pipenv run invenio users create admin@invenio.org --password 123456 --active
User created successfully.
{'email': 'admin@invenio.org', 'password': '****', 'active': True}
$ pipenv run invenio roles add admin@invenio.org admin
Role "admin - None" added to user "User <id=2, email=admin@invenio.org>" successfully.
```

## Step 7: Access the Admin Panel

If you now login as the newly created `admin@invenio.org` user with password
`123456`, a new "Administration" option will be visible in the user menu:

![User menu administration option](./images/admin-options.png)

If you click on it, you will be redirected to the Admin panel page, where you
can manage a variety of internal entities for your Invenio instance:

![Records administration page](./images/admin-records.png)
![Users administration page](./images/admin-users.png)

## Step 8: Access the OAI-PMH endpoint

The instance also provides by default an OAI-PMH endpoint at
<https://localhost:5000/oai2d>. Let's access the `Identify` verb via `curl`:

```bash
$ curl -k "https://localhost:5000/oai2d?verb=Identify"
<?xml version='1.0' encoding='UTF-8'?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
  <responseDate>2019-03-18T23:21:19Z</responseDate>
  <request verb="Identify">https://localhost:5000/oai2d</request>
  <Identify>
    <repositoryName>My site</repositoryName>
    <baseURL>https://localhost:5000/oai2d</baseURL>
    <protocolVersion>2.0</protocolVersion>
    <adminEmail>info@inveniosoftware.org</adminEmail>
    <earliestDatestamp>0001-01-01T00:00:00Z</earliestDatestamp>
    <deletedRecord>no</deletedRecord>
    <granularity>YYYY-MM-DDThh:mm:ssZ</granularity>
  </Identify>
</OAI-PMH>
```

## What did we learn

- How to register a user and the UI views a registered user has access to
- Basic REST API operations
- How to use the search and record UI pages
- How to create an admin user and access the Admin panel
- Where the OAI-PMH endpoint is
