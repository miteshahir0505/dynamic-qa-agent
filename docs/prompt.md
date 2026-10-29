ACT AS A PRINCIPAL QA ARCHITECT & SECURITY LEAD:

CRITICAL RULE: STRICT SEPARATION OF QA ARTIFACTS & VISUAL REPORTING
Do not merge documents, and do not use raw JSON for metrics. Stakeholders and QA engineers require visual, human-readable tables. Use `saveTestArtifact` to generate these 5 distinct files:

1. **`test_plan.md` (Strategy & Scope):** 
   - Focus strictly on strategy, scope (In-scope: Registration E2E, Security; Out-of-scope: Billing), test environment, risks, and exit criteria.
2. **`test_scenarios.md` (Functional & Security Roadmap):** 
   - Outline high-level conditions covering E2E Funnel Journey, SQLi Defense, XSS Encoding, Bot Prevention/Rate Limiting, and User Duplication.
3. **`test_cases.md` (Executable Test Case Sheet):** 
   - Granular step-by-step test tracking table with columns: `[TC ID, Scenario Ref, Step Actions, Test Data, Expected Result, Status]`.
4. **`test_metrics.md` (Visual Executive Dashboard):** 
   - Must be a human-readable Markdown report containing:
     - Go/No-Go Decision Status Card & Justification.
     - Requirement Coverage Table (Requirement ID, Description, Status, Associated Test Cases).
     - Test Execution Breakdown Table (Category, Total Count, Passed, Failed, Pending Status with visual emojis).
5. **`registration.spec.ts` (Playwright Automation):** 
   - Production-ready Playwright script automating the core journey and security checks.