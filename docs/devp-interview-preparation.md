# Senior DevOps / Developer Experience Interview Preparation

This guide is tailored to the Senior AWS DevOps Engineer role supporting an Internal Developer Portal for more than 2,000 engineers.

It uses evidence visible in the Techbleat Global Bank project. Sections marked **Complete with your evidence** must be filled with genuine examples from your employment history. Do not present hypothetical examples as personal experience.

## Core positioning

Do not position yourself only as a Port specialist. Position yourself as a DevOps and platform engineer who understands how an IDP brings together AWS, infrastructure as code, CI/CD, observability, ownership, documentation, standards, and safe self-service.

### Thirty-second introduction

> I am a DevOps and platform-focused engineer with hands-on experience across infrastructure as code, CI/CD, containers, Kubernetes, Helm, observability, security scanning, and developer enablement. In my banking platform work, I built a microservices delivery environment and then implemented an internal developer portal pattern using Port. I automated GitHub ingestion, modelled services and infrastructure relationships, stored the portal configuration in Git, and exposed governed self-service workflows. My interest in this role is the opportunity to apply those engineering principles at organisational scale: making delivery safer, more consistent, and easier for engineering teams.

## What this role is testing

Prepare across five areas:

| Area | Suggested preparation weight |
| --- | ---: |
| IDP and developer experience | 25% |
| AWS architecture and infrastructure as code | 25% |
| CI/CD and software supply-chain security | 20% |
| Reliability and operations | 15% |
| Leadership, influence, and mentoring | 15% |

## Your verified project evidence

The banking platform demonstrates:

- A React frontend.
- Python/FastAPI user and activity services.
- A Java/Spring Boot transaction service.
- PostgreSQL, Redis, and Kafka dependencies.
- Docker containerisation.
- Kubernetes manifests packaged using Helm.
- Horizontal Pod Autoscaling for the transaction service.
- Prometheus rules, ServiceMonitors, Grafana dashboards, and runbooks.
- GitHub Actions for testing, builds, Gitleaks, Checkov, SonarQube, and Trivy.
- A Port GitHub Ocean integration.
- Repository-managed Port blueprints, entities, and relations.
- Idempotent Port API automation.
- Port self-service actions backed by GitHub workflows.

## Opening questions

### Tell us about yourself and why you are suitable for this role.

> I am a DevOps and platform-focused engineer who enjoys converting repeated delivery and operational tasks into reusable, secure capabilities. My practical experience covers CI/CD, infrastructure and configuration as code, Linux scripting, containers, Kubernetes, Helm, observability, and security automation.
>
> In the Techbleat Global Bank platform, I worked across the full delivery path. I supported four application services, packaged the runtime in Helm, added monitoring and alerting, and implemented GitHub Actions pipelines covering tests, builds, secret detection, static analysis, infrastructure checks, and container scanning. I then added an internal developer portal pattern using Port. The portal models services, dependencies, infrastructure resources, and environments, while GitHub Ocean synchronizes source-system data. Its configuration is version-controlled and applied using idempotent automation.
>
> This role appeals to me because it combines hands-on engineering with developer enablement and technical leadership. At a scale of more than 2,000 engineers, success requires more than selecting a portal product. It requires trustworthy metadata, reusable golden paths, secure self-service, highly available AWS foundations, measurable developer outcomes, and sustained engagement with engineering teams.

### Why do you want to work on an Internal Developer Platform?

> Platform engineering has leverage. Solving a delivery problem once for a shared platform can remove friction for many teams. I am interested in the intersection of automation, reliability, and developer experience: creating capabilities that make the safe path the easiest path. An IDP makes those capabilities discoverable and connects them to service ownership, documentation, dependencies, standards, and operational information.

### Why this role rather than a conventional DevOps position?

> A conventional DevOps role can become focused on supporting individual delivery teams. This role is explicitly about creating reusable organisational capabilities. That requires product thinking, platform engineering, technical breadth, and influence. Those are the areas in which I want to have the greatest impact.

## Internal Developer Portal questions

### What is an Internal Developer Portal?

> An IDP is a central interface through which engineers can discover services, understand ownership and dependencies, find documentation and operational information, and execute approved workflows. It reduces cognitive load by presenting capabilities from GitHub, CI/CD, AWS, Kubernetes, observability, and incident tooling through one consistent experience.

### Is a portal the same as a platform?

> No. The platform provides the underlying infrastructure, automation, policies, and operational capabilities. The portal is the front door that makes those capabilities discoverable and usable. A portal without a capable platform is only a user interface; a platform without an effective portal can remain difficult for developers to navigate.

