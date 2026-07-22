# ServiceDown

**Severity:** Critical
**Condition:** A Prometheus target in the `banking` namespace is unavailable for two minutes.

## Meaning and customer impact

Prometheus cannot scrape a service or exporter. The workload may be unavailable, its ServiceMonitor may be misconfigured, or monitoring connectivity may be broken.

## Confirm

```bash
kubectl -n banking get pods,svc,endpoints
kubectl -n banking get servicemonitors
kubectl -n banking describe servicemonitor <name>
```

Check Prometheus **Status → Targets** for the scrape error and test the target metrics endpoint from inside the cluster.

## First three remediation steps

1. Determine whether the application is actually unavailable or only metrics collection is failing.
2. Restore healthy endpoints by correcting pods, Services, selectors, ports, NetworkPolicies, or ServiceMonitor configuration.
3. If a release caused the failure, roll back and validate customer-facing health before resuming deployments.

## Escalate

Escalate immediately when the application endpoint is down or monitoring coverage for a critical service is lost during an incident.

## Validate recovery

Confirm the target is `UP`, service endpoints are populated, health checks succeed, and the alert resolves.
