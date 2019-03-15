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