### What would you include in an IDP for 2,000 engineers?

> I would design it in layers. The experience layer would include a searchable service catalog, ownership, documentation, scorecards, dependency views, templates, and self-service actions. The integration layer would connect source control, CI/CD, AWS, Kubernetes, observability, security, and incident management. The control layer would provide SSO, RBAC, policy, approvals, auditability, and workflow orchestration. The operating model would define platform ownership, contribution standards, support, versioning, deprecation, and SLOs.
>
> At that scale I would decentralise service metadata ownership to product teams while centralising schemas, controls, integration patterns, and reusable capabilities within the platform team.

### How would you keep the catalog accurate?

> I would keep metadata close to its source, automate discovery, validate metadata in CI, consume events for fast updates, and run scheduled reconciliation to recover from missed events. Every entity should have an owner and lifecycle. I would monitor ingestion failures and catalog staleness, and use scorecards to highlight missing ownership, documentation, runbooks, or operational metadata. Catalog freshness should have an SLO because a catalog that developers do not trust rapidly loses adoption.

### How do you balance standards with team autonomy?

> I would standardise the common 80% using versioned golden paths, reusable pipeline components, secure defaults, and supported infrastructure modules. Teams should have controlled extension points for the remaining 20%. Where teams need to deviate, the exception should be explicit, justified, visible, and reviewed. The aim is a paved road that is easier and safer, not a rigid platform that prevents legitimate innovation.

### Port or Backstage: how would you choose?

> I would begin with organisational requirements rather than product preference. I would compare time to value, customisation needs, operating cost, integration coverage, hosting model, security, contribution model, data ownership, workflow support, and the skills available internally. Port can reduce the amount of portal software the organisation must operate, while Backstage offers extensive code-level customisation and ecosystem flexibility. A proof of value using representative workflows and teams would validate the decision.

### How would you drive adoption?

> I would begin with developer interviews and workflow data to identify high-friction tasks. I would deliver a small number of valuable golden paths, recruit early adopters, measure outcomes, and improve them based on feedback. I would establish champions across teams, publish migration guidance, and make contribution and support models clear. Adoption should follow demonstrated value: the paved road must be easier and safer than the alternatives.

### How would you measure IDP success?

> I would combine platform, developer-experience, and delivery metrics. Platform measures include availability, latency, ingestion lag, and workflow success. Experience measures include active users, self-service adoption, task completion time, onboarding time, support-ticket reduction, and developer satisfaction. Delivery outcomes include lead time, deployment frequency, change failure rate, and recovery time. I would avoid relying on page views alone because usage does not automatically prove value.

## Your Port implementation

### What did you implement?

> I implemented a repository-managed Port setup for an event-driven banking application. GitHub Ocean synchronizes repository data. Six custom blueprints model the business domain, application, services, resources, environments, and deployments. Eleven initial entities describe the four application services, PostgreSQL, Redis, Kafka, and development and production environments. Relations show service dependencies and resource usage.
>
> I used GitHub Actions and shell automation to authenticate to the Port API, create or update blueprints, and upsert entities. The configuration is idempotent, reviewable, and reproducible. I also created self-service actions for targeted service tests, image security scanning, and controlled catalog synchronization.

### What problems did you diagnose?

> The GitHub Ocean workflow initially failed because Port credentials were present but GitHub authentication was not passed into the integration container. I inspected the workflow state and Port's current integration schema, identified the missing `github_token` and organisation configuration, corrected the workflow, and verified a successful run.
>
> The first catalog apply then exposed an entity-ordering problem: the frontend related to services that had not been created yet. I used Port's supported missing-related-entity behavior and retained upsert semantics. The corrected run created the complete catalog and relationships successfully.

### What would you improve for enterprise production?

> I would replace the PAT with GitHub App authentication, run Ocean continuously for live events, integrate EKS and AWS accounts, add team ownership, implement production-readiness scorecards, ingest deployment history, define portal SLOs, add drift detection, and test backup and recovery. I would also add approved deployment, rollback, restart, and scaling actions after establishing a secure execution path to the runtime platform.

## Self-service and golden paths

### What makes a good self-service workflow?

> It should solve a real developer problem, be discoverable, safe by default, idempotent, observable, auditable, and supported. Inputs should be bounded and validated. Credentials should use least privilege. Higher-risk operations should require approval. The workflow should report progress clearly and have a defined rollback or recovery process.

### Why use Port rather than letting developers run GitHub Actions directly?

> GitHub Actions remains the execution engine, but Port adds catalog context, a consistent interface, validated inputs, permissions, approvals, and an entity-level audit trail. A developer can run an action from the affected service rather than finding the correct repository, workflow, input format, and operating procedure manually.

### How would you implement a deployment action?

> The action would accept an allow-listed service, environment, and immutable image reference. Port would dispatch a reusable deployment workflow. The workflow would authenticate using short-lived environment-scoped credentials, run Helm upgrade, wait for rollout health, execute smoke tests, record the deployment, and report the result. Production would use a protected environment, explicit approval, concurrency controls, and rollback support.

### Why did you not expose production deployment in the bank project?

> The development runtime is Minikube and cannot be reached securely from GitHub-hosted runners. Exposing an action without a real and secure execution path would be misleading. I documented the limitation and would add a self-hosted runner or a remotely accessible cluster with a namespace-scoped service account before enabling deployment operations.

## CI/CD questions

### Describe your CI/CD approach for the banking platform.

> The primary quality workflow runs on pull requests, pushes, and manual dispatch. It starts with Gitleaks secret scanning. It then runs frontend tests and builds, Python tests for the user and activity services, and Maven tests for the transaction service. After tests, it runs SonarQube analysis where configured and Checkov against Dockerfiles. It builds each container image, scans it with Trivy, uploads the reports, and fails the gate when high or critical vulnerabilities are found.

### How would you design reusable pipelines for many teams?

> I would use versioned reusable workflows with clearly documented inputs and outputs. They would implement secure defaults for tests, scanning, artifact creation, provenance, deployment, and reporting. Consumers would pin supported versions rather than reference an unversioned branch. The components themselves would have tests, release notes, compatibility guarantees, telemetry, ownership, and a deprecation process.

### Describe a secure software delivery pipeline.

> A secure pipeline should run tests, static analysis, dependency and secret scanning, create an immutable artifact, generate an SBOM and provenance, scan the built artifact, sign it where appropriate, and promote the same artifact between environments. CI should use OIDC or another short-lived authentication mechanism rather than long-lived cloud keys. Production deployment should require policy checks and approval, and deployment results should be observable and auditable.

### How do you handle pipeline failures?

> I distinguish product failures from platform failures, make errors actionable, retain logs and artifacts, and define retry behavior only for genuinely transient operations. Shared pipeline components should publish reliability metrics so repeated failures can be treated as platform problems. I avoid using `continue-on-error` for mandatory gates unless the exception is explicit and visible.

### What would you improve in the current bank pipelines?

> I would publish immutable images to a registry, generate and sign SBOM and provenance metadata, use OIDC for registry and AWS access, pin third-party actions to immutable commit SHAs, separate advisory and mandatory security policies, add caching metrics, and implement deployment promotion rather than rebuilding per environment.

## AWS architecture

### How would you design the AWS platform for this workload?

> I would start with AWS Organizations and separate accounts for production, non-production, security, logging, and shared platform services. Workloads would run across multiple Availability Zones. Depending on organisational standards, services could run on EKS or ECS, with managed data services such as RDS and ElastiCache where appropriate. Kafka could use MSK if its operational and cost profile is justified.
>
> Networking would use private subnets for workloads and data, controlled ingress through managed load balancers, Route 53 for DNS, and central egress controls. IAM roles and workload identity would replace static credentials. Secrets Manager and KMS would protect secrets and encryption keys. CloudWatch and the organisation's observability platform would collect logs, metrics, and traces. Terraform modules would provide repeatable account and workload configuration.

### How would you make it highly available and resilient?

> I would use Multi-AZ workloads, health-based load balancing, horizontal scaling, managed database failover, tested backups, and stateless application components where possible. Asynchronous integrations would use queues, retry with backoff, dead-letter handling, and idempotent consumers. I would define SLOs, alert on user-impacting symptoms, test restoration, and document degraded modes when dependencies such as GitHub are unavailable.

### How would you secure AWS access from CI/CD?

> I would use GitHub OIDC federation to assume narrowly scoped IAM roles. Trust policies would restrict repository, branch, environment, and workflow context. Development and production would use separate roles, with production protected by approval. Sessions would be short-lived and recorded in CloudTrail. Long-lived AWS access keys would not be stored in repository secrets.

### How would you structure AWS accounts?

> I would use separate organisational units and accounts to create security and billing boundaries. A typical structure includes management, security tooling, log archive, network, shared services, non-production, and production accounts. Service Control Policies would establish organisation-level guardrails, while workload roles provide the application-specific permissions.

## Infrastructure as code

### How do you manage infrastructure as code at scale?

> I use small, versioned modules with clear ownership and contracts. State is separated by bounded context and stored remotely with encryption, locking, access control, and backup. Pull requests run formatting, validation, security checks, and plans. Production apply requires approval. I also use drift detection, policy as code, module upgrade guidance, and a documented import process for existing resources.

