# Tutorial 14 - Deployment and monitoring

In this session, we will present how tune deployment configuration of each part of the infrastructure and how to size it to be able to serve a targeted number of requests. We will also explain what to monitor and a few tips on how to take advantage of logging.

## Benchmark

You can use [Locust](https://locust.io/).

```bash
$ pipenv run pip install locustio
$ ./scripts/server
$ pipenv run locust --host=https://127.0.0.1/ --no-web -c 1000 -r 100
```

`locustfile.py`

```python
from locust import HttpLocust, TaskSet, task

class Home(TaskSet):

    @task
    def get_something(self):
        self.client.get("/")

class WebsiteUser(HttpLocust):
    task_set = Home
```

## Sentry configuration

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
