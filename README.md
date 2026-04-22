# FHIR Patient Data Browser

> A serverless healthcare interoperability application that queries live **HL7 FHIR R4** resources from a public sandbox, built on AWS with zero ongoing infrastructure cost.

![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20API%20Gateway%20%7C%20S3-FF9900?style=flat&logo=amazonaws&logoColor=white)
![FHIR](https://img.shields.io/badge/FHIR-R4-E8174C?style=flat)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Cost](https://img.shields.io/badge/Monthly%20Cost-%240-2ea44f?style=flat)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat)

---

## Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Architecture](#architecture)
- [FHIR Resources Used](#fhir-resources-used)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Development](#local-development)
- [AWS Deployment](#aws-deployment)
- [Security Controls](#security-controls)
- [Cost Breakdown](#cost-breakdown)
- [Roadmap](#roadmap)
- [Standards & Compliance Context](#standards--compliance-context)

---

## Overview

This project demonstrates hands-on proficiency with **HL7 FHIR R4** interoperability standards in a real, deployed application. It queries live patient data — `Patient`, `Condition`, `MedicationRequest`, and `Observation` resources — from the public [HAPI FHIR R4 sandbox](https://hapi.fhir.org/baseR4) via RESTful FHIR search parameters, and presents it through a clean browser interface.

The backend is a **serverless Python Lambda function** deployed behind AWS API Gateway. The frontend is a **static single-page application** hosted on Amazon S3. Total infrastructure cost: **$0/month** within AWS Free Tier.

Built as a portfolio project to demonstrate practical healthcare data engineering skills including FHIR resource navigation, RESTful API design, AWS serverless architecture, and security-first deployment practices.

---

## Live Demo

🌐 **Frontend:** `http://fhir-patient-browser-ui.s3-website-us-east-1.amazonaws.com`

🔌 **API Endpoint:**
```
GET https://<api-id>.execute-api.us-east-1.amazonaws.com/prod/patients?name=Smith
GET https://<api-id>.execute-api.us-east-1.amazonaws.com/prod/patient/{id}
```

**Try it in your browser or with curl:**
```bash
curl "https://<api-id>.execute-api.us-east-1.amazonaws.com/prod/patients?name=Smith"
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER                        │
└─────────────────────┬───────────────────────────────────────┘
                       │ HTTPS
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Amazon S3 — Static Website Hosting              │
│                      index.html (SPA)                        │
└─────────────────────┬───────────────────────────────────────┘
                       │ HTTPS fetch()
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           AWS API Gateway — HTTP API                         │
│   • Throttling: 10 req/sec, burst 20                        │
│   • CORS enforced                                            │
│   • Routes: GET /patients  GET /patient/{id}                 │
└─────────────────────┬───────────────────────────────────────┘
                       │ IAM-scoped invocation only
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           AWS Lambda — Python 3.12 (128 MB)                  │
│   • Input validation (regex)                                 │
│   • FHIR R4 REST client                                      │
│   • JSON resource parsing                                    │
│   • Security response headers                                │
└─────────────────────┬───────────────────────────────────────┘
                       │ HTTPS (public sandbox)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           HAPI FHIR R4 Public Sandbox                        │
│           https://hapi.fhir.org/baseR4                       │
│   Resources: Patient · Condition · MedicationRequest         │
│              Observation                                     │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         Amazon CloudWatch — Logs & Billing Alerts            │
└─────────────────────────────────────────────────────────────┘
```

---

## FHIR Resources Used

| FHIR Resource | Purpose | Key Fields Parsed |
|---|---|---|
| `Patient` | Demographics search and display | `name.given`, `name.family`, `birthDate`, `gender` |
| `Condition` | Patient diagnosis list | `code.coding[].display`, `clinicalStatus` |
| `MedicationRequest` | Prescribed medications | `medicationCodeableConcept.coding[].display` |
| `Observation` | Lab results and vitals | `code.display`, `valueQuantity`, `effectiveDateTime` |

**FHIR Search Parameters used:**
```
GET /Patient?name=Smith&_count=10
GET /Condition?patient={id}&_count=20
GET /MedicationRequest?patient={id}&_count=20
GET /Observation?patient={id}&_count=20&_sort=-date
```

---

## Features

- 🔍 **Patient search** by name using FHIR `name` search parameter
- 📋 **Patient profile view** — conditions, medications pulled via compartment search
- 🔒 **Input validation** — regex-enforced sanitization on all query parameters
- 🛡️ **Security headers** — HSTS, X-Frame-Options, X-Content-Type-Options on all responses
- ⚡ **Serverless** — no servers to manage, scales to zero when idle
- 💰 **Zero cost** — operates entirely within AWS Free Tier limits
- 📊 **CloudWatch logging** — all Lambda invocations logged with path and parameter context

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, Vanilla JavaScript (ES6+), CSS3 |
| **Backend** | Python 3.12, AWS Lambda |
| **API Layer** | AWS API Gateway HTTP API |
| **Static Hosting** | Amazon S3 Static Website |
| **Monitoring** | Amazon CloudWatch Logs |
| **FHIR Standard** | HL7 FHIR R4 (4.0.1) |
| **Sandbox** | HAPI FHIR Public Test Server |
| **HTTP Client** | Python `requests` library |

---

## Project Structure

```
fhir-patient-browser/
│
├── lambda/
│   ├── lambda_function.py      # Lambda handler, routing, input validation
│   ├── fhir_client.py          # FHIR R4 REST client & resource parsers
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   └── index.html              # Single-page app (search + patient profile UI)
│
├── tests/
│   ├── test_fhir_client.py     # FHIR API connectivity & parsing tests
│   └── test_lambda.py          # Lambda handler unit tests (pytest)
│
├── run_local.py                # Local Lambda simulation (no AWS required)
├── local_server.py             # Flask dev server for full local UI testing
├── deploy.ps1                  # Windows one-click deployment script
├── deploy.sh                   # Mac/Linux one-click deployment script
└── README.md
```

---

## Local Development

### Prerequisites
- Python 3.9+
- pip
- Git

### Setup

```bash
# Clone the repo
git clone https://github.com/nagakirankasi/fhir-patient-browser.git
cd fhir-patient-browser

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r lambda/requirements.txt
pip install flask flask-cors pytest
```

### Run Tests

```bash
# Test FHIR API connectivity and resource parsing
python tests/test_fhir_client.py

# Test Lambda handler logic
pytest tests/ -v
```

### Run Full Local Stack

```bash
# Terminal 1 — start the backend API server
python local_server.py
# Runs at http://localhost:5000

# Terminal 2 — serve the frontend
cd frontend
python -m http.server 8080
# Open http://localhost:8080 in browser
```

### Simulate Lambda Events Locally

```bash
python run_local.py
```

This runs four test scenarios against your Lambda handler without any AWS dependencies:
- Patient search by name
- Patient profile fetch
- 404 unknown route
- Empty search result handling

---

## AWS Deployment

### Prerequisites
- AWS account (Free Tier)
- AWS CLI configured (`aws configure`)

### One-Command Deploy (Windows PowerShell)

```powershell
.\deploy.ps1
```

### One-Command Deploy (Mac/Linux)

```bash
chmod +x deploy.sh && ./deploy.sh
```

### Manual Deployment Steps

**1. Package Lambda with dependencies**
```powershell
# Windows
mkdir package
pip install requests -t package/
Copy-Item lambda\lambda_function.py package\
Copy-Item lambda\fhir_client.py package\
Set-Location package
Compress-Archive -Path * -DestinationPath ..\fhir_browser.zip
Set-Location ..
```

**2. Deploy to Lambda**
- Runtime: Python 3.12
- Memory: 128 MB
- Timeout: 10 seconds
- IAM Role: `AWSLambdaBasicExecutionRole` only (least privilege)

**3. Configure API Gateway**
- Type: HTTP API
- Routes: `GET /patients`, `GET /patient/{id}`, `OPTIONS /patients`, `OPTIONS /patient/{id}`
- Throttling: Rate 10 req/sec, Burst 20
- CORS: Allow-Origin `*`, Methods `GET, OPTIONS`

**4. Host frontend on S3**
- Enable Static Website Hosting
- Upload `frontend/index.html`
- Update `const API = "https://your-api-gateway-url/prod"` before uploading

**5. Set billing alert**
- AWS Budgets → Create $1.00 cost budget with email alert

---

## Security Controls

| Control | Implementation |
|---|---|
| **Input validation** | Regex on all query parameters — blocks injection attempts |
| **Least-privilege IAM** | Lambda role limited to `BasicExecutionRole` only |
| **API Gateway-only invocation** | Resource-based policy blocks direct Lambda URL access |
| **Rate throttling** | 10 req/sec at API Gateway — prevents cost runaway and DDoS |
| **Security response headers** | HSTS, X-Frame-Options, X-Content-Type-Options, Cache-Control: no-store |
| **CORS scoping** | Explicit origin, method, and header allowlists |
| **Error sanitization** | Generic 500 messages to caller; full detail only in CloudWatch |
| **No secrets in code** | Public sandbox only — no credentials or PHI anywhere in codebase |
| **Billing alert** | CloudWatch budget alarm at $1.00 threshold |

> **Note:** This project queries a public test sandbox. No real PHI is used or stored anywhere. For production healthcare applications, additional controls are required: HIPAA BAA with AWS, VPC isolation, encryption at rest and in transit, audit logging via CloudTrail, and access controls compliant with applicable regulations.

---

## Cost Breakdown

| AWS Service | Free Tier | Projected Monthly Usage | Cost |
|---|---|---|---|
| Lambda | 1M requests + 400K GB-sec | ~hundreds of requests | **$0** |
| API Gateway (HTTP) | 1M calls/month (12 months) | ~hundreds of calls | **$0** |
| S3 Static Hosting | 5GB + 20K GET requests | < 1MB | **$0** |
| CloudWatch Logs | 5GB ingestion/month | kilobytes | **$0** |
| **Total** | | | **$0/month** |

After the 12-month free tier: Lambda and CloudWatch remain free at this usage scale. API Gateway HTTP API costs $1.00 per million calls.

---

## Roadmap

### Phase 2 — Clinical Depth
- [ ] Observations dashboard with vitals trend charts (Chart.js)
- [ ] ICD-10 and SNOMED CT code display alongside condition names
- [ ] Tabbed patient profile layout (Conditions / Medications / Labs)
- [ ] FHIR Bundle pagination for large result sets

### Phase 3 — Architecture Upgrades
- [ ] CloudFront distribution in front of S3 (HTTPS + CDN)
- [ ] Search history persistence with DynamoDB On-Demand
- [ ] Export patient summary as PDF

### Phase 4 — Gen AI Integration
- [ ] "Summarize Patient" button using Amazon Bedrock
- [ ] Plain-English clinical summary generated from FHIR resource data
- [ ] Demonstrates applied Gen AI in healthcare use case

---

## Standards & Compliance Context

This project was built to demonstrate practical familiarity with the following standards and regulatory frameworks relevant to healthcare interoperability roles:

- **HL7 FHIR R4** — RESTful API design, resource structure, search parameters, Bundle navigation
- **CMS Interoperability Rule (CMS-9115-F)** — Patient Access API and Provider Directory API requirements that this architecture pattern supports
- **CMS Prior Authorization Rule (CMS-0057-F)** — FHIR-based prior auth API patterns
- **HIPAA** — Security controls applied (no PHI used; production extension points documented)
- **US Core Implementation Guide** — Resource profiles referenced for Patient and Condition resources

---

## Author

**Kasi** — Healthcare IT Solutions Architect  
Focused on CMS interoperability compliance, FHIR-based API implementation, and payer-side data architecture.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/yourprofile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/yourusername)

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built with HL7 FHIR R4 · Deployed on AWS · $0/month*
