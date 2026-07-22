# Port developer portal

The Techbleat Global Bank catalog and self-service actions are managed from this repository and applied to the Port EU API by GitHub Actions.

## Catalog model

The catalog setup is defined in:

- `port/catalog/blueprints.json`
- `port/catalog/entities.json`
- `scripts/setup-port-catalog.sh`
- `.github/workflows/setup-port-catalog.yml`

The model contains six blueprints:

| Blueprint | Purpose |
| --- | --- |
| `bankDomain` | Banking business domains |
| `bankApplication` | The overall banking application |
| `bankService` | Independently testable and deployable services |
| `bankResource` | Databases, caches, and message brokers |
| `bankEnvironment` | Development and production runtime environments |
| `bankDeployment` | Deployment history for a service and environment |

### Relationships

```text
Retail Banking domain
└── Techbleat Global Bank application
    ├── Banking Frontend
    │   └── depends on User, Transaction, and Activity services
    ├── User Service
    │   └── uses PostgreSQL
    ├── Transaction Service
    │   └── uses PostgreSQL, Redis, and Kafka
    ├── Activity Service
    │   ├── depends on Transaction Service
    │   └── uses PostgreSQL and Kafka
    ├── Development environment
    └── Production environment
```

The setup script is idempotent. Updating either catalog JSON file on `main` automatically reapplies the model and entities. It does not delete unrelated Port data.

## Self-service actions

Self-service definitions are managed in:

- `port/self-service/actions.json`
- `scripts/setup-port-self-service.sh`
- `.github/workflows/setup-port-self-service.yml`

The following actions are available in Port:

| Action | Location | Approval | Backend |
| --- | --- | --- | --- |
| Run bank service tests | Each Bank Service entity | No | `run-bank-service-tests.yml` |
| Run bank image security scan | Self-service page | No | `image-scan.yaml` |
| Resync bank catalog | Self-service page | Yes | `setup-port-catalog.yml` |

The GitHub Ocean integration reports the dispatched workflow result back to the Port action run.

## Required GitHub Actions secrets

| Secret | Purpose |
| --- | --- |
| `PORT_CLIENT_ID` | Port organization API client ID |
| `PORT_CLIENT_SECRET` | Port organization API client secret |
| `PORT_GITHUB_TOKEN` | GitHub authentication for the Ocean exporter |

Secret values must remain in GitHub Actions secrets and must never be committed.

## Running setup manually

From GitHub, open **Actions** and run either:

1. **Setup Port Bank Catalog** to reapply blueprints, entities, and relationships.
2. **Setup Port Self-Service** to reapply the action definitions.

## Deployment actions

Production deployment, rollback, restart, and scaling actions are intentionally not exposed yet. The current development runtime is Minikube, which is not reachable from GitHub-hosted runners. Add a GitHub-accessible Kubernetes target or a self-hosted runner with a narrowly scoped service account before exposing these operations.

When that runtime connection exists, production actions should require approval and use environment-scoped credentials, while development actions should enforce bounded service and replica inputs.
