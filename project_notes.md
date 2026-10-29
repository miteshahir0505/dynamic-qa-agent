# 🛠️ Project Architecture & Codebase Status (`main.py`)

## Stack & Configuration
- **Language:** Python
- **SDK:** Google GenAI SDK (`google-genai`)
- **Model:** `gemini-3.5-flash` (temperature `0.0` for deterministic tool calls)
- **Environment Management:** `python-dotenv` with secure API key loading from `.env`.

## Core Tools Implemented
1. **`run_api_smoke_test(endpoint: str, expected_status: int = 200) -> str`**
   - Simulates automated smoke tests against API endpoints.
   - Handles enterprise status codes dynamically based on URL keywords:
     - `200` (Default healthy staging/v1 endpoint)
     - `201` (Resource creation via `/create` or `/register`)
     - `401` (Authorization failure via `/payment` or `/secure`)
     - `429` (Rate limiting via `/limit` or `/stress`)
     - `400` (Bad request via `/bad` or `/invalid`)
     - `500` (Internal server error via `/error` or `/crash`)
     - `504` (Gateway timeout via `/timeout` or `/outage`)
   - Returns structured JSON containing test results, HTTP codes, latency, and messages.

2. **`query_error_logs(service_name: str) -> str`**
   - Centralized log management audit tool.
   - Searches mock databases for microservices like `auth-service` and `payment-service`.
   - Returns severity levels, error codes (e.g., `AUTH_500_TOKEN_EXPIRED`), descriptions, and recommended actions.
