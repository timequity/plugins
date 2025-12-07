---
name: data-engineer
description: Data engineering best practices for pipelines, transformations, and data quality.
---

# Data Engineer

Build reliable, scalable data pipelines with modern tools.

## Skills

| Skill | When to Use |
|-------|-------------|
| **pipeline-design** | Design ETL/ELT architecture |
| **dbt-expert** | SQL transformations, models, tests |
| **airflow-workflows** | DAG design, scheduling, operators |
| **data-modeling** | Dimensional modeling, normalization |
| **data-quality** | Tests, validation, monitoring |
| **warehouse-optimization** | Partitioning, indexes, query tuning |
| **spark-basics** | Distributed processing with PySpark |
| **data-governance** | Lineage, cataloging, access control |

## Commands

| Command | Purpose |
|---------|---------|
| `/data:pipeline` | Design data pipeline architecture |
| `/data:model` | Create dbt model with tests |
| `/data:quality` | Add data quality checks |
| `/data:dag` | Create Airflow DAG |

## Templates

- **dbt-starter** - dbt project with best practices
- **airflow-etl** - Airflow DAGs with common patterns
- **spark-job** - PySpark job template

## Philosophy

- **Test everything** - Data quality is non-negotiable
- **Idempotent** - Pipelines can be re-run safely
- **Observable** - Logging, metrics, alerts
- **Documented** - Lineage and business context
