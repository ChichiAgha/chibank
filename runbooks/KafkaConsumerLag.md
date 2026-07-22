# KafkaConsumerLag

**Severity:** Warning  
**Condition:** Activity Service consumer lag exceeds 100 messages for three minutes.

## Confirm

Check the Kafka lag graph, Activity Service pod health, consumer error logs and PostgreSQL write health.

```bash
kubectl -n banking get pods -l app.kubernetes.io/name=activity-service
kubectl -n banking logs deployment/activity-service --since=10m
kubectl -n banking exec kafka-0 -- kafka-consumer-groups --bootstrap-server kafka:29092 --group activity-service-group --describe
```

## Remediate

1. Restore the Activity Service or PostgreSQL if either is unhealthy.
2. Remove poison messages only through an approved recovery procedure; preserve evidence first.
3. Scale consumers only after confirming partition count and consumer safety, then verify lag trends toward zero.
