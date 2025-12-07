---
name: security-hardening
description: Infrastructure security, CIS benchmarks, and vulnerability scanning.
---

# Security Hardening

## CIS Benchmarks

### AWS

- Enable CloudTrail in all regions
- Enable VPC Flow Logs
- Disable root account access keys
- Enable MFA for root and IAM users
- Encrypt EBS volumes

### Kubernetes

- Enable RBAC
- Use Network Policies
- Run as non-root
- Read-only root filesystem
- Resource limits

## Pod Security

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
  containers:
    - name: app
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL
```

## Network Security

```yaml
# Network Policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - port: 8080
```

## Secrets Management

```yaml
# External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: app-secrets
  data:
    - secretKey: database-url
      remoteRef:
        key: prod/database
        property: url
```

## Scanning

```bash
# Container scanning
trivy image myapp:latest

# IaC scanning
tfsec .
checkov -d .

# Kubernetes scanning
kubesec scan pod.yaml
```
