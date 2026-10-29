# Dynamic QA Agent

An intelligent, enterprise-grade quality assurance automation framework that bridges the gap between traditional automated browser testing and real-world business requirements using AI.

---

## Table of Contents
1. [Plain English Summary For Non-Technical Stakeholders](#plain-english-summary-for-non-technical-stakeholders)
2. [Overview](#overview)
3. [Core Workflows Covered](#core-workflows-covered)
4. [System Architecture](#system-architecture)
5. [Tech Stack](#tech-stack)
6. [Prerequisites](#prerequisites)
7. [Quick Start Guide For Developers](#quick-start-guide-for-developers)
8. [Execution Examples and Expected Output](#execution-examples-and-expected-output)
9. [Resiliency and Offline Mode](#resiliency-and-offline-mode)

---

## Plain English Summary For Non-Technical Stakeholders

### What is this project?
Imagine hiring a meticulous software tester who never sleeps. Whenever your website changes, this "agent" automatically opens a web browser, clicks through your website just like a real customer would, and checks two things:
1. **Did the website work technically?** (Did buttons click, pages load, and forms submit without crashing?)
2. **Did the website follow the actual business rules?** (Did it correctly enforce password rules during registration? Did the correct total show up at checkout?)

### Why is this unique?
Traditional automated tests only check basic technical actions (like *"Can I click this button?"*). They cannot check complex logic or business rules. 

The **Dynamic QA Agent** solves this by acting like a smart judge:
* It **remembers** your official company rules using a local AI memory bank (Vector Database).
* It **watches** an automated web browser run user journeys using Playwright.
* It **grades** the results using an AI judge to tell you with absolute certainty whether the feature passed or failed according to your exact requirements.

---

## Overview

Traditional test automation checks whether UI components render or buttons click, but often fails to verify if complex business rules and feature acceptance criteria are genuinely met. The **Dynamic QA Agent** bridges this gap by combining programmatic web browser automation with semantic vector search and LLM-driven evaluation. 

When a test run executes, the agent dynamically fetches official acceptance criteria from a local vector store, evaluates test execution artifacts against those rules using an LLM judge, and produces structured pass/fail verdicts with detailed reasoning.

---

## Core Workflows Covered

The framework focuses on four critical e-commerce and user account journeys:
- **User Registration (`registration`):** Validates account creation constraints, password complexity rules, mandatory fields, and duplicate email prevention.
- **Add to Cart (`add-to-cart`):** Verifies product selection, inventory checks, pricing accuracy, and cart state persistence across page interactions.
- **Checkout (`checkout`):** Tests end-to-end order placement, shipping address validation, payment gateway stubbing, and order confirmation generation.
- **Profile Completion (`profile-completion`):** Ensures user account details, billing profiles, and preference updates synchronize and persist correctly.

---

## System Architecture

```text
┌─────────────────────────────┐        ┌──────────────────────────────┐
│  1. Playwright Web Browser  │        │  2. ChromaDB RAG Memory Bank │
│     (Automates User Journeys)        │     (Stores Official Rules)  │
└──────────────┬──────────────┘        └──────────────┬───────────────┘
               │                                      │
               └───────────────────┬──────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────┐
│                 3. TypeScript Orchestrator                  │
│             (Coordinates testing and retrieval)             │
└──────────────────────────────────┬──────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────┐
│                     4. LLM-as-a-Judge Engine                │
│       (Grades test output against official business rules)  │
└─────────────────────────────────────────────────────────────┘
```

* **The Knowledge Base (`source/knowledge_base.py` & `source/get_guidance.py`):** Stores official feature acceptance criteria in a local vector store (`qa_testbed`) using lightweight sentence embeddings (`SentenceTransformers`).
* **The Test Runner (`source/run_dynamic_evaluation.ts`):** Orchestrates the connection between Python vector retrieval and TypeScript test assertions.
* **The AI Judge (`source/evaluation.ts`):** Evaluates test execution data against retrieved acceptance rules using the Gemini API, complete with a 45-second timeout guard and a local offline fallback mode (`USE_LOCAL_JUDGE=true`) to prevent rate-limit crashes.

---

## Tech Stack

* **Languages:** TypeScript, JavaScript, Python (3.10+)
* **Browser Automation:** Playwright
* **AI & Vector Storage:** ChromaDB, SentenceTransformers, Google Gemini API
* **Environment:** Node.js, Python Virtual Environments (`venv`), Windows PowerShell, Git

---

## Prerequisites

Ensure you have the following installed on your machine:
* **Node.js** (v18 or higher recommended)
* **Python** (v3.10 or higher)
* **Git**

---

## Quick Start Guide For Developers

### Step 1: Clone and Install Dependencies
Open your terminal in the project folder and run:
```bash
npm install
python -m venv venv
.\venv\Scripts\activate
pip install chromadb sentence-transformers
```

### Step 2: Configure Environment Variables
Copy the template file to create your local `.env` configuration:
```bash
cp .env.example .env
```
*(Open `.env` and add your `GEMINI_API_KEY`. If you are working offline or wish to protect API quotas, you can set `USE_LOCAL_JUDGE=true`)*

### Step 3: Populate the Knowledge Base
Index your project's acceptance criteria into the local vector database:
```bash
python source/knowledge_base.py
```

### Step 4: Run the Dynamic Evaluation Suite
Execute the end-to-end orchestration workflow:
```bash
npx tsx source/run_dynamic_evaluation.ts
```

---

## Execution Examples and Expected Output

When you run the evaluation suite, you will see structured console output detailing the retrieval, execution, and grading process:

```text
[INFO] Initializing Dynamic QA Agent Orchestrator...
[RAG] Querying ChromaDB knowledge base for workflow: checkout...
[RAG] Retrieved 2 matching acceptance criteria items.
[PLAYWRIGHT] Executing automated flow: Checkout Validation...
[JUDGE] Evaluating test execution results against acceptance criteria...
[RESULT] Status: PASSED | Confidence: 98% | Judge Mode: Local Fallback (USE_LOCAL_JUDGE=true)
```

---

## Resiliency and Offline Mode

* **Live AI Mode (`USE_LOCAL_JUDGE=false`):** Routes evaluation requests to the Google Gemini API with a strict 45-second timeout guard to ensure pipelines never hang.
* **Offline Fallback Mode (`USE_LOCAL_JUDGE=true`):** Evaluates test rules locally using deterministic matching, ensuring your test suite runs smoothly without internet access or API rate-limit interruptions.