# Port and Internal Developer Portal Interview Guide

This guide covers likely Port and Internal Developer Portal (IDP) interview questions, using the Techbleat Global Bank implementation as the practical example.

## Your 30-second project introduction

> I integrated a microservices banking platform with Port using the GitHub Ocean exporter. I secured the integration with GitHub Actions secrets, modelled domains, applications, services, resources, environments, and deployments, and created relationships showing service dependencies and infrastructure usage. I made the configuration reproducible through idempotent scripts and GitHub workflows. I then created governed self-service actions for service testing, container security scanning, and catalog synchronization, with approval for higher-risk operations.

## Core IDP concepts

### 1. What is an Internal Developer Portal?

An Internal Developer Portal is a central interface where developers can discover services, understand ownership and dependencies, access documentation, and execute approved operational workflows.

It reduces cognitive load by providing a consistent layer over GitHub, Kubernetes, CI/CD, monitoring, cloud platforms, and other engineering tools.

### 2. Is an IDP the same as an Internal Developer Platform?

No.

- The platform provides the underlying infrastructure and automation capabilities.
- The portal exposes those capabilities through a developer-friendly interface.

The portal is the front door; the platform is the machinery behind it.

### 3. What problems does an IDP solve?

An IDP addresses:

- Fragmented service information.
- Unclear ownership.
- Tool sprawl.
- Inconsistent operational procedures.
- Poor dependency visibility.
- Slow developer onboarding.
- Repetitive platform support requests.
- Unsafe manual production operations.

### 4. What is Port?

Port is an internal developer portal platform used to build a software catalog, model relationships, define engineering standards, and expose governed self-service workflows.

It integrates with systems such as GitHub, Kubernetes, cloud providers, CI/CD systems, and observability tools.

### 5. What are the main components of Port?

The main components are:

1. Software catalog.
2. Blueprints and entities.
3. Relationships.
4. Integrations and data ingestion.
5. Self-service actions.
6. Scorecards and standards.
7. Dashboards and entity pages.
8. Permissions, approvals, and audit logs.

## Catalog and data model

### 6. What is a blueprint?

A blueprint is the schema for a type of asset.

For example, the `bankService` blueprint defines properties such as language, framework, criticality, and documentation. It also defines relationships to applications, other services, and infrastructure resources.

A blueprint is comparable to a class or database table definition.

### 7. What is an entity?

An entity is an instance of a blueprint.

For example:

```text
Blueprint: bankService
Entity: transaction-service
```

The blueprint defines the structure; the entity contains the actual values.

### 8. What is the difference between a property and a relation?

A property describes an entity:

```text
language = Java
criticality = critical
```

A relation connects the entity to another entity:

```text
transaction-service uses banking-kafka
transaction-service belongs to techbleat-bank
```

Properties describe; relations connect.

### 9. Why are relationships important?

Relationships provide operational context and support impact analysis.

If Kafka fails, the catalog can identify the transaction and activity services as consumers. If the transaction service changes, engineers can see its dependencies and potentially affected services.

Without relationships, a catalog is only an inventory.

### 10. What types of relationships does Port support?

Port supports:

- Single relationships.
- Many relationships.
- Self-relations between entities of the same blueprint.
- Reverse or mirror relationships.
- Indirect relationships through a relation path.

In this project, `bankService.dependsOn` is a many-valued self-relation.

### 11. Describe the banking catalog model.

The model contains six blueprints:

- `bankDomain`.
- `bankApplication`.
- `bankService`.
- `bankResource`.
- `bankEnvironment`.
- `bankDeployment`.

The domain contains the application. The application contains services, resources, and environments. Services depend on other services and use infrastructure resources. Deployments connect a service to an environment.

### 12. Describe the important banking relationships.

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

### 13. How do you prevent the catalog from becoming stale?

Use automated ingestion rather than relying only on manual entry.

In this implementation:

- GitHub Ocean synchronizes GitHub data.
- Scheduled workflows perform regular synchronization.
- Catalog definitions are reapplied from version-controlled JSON.
- Future Kubernetes integration can ingest live runtime resources.
- Scorecards can highlight missing ownership or documentation.

### 14. What is the difference between the data model graph and entity graph?

The data model graph shows blueprint types and allowed relationships.

The entity graph shows actual instances and their relationships.

```text
Data model: Bank Service → Bank Resource
Entity graph: Transaction Service → Banking Redis
```

## Port integrations and Ocean

