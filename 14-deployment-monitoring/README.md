# Tutorial 14 - Deployment and monitoring

## Benchmark

You can use [Locust](https://locust.io/).

```bash
pip install locustio
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
