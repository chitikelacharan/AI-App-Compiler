# AI App Compiler

Natural Language → Structured Config → Validated → Executable Application

## Overview

AI App Compiler is a compiler-inspired application generation system that converts open-ended natural language requirements into structured, validated, and executable application configurations.

Unlike a single-prompt approach, the system uses a multi-stage pipeline that decomposes application generation into separate deterministic stages. This improves reliability, consistency, validation, and execution readiness.

## Problem Statement

Users provide application requirements in natural language, such as:

> Build a CRM with login, contacts, dashboard, role-based access, and premium plans with payments. Admins can see analytics.

The system converts these requirements into:

* UI Schema
* API Schema
* Database Schema
* Authentication Rules
* Business Logic Rules

All outputs are validated and repaired before execution.

---

## Architecture

User Prompt

↓

Intent Extraction

↓

System Design Layer

↓

Schema Generation

↓

Validation Engine

↓

Repair Engine

↓

Runtime Simulator

↓

Executable Application Configuration

---

## Multi-Stage Pipeline

### 1. Intent Extraction

Extracts:

* Application Type
* Features
* Roles
* Permissions
* Business Requirements

Example:

```json
{
  "app_type": "CRM",
  "features": [
    "login",
    "contacts",
    "dashboard"
  ],
  "roles": [
    "admin",
    "user"
  ]
}
```

### 2. System Design Layer

Creates application architecture.

Defines:

* Entities
* User Flows
* Roles
* Permissions
* Business Rules

### 3. Schema Generation

Generates:

#### UI Schema

* Pages
* Components
* Layouts

#### API Schema

* Endpoints
* Methods
* Validation Rules

#### Database Schema

* Tables
* Fields
* Relationships

#### Auth Schema

* Roles
* Permissions
* Access Policies

### 4. Validation Engine

Validates:

* JSON structure
* Required fields
* Data types
* Schema consistency
* API ↔ Database alignment
* UI ↔ API alignment

### 5. Repair Engine

Automatically fixes:

* Missing fields
* Invalid JSON
* Schema mismatches
* Inconsistent relationships

Instead of regenerating the entire output, only affected sections are repaired.

### 6. Runtime Simulator

Simulates execution of the generated configuration and verifies that outputs are executable without manual modification.

---

## Features

* Multi-stage generation pipeline
* Deterministic structured outputs
* Schema validation
* Automatic repair engine
* Runtime simulation
* Failure handling
* Evaluation framework

---

## Tech Stack

### Backend

* Python
* FastAPI
* Pydantic

### Frontend

* Next.js
* TypeScript

### AI Layer

* LLM-based generation pipeline

---

## Example Input

Build a CRM with login, contacts, dashboard, role-based access, and premium plans with payments. Admins can see analytics.

## Example Output

### Database

```json
{
  "tables": [
    "users",
    "contacts",
    "payments"
  ]
}
```

### API

```json
{
  "endpoint": "/contacts",
  "method": "GET"
}
```

### Roles

```json
{
  "admin": [
    "analytics",
    "manage_users"
  ],
  "user": [
    "contacts"
  ]
}
```

---

## Evaluation Framework

The project includes an evaluation framework containing:

* Real-world product prompts
* Ambiguous prompts
* Conflicting prompts
* Incomplete prompts

Metrics tracked:

* Success Rate
* Retry Count
* Failure Types
* Latency
* Repair Frequency

---

## Project Structure

```text
backend/
frontend/
compiler/
runtime/
evaluation/
```

---

## Setup Instructions

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Future Improvements

* Real application code generation
* Multi-model orchestration
* Advanced schema optimization
* Production deployment pipeline

---

## Author

Chitikela Charan

B.Tech CSE (AI & ML)
RGMCET
