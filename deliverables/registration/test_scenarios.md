# High-Level Test Scenarios: Functional & Security Roadmap
**Component:** User Registration Service  
**Target:** Web & API Form Validation Engine  

---

## Scenario Groups Overview

```
Registration Testing Roadmap
 ├── 1.0 End-to-End Funnel Journey (E2E)
 ├── 2.0 Input Boundary & Validation (BVA & Equivalence Partitioning)
 ├── 3.0 Duplicate Identity & State Integrity
 ├── 4.0 Application Security & Defensive Validation (OWASP)
 └── 5.0 Bot Defense, Rate Limiting & Abuse Prevention
```

---

## 1.0 End-to-End Funnel Journey (E2E)
* **TS-E2E-01 (Happy Path Complete Journey):** Verify that a new user completing all fields with valid data (`firstname`, `lastname`, valid non-registered `email`, compliant `password`, matching `confirmPassword`) and ticking "Agree to Terms" successfully submits the form and receives a 302/200 redirect to `/profile/complete`.
* **TS-E2E-02 (Session Persistence Post-Redirect):** Verify that upon redirection to `/profile/complete`, a valid session token/cookie (HttpOnly, Secure, SameSite=Strict) is issued and authenticated state is maintained.

---

## 2.0 Input Boundary & Equivalence Partitioning
* **TS-BVA-01 (Name Field Length Boundaries):**
  * `firstname` / `lastname` at 1 character (Invalid - below minimum).
  * `firstname` / `lastname` at 2 characters (Valid - boundary lower limit).
  * `firstname` / `lastname` at 10 characters (Valid - boundary upper limit).
  * `firstname` / `lastname` at 11 characters (Invalid - exceeding upper limit).
* **TS-BVA-02 (Email Formatting Compliance):**
  * Standard email (`user@example.com`).
  * Sub-domain routing (`user@mail.sub.domain.org`).
  * Invalid syntax (`user@`, `@domain.com`, `user@domain`, `user..name@domain.com`, space in email).
* **TS-BVA-03 (Password Complexity Validation):**
  * Sub-minimum length: `< 8` characters (Reject).
  * 8+ characters without numeric digit (Reject).
  * 8+ characters without special character (Reject).
  * 8+ characters with digits and symbols (Accept).
* **TS-BVA-04 (Password Confirmation Parity):**
  * Match verification: `password` !== `confirmPassword` (Reject submission, preserve fields, scrub password fields).
* **TS-BVA-05 (Terms & Conditions Checkbox State Machine):**
  * Unchecked: Submit button remains strictly disabled (HTML attribute `disabled` present and non-clickable).
  * Checked: Submit button mutates to enabled state immediately.
  * Re-toggling: Unchecking returns the submit button to disabled state.

---

## 3.0 Duplicate Identity & State Integrity
* **TS-DUP-01 (Deterministic Email Duplication):** Validate that an attempt to register with an existing active email immediately yields an inline validation error: `"Email already in use"` without state leakage.
* **TS-DUP-02 (Case-Insensitive Duplicate Detection):** Ensure duplicate checks normalize casing (`USER@DOMAIN.COM` equals `user@domain.com`).
* **TS-DUP-03 (Concurrent Submission Race Condition):** Fire 10 parallel HTTP POST requests with identical payload; precisely 1 must succeed with 201 Created, remaining 9 must fail with 409 Conflict.

---

## 4.0 Application Security & Defensive Validation (OWASP Top 10)
* **TS-SEC-01 (SQL Injection Defense):**
  * Inject standard tautology payloads (`' OR '1'='1`, `admin'--`, `'; DROP TABLE users;--`) into `firstname`, `lastname`, and `email`.
  * Expected: Raw query inputs parameterized; inputs safely rejected by schema validator or escaped cleanly; no database stack traces exposed.
* **TS-SEC-02 (Cross-Site Scripting [XSS] Sanitization & Context Encoding):**
  * Inject polyglot and standard scripts (`<script>alert(1)</script>`, `<img src=x onerror=alert(document.cookie)>`) into `firstname` and `lastname`.
  * Expected: Inputs encoded prior to DOM insertion; no arbitrary JavaScript execution on form, error bubbles, or redirect screens.
* **TS-SEC-03 (Credential Harvesting Defense):**
  * Verify `password` and `confirmPassword` input elements specify `type="password"`.
  * Verify copy/paste behavior and masking.
  * Verify network payload is encrypted over HTTPS (TLS 1.3).

---

## 5.0 Bot Defense, Rate Limiting & Abuse Prevention
* **TS-ABUSE-01 (Form Throttling / Rate Limiting):**
  * Send $> 10$ rapid POST requests within a 60-second window from a single IP/fingerprint.
  * Expected: Server returns HTTP 429 (Too Many Requests) with `Retry-After` header.
* **TS-ABUSE-02 (Headless Automation Trapping):**
  * Verify hidden honeypot field integrity or CAPTCHA trigger on irregular interaction patterns.