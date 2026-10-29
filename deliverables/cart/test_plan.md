# Master Test Plan: Product Catalog & Cart Subsystem

**Document Version:** 1.0.0  
**Author:** Principal QA Architect & Security Lead  
**Target Ticket:** Product Catalog & Cart — Variant Selection & Add-to-Cart  

---

## 1. Executive Summary & Strategy
The Product Catalog & Cart subsystem governs critical user conversion paths and direct revenue generation. This test plan establishes a risk-based, zero-trust quality assurance framework spanning functional UX, concurrent cart state synchronization, API integrity, and adversarial resilience (parameter tampering, bot mitigation, and authorization isolation). 

Testing follows a "Shift-Left" and "Continuous Security" model:
* **Client-Side Verification:** Fast feedback loops via Playwright component/E2E suites.
* **Server-Side Integrity Testing:** Negative security testing, intercepting requests to validate immutable authoritative pricing and inventory boundaries.
* **Non-Functional Testing:** Concurrency, race conditions, rate limiting, and responsiveness across viewports.

---

## 2. Scope Definition

### 2.1 In-Scope
* **Dynamic Variant Engine:** Real-time DOM updates for SKU selection (Size, Color), reflective stock statuses, and tiered pricing displays.
* **Reactive Cart Experience:** Asynchronous state modifications, optimistic UI updates, and non-blocking cart badge counter changes.
* **Inventory Boundary Controls:** Exhaustion boundaries, out-of-stock lockout, and backorder prevention messaging.
* **State Persistence & Hydration:** Resilient state hydration across page reloads, tab duplication, and network drops via `localStorage`/encrypted session cookies.
* **Multi-Tenant Account Safety (AuthZ):** Cross-tenant cart isolation, IDOR prevention on cart operations, and session-binding validation.
* **Robust Input Sanitization:** Defensive boundaries against SQLi, XSS vectors in cart notes/variant fields, integer overflows, floats, and zero/negative quantity values.
* **Price Authority & Tamper Defense:** Enforcement of server-authoritative catalog pricing irrespective of client-side DOM/network payload alterations.
* **Abuse & Bot Deterrence:** Token-bucket rate limiting, rapid-click debouncing, and automated cart-stuffing prevention.
* **Cart Calculations & Visual Integrity:** Real-time subtotal, tax calculation, shipping tier estimates, and responsive layout across desktop, tablet, and mobile viewports.

### 2.2 Out-of-Scope
* Payment gateway settlement, tokenization, and 3D Secure challenges (deferred to Checkout/Billing test phases).
* Physical warehouse logistics, picking, packing, and fulfillment dispatch routines.
* Upstream third-party ERP inventory sync jobs (validated via integration stubs/contract tests).

---

## 3. Test Environment & Tooling Topology

```
+-------------------------------------------------------------------------------+
|                             TEST RUNNER INFRASTRUCTURE                        |
|   +--------------------------+                 +--------------------------+   |
|   |   Playwright Test Suite  |                 |     OWASP ZAP / Caido    |   |
|   |  (E2E, State, Visual)    |                 |   (Security / Tampering) |   |
|   +------------+-------------+                 +------------+-------------+   |
+----------------|--------------------------------------------|-----------------+
                 v                                            v
+-------------------------------------------------------------------------------+
|                            STAGING SYSTEM UNDER TEST                          |
|   +--------------------------+                 +--------------------------+   |
|   |   Next.js / React Web    | <=============> |     Node.js / Go API     |   |
|   |   Storefront (Isolated)  |   HTTPS/WSS     |     Cart & Catalog Svc   |   |
|   +--------------------------+                 +------------+-------------+   |
|                                                             |                 |
|                                                +------------+-------------+   |
|                                                | Redis (Cache/Session/RL) |   |
|                                                | PostgreSQL (Catalog/DB)  |   |
|                                                +--------------------------+   |
+-------------------------------------------------------------------------------+
```

* **Staging Environment:** Ephemeral staging cluster mirroring production infrastructure (isolated VPC, SSL termination, Redis clustering, PostgreSQL replica).
* **Execution Framework:** Playwright (TypeScript) executed across Chromium, WebKit, and Firefox engines.
* **Security & Proxy Inspection:** OWASP ZAP / Burp Suite / Mitmproxy for request tampering and fuzzing.
* **Data Seeding Service:** Automated DB fixtures to generate clean test tenants, SKUs with varying stock levels (0, 1, 5, 99999), and authenticated sessions.

---

## 4. Key Risks & Mitigation Strategies

| Risk ID | Description | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **RSK-01** | **Client-Side Price Tampering:** Malicious users alter payload price to `$0.00` via DevTools or Proxy. | **CRITICAL** | Enforce total server-side price recalculation against catalog DB; reject client-provided unit costs outright. |
| **RSK-02** | **Race Conditions (Overselling):** Concurrent requests reserve the final inventory item simultaneously. | **CRITICAL** | Implement atomic DB transactions (`SELECT FOR UPDATE` or Redis distributed locks) during stock allocation; stress test with parallel threads. |
| **RSK-03** | **Cart Hijacking / IDOR:** Manipulating `cart_id` or session headers to access or alter another user's cart. | **HIGH** | Strict cryptographically signed session tokens; bind carts strictly to authenticated user context; assert 403 Forbidden on foreign entity access. |
| **RSK-04** | **Inventory Hoarding (Bot Exhaustion):** Distributed automated scripts hoarding inventory in carts, denying real buyers. | **HIGH** | Enforce token-bucket rate limiting on `/api/cart/add`, CAPTCHA step-up on anomaly thresholds, and short cart reservation TTLs. |
| **RSK-05** | **Memory/Integer Overflow in Quantity:** Inputting $2^{31}-1$ or floats causes backend crash or zero-pricing anomalies. | **MEDIUM** | Strict schema validation via Zod/Joi; reject non-integers, enforce strict integer ceiling (`MAX_ITEM_QTY = 99`). |

---

## 5. Exit & Quality Gate Criteria
1. **Defect Threshold:** 0 Critical (P0), 0 High (P1), and ≤ 3 Medium (P2) defects with verified workarounds.
2. **Security Compliance:** 100% pass on Server-Side Price Tampering, IDOR, SQLi, and Stored XSS test cases.
3. **Automated Coverage:** Minimum 95% pass rate across core functional Playwright test suites.
4. **Performance Gate:** Header badge counter updates in `< 250ms` (95th percentile) without full page reload.
5. **Sign-off:** Dual approval from Principal QA Architect and Application Security Lead.