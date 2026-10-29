# High-Level Test Scenarios: Product Catalog & Cart

---

## TS-01: End-to-End Dynamic Variant Journey
* **Description:** Validate user navigation across multi-dimensional product variants (Size, Color), observing dynamic DOM updates for price, stock indicator, SKU identifier, and responsive imagery without browser reloads.
* **Scope:** Functional UI, DOM reactivity, MutationObserver stability.
* **Success Criteria:** Price updates immediately to reflect variant changes; out-of-stock options disable the "Add to Cart" button; active variant selection highlights correctly.

## TS-02: Instant Reactive Cart Counter & Asynchronous Add-to-Cart
* **Description:** Verify the performance and behavior of clicking "Add to Cart", confirming that the cart counter badge increments instantaneously via optimistic UI or asynchronous XHR/Fetch, maintaining page scroll and component state.
* **Scope:** Client-side state management, async network interaction, error fallback.
* **Success Criteria:** Cart badge increments within 250ms without full page reload; network failures roll back the optimistic counter with a clear toast notification.

## TS-03: Inventory Boundary & Concurrency (Anti-Overselling)
* **Description:** Verify strict stock allocation when quantity added approaches or exceeds available inventory, including multi-tab and multi-session race conditions targeting the final available SKU.
* **Scope:** Inventory validation, atomic reservations, user-friendly UI warnings.
* **Success Criteria:** Clear non-technical stock limitation message displayed when requested quantity exceeds stock; total reserved items never exceed database balance.

## TS-04: Session Continuity & Storage Hydration
* **Description:** Validate cart item preservation across hard refreshes (`Ctrl+F5`), accidental tab closures, and multi-tab browsing within identical user sessions.
* **Scope:** Storage engines (`localStorage`, `sessionStorage`, HTTP-only session cookies).
* **Success Criteria:** Cart persists unchanged after hard refresh; modifications in Tab A reflect in Tab B upon focus or through BroadcastChannel/storage events.

## TS-05: Multi-Tenant Cart Isolation & Anti-IDOR Security
* **Description:** Verify complete isolation of cart entities between distinct authenticated sessions, preventing unauthorized read/write access via manipulated cart identifiers or session spoofing.
* **Scope:** Authorization, IDOR security, session fixation, token handling.
* **Success Criteria:** User A cannot view, add to, or modify User B's cart through identifier substitution in API payloads; unauthenticated carts merge cleanly upon login without overwriting existing items.

## TS-06: Defensive Quantity Validation & Boundary Hardening
* **Description:** Probe quantity input controls with invalid payloads: negative numbers, zero, floating-point decimals, non-numeric values, exponential notations, and 32/64-bit integer overflow limits.
* **Scope:** Input validation, API schema validation, backend numeric type safety.
* **Success Criteria:** All malformed or out-of-bounds quantity values are rejected by both client-side constraints and backend schema validators with appropriate HTTP 400 Bad Request responses.

## TS-07: Authoritative Server-Side Price Integrity (Anti-Tampering)
* **Description:** Evaluate server response when intercepting `/api/cart/add` or `/api/cart/update` and modifying price, currency, or discount values within the client payload.
* **Scope:** Parameter tampering, API security, financial integrity.
* **Success Criteria:** Server ignores all client-submitted prices, calculates totals strictly from authoritative database records, and logs a security warning event.

## TS-08: Rate Limiting & Bot Hoarding Mitigation
* **Description:** Simulate high-frequency programmatic bursts and rapid double-clicks on the "Add to Cart" action to evaluate rate-limiting thresholds and debouncing mechanisms.
* **Scope:** Anti-spam, DDoS resilience, token-bucket/leaky-bucket rate limiters.
* **Success Criteria:** UI debounces multiple rapid clicks to prevent duplicate submissions; automated bursts exceeding 10 req/sec trigger HTTP 429 Too Many Requests with exponential backoff hints.

## TS-09: Financial Accuracy & Responsive Cart Display
* **Description:** Verify dynamic calculation of subtotal, tiered sales taxes, shipping thresholds, and discounts across small mobile (375px), tablet (768px), and ultra-wide desktop (1440px+) layouts.
* **Scope:** Mathematical accuracy, currency rounding, responsive CSS/layout stability.
* **Success Criteria:** Calculations accurate to two decimal places without floating-point artifacts (e.g., `$19.99 * 3 = $59.97`); zero layout breakage, horizontal scrolling, or truncated prices across viewports.