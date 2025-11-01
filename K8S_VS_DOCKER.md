# Kubernetes Pod vs Docker Container

## Docker Container
A standalone packaged application with dependencies.

**Key Features:**
- Single process/application
- Runs on one host
- Manual scaling
- No orchestration

## Kubernetes Pod
Smallest unit in K8s, containing one or more containers.

**Key Features:**
- Can group containers
- Scheduled across nodes
- Auto-restart on failure
- Part of orchestration

## Critical Differences

| Feature | Docker | Kubernetes Pod |
|---------|--------|----------------|
| Orchestration | None | Full |
| Scaling | Manual | Automatic |
| Self-Healing | No | Yes |
| Load Balancing | External | Built-in |

## Why Kubernetes?

**Docker:** Packages the app  
**Kubernetes:** Runs it at scale reliably

Benefits: auto-scaling, self-healing, zero-downtime updates, load balancing
