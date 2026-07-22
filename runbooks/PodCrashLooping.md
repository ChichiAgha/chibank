# PodCrashLooping

**Severity:** Critical
**Condition:** A banking container restarts more than three times in ten minutes.

## Meaning and customer impact

Kubernetes cannot keep a container healthy. Capacity may be reduced and requests may fail if remaining replicas cannot absorb traffic.

## Confirm

```bash
kubectl -n banking get pods
kubectl -n banking describe pod <pod>
kubectl -n banking logs <pod> -c <container> --previous
```

Check termination reason, exit code, OOM events, failed probes, missing Secrets/ConfigMaps, and dependency connectivity.

## First three remediation steps

1. Stop or roll back a recent deployment if the restart loop began with a new image or configuration.
2. Correct the immediate cause: invalid configuration, unavailable dependency, insufficient memory, permissions, or probe timing.
3. Restart or redeploy only after the correction, then watch readiness and restart counts.

## Escalate

Escalate immediately when the crashing workload is PostgreSQL, Kafka, or all replicas of a customer-facing service.

## Validate recovery

Confirm pods remain Ready with stable restart counts and the relevant API health and metrics endpoints respond.
