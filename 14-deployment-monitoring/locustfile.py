from locust import HttpLocust, TaskSet, task


class AnonymousWebsiteTasks(TaskSet):

    base_url = 'https://127.0.0.1:5000/'

    def on_start(self):
        self.client.verify = False

    @task
    def homepage(self):
        """Task home page."""
        self.client.get(self.base_url)


class WebsiteUser(HttpLocust):
    """Locust.

    To run it, just `locust --host=https://127.0.0.1:5000/` and
    open the browser `http://127.0.0.1:8089/`
    """

    task_set = AnonymousWebsiteTasks
    min_wait = 5000
    max_wait = 15000
