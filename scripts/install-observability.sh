#!/usr/bin/env bash
set -euo pipefail

MONITORING_NAMESPACE="monitoring"

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

kubectl create namespace "${MONITORING_NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

if ! kubectl -n "${MONITORING_NAMESPACE}" get secret grafana-admin >/dev/null 2>&1; then
  GRAFANA_PASSWORD="$(openssl rand -base64 24)"
  kubectl -n "${MONITORING_NAMESPACE}" create secret generic grafana-admin \
    --from-literal=admin-user=admin \
    --from-literal=admin-password="${GRAFANA_PASSWORD}"
  echo "Grafana password created. Retrieve it with the command documented in docs/deployment.md."
fi

helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace "${MONITORING_NAMESPACE}" \
  --values monitoring/kube-prometheus-stack-values.yaml \
  --wait --timeout 15m

helm upgrade --install loki grafana/loki \
  --namespace "${MONITORING_NAMESPACE}" \
  --values monitoring/loki-values.yaml \
  --wait --timeout 15m

helm upgrade --install alloy grafana/alloy \
  --namespace "${MONITORING_NAMESPACE}" \
  --values monitoring/alloy-values.yaml \
  --wait --timeout 10m

kubectl -n "${MONITORING_NAMESPACE}" create configmap bleatbank-grafana-dashboards \
  --from-file=dashboards/operations-overview.json \
  --from-file=dashboards/business-metrics.json \
  --dry-run=client -o yaml | kubectl apply -f -
kubectl -n "${MONITORING_NAMESPACE}" label configmap bleatbank-grafana-dashboards \
  grafana_dashboard=1 --overwrite

echo "Prometheus, Grafana, Loki and Alloy are installed."

