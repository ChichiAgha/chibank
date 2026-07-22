# HPAMaxReplicasReached

**Severity:** Warning  
**Condition:** The Transaction Service HPA remains at six replicas for five minutes.

## Confirm

```bash
kubectl -n banking describe hpa transaction-service
kubectl -n banking top pods -l app.kubernetes.io/name=transaction-service
kubectl -n banking get events --sort-by=.lastTimestamp
```

Compare request rate, latency, errors, node capacity, pending pods and downstream saturation.

## Remediate

1. Confirm whether demand is legitimate or caused by retries, abuse, or a dependency slowdown.
2. Ensure all six replicas are scheduled and Ready; add node capacity if pods are pending.
3. Raise the maximum only through a reviewed capacity change after confirming database, Redis and Kafka headroom.