### 15. What is Port Ocean?

Ocean is Port's integration framework. It extracts data from external systems, transforms it according to mappings, and loads it into Port.

It supports integrations such as GitHub, Kubernetes, cloud providers, and observability platforms.

### 16. How does the GitHub Ocean integration work?

The GitHub workflow starts an Ocean container and supplies:

- Port client ID and client secret.
- Port API URL.
- GitHub API URL.
- GitHub token.
- GitHub organization.

The integration reads GitHub resources and synchronizes them into Port.

### 17. Why did the Ocean exporter initially fail?

The workflow included Port credentials but did not pass a GitHub authentication mechanism into the Ocean container.

The fix was:

```yaml
github_token: ${{ secrets.PORT_GITHUB_TOKEN }}
github_organization: ChichiAgha
```

The key lesson is that credentials available in a GitHub workflow are not automatically available inside every action or container.

### 18. How did you secure the integration credentials?

The Port client ID, Port client secret, and GitHub token are stored as encrypted GitHub Actions secrets.

The workflow references secret names without storing their values in Git:

```yaml
${{ secrets.PORT_CLIENT_SECRET }}
```

### 19. What is the difference between a GitHub PAT and a GitHub App?

A PAT represents a user. It is simple to configure, but may have broad permissions and requires rotation.

A GitHub App provides granular installation permissions, higher API limits, and automatically generated short-lived tokens. A GitHub App is generally preferable for a larger production environment.

### 20. Why run Ocean on a schedule?

A scheduled resync provides eventual consistency and recovers from missed events.

The trade-off is that synchronization is not instantaneous. For real-time updates, Ocean should run continuously with webhooks or live events enabled.

### 21. What is the rate-limit reservation threshold?

It controls when resynchronization pauses to preserve GitHub API capacity for higher-priority operations such as webhooks and actions.

A value of 95 means resync processing pauses when approximately 95% of the available quota has been consumed.

## Self-service actions

### 22. What is a self-service action?

A self-service action is a controlled workflow developers can execute through the portal.

The portal collects validated inputs, applies permissions and approvals, invokes the backend, and records the result.

### 23. What self-service actions did you implement?

The implementation provides:

1. Run tests for a selected bank service.
2. Scan all bank container images for vulnerabilities.
3. Resynchronize the bank catalog.

Catalog resynchronization requires approval because it can modify the data model.

### 24. How does Port trigger GitHub Actions?

The action uses the GitHub Ocean integration backend and specifies:

- Integration installation ID.
- GitHub organization.
- Repository.
- Workflow filename.
- Workflow inputs.

Port asks the integration to dispatch the workflow. The integration reports its final status to the Port action run.

### 25. How is catalog context passed to a workflow?

Port templates can reference the selected entity:

```json
"workflowInputs": {
  "service": "{{ .entity.identifier }}"
}
```

When the action runs from User Service, GitHub receives `user-service` as the workflow input.

### 26. Why not let developers run GitHub Actions directly?

Port adds:

- A consistent interface.
- Catalog and entity context.
- Validated inputs.
- Approval policies.
- Role-based access control.
- Audit history.
- A relationship between the action and affected entity.

GitHub remains the execution engine; Port becomes the governed control plane.

### 27. How do you design a safe self-service action?

Use:

- Restricted input types.
- Allow-listed services and environments.
- Least-privilege credentials.
- Approval for production changes.
- Idempotent backend operations.
- Timeouts.
- Clear logs and status reporting.
- Rollback procedures.
- Concurrency controls where appropriate.

### 28. Why does catalog resync require approval?

It modifies organizational metadata and may change blueprints, entities, or relationships.

Testing and scanning are read-only, so they can run without approval. Governance should match the risk of the operation.

### 29. Why did you not create a production deployment action?

The current Minikube cluster is not reachable from GitHub-hosted runners.

Creating an action without a secure execution path would be misleading. Before exposing deployment, add a self-hosted runner or remotely accessible cluster with a namespace-scoped service account and a protected GitHub environment.

This demonstrates engineering judgment: do not expose an action until it can be implemented securely and reliably.

### 30. How would you implement deployment self-service?

The Port action would collect:

- Service.
- Environment.
- Image tag.
- Optional change reference.

The GitHub workflow would:

1. Validate the image.
2. Obtain environment-scoped credentials.
3. Run Helm upgrade.
4. Wait for rollout completion.
5. Perform health checks.
6. Create or update a deployment entity.
7. Report success or failure to Port.

