# CrashLoopBackOff Runbook

## Meaning

CrashLoopBackOff means a container is repeatedly starting, crashing, and being restarted by Kubernetes.

## Common Causes

- Missing environment variables
- Missing Kubernetes Secret
- Invalid ConfigMap
- Application startup error
- Database connection failure
- Wrong image version
- Permission issue
- Port binding issue
- Dependency service unavailable

## Debug Commands

```bash
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous
kubectl get events -n <namespace> --sort-by=.lastTimestamp
kubectl rollout history deployment/<deployment-name> -n <namespace>
