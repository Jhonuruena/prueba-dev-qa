import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  rps: 200,         
  duration: '2m',   
  thresholds: {
    http_req_duration: ['p(95)<3000'],  
    http_req_failed: ['rate==0'],   
  },
};

const BASE_URL = 'https://petstore.swagger.io/v2';

export default function () {
  const res = http.get(`${BASE_URL}/pet/1`);
  check(res, {
    'status was 200': (r) => r.status === 200,
    'response has pet data': (r) => r.json().name !== undefined,
  });
  sleep(0.3);
}