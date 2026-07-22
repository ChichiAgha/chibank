# Architecture

Techbleat Global Bank runs in the dedicated `banking` namespace. NGINX Ingress is the only application entry point. It routes `/` to the React frontend and `/api/users`, `/api/transactions`, and `/api/activities` to internal ClusterIP services.

```text
Browser -> NGINX Ingress -> Frontend
                       |-> User Service ---------> PostgreSQL
                       |-> Transaction Service --> PostgreSQL + Redis + Kafka
                       `-> Activity Service -----> PostgreSQL
                                                  ^
                                      Kafka consumer

Prometheus <- ServiceMonitors <- application /metrics + exporters
Grafana    <- Prometheus and Loki
Alloy      -> Loki (structured container logs)
Alertmanager -> Slack/webhook when enabled
```

PostgreSQL and Kafka use StatefulSets; PostgreSQL data is held on a PVC. Application configuration is in a ConfigMap and credentials are in a Secret. Transaction Service scales from two to six replicas through an HPA. Every application container has resource requests/limits and health probes.

The observability path uses kube-prometheus-stack for Prometheus, Grafana, Alertmanager, kube-state-metrics, and node metrics. Dedicated exporters expose PostgreSQL, Redis, and Kafka metrics. Grafana Alloy collects logs from the `banking` namespace and sends them to Loki.
