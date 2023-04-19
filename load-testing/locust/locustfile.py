import os
import random
from pathlib import Path

from locust import task, FastHttpUser
from locust.contrib.fasthttp import FastHttpSession


class User(FastHttpUser):
    host = os.environ.get('SIMOD_HTTP_URL')
    endpoint_url = f'{host}/discoveries'
    assets_dir = Path(__file__).parent / 'assets'

    def wait_time(self):
        return random.expovariate(1 / 60)

    @task
    def post1(self):
        make_post(self.client, self.assets_dir, self.endpoint_url, 'PurchasingExample.xes')

    @task
    def post2(self):
        make_post(self.client, self.assets_dir, self.endpoint_url, 'PurchasingExample.xes')


def make_post(client: FastHttpSession, assets_dir: Path, endpoint_url: str, event_log_name: str):
    configuration_path = assets_dir / 'sample.yaml'
    event_log_path = assets_dir / event_log_name

    data = {
        'configuration': ('configuration.yaml', configuration_path.open('rb'), 'text/yaml'),
        'event_log': ('event_log.xes', event_log_path.open('rb'), 'application/xml'),
    }

    client.post(
        endpoint_url,
        headers={'Content-Type': 'multipart/form-data'},
        files=data,
    )
