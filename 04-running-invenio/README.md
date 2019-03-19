# Tutorial 04 - Running Invenio

In this session, we will explore basic concepts and commands that are useful
for the day-to-day development and running of an Invenio instance.

### Table of Contents

- [Step 1: Bring up the basic/development docker-compose setup](#step-1-bring-up-the-basicdevelopment-docker-compose-setup)
- [Step 2: Understanding your Python environment](#step-2-understanding-your-python-environment)
- [Step 3: Running an (I)Python shell](#step-3-running-an-ipython-shell)
- [Step 4: The `invenio` command](#step-4-the-invenio-command)
- [Step 5: `invenio shell`: interacting with the programmatic APIs](#step-5-invenio-shell-interacting-with-the-programmatic-apis)
- [Step 6: `invenio run`: running the web development server](#step-6-invenio-run-running-the-web-development-server)
- [Step 7: Running the Celery worker](#step-7-running-the-celery-worker)
- [Step 8: Entrypoints: where the magic happens](#step-8-entrypoints-where-the-magic-happens)
- [Step 9: Configuration loading](#step-9-configuration-loading)
- [What did we learn](#what-did-we-learn)

## Step 1: Bring up the basic/development docker-compose setup

First, let's bring back the basic development container setup:

```bash
# Bring down the full setup
$ docker-compose -f docker-compose.full.yml stop
$ docker-compose up -d
```

We are now running only the database, Elasticsearch, Redis and RabbitMQ
service containers.

## Step 2: Understanding your Python environment

When developing a Python project, we usually want to manage our environment in
an isolation manner (e.g. without affecting other Python applications or our
OS). One way to do this in Python is by using `virtualenv`s. A `virtualenv`
encapsulates in a folder the Python version we are running and our installed
Python packages (i.e. our dependencies).

When we initially run the `./scripts/bootstrap` command a Python 3.6
`virtualenv` was automatically created by the `pipenv` CLI tool, and all of our
Invenio instance's dependencies were installed.

Let's activate this `virtualenv` and see what we got:

```bash
# Let's see where the virtualenv was created
$ pipenv --venv
/home/bootcamp/.local/share/virtualenvs/my-site-7Oi5HgLM
# Let's activate the virtualenv through pipenv
$ pipenv shell
(my-site) $ python --version  # let's verify the Python version
Python 3.6.7
(my-site) $ pip freeze  # let's see what packages were installed
alabaster==0.7.12
alembic==1.0.8
amqp==2.4.2
angular-gettext-babel==0.3
apipkg==1.5
arrow==0.13.1
asn1crypto==0.24.0
atomicwrites==1.3.0
attrs==19.1.0
Babel==2.6.0
backcall==0.1.0
billiard==3.5.0.5
binaryornot==0.4.4
bleach==3.1.0
blinker==1.4
celery==4.2.1
...
```

## Step 3: Running an (I)Python shell

Let's bring up a Python shell:

```bash
(my-site) $ python
Python 3.6.7 (default, Oct 22 2018, 11:32:17)
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 2 + 2
4
>>> exit()  # or Ctrl-D

# Or an IPython shell...
(my-site) $ ipython
Python 3.6.7 (default, Oct 22 2018, 11:32:17)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.3.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import requests
In [2]: requests.get('https://httpbin.org/json')
Out[2]: <Response [200]>
In [3]: exit
```

## Step 4: The `invenio` command

From the Python packages that were installed we also got the `invenio` CLI
command which is used to interact with your instance:

```bash
(my-site) $ invenio --help
Usage: invenio [OPTIONS] COMMAND [ARGS]...

  Command Line Interface for Invenio.

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  access    Account commands.
  alembic   Perform database migrations.
  assets    Web assets commands.
  collect   Collect static files.
  db        Database commands.
  index     Manage search indices.
  instance  Instance commands.
  npm       Generate a package.json file.
  pid       PID-Store management commands.
  records   Records management.
  roles     Role commands.
  routes    Show the routes for the app.
  run       Runs a development server.
  shell     Runs a shell in the app context.
  tokens    OAuth2 server token commands.
  users     User commands.
  webpack   Webpack commands.
```

As you can see there is a variety of commands used for managing different parts
of the instance. Let's focus on two essential commands, `shell` and `run`.

## Step 5: `invenio shell`: interacting with the programmatic APIs

Let's run the `invenio shell` command:

```bash
(my-site) $ invenio shell
Python 3.6.7 (default, Oct 22 2018, 11:32:17)
[GCC 8.2.0] on linux
IPython: 7.3.0
App: invenio [production]
Instance: /home/bootcamp/.local/share/virtualenvs/my-site-7Oi5HgLM/var/instance
In [1]: app.config
Out[1]: {'ACCOUNTS_BASE_TEMPLATE': 'my_site/page.html',
 'ACCOUNTS_COVER_TEMPLATE': 'invenio_theme/page_cover.html',
 'ACCOUNTS_SESSION_REDIS_URL': 'redis://localhost:6379/1',
 'ACCOUNTS_SETTINGS_TEMPLATE': 'invenio_theme/page_settings.html',
 'ACCOUNTS_SITENAME': 'My site',
 'ACCOUNTS_USERINFO_HEADERS': True,
 'ACCOUNTS_USE_CELERY': True,
 'ADMIN_BASE_TEMPLATE': 'invenio_theme/page_admin.html',
 'ADMIN_LOGIN_ENDPOINT': 'security.login',
 ... }

In [2]: from invenio_accounts.models import User
In [3]: User.query.all()
Out[3]: [<User 1>, <User 2>]
In [4]: exit
```

The difference between a regular Python shell and one spawned via the `invenio
shell` command is that the latter has automatically loaded your application
context. This effectively means that all the configuration and extensions you
are using have been loaded and for that reason you can e.g. use high-level
programmatic APIs (like the `User` class to query the database), without having
to provide low-level details, like e.g. a DB connection string.

## Step 6: `invenio run`: running the web development server

First and foremost, our Invenio application is a web application. Let's run an
HTTPS web development server using the `invenio run` command:

```bash
(my-site) $ export FLASK_ENV=development
(my-site) $ invenio run \
    --cert ./docker/nginx/test.crt \
    --key ./docker/nginx/test.key
 * Environment: development
 * Debug mode: on
[2019-03-18 11:28:27,740] DEBUG in entrypoint: Loading config for entry point my_site = my_site.config
 * Running on https://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
[2019-03-18 11:28:32,375] DEBUG in entrypoint: Loading config for entry point my_site = my_site.config
[2019-03-18 11:28:33,125] DEBUG in entrypoint: Loading config for entry point my_site = my_site.config
 * Debugger is active!
 * Debugger PIN: 247-937-089
[2019-03-18 11:28:35,261] DEBUG in entrypoint: Loading config for entry point my_site = my_site.config
```

If you now navigate to <https://127.0.0.1:5000/> you will see the frontpage we
got to know in the previous sessions. Let's look at our console logs:

```bash
127.0.0.1 - - [18/Mar/2019 11:30:50] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [18/Mar/2019 11:30:51] "GET /static/dist/css/my-site-theme.4b596e8ec01854b4f9f6.css HTTP/1.1" 200 -
127.0.0.1 - - [18/Mar/2019 11:30:51] "GET /static/dist/js/manifest.efb16760b9de4e3f95a5.js HTTP/1.1" 200 -
127.0.0.1 - - [18/Mar/2019 11:30:51] "GET /static/dist/js/1.e5303e5d8fea8c843b1a.js HTTP/1.1" 200 -
127.0.0.1 - - [18/Mar/2019 11:30:51] "GET /static/dist/js/3.d9c64c473b78375ce5a6.js HTTP/1.1" 200 -
127.0.0.1 - - [18/Mar/2019 11:30:51] "GET /_debug_toolbar/static/js/jquery.js HTTP/1.1" 200 -
127.0.0.1 - - [18/Mar/2019 11:30:51] "GET /static/dist/js/4.b0eaa1403ef7e28f1b55.js HTTP/1.1" 200 -
127.0.0.1 - - [18/Mar/2019 11:30:51] "GET /static/images/invenio-white.svg HTTP/1.1" 200 -
127.0.0.1 - - [18/Mar/2019 11:30:51] "GET /static/dist/fonts/fontawesome-webfont.4b5a84a.woff2 HTTP/1.1" 200 -
127.0.0.1 - - [18/Mar/2019 11:30:52] "GET /static/apple-touch-icon-144-precomposed.png HTTP/1.1" 404 -
127.0.0.1 - - [18/Mar/2019 11:30:52] "GET /static/favicon.ico HTTP/1.1" 404 -
```

You can see a `GET /` request, followed by multiple `GET /static/...` requests
to fetch some static content (plus some `/_debug/...` requests, which we won't
discuss now).

We can of course access the REST API, by opening a terminal and running:

```bash
$ curl -k https://localhost:5000/api/records/?prettyprint=1
{
  "aggregations": {...},
  "hits": {
    "hits": [...]
  }
}
```

...which results to the following logs:

```bash
127.0.0.1 - - [18/Mar/2019 11:35:24] "GET /api/records/?prettyprint=1 HTTP/1.1" 200 -
```

What is important about the development server, is that it provides a much
smoother development experience for a number of reasons:

- Automatic server reloading on Python code changes
- DEBUG-level logging
- Stack traces for Python exceptions
- Integrations with debug/development-mode aware extensions

## Step 7: Running the Celery worker

Another integral part of an Invenio instance is background Celery workers. To
run these you have use the `celery` command:

```bash
(my-site) $ celery worker -A invenio_app.celery -l INFO

 -------------- celery@invenio v4.2.1 (windowlicker)
---- **** -----
--- * ***  * -- Linux-4.18.0-16-generic-x86_64-with-Ubuntu-18.04-bionic 2019-03-18 11:46:46
-- * - **** ---
- ** ---------- [config]
- ** ---------- .> app:         default:0x7fa1354a64a8 (.default.Loader)
- ** ---------- .> transport:   amqp://guest:**@localhost:5672//
- ** ---------- .> results:     redis://localhost:6379/2
- *** --- * --- .> concurrency: 1 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery


[tasks]
  . invenio_accounts.tasks.clean_session_table
  . invenio_accounts.tasks.send_security_email
  . invenio_indexer.tasks.delete_record
  . invenio_indexer.tasks.index_record
  . invenio_indexer.tasks.process_bulk_queue
  . invenio_mail.tasks.send_email
  . invenio_oaiserver.tasks.update_affected_records
  . invenio_oaiserver.tasks.update_records_sets

[2019-03-18 11:46:47,237: INFO/MainProcess] Connected to amqp://guest:**@127.0.0.1:5672//
[2019-03-18 11:46:47,253: INFO/MainProcess] mingle: searching for neighbors
[2019-03-18 11:46:48,406: INFO/MainProcess] mingle: all alone
[2019-03-18 11:46:48,509: INFO/MainProcess] celery@invenio ready.
```

Let's ship-off a Celery task to send an email to a user:

```bash
(my-site) $ invenio shell
Python 3.6.7 (default, Jan 20 2019, 17:24:36)
[GCC 7.3.0] on linux
IPython: 7.3.0
App: invenio [production]
Instance: /home/bootcamp/.local/share/virtualenvs/my-site-7Oi5HgLM/var/instance
In [1]: from invenio_mail.tasks import send_email
In [2]: message_data = {
   ...:     'sender': 'test@invenio.org',
   ...:     'recipients': ['example@invenio.org'],
   ...:     'subject': 'Greetings!',
   ...:     'body': 'Hi there user!',
   ...: }
In [3]: send_email.delay(data=message_data)
Out[3]: <AsyncResult: 3f592586-2b72-4da1-abca-20ac04f7fdd0>
```

You should be able to see log entries of the task running and finishing:

```
[2019-03-18 14:35:44,679: INFO/MainProcess] Received task: invenio_mail.tasks.send_email[209f9f5d-117d-448b-83f2-cf8d0b5123b1]
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Greetings!
From: test@invenio.org
To: example@invenio.org
Date: Mon, 18 Mar 2019 14:35:44 +0100
Message-ID: <155291614468.7058.17159562492750391584@invenio.cern.ch>

Hi there user!
-------------------------------------------------------------------------------
[2019-03-18 14:35:44,699: INFO/ForkPoolWorker-2] Task invenio_mail.tasks.send_email[209f9f5d-117d-448b-83f2-cf8d0b5123b1] succeeded in 0.017092917001718888s: None
```

## Step 8: Entrypoints: where the magic happens

In order for an Invenio instance to be modular and extensible, there has to be
a plugin system in place which allows for automatic discovery of e.g.
extensions, views, DB models, ES indices, etc. Invenio uses [Python's
entrypoints](https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins)
feature to facilitate this.

You can get a full list of all the entrypoints Invenio packages and your
instance use, by running:

```bash
(my-site) $ invenio instance entrypoints
invenio_assets.webpack
  invenio_i18n = invenio_i18n.webpack:i18n
  invenio_search_ui = invenio_search_ui.webpack:search_ui
  ...
invenio_base.apps
  invenio_access = invenio_access:InvenioAccess
  my_site_records = my_site.records:Mysite
  ...
invenio_base.blueprints
  invenio_accounts = invenio_accounts.views.settings:blueprint
  my_site = my_site.theme.views:blueprint
  ...
invenio_celery.tasks
  invenio_indexer = invenio_indexer.tasks
  invenio_mail = invenio_mail.tasks
invenio_config.module
  my_site = my_site.config
invenio_db.models
  invenio_access = invenio_access.models
  invenio_accounts = invenio_accounts.models
  ...
invenio_jsonschemas.schemas
  my_site = my_site.records.jsonschemas
  ...
```

## Step 9: Configuration loading

An important aspect of any deployable application is its configuration. Invenio
uses the `invenio-config` module to load configuration from a variety of
places, with the purpose of making it easy to override config variables
depending on the environment the application is running (e.g. Dev/QA/Prod). The
order configuration is loaded is:

- Configuation modules defined in `invenio_config.module` entrypoints.
  `my_site/config.py` is actually one of them
- Configuration in the `<app.instance_path>/invenio.cfg`. For local development
  this is usually `${VIRUAL_ENV}/var/instance/invenio.cfg`
- `INVENIO_`-prefixed environment variables. If for example you want to
  override the `SECRET_KEY`, you would have to do `export
  INVENIO_SECRET_KEY="my-secret"`

## What did we learn

- Basics on the application's Python environment
- Programmatically interacting with our application
- Running the web development server
- Running the Celery worker
- Inspecting Invenio entrypoints
- How Invenio configuration is loaded
