import http from 'k6/http';
import { check } from 'k6';
import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js';

const configuration = open('assets/sample.yaml', 'b');
const event_log = open('assets/PurchasingExample.xes', 'b');

const endpoint = __ENV.SIMOD_HTTP_URL || 'http://localhost:8000';

export default function () {
  const fd = new FormData();

  fd.append('configuration', http.file(configuration, 'sample.yaml', 'text/yaml'));
  fd.append('event_log', http.file(event_log, 'PurchasingExample.xes', 'application/xml'));

  const res = http.post(`${endpoint}/discoveries`, fd.body(), {
    headers: {
      'Content-Type': `multipart/form-data; boundary=${fd.boundary}`,
    },
  });

  check(res, {
    'status is 202': (r) => r.status === 202,
  });
}