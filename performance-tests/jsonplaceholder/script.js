import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 100,           
  duration: '2m',    
};

export default function () {
  const res = http.get('https://jsonplaceholder.typicode.com/posts');
  check(res, {
    'status was 200': (r) => r.status === 200,
  });
  sleep(1); 
}