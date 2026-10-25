# AWS Infrastructure Automated Audit and IaC Project

A modular, enterprise-grade Python application and infrastructure project designed to provision, inspect, audit, and inventory AWS cloud infrastructure resources using Terraform and boto3. Built with DevOps best practices, containerization, and automated CI/CD workflows.

---

## Tech Stack and Architecture

- **Cloud Provider:** AWS (Amazon Web Services) - region eu-central-1 (Frankfurt)
- **Infrastructure as Code:** Terraform v1.x
- **Language:** Python 3.12
- **AWS SDK:** boto3 (VPC, EC2, Security Groups)
- **Containerization:** Docker
- **Orchestration:** Kubernetes (Job and Deployment Manifests)
- **CI/CD:** GitHub Actions

---

## Architecture Overview

The infrastructure is deployed in the `eu-central-1` region following a secure, multi-tier, multi-AZ VPC architecture:

- **Public Subnets:** Contain the Internet Gateway (`IGW`) and NAT Gateway for secure outbound internet access.
- **Private App Subnets:** Host the core application workloads and EC2 instances (`APP`).
- **Private Data Subnets:** Dedicated to database tiers (`DB`), isolated from direct public exposure.

## Project Roadmap and Infrastructure Overview

This project is developed iteratively across four core DevOps phases, starting with foundational network provisioning via Terraform followed by automated Python auditing operations:

- [x] Phase 1: Core Network & Security Infrastructure (VPC, Subnets, Routing, NAT Gateway, Gateway Endpoints, Security Groups)
- [x] Phase 2: AWS Infrastructure Automation & Operations via Python (Boto3)
- [ ] Phase 3: Automated CI/CD Pipeline for IaC and Code Validation (GitHub Actions)
- [ ] Phase 4: Application & Compute Layer Integration (EC2 / EKS Kubernetes)

The baseline architecture provisions a multi-Availability Zone (Multi-AZ) VPC (10.0.0.0/16) featuring public subnets, private app subnets, isolated private data subnets, a NAT Gateway, and a direct VPC S3 Gateway Endpoint. Access control follows strict least-privilege security groups (alb_sg, app_sg, db_sg).

---

## Repository Structure

aws-iac-pr1/
├── .github/workflows/   # CI/CD pipelines (GitHub Actions)
├── k8s/                 # Kubernetes deployment and service manifests
├── scripts/             # Core audit modules (audit_vpc.py, audit_ec2.py)
├── terraform/           # IaC configurations (main.tf, variables.tf, outputs.tf, provider.tf)
├── Dockerfile           # Container build definition
├── main.py              # Centralized CLI entry point
└── requirements.txt     # Python dependencies

---

## Getting Started and Local Setup

### 1. Clone the Repository
git clone https://github.com/your-username/aws-iac-pr1.git
cd aws-iac-pr1

### 2. Set Up Virtual Environment and Python Dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

### 3. Configure AWS Credentials
Ensure your AWS CLI is configured with valid access keys:
aws configure

### 4. Run the Audit Tool
python main.py

---

## Terraform Infrastructure Management

To provision or manage cloud infrastructure resources through Terraform:

cd terraform
terraform init
terraform apply

To manage cloud resources efficiently and avoid unnecessary runtime charges (such as NAT Gateway hourly fees), destroy all provisioned infrastructure when not actively testing:

cd terraform
terraform destroy -auto-approve

---

## Docker Support

To build and run the tool inside a Docker container:

docker build -t aws-audit-tool .
docker run --rm -it aws-audit-tool

---

## CI/CD Pipeline

This repository uses GitHub Actions to automatically list, test, and validate Python code syntax and infrastructure configurations on every push or pull request to the main branch.