## Tutorial 09 - Securing your Invenio instance

In this session, we will discover the key points which will ensure that your Invenio instances are secure. We will learn how to protect the web application with configuration, package management and authentication. We will explore with small exercises on how the vulnerabilities can be exploited due to misconfiguration or security issues.

Jump to: [Step 1](#step-1) | [Step 2](#step-2) | [Step 3](#step-3) | [Step 4](#step-4)

Any extra long description

## Step 1

Start from a clean and working instance:

```bash
$ cd 08-securing-your-invenio-instance/
$ ./init.sh
```

## Step 2

```console
$ curl -ki -H "Host: test" https://127.0.0.1:5000/api/records/
HTTP/1.0 400 BAD REQUEST
Content-Type: application/json
Content-Length: 56
X-Frame-Options: sameorigin
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Content-Security-Policy: default-src 'self'; object-src 'none'
X-Content-Security-Policy: default-src 'self'; object-src 'none'
Strict-Transport-Security: max-age=31556926; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
Server: Werkzeug/0.14.1 Python/3.6.7
Date: Wed, 13 Mar 2019 05:35:18 GMT

{"message":"Host \"test\" is not trusted","status":400}
```

Lets say now that we allow any host in `my_site/config.py`:
```diff
 #: provided, the allowed hosts variable is set to localhost. In production it
 #: should be set to the correct host and it is strongly recommended to only
 #: route correct hosts to the application.
-APP_ALLOWED_HOSTS = ['my-site.com', 'localhost', '127.0.0.1']
+APP_ALLOWED_HOSTS = ['*']

 # OAI-PMH
 # =======
```

```console
$ curl -ki -H "Host: attacker.com" https://127.0.0.1:5000/api/records/
TODO this should show a link to attacker.com/aleluya
```

## Step 3 : Change secret key

`my_site/config.py`:

```diff
 #: Secret key - each installation (dev, production, ...) needs a separate key.
 #: It should be changed before deploying.
-SECRET_KEY = 'CHANGE_ME'
+SECRET_KEY = '<strong-randomly-generated-key>'
 #: Max upload size for form data via application/mulitpart-formdata.
 MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MiB
 #: Sets cookie with the secure flag by default
```
TODO Recommendation on how to generate? interactive


## Step 4: change your certificates

Invenio works only with HTTPS so we create temporary certificates when starting new instances, **these certificates need to be updated**.

TODO interactive how to generate?

## Step 5: CSP

Where do you allow content in your Invenio instance to be loaded from.

TODO interactive example with trying to load in line css and unknown origin assets


## Step 6: Keep packages up to date

- [upgrade workflow](https://pipenv.readthedocs.io/en/latest/basics/#example-pipenv-upgrade-workflow)
```console
$ pipenv update --outdated
$ pipenv update [package]
```
- Security checks

```console
$ pipenv check
```

## What did we learn

* How to securely configure Invenio
* How Invenio handles CSP rules
* How Invenio takes care of serving files (potential vector of attack)
* How sessions works in Invenio
* Storing encrypted properties in DB and migrating secret keys.
