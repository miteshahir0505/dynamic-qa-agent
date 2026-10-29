# 🗺️ Master Project Roadmap: AI Automation Testing & Agentic QA

## Day 1: Foundation & Tooling (Completed)
- Environment setup (`google-genai`, `gemini-3.5-flash`, dotenv).
- Built functional autonomous tools: `run_api_smoke_test` (covering enterprise HTTP status codes 200, 201, 400, 401, 429, 500, 504) and `query_error_logs` (for microservices like `auth-service`).
- Established readability standards with clean function-specific log tags (`[API Smoke Test Tool]`, `[Log Audit Tool]`).

## Day 2: Agent Memory, Error Recovery & ReAct Framework
- Building `self-healing-test-agent`: An agent that catches test assertion failures, analyzes logs, and suggests/applies code fixes.

## Day 3: Vector Embeddings & ChromaDB
- Building `rag-testbed-generator`: A local vector database loaded with sample PRDs and API documentation.

## Day 4: LLM-as-a-Judge & Metrics
- Building `rag-evaluation-suite`: Automated test scripts measuring hallucination and retrieval accuracy.

## Day 5: Model Context Protocol (MCP)
- Building `mcp-qa-server`: Custom MCP server architecture allowing LLMs to interact seamlessly with testing environments.
