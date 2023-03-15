from pathlib import Path
import random

from locust import HttpUser, task
from requests_toolbelt import MultipartEncoder


class ExponentialUser(HttpUser):
    endpoint_url = 'http://localhost:8000/discoveries'
    assets_dir = Path(__file__).parent / 'assets'

    def wait_time(self):
        return random.expovariate(1 / 60)

    @task
    def post(self):
        configuration_path = self.assets_dir / 'sample.yaml'
        event_log_path = self.assets_dir / 'PurchasingExample.xes'

        data = MultipartEncoder(
            fields={
                'configuration': ('configuration.yaml', configuration_path.open('rb'), 'text/yaml'),
                'event_log': ('event_log.xes', event_log_path.open('rb'), 'application/xml'),
            }
        )

        self.client.post(
            self.endpoint_url,
            headers={"Content-Type": data.content_type},
            data=data,
        )
