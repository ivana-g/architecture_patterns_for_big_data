import http from 'k6/http';
import { check } from 'k6';

// Base case
// export const options = {
//     vus: 10,
//     duration: '30s',
//   };

// Ramp-up case
export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '30s', target: 50 },
    { duration: '30s', target: 100 },
    { duration: '30s', target: 200 },
    { duration: '30s', target: 0 },
  ],
};

export default function () {
  const url = 'http://localhost:8081/request-registration';
  const payload = JSON.stringify({ email: "test@example.com" });
  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };
  const res = http.post(url, payload, params);
  check(res, {
    'status is 204': (r) => r.status === 204,
  });
}
