# Deployment and operations guide

## Prerequisites

Install Docker, `kubectl`, Helm 3, Minikube, and an NGINX Ingress controller. The same chart can target EKS when an appropriate StorageClass and ingress controller are available.

## Local cluster

```bash
minikube start --cpus=4 --memory=8192
minikube addons enable ingress
minikube addons enable metrics-server
```

Update the four image repositories in `charts/bleatbank/values.yaml`. Then install monitoring first and the bank second:

```bash
./scripts/install-observability.sh
helm dependency update charts/bleatbank
helm upgrade --install bleatbank charts/bleatbank \
  --namespace banking --create-namespace \
  --values charts/bleatbank/values-dev.yaml \
  --wait --timeout 15m
kubectl get pods,svc,ingress,hpa,pvc -n banking
```

Map `bleatbank.local` to the output of `minikube ip` in the workstation hosts file, then open `http://bleatbank.local`. For production, supply the database password at deployment from the organisation's secret manager; do not commit it.

## Access Grafana

```bash
kubectl -n monitoring port-forward svc/kube-prometheus-stack-grafana 3000:80
kubectl -n monitoring get secret grafana-admin -o jsonpath='{.data.admin-password}' | base64 -d; echo
```

Open `http://localhost:3000`, sign in as `admin`, and select the automatically provisioned Operations Overview or Business Metrics dashboard. Prometheus and Loki are preconfigured data sources.

## Verify telemetry and alerts

```bash
kubectl get servicemonitors,prometheusrules -n banking
kubectl -n banking port-forward svc/transaction-service 8080:8080
curl http://localhost:8080/actuator/prometheus
```

Test `ServiceDown` in a demo environment by scaling one service to zero, wait over two minutes, verify firing and notification delivery, then restore it. Test `PodCrashLooping` only in a disposable environment. Capture Grafana and Alertmanager screenshots after the alert fires and again after it resolves.

Slack routing is disabled by default. Create the webhook secret and enable it without committing the URL:

```bash
kubectl -n banking create secret generic alertmanager-slack-webhook \
  --from-literal=webhook-url='https://hooks.slack.com/services/REPLACE_ME'
helm upgrade bleatbank charts/bleatbank -n banking \
  --reuse-values --set monitoring.alerting.enabled=true
```

## Troubleshooting

Start with `kubectl get events -n banking --sort-by=.lastTimestamp`, pod logs, probe output, and Prometheus target status. Infrastructure starts before application workloads, but readiness probes—not startup ordering—control whether a dependency receives traffic. See `runbooks/` for alert-specific diagnosis and remediation.
