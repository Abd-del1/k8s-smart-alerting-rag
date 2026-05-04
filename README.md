# Kubernetes Smart Alerting System using RAG, OpenAI, ArgoCD, and Email Notifications

## Overview

This project is a production-style Kubernetes smart alerting platform that transforms raw infrastructure alerts into meaningful, context-rich incident reports.

Instead of sending simple alerts like:

> Pod is crashing in namespace `payments`

this system collects Kubernetes context, retrieves relevant runbooks using RAG, analyzes the incident using OpenAI, and sends a clear email alert with probable root cause, evidence, severity, and remediation steps.

The project follows a GitOps-based deployment model using GitHub, GitHub Actions, and ArgoCD.

---

## Problem Statement

Traditional Kubernetes alerts often lack enough context for fast incident response. Engineers usually need to manually check pod logs, events, deployment history, node status, and internal runbooks before understanding the real issue.

This project solves that problem by automatically enriching alerts with:

- Kubernetes pod logs
- Pod events
- Deployment metadata
- Namespace-level events
- Relevant troubleshooting runbooks
- AI-generated root cause analysis
- Recommended remediation steps
- Email-based incident notification

---

## Key Features

- Receives alerts from Prometheus Alertmanager
- Collects Kubernetes context using the Kubernetes API
- Uses RAG to retrieve relevant troubleshooting documents
- Uses OpenAI to generate incident summaries and root cause analysis
- Sends enriched alerts through email
- Deploys through ArgoCD using GitOps
- Uses GitHub as the source of truth
- Includes GitHub Actions for CI validation and Docker image builds
- Designed with production DevOps practices in mind

---

## Architecture