Production deployment would require approval.

## GitOps, automation, and reproducibility

### 31. Why store Port configuration in Git?

It provides:

- Version history.
- Peer review.
- Change attribution.
- Repeatability.
- Rollback.
- Disaster recovery.
- Consistency across environments.

It avoids relying entirely on undocumented UI configuration.

### 32. What does idempotent mean?

An idempotent operation can run repeatedly and converge on the same desired state without creating duplicates or corrupting data.

The setup checks whether blueprints and actions exist, then creates or updates them. Entities are written using upsert behavior.

### 33. How would you recreate the complete Port setup?

1. Create a Port organization.
2. Retrieve the Port client ID and secret.
3. Create a GitHub PAT or GitHub App.
4. Add `PORT_CLIENT_ID`, `PORT_CLIENT_SECRET`, and `PORT_GITHUB_TOKEN` as GitHub Actions secrets.
5. Run the GitHub Ocean workflow.
6. Run the catalog setup workflow.
7. Run the self-service setup workflow.
8. Validate the entities, relations, and actions in Port.

### 34. How do you handle ordering between related entities?

Some entities reference other entities that might not yet exist.

The setup uses Port's `create_missing_related_entities` option and then upserts the full entity definitions. This allows relationships to resolve while preserving repeatability.

### 35. What happens if someone manually changes Port?

The next repository-driven apply updates managed objects toward the version-controlled definition.

For stronger drift control, add scheduled validation that reports differences before applying potentially destructive changes.

## Scorecards and governance

### 36. What is a scorecard?

A scorecard evaluates entities against engineering standards.

Service rules might check whether:

- Ownership exists.
- Documentation exists.
- Tests are enabled.
- Monitoring is configured.
- Alerts are configured.
- A runbook exists.
- Critical vulnerabilities are unresolved.

### 37. What scorecard would you add to this project?

A production-readiness scorecard:

**Bronze**

- Repository linked.
- Owner assigned.
- Documentation present.

**Silver**

- Tests enabled.
- Monitoring enabled.
- Alerts enabled.

**Gold**

- Runbook present.
- Rollback tested.
- Security scanning enabled.
- SLO defined.

### 38. How are scorecards different from dashboards?

A dashboard visualizes information.

A scorecard evaluates compliance against explicit rules and assigns a maturity level. Dashboards show; scorecards judge.

### 39. How would you govern production actions?

Use:

- Team or role-based access.
- Mandatory approval.
- Protected GitHub environments.
- Restricted deployment inputs.
- Namespace-scoped Kubernetes access.
- Complete action audit logs.
- Change-ticket requirements for critical services.

## Security questions

### 40. What is the principle of least privilege?

Every user, token, and automation should receive only the permissions required for its responsibility.

For example, a test workflow requires repository read access but does not require Kubernetes administrator privileges.

### 41. How would you rotate secrets?

1. Generate new credentials.
2. Update GitHub Actions secrets.
3. Validate the workflows.
4. Revoke the old credentials.
5. Record the rotation in the audit process.

A GitHub App can reduce manual PAT rotation.

### 42. What are the risks of self-service?

Risks include:

- Excessive permissions.
- Invalid inputs.
- Uncontrolled cost.
- Production outages.
- Secret leakage.
- Concurrent conflicting operations.
- Inadequate auditing.

Mitigations include approvals, RBAC, input validation, scoped credentials, locking, quotas, and audit logs.

## Scenario questions

### 43. A database is down. How does the IDP help?

The engineer opens the database entity and sees:

- Which services use it.
- Service owners.
- Relevant runbooks.
- Monitoring dashboards.
- Active incidents.
- Recent deployments.
- Approved remediation actions.

The relationship model reduces discovery time during an incident.

### 44. A developer asks for Kubernetes administrator access. What do you do?

First identify the task they need to perform.

If it is repetitive and well-defined, expose a narrowly scoped self-service action rather than granting broad cluster access.

### 45. How do you measure whether an IDP is successful?

Possible metrics include:

- Developer onboarding time.
- Time required to identify service ownership.
- Deployment lead time.
- Self-service adoption.
- Reduction in platform support tickets.
- Change failure rate.
- Mean time to recovery.
- Scorecard compliance.
- Developer satisfaction.

### 46. What should not go into an IDP?

Avoid exposing:

- Unbounded shell execution.
- Raw production administrator credentials.
- Actions without ownership.
- Workflows without rollback.
- Unverified or stale catalog data.
- Every possible internal implementation detail.