### Why separate Terraform state?

> Smaller state boundaries reduce blast radius, lock contention, and unnecessary privileges. They also allow different lifecycle and ownership models. State should not be split so aggressively that every dependency becomes a manual coordination problem, so the boundary should reflect operational ownership and change coupling.

### How would you test Terraform?

> I would run formatting and validation, static checks such as Checkov or tfsec, policy checks, and speculative plans. Shared modules should have automated tests against temporary environments where practical. Critical changes should include post-apply verification and scheduled drift detection.

## Linux and scripting

### Give an example of your Linux and scripting experience.

> In the bank portal implementation, I wrote Bash automation using strict mode, `curl`, and `jq`. The scripts validate required environment variables, exchange Port machine credentials for an access token, inspect existing resources, create or patch blueprints and actions, and upsert entities. They return non-zero status on API failure and are safe to rerun. I also used command-line tools to inspect Git history, validate JSON and YAML, retrieve GitHub Actions metadata, and diagnose workflow failures.

### What practices do you use in shell scripts?

> I use strict error handling, quote variables, validate required inputs, avoid printing secrets, use temporary files safely, check HTTP status codes, make operations idempotent, and keep scripts small enough to test and understand. For complex logic or data structures, I would move to a language with stronger testing and error-handling support.

## Reliability and operations

### What would you monitor for the IDP?

> Platform metrics include availability, latency, errors, saturation, authentication failures, integration success, ingestion lag, workflow dispatch success, queue depth, API rate limits, and database health. Developer-experience metrics include active users, self-service completion, task duration, onboarding time, and support requests. Delivery outcomes include lead time, deployment frequency, change failure rate, and recovery time.

### GitHub is unavailable. What should happen?

> The portal should continue serving the last known catalog where safe. New GitHub-dependent workflows should fail clearly or queue only where delayed execution is acceptable. Synchronization should retry with bounded backoff and reconciliation should recover missed changes. A third-party outage should not cause the entire portal to become unavailable.

### A database is down. How does the catalog help?

> An engineer can open the database entity and see consuming services, ownership, runbooks, dashboards, recent deployments, and available remediation actions. The relationship model reduces time spent discovering blast radius and finding the correct responders.

### How do you approach an incident?

> I first establish user impact and stabilise the service. I create a shared timeline, use telemetry to test hypotheses, communicate at an appropriate cadence, and avoid making multiple uncontrolled changes. After recovery, I preserve evidence, identify contributing technical and process factors, and track corrective actions through completion. The review should be blameless and focused on learning.

## Security and governance

### What is least privilege?

> Every human and workload receives only the permissions needed for its responsibility, for the shortest practical duration. For example, a test workflow needs repository read access but no Kubernetes administration. A deployment workflow should receive a namespace- and environment-scoped role rather than cluster administrator access.

### What risks does self-service introduce?

> Risks include excessive permissions, invalid input, uncontrolled cost, production outages, conflicting operations, secret exposure, and insufficient auditing. I mitigate these using bounded inputs, policy, RBAC, approvals, quotas, least-privilege credentials, concurrency controls, audit logs, and rollback procedures.

### A developer asks for Kubernetes administrator access. What do you do?

> I first understand the task. If it is repetitive and well-defined, I provide a narrowly scoped, auditable self-service workflow instead of broad access. If direct access is justified, it should be time-bound, approved, and limited to the necessary environment and resources.

## Leadership and behaviour questions

These answers require genuine examples from your work. Complete the blanks before the interview.

### Tell us about a time you influenced teams to adopt a standard.

**Complete with your evidence**

- Situation: Teams were using `[different process/tool]`, causing `[measurable problem]`.
- Task: I was responsible for `[your responsibility]`.
- Action: I gathered `[evidence]`, involved `[stakeholders]`, created `[prototype/standard]`, addressed `[objections]`, and supported adoption through `[documentation/workshops/pairing]`.
- Result: Adoption reached `[number/%]`, while `[lead time/failures/support requests]` changed by `[measure]`.
- Reflection: I learned `[specific learning]`.

Suggested answer shape:

> I did not begin by mandating a tool. I first quantified the cost of the existing variation and involved representatives from the affected teams. I created a small reusable implementation, documented extension points, and used early adopters to test it. I incorporated feedback, published a migration path, and measured the result. The important lesson was that adoption depended as much on trust and support as on technical quality.

### Tell us about a time you mentored an engineer.

**Complete with your evidence**