```text
GitHub Repository
    |
    |-- Application code
    |-- Kubernetes manifests
    |-- ArgoCD application manifest
    |-- Monitoring configuration
    |-- RAG knowledge base
    |
    v
GitHub Actions
    |
    |-- Validate code
    |-- Build Docker image
    |-- Push image to GitHub Container Registry
    |
    v
GitHub Container Registry
    |
    v
ArgoCD
    |
    |-- Watches GitHub repository
    |-- Syncs desired state to Kubernetes
    |
    v
Kubernetes Cluster
    |
    |-- smart-alert-api
    |-- Prometheus
    |-- Alertmanager
    |-- kube-state-metrics
    |
    v
Smart Alerting Workflow
    |
    |-- Alertmanager sends alert to API
    |-- API collects Kubernetes logs/events
    |-- RAG retrieves relevant runbooks
    |-- OpenAI analyzes the incident
    |-- Email alert is sent to DevOps/SRE team
High-Level Workflow
Prometheus detects an issue in the Kubernetes cluster.
Alertmanager receives and routes the alert.
Alertmanager sends the alert payload to the Smart Alert API webhook.
The Smart Alert API extracts alert details such as namespace, pod, deployment, and severity.
The API collects live Kubernetes context such as logs, pod status, restart count, and events.
The RAG engine searches internal runbooks and troubleshooting documents.
OpenAI analyzes the alert, Kubernetes context, and runbook data.
The system generates a smart incident report.
The final enriched alert is sent through email.
Example Smart Alert
Subject: Critical Kubernetes Alert - payment-api CrashLoopBackOff

Service: payment-api
Namespace: payments
Severity: Critical
Alert: PodCrashLoopBackOff

Summary:
The payment-api pod is repeatedly crashing after the latest deployment.

Likely Root Cause:
The application is failing during startup because the required DB_PASSWORD environment variable is missing.

Evidence:
- Pod is in CrashLoopBackOff state
- Restart count is 8
- Last container exit code is 1
- Logs show: "DB_PASSWORD environment variable not found"
- Issue started after the latest deployment rollout

Recommended Actions:
1. Verify the Kubernetes Secret used by payment-api.
2. Check whether Vault or External Secrets synced the latest secret value.
3. Restart the deployment after restoring the secret.
4. Roll back the deployment if the secret cannot be restored quickly.

Useful Commands:
kubectl logs payment-api-7d9f8c6f9b-x2abc -n payments
kubectl describe pod payment-api-7d9f8c6f9b-x2abc -n payments
kubectl get events -n payments --sort-by=.lastTimestamp
kubectl rollout history deployment/payment-api -n payments
kubectl rollout undo deployment/payment-api -n payments
Tech Stack
Category	Tools
Container Orchestration	Kubernetes
Monitoring	Prometheus, Alertmanager
GitOps	ArgoCD
CI/CD	GitHub Actions
Container Registry	GitHub Container Registry
Backend	Python, FastAPI
AI	OpenAI API
RAG / Vector Search	ChromaDB
Alert Delivery	Email / SMTP
Containerization	Docker
Kubernetes Access	Kubernetes Python Client
Configuration	YAML, Kustomize
Future Infrastructure	Terraform, AWS EKS
Repository Structure
k8s-smart-alerting-rag/
│
├── app/
│   ├── main.py
│   ├── api/
│   ├── core/
│   └── services/
│
├── knowledge-base/
│   ├── crashloopbackoff.md
│   ├── imagepullbackoff.md
│   ├── oomkilled.md
│   └── node-not-ready.md
│
├── k8s/
│   ├── base/
│   │   ├── namespace.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── kustomization.yaml
│   │
│   └── overlays/
│       ├── dev/
│       └── prod/
│
├── argocd/
│   └── smart-alerting-app.yaml
│
├── monitoring/
│   ├── prometheus/
│   └── alertmanager/
│
├── docs/
│   └── architecture.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
Current Project Status

The initial version of the project includes:

Basic FastAPI webhook service
Dockerfile for containerization
Kubernetes deployment and service manifests
ArgoCD application manifest
GitHub Actions CI workflow
Initial RAG knowledge base folder
Email alerting planned as the notification channel
Prerequisites

Before running this project, make sure you have the following installed:

Git
Docker
kubectl
Minikube, Kind, or a Kubernetes cluster
ArgoCD
Python 3.11+
GitHub account
GitHub Container Registry access
OpenAI API key
SMTP email credentials
Environment Variables

Create a .env file locally using .env.example as a reference.

OPENAI_API_KEY=
SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
ALERT_EMAIL_FROM=
ALERT_EMAIL_TO=
ENVIRONMENT=dev

Never commit real secrets to GitHub.

Use Kubernetes Secrets, External Secrets, Vault, or a cloud secrets manager for production environments.

Running Locally
1. Clone the repository
git clone https://github.com/Abd-del1/k8s-smart-alerting-rag.git
cd k8s-smart-alerting-rag
2. Create a virtual environment
python -m venv .venv

Activate it:

source .venv/bin/activate

For Windows PowerShell:

.venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Run the FastAPI app
uvicorn app.main:app --reload
5. Test the health endpoint

Open:

http://localhost:8000/health

Expected response:

{
  "status": "healthy",
  "service": "smart-alert-api",
  "timestamp": "..."
}
Running with Docker
1. Build the Docker image
docker build -t smart-alert-api:local .
2. Run the container
docker run -p 8000:8000 smart-alert-api:local
3. Test the service
curl http://localhost:8000/health
Kubernetes Deployment

The Kubernetes manifests are stored in:

k8s/base/

Apply manually for testing:

kubectl apply -k k8s/base

Check the namespace:

kubectl get ns

Check the pods:

kubectl get pods -n smart-alerting

Check the service:

kubectl get svc -n smart-alerting
ArgoCD GitOps Deployment

The ArgoCD application manifest is stored in:

argocd/smart-alerting-app.yaml

Apply it using:

kubectl apply -f argocd/smart-alerting-app.yaml

Check ArgoCD application status:

kubectl get applications -n argocd

Once ArgoCD syncs the application, it will deploy the resources from:

k8s/base/

This means GitHub becomes the source of truth for the Kubernetes deployment.

GitHub Container Registry Image

The Docker image is expected to be pushed to GitHub Container Registry:

ghcr.io/abd-del1/k8s-smart-alerting-rag:latest

The Kubernetes deployment uses this image:

image: ghcr.io/abd-del1/k8s-smart-alerting-rag:latest

In later stages, GitHub Actions will automatically build and push versioned images using commit SHA tags.

GitHub Actions CI

The CI workflow is located at:

.github/workflows/ci.yml

Current CI tasks:

Checkout repository
Set up Python
Install dependencies
Validate Python syntax
Build Docker image

Planned CI improvements:

Run unit tests
Scan Docker image
Push image to GHCR
Update Kubernetes image tag
Let ArgoCD sync the new version
RAG Knowledge Base

The knowledge base is stored in:

knowledge-base/

Example runbooks:

crashloopbackoff.md
imagepullbackoff.md
oomkilled.md
node-not-ready.md

These files are used by the RAG engine to retrieve relevant troubleshooting information when an alert is received.

Example:

If an alert contains:

CrashLoopBackOff

the system retrieves:

knowledge-base/crashloopbackoff.md

Then the retrieved context is passed to OpenAI along with live Kubernetes logs and events.

Alert Types Planned

The system will support smart analysis for:

CrashLoopBackOff
ImagePullBackOff
OOMKilled
PodNotReady
NodeNotReady
High CPU usage
High memory usage
Deployment replica mismatch
PersistentVolume storage pressure
Failed rollout
Application health check failures
Email Alerting

Email is the chosen notification channel for this project.

The enriched alert email will include:

Alert name
Namespace
Pod or deployment name
Severity
Summary
Probable root cause
Evidence
Recommended actions
Useful kubectl commands
Relevant runbook references

Example email subject:

[CRITICAL] Kubernetes Alert: payment-api CrashLoopBackOff
Security Considerations

This project is designed with production security practices in mind:

OpenAI API key is not stored in Git
SMTP credentials are not stored in Git
Kubernetes access should use a dedicated ServiceAccount
RBAC permissions should be minimal
Secrets should be stored using Kubernetes Secrets, Vault, or External Secrets
GitHub Actions should use repository secrets
ArgoCD should deploy from Git instead of manual cluster changes
Application should only collect the minimum required Kubernetes data
Sensitive log data should be filtered before being sent to AI services
Future Enhancements

Planned improvements:

Add Kubernetes RBAC manifests
Add Alertmanager email and webhook configuration
Add real OpenAI analysis service
Add ChromaDB-based vector search
Add Prometheus alert rules
Add Helm chart
Add Kustomize overlays for dev and prod
Add image scanning in GitHub Actions
Add GitHub Actions push to GHCR
Add ArgoCD image updater
Add incident history memory
Add alert deduplication
Add severity scoring
Add rollback recommendation logic
Add support for Jira ticket creation
Add support for Slack and Microsoft Teams
Add Grafana dashboard links
Add Terraform infrastructure for AWS EKS
Production Design Principles

This project follows these DevOps and SRE principles:

GitOps-based deployment
Infrastructure and application configuration stored in Git
Automated validation through CI
Kubernetes-native deployment
Alert enrichment before notification
Runbook-driven incident response
Least-privilege Kubernetes access
Secure secret management
Observability-first architecture
Repeatable and scalable deployment model
Learning Goals

This project demonstrates hands-on experience with:

Kubernetes production workloads
Prometheus and Alertmanager
ArgoCD GitOps workflows
GitHub Actions CI/CD
Docker image builds
Kubernetes manifests and Kustomize
AI integration in DevOps workflows
RAG-based knowledge retrieval
Email-based incident notification
Incident response automation
SRE-style alert enrichment
Resume Summary

Built a production-style Kubernetes smart alerting system using Prometheus, Alertmanager, FastAPI, RAG, OpenAI, ArgoCD, GitHub Actions, and email notifications to transform raw cluster alerts into context-rich incident reports with probable root cause analysis, evidence, and remediation steps.

Author

Abd-del1

GitHub: https://github.com/Abd-del1
