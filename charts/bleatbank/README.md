# Bleatbank Helm chart

This chart deploys the four application components plus PostgreSQL, Redis, Kafka, ingress, ServiceMonitors, exporters, alerts, and the Transaction Service HPA into the `banking` namespace.

```bash
helm lint charts/bleatbank --set-string postgres.password=test-only
helm upgrade --install bleatbank charts/bleatbank \
  --namespace banking --create-namespace \
  --values charts/bleatbank/values-dev.yaml
```

Production deployments must override image repositories, immutable tags, ingress host, StorageClass where required, and `postgres.password` from an external secret source. Monitoring custom resources require kube-prometheus-stack to be installed first.
