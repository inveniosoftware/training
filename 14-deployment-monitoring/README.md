# Tutorial 14 - Deployment and monitoring

In this session, we will present how to tune deployment configuration of each part of the infrastructure and how to size it to be able to serve a targeted number of requests. We will also explain what to monitor and a few tips on how to take advantage of logging.

## Table of Contents

- [Tutorial 14 - Deployment and monitoring](#tutorial-14---deployment-and-monitoring)
  - [Table of Contents](#table-of-contents)
  - [Step 1: Benchmark](#step-1-benchmark)
  - [Step 2: Example of Sentry configuration](#step-2-example-of-sentry-configuration)

## Step 1: Benchmark

[Locust](https://locust.io/) is a nice tool to test your instance given that you can set the number of concurrent requests per second to perform.

It does not make much sense to run this stress test in the development environment, but we will do it just to see how it works.

Ensure that docker-compose **full** is running.

```bash
cd ~/src/my-site
docker-compose stop
docker-compose -f docker-compose.full.yml up
```

Let's install `locust` in our virtualenv and run the server.

```bash
cd ~/src/my-site
pipenv run pip install locust
./scripts/server
```

In another terminal, now copy the file `locustfile.py` in your `my-site` folder (to be in the virtualenv) and then run locust in the same folder:

```bash
cp ~/src/training/14-deployement-monitoring/locustfile.py ~/src/my-site/
cd ~/src/my-site
pipenv run locust --host=https://127.0.0.1:5000/
firefox http://127.0.0.1:8089
```

## Step 2: Example of Sentry configuration

If you need to configure Sentry in your Invenio instance, here an example:

```python
SENTRY_DSN = "sync+https://mysentry.domain.org/4",
SENTRY_CONFIG = {'environment': 'production'}
LOGGING_SENTRY_CELERY = False
try:
    # Try to get the release tag
    from raven import fetch_git_sha
    SENTRY_CONFIG['release'] = fetch_git_sha('/path/to/git/repo')
except Exception:
    pass

LOGGING_FS_LOGFILE = "/path/to/file/log.err"
```
