import sys, time, random
from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def list(self):
        self.client.get('/fetch-users/')