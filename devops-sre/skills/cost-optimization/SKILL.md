---
name: cost-optimization
description: Cloud cost management, rightsizing, and FinOps practices.
---

# Cost Optimization

## FinOps Principles

1. **Visibility** - Know what you spend
2. **Optimization** - Reduce waste
3. **Governance** - Control growth

## Quick Wins

| Action | Savings |
|--------|---------|
| Reserved instances | 30-70% |
| Spot instances | 60-90% |
| Rightsizing | 20-40% |
| Unused resources | 100% |
| Storage tiering | 50-80% |

## Rightsizing

```bash
# AWS: Find underutilized instances
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxx \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-31T00:00:00Z \
  --period 86400 \
  --statistics Average
```

**If CPU < 20% avg:** Downsize or use smaller instance.

## Reserved vs Spot

| Workload | Recommendation |
|----------|----------------|
| Steady baseline | Reserved (1-3 year) |
| Variable load | On-demand + Spot |
| Batch processing | Spot |
| Stateless services | Spot with fallback |

## Storage Optimization

```hcl
# S3 Lifecycle
resource "aws_s3_bucket_lifecycle_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    id     = "archive"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }
  }
}
```

## Monitoring Costs

- AWS Cost Explorer
- GCP Billing Reports
- Azure Cost Management
- Third-party: CloudHealth, Spot.io

## Tagging Strategy

```hcl
tags = {
  Environment = "production"
  Team        = "platform"
  Service     = "api"
  CostCenter  = "engineering"
}
```