- Engineer's starting point: `[blank]`.
- Skill or responsibility being developed: `[blank]`.
- Actions you took: `[pairing, feedback, delegated ownership, workshops]`.
- Result for the engineer: `[blank]`.
- Result for the team: `[blank]`.

Suggested answer shape:

> I agreed a clear development goal with the engineer and combined explanation with progressively greater ownership. We paired initially, then I reviewed their design decisions rather than only correcting implementation details. I created opportunities for them to present the work and support others. The result was `[your genuine result]`.

### Tell us about a technical disagreement.

**Complete with your evidence**

- Decision being debated: `[blank]`.
- Stakeholders and constraints: `[blank]`.
- Evidence you gathered: `[blank]`.
- How you included opposing views: `[blank]`.
- Decision and result: `[blank]`.

Avoid portraying the other person as incompetent. Show listening, evidence, and accountability.

### Tell us about a production incident.

**Complete with your evidence**

- User impact: `[blank]`.
- Your role: `[blank]`.
- Stabilisation action: `[blank]`.
- Diagnosis: `[blank]`.
- Communication: `[blank]`.
- Recovery: `[blank]`.
- Preventive improvements: `[blank]`.
- Measurable result: `[blank]`.

### Tell us about a significant CI/CD improvement.

**Complete with your evidence**

- Previous process and pain: `[blank]`.
- Your responsibility: `[blank]`.
- Pipeline or reusable component created: `[blank]`.
- Security/reliability controls added: `[blank]`.
- Teams affected: `[blank]`.
- Lead-time or failure-rate improvement: `[blank]`.

### Tell us about an infrastructure-as-code implementation.

**Complete with your evidence**

- Infrastructure and scale: `[blank]`.
- Previous provisioning method: `[blank]`.
- IaC structure and state approach: `[blank]`.
- Testing and approval controls: `[blank]`.
- Migration method: `[blank]`.
- Result: `[blank]`.

## Technical exercise preparation

The exercise may ask you to design or implement:

- A catalog data model.
- A software template.
- A reusable pipeline.
- An AWS architecture.
- Terraform infrastructure.
- A self-service workflow.
- Security and approval controls.
- Observability.
- Operational documentation.

Do not use AI during the actual exercise because the vacancy explicitly prohibits it. Use this guide only for preparation.

### Recommended exercise structure

1. Requirements and assumptions.
2. Architecture and boundaries.
3. Data model.
4. Security model.
5. Delivery workflow.
6. Reliability and failure handling.
7. Observability and SLOs.
8. Developer experience.
9. Trade-offs.
10. Future improvements.

### Technical exercise checklist

- Are assumptions explicit?
- Is there a diagram?
- Are trust boundaries shown?
- Are credentials short-lived and scoped?
- Is the workflow idempotent?
- Are production approvals defined?
- Is failure handling explained?
- Are logs, metrics, and traces considered?
- Is ownership clear?
- Are trade-offs discussed?
- Can the solution evolve without a rewrite?

## Six STAR stories to prepare

Prepare genuine examples for:

1. A significant CI/CD improvement.
2. Infrastructure or configuration as code.
3. A production incident or difficult operational problem.
4. Influencing teams to adopt a standard.
5. Mentoring or developing another engineer.
6. Designing or improving a developer platform.

For every story, record:

```text
Situation:
Task:
Action I personally took:
Result with evidence:
What I learned:
```

## Questions to ask the interviewers

1. How do you currently measure developer experience and portal adoption?
2. Which capabilities are already mature, and where is the greatest developer friction?
3. How is ownership divided between the Developer Experience team and product teams?
4. How do teams contribute to shared templates and platform capabilities?
5. What is the current AWS account and runtime model?
6. How are portal and pipeline changes versioned and rolled out?
7. What would success look like after six and twelve months?
8. What are the largest technical and organisational constraints facing the platform today?

## Final reminders

- Say **I** when describing your contribution.
- Use metrics where you genuinely have them.
- Discuss trade-offs rather than claiming one perfect solution.
- Treat the IDP as a product, not only a tool.
- Connect technical choices to developer and organisational outcomes.
- Do not claim enterprise scale that you have not personally operated.
- Distinguish verified experience from what you would design at scale.

## Closing answer

> My strength is not limited to knowing a particular portal product. I understand how to connect infrastructure, CI/CD, security, observability, ownership, and developer workflows into a reliable platform experience. The banking implementation demonstrates that I can work hands-on across those layers, diagnose integration failures, model operational context, and automate repeatable self-service. At organisational scale, I would combine that technical approach with product thinking, clear standards, measurable outcomes, and sustained engagement with engineering teams.

