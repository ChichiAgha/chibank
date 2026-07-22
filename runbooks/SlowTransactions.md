# SlowTransactions

**Severity:** Warning  
**Condition:** Transaction Service P95 request latency exceeds two seconds for five minutes.

## Confirm

Check the latency dashboard by endpoint, pod CPU/memory, HPA state, PostgreSQL query duration and connections, Redis errors, and Kafka producer errors.

```bash
kubectl -n banking top pods -l app.kubernetes.io/name=transaction-service
kubectl -n banking describe hpa transaction-service
kubectl -n banking logs deployment/transaction-service --since=10m
```

## Remediate

1. Identify the slow endpoint and dependency.
2. Scale within safe limits if the service is resource constrained.
3. Correct the query, cache, broker, or downstream bottleneck and verify P95 returns below two seconds.
