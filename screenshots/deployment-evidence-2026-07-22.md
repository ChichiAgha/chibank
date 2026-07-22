# Live deployment evidence — 22 July 2026

This evidence was captured from the running Minikube development cluster after the instrumentation rollout.

## Published immutable images

| Component | Image | Docker Hub digest |
| --- | --- | --- |
| Frontend | `chigoldd/chibank-frontend:v1.1.0` | `sha256:18c709bec37ae175e999a0855273bfc94d2807ba3d7782166f8fadebd6dd2ae3` |
| User Service | `chigoldd/chibank-user-service:v1.1.0` | `sha256:183d350115eb2b8659cc44a07a4eea644dd951c5398a8aa8b3a536927480bc1d` |
| Activity Service | `chigoldd/chibank-activity-service:v1.1.0` | `sha256:a2cc956af990ba190989cf197f685dfc1b443e72fb3e790c078669d309b3878d` |
| Transaction Service | `chigoldd/chibank-transaction-service:v1.1.0` | `sha256:fcce132f00c7a9b0ffb8c321052a09362719725a638ebf4afcf1b50b79678f6d` |

## Verified Kubernetes state

```text
NAME                  READY   DESIRED   IMAGE
frontend              1       1         chigoldd/chibank-frontend:v1.1.0
user-service          1       1         chigoldd/chibank-user-service:v1.1.0
activity-service      1       1         chigoldd/chibank-activity-service:v1.1.0
transaction-service   2       2         chigoldd/chibank-transaction-service:v1.1.0
```

The live cluster also contains:

- `activity-service` ServiceMonitor plus the existing application and exporter ServiceMonitors.
- `bleatbank-alerts` PrometheusRule with all seven required alert names.
- `bleatbank-grafana-dashboards` ConfigMap with Operations and Business dashboard JSON.
- Grafana API-confirmed dashboards with UIDs `bleatbank-operations` and `bleatbank-business`.

## Screenshot status

Grafana 13.0.2 loaded both dashboards successfully. A genuine image-renderer workload was temporarily enabled, but rendering timed out on the resource-constrained ARM Minikube node. The optional renderer was removed again to restore headroom. Visual PNG evidence therefore still needs to be captured interactively from the live Grafana UI; no screenshot has been fabricated.

