# k6 run ws_load_test.js

# wrk -t1 -c5 -d30s http://<domain-name>/plaintext/
# wrk -t1 -c5 -d30s http://<domain-name>/json/
# wrk -t1 -c5 -d30s http://<domain-name>/db/
# wrk -t1 -c5 -d30s http://<domain-name>/dbs/?queries=20
# wrk -t1 -c5 -d30s http://<domain-name>/fortunes/
# wrk -t1 -c5 -d30s http://<domain-name>/update/?queries=20

# curl -N http://localhost:8000/sse/
# curl -N http://localhost:8001/sse_async/
