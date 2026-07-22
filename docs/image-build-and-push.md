# Build, publish, and scan images

Use an immutable semantic version. Replace `REGISTRY_USER` with your Docker Hub account.

```bash
export IMAGE_VERSION=v1.0.0
export REGISTRY_USER=REGISTRY_USER

docker build -t "$REGISTRY_USER/bleatbank-frontend:$IMAGE_VERSION" techbleat-global-bank-frontend
docker build -t "$REGISTRY_USER/bleatbank-user-service:$IMAGE_VERSION" techbleat-global-bank-backend/user-service
docker build -t "$REGISTRY_USER/bleatbank-transaction-service:$IMAGE_VERSION" techbleat-global-bank-backend/transaction-service
docker build -t "$REGISTRY_USER/bleatbank-activity-service:$IMAGE_VERSION" techbleat-global-bank-backend/activity-service

docker push "$REGISTRY_USER/bleatbank-frontend:$IMAGE_VERSION"
docker push "$REGISTRY_USER/bleatbank-user-service:$IMAGE_VERSION"
docker push "$REGISTRY_USER/bleatbank-transaction-service:$IMAGE_VERSION"
docker push "$REGISTRY_USER/bleatbank-activity-service:$IMAGE_VERSION"
```

Scan each immutable image and retain the reports as CI artifacts:

```bash
mkdir -p scan-results
for image in frontend user-service transaction-service activity-service; do
  trivy image --severity HIGH,CRITICAL --format json \
    --output "scan-results/${image}.json" \
    "$REGISTRY_USER/bleatbank-${image}:$IMAGE_VERSION"
done
```

Do not waive a critical finding silently. Record the CVE, affected package, exposure, compensating control, owner, and remediation deadline in the release record. Update `charts/bleatbank/values.yaml` with the published repositories and version before deployment.

Alternatively, add the GitHub repository secrets `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`, then run the **Publish versioned application images** workflow with a semantic version. It validates the version, builds, blocks on high/critical Trivy findings, and only then pushes each image.
