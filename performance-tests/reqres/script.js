import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,
  duration: '2m',
  thresholds: {
    http_req_duration: ['p(95)<2000'],
    http_req_failed: ['rate==0'],
  },
};

const BASE_URL = 'https://reqres.in/api';

export default function () {
  const res = http.get(`${BASE_URL}/users`, {
    headers: {
      'x-api-key': 'reqres-free-v1',
    },
  });

  function isValidJSON(body) {
    try {
      JSON.parse(body);
      return true;
    } catch (e) {
      return false;
    }
  }

  function safeJson(body) {
    try {
      return JSON.parse(body);
    } catch (e) {
      return null;
    }
  }

  check(res, {
    'status was 200': (r) => r.status === 200,
    'response body is not empty': (r) => r.body.length > 0,
    'response is valid JSON': (r) => isValidJSON(r.body),
    'response has users data array': (r) => {
      const json = safeJson(r.body);
      return Array.isArray(json?.data) && json.data.length > 0;
    },
  });

  sleep(1);
}