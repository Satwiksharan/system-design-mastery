# System Design Assignment — Python Code

This package contains the code for the three assignment tasks:
1. `app_shortener.py` — URL Shortener Lite (port 5000)
2. `app_rate_limiter.py` — Rate Limiter Mini (port 5004)
3. `app_backend.py` — reusable mock backend server (ports 5001, 5002, 5003)
4. `app_lb.py` — round-robin load balancer (port 8080)

## Setup on macOS

From this folder, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Task 1 — URL Shortener

Start the service:

```bash
python app_shortener.py
```

In another terminal:

```bash
curl -i -X POST http://127.0.0.1:5000/shorten \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://www.example.com/target-destination-page"}'
```

Copy the returned `short_id` and test the redirect, replacing `<short_id>` with the actual value:

```bash
curl -i http://127.0.0.1:5000/<short_id>
```

Expected: POST returns HTTP 201; the redirect endpoint returns HTTP 302 with a `Location` header. Unknown IDs return HTTP 404.

## Task 2 — Rate Limiter

Start the service:

```bash
python app_rate_limiter.py
```

Send six requests with the same user ID:

```bash
for i in {1..6}; do
  echo "--- Request $i ---"
  curl -i 'http://127.0.0.1:5004/data?user_id=user_id_1'
  echo
done
```

Expected: the first five requests return HTTP 200; the sixth within 60 seconds returns HTTP 429 and `Too Many Requests: Try again later.`

## Task 3 — Round-Robin Load Balancer

Open four terminal tabs in this folder. Run one command in each of the first three tabs:

```bash
python app_backend.py 1 5001
python app_backend.py 2 5002
python app_backend.py 3 5003
```

In the fourth terminal, start the load balancer:

```bash
python app_lb.py
```

Test six requests:

```bash
for i in {1..6}; do
  curl -s http://127.0.0.1:8080/
done
```

Expected response sequence:

```text
Hello from Server 1!
Hello from Server 2!
Hello from Server 3!
Hello from Server 1!
Hello from Server 2!
Hello from Server 3!
```

## Notes

- The URL mappings and rate-limit timestamps are stored in memory and reset when their service restarts.
- The load balancer is a learning simulation and currently forwards GET requests to `/` only.
- Capture your own terminal screenshots after running the services for the assignment submission.
