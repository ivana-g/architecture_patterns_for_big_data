# Performance Results 

Just out of curiosity, outside of the base case, I went on to test how the app performes on my machine under different loads in a ramp-up scenario to up to 200 virtual users for a total suration of 2 min and 30 sec. Below are the results. I notice that my req/s metric in the ramp-up scenario stays almost the same as in the base scenario. I didn't dig deeper to see what the reason for that is, the expectation however is that req/s should be higher in ramp-up case than it is in base case.

## Summary Table

| Test Case         | VUs / Stages         | Duration | Total Requests | Requests/sec | Avg Resp Time | Median | 95th %ile | Max Resp Time | Error Rate |
|------------------|---------------------|----------|---------------|-------------|---------------|--------|-----------|---------------|------------|
| Steady 10 VUs    | 10 VUs              | 30s      | 24,062        | 798.5       | 12.35 ms      | 11.92  | 17.53     | 139.34 ms     | 0%         |
| Ramp-up to 200   | 10→50→100→200 VUs   | 2m30s    | 115,406       | 766.2       | 93.63 ms      | 79.43  | 234.95    | 367.44 ms     | 0%         |

---

## Results: 
command: `k6 run test.js`

### scenario 1: (100.00%) 1 scenario, 10 max VUs, 1m0s max duration (incl. graceful stop): * default: 10 looping VUs for 30s (gracefulStop: 30s)



  █ TOTAL RESULTS

    checks_total.......................: 24062   798.513743/s
    checks_succeeded...................: 100.00% 24062 out of 24062
    checks_failed......................: 0.00%   0 out of 24062

    ✓ status is 204

    HTTP
    http_req_duration.......................................................: avg=12.35ms min=5.24ms med=11.92ms max=139.34ms p(90)=16.09ms p(95)=17.53ms
      { expected_response:true }............................................: avg=12.35ms min=5.24ms med=11.92ms max=139.34ms p(90)=16.09ms p(95)=17.53ms
    http_req_failed.........................................................: 0.00%  0 out of 24062
    http_reqs...............................................................: 24062  798.513743/s

    EXECUTION
    iteration_duration......................................................: avg=12.45ms min=5.35ms med=12.07ms max=64.71ms  p(90)=16.23ms p(95)=17.68ms
    iterations..............................................................: 24062  798.513743/s
    vus.....................................................................: 10     min=10         max=10
    vus_max.................................................................: 10     min=10         max=10

    NETWORK
    data_received...........................................................: 650 kB 22 kB/s
    data_sent...............................................................: 4.1 MB 137 kB/s


running (0m30.1s), 00/10 VUs, 24062 complete and 0 interrupted iterations
default ✓ [======================================] 10 VUs  30s


### scenario 2: (100.00%) 1 scenario, 200 max VUs, 3m0s max duration (incl. graceful stop): * default: Up to 200 looping VUs for 2m30s over 5 stages (gracefulRampDown: 30s, gracefulStop: 30s)

  █ TOTAL RESULTS

    checks_total.......................: 115406  766.161173/s
    checks_succeeded...................: 100.00% 115406 out of 115406
    checks_failed......................: 0.00%   0 out of 115406

    ✓ status is 204

    HTTP
    http_req_duration.......................................................: avg=93.63ms min=4.07ms med=79.43ms max=367.44ms p(90)=212.48ms p(95)=234.95ms
      { expected_response:true }............................................: avg=93.63ms min=4.07ms med=79.43ms max=367.44ms p(90)=212.48ms p(95)=234.95ms
    http_req_failed.........................................................: 0.00%  0 out of 115406
    http_reqs...............................................................: 115406 766.161173/s

    EXECUTION
    iteration_duration......................................................: avg=93.41ms min=4.21ms med=79.51ms max=367.64ms p(90)=211.49ms p(95)=234.2ms
    iterations..............................................................: 115406 766.161173/s
    vus.....................................................................: 1      min=1           max=199
    vus_max.................................................................: 200    min=200         max=200

    NETWORK
    data_received...........................................................: 3.1 MB 21 kB/s
    data_sent...............................................................: 20 MB  131 kB/s


running (2m30.6s), 000/200 VUs, 115406 complete and 0 interrupted iterations
default ✓ [======================================] 000/200 VUs  2m30s

