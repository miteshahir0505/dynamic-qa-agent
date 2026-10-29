# Dynamic QA Agent

An end-to-end intelligent QA automation system combining **Playwright** web flows, a local **ChromaDB RAG** knowledge base, and an **LLM-as-a-Judge** evaluation engine.

## Core Workflows Covered
* **User Registration:** Validates account creation rules and required profile fields.
* **Add to Cart:** Verifies item selection and cart state persistence.
* **Checkout:** Tests end-to-end order placement and validation steps.
* **Profile Completion:** Ensures user account details update accurately.

## System Architecture
1. **Local RAG Knowledge Base (`source/knowledge_base.py` & `source/get_guidance.py`):** Stores and retrieves official feature acceptance criteria using ChromaDB (`qa_testbed`) and SentenceTransformers (`all-MiniLM-L6-v2`).
2. **LLM-as-a-Judge Evaluation (`source/evaluation.ts`):** Grades test execution results against retrieved acceptance criteria using the Gemini API, complete with a 45-second timeout safeguard and a built-in local offline fallback mode (`USE_LOCAL_JUDGE=true`) for rate-limit resiliency.
3. **Dynamic Orchestration (`source/run_dynamic_evaluation.ts`):** Connects the Python vector retrieval bridge with TypeScript test evaluations in a single unified flow.
4. **Automated Web Flows:** Self-healing Playwright test suites organized by core user journeys.

## Quick Start

### 1. Environment Setup
Clone the repository and install dependencies:
```bash
npm install
python -m venv venv
.\venv\Scripts\activate
pip install chromadb sentence-transformers