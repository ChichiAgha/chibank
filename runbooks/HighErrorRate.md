# HighErrorRate

**Severity:** Critical
**Condition:** More than 5% of HTTP requests return 5xx responses for five minutes.

## Meaning and customer impact

A bank API is failing a material share of requests. Customers may be unable to register, view balances, or complete transactions.

## Confirm

```bash
kubectl -n banking get pods
kubectl -n banking logs deployment/transaction-service --since=10m
kubectl -n banking get events --sort-by=.lastTimestamp
```

In Grafana, identify the affected `job`, endpoint, status code, and whether latency or dependency errors increased at the same time.

## First three remediation steps

1. Identify whether the failures began after a deployment; pause further releases and roll back the affected Helm revision if necessary.
2. Check PostgreSQL, Redis, and Kafka health plus connection saturation, consumer lag, and pod resource pressure.
3. Scale the affected stateless service within its tested limits or remove unhealthy instances while addressing the root cause.

## Escalate

Escalate to the banking service owner and incident commander if customer transactions are failing or if the error ratio continues for ten minutes.

## Validate recovery

Confirm the 5xx ratio is below 1%, probes are healthy, synthetic transactions succeed, and the alert resolves.