The portal should provide curated, reliable workflows and trusted context.

### 47. How would this design scale beyond one repository?

I would:

- Establish organization-wide blueprint standards.
- Use GitHub App authentication.
- Use repository or organization mappings.
- Assign service ownership.
- Deploy long-running Ocean integrations.
- Add Kubernetes and cloud integrations.
- Standardize service metadata.
- Apply scorecards across all services.
- Provide reusable action templates.

## Project implementation walkthrough

### Application architecture

The banking application includes:

- React frontend.
- Python/FastAPI user service.
- Java/Spring Boot transaction service.
- Python/FastAPI activity service.
- PostgreSQL persistent storage.
- Redis balance cache.
- Kafka transaction-event streaming.
- Kubernetes and Helm deployment resources.
- Prometheus monitoring and alert rules.

### GitHub Ocean configuration

The exporter workflow passes Port and GitHub authentication to Ocean:

```yaml
- name: Run GitHub Ocean integration
  uses: port-labs/ocean-sail@v1
  with:
    type: github-ocean
    port_client_id: ${{ secrets.PORT_CLIENT_ID }}
    port_client_secret: ${{ secrets.PORT_CLIENT_SECRET }}
    port_base_url: https://api.port.io
    config: |
      github_host: https://api.github.com
      github_token: ${{ secrets.PORT_GITHUB_TOKEN }}
      github_organization: ChichiAgha
      resync_ratelimit_reservation_threshold: 95
```

### Repository-managed configuration

The main configuration files are:

```text
port/catalog/blueprints.json
port/catalog/entities.json
port/self-service/actions.json
scripts/setup-port-catalog.sh
scripts/setup-port-self-service.sh
.github/workflows/github-ocean.yml
.github/workflows/setup-port-catalog.yml
.github/workflows/setup-port-self-service.yml
.github/workflows/run-bank-service-tests.yml
```

### Demonstration sequence

1. Show the application architecture.
2. Open Port's Bank Service catalog.
3. Open Transaction Service and show language, criticality, documentation, monitoring, alerts, and runbooks.
4. Open Related Entities and show PostgreSQL, Redis, Kafka, and service dependencies.
5. Run the service-test self-service action.
6. Show the GitHub workflow execution and Port action result.
7. Open the repository configuration to demonstrate reproducibility.

## Rapid-fire definitions

### Portal or platform?

The portal is the interface; the platform supplies the underlying capabilities.

### Blueprint or entity?

A blueprint is the schema; an entity is an instance.

### Property or relation?

A property describes; a relation connects.

### Catalog or CMDB?

A modern software catalog is developer-focused, relationship-aware, and integrated with delivery workflows. A traditional CMDB is broader and primarily focused on configuration control.

### Why Port?

Port combines catalog, relationships, scorecards, and governed self-service while allowing existing tools such as GitHub Actions and Kubernetes to remain the execution layer.

### Biggest lesson?

An IDP succeeds when its data is trustworthy and its actions are safe. A polished interface cannot compensate for stale catalog data or uncontrolled automation.

## Strong interview phrases

### On troubleshooting

> I traced the Ocean failure to the authentication boundary between the GitHub Actions runner and the integration container. The solution was to pass a dedicated, least-privilege GitHub credential through encrypted Actions secrets.

### On relationships

> A flat service list is only inventory. Relationships add operational context and make dependency and blast-radius analysis possible.

### On GitOps

> I avoided making the portal dependent on undocumented UI configuration. The data model and actions are version-controlled, reviewable, and reproducible through idempotent workflows.

### On self-service

> GitHub Actions remains the execution engine, while Port provides the governed control plane with catalog context, approvals, permissions, and audit history.

### On production safety

> I deliberately did not expose a production deployment action until there was a secure execution path to the cluster. A portal action should represent a real, reliable, and appropriately governed capability.

## Strong closing answer

If asked, "Tell me about your Port experience," answer:

> I implemented Port for an event-driven banking platform. I integrated GitHub using Ocean, diagnosed and fixed an authentication issue, and modelled the application using domains, services, infrastructure resources, environments, and deployments. I represented dependencies such as the transaction service using PostgreSQL, Redis, and Kafka. I stored the model in Git and applied it through idempotent GitHub workflows. I also created governed self-service actions for service testing, image security scanning, and catalog synchronization, with approvals applied according to operational risk.

