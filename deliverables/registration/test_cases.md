# Granular Test Execution Specification

| TC ID | Scenario Ref | Step Actions | Test Data | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-REG-01** | TS-E2E-01 | 1. Navigate to `/register`<br>2. Fill First Name<br>3. Fill Last Name<br>4. Fill Email<br>5. Fill Password & Confirm<br>6. Check 'Terms'<br>7. Click Submit | First: `Alex`<br>Last: `Vance`<br>Email: `unique_${timestamp}@test.com`<br>Pass: `P@ssw0rd2024!`<br>Confirm: `P@ssw0rd2024!`<br>Terms: `true` | Form submits; user is redirected to `/profile/complete`; HTTP 200/302. | PASS |
| **TC-REG-02** | TS-BVA-01 | 1. Enter 1 char in First Name<br>2. Tab to next field | First: `A` | Field displays validation error: "Minimum 2 characters required". Submit disabled. | PASS |
| **TC-REG-03** | TS-BVA-01 | 1. Enter 2 chars in First Name<br>2. Enter 2 chars in Last Name | First: `Al`<br>Last: `Bo` | Validation passes; no field error displayed. | PASS |
| **TC-REG-04** | TS-BVA-01 | 1. Enter 10 chars in First Name<br>2. Enter 10 chars in Last Name | First: `Alexander1`<br>Last: `Livingston` | Validation passes; accepted within upper boundary. | PASS |
| **TC-REG-05** | TS-BVA-01 | 1. Enter 11 chars in First Name | First: `Alexander11` | Input blocked at 10 chars via `maxlength` or error: "Maximum 10 characters allowed". | PASS |
| **TC-REG-06** | TS-BVA-02 | 1. Enter malformed email addresses | Email: `plainaddress`, `@missinguser.com`, `user@.com.my` | Inline validation error: "Please enter a valid email address". | PASS |
| **TC-REG-07** | TS-DUP-01 | 1. Enter already registered email<br>2. Fill other valid fields<br>3. Check Terms<br>4. Click Submit | Email: `existing_user@test.com` | Submission rejected with error: "Email already used. Please choose another or log in". | PASS |
| **TC-REG-08** | TS-DUP-02 | 1. Enter duplicate email with varied casing | Email: `EXISTING_USER@test.com` | System treats email as lowercase; collision detected and rejected. | PASS |
| **TC-REG-09** | TS-BVA-03 | 1. Enter password with $< 8$ chars | Password: `P@ss1` | Validation error: "Password must be at least 8 characters long". | PASS |
| **TC-REG-10** | TS-BVA-03 | 1. Enter 8+ char password without numbers | Password: `Password!@#` | Validation error: "Password must include at least 1 number". | PASS |
| **TC-REG-11** | TS-BVA-03 | 1. Enter 8+ char password without special chars | Password: `Password123` | Validation error: "Password must include at least 1 special character". | PASS |
| **TC-REG-12** | TS-BVA-04 | 1. Enter mismatched Confirm Password | Pass: `Secure#123`<br>Confirm: `Secure#999` | Validation error: "Passwords do not match". Form cannot submit. | PASS |
| **TC-REG-13** | TS-BVA-05 | 1. Populate all fields with valid data<br>2. Leave Terms checkbox unchecked | Valid details<br>Terms: `false` | Submit button has `disabled` attribute; cursor shows `not-allowed`. | PASS |
| **TC-REG-14** | TS-BVA-05 | 1. Check Terms checkbox<br>2. Uncheck Terms checkbox | Terms: `true` -> `false` | Submit button toggles from enabled back to disabled. | PASS |
| **TC-REG-15** | TS-SEC-01 | 1. Inject SQLi payload into First Name & Email<br>2. Submit form | First: `' OR '1'='1`<br>Email: `sqli'--@test.com` | Input sanitized or blocked by email/name format regex; zero DB crash or bypass. | PASS |
| **TC-REG-16** | TS-SEC-02 | 1. Inject XSS script payload in First Name<br>2. Submit and trigger response | First: `<script>alert(1)</script>` | First name validation rejects input due to length ($>10$) or encodes characters (`&lt;script&gt;`). No script executes. | PASS |
| **TC-REG-17** | TS-SEC-03 | 1. Trigger 20 rapid submit requests via script within 10 seconds | Automated loop payload | Server returns HTTP 429 Too Many Requests; rate limit error displayed. | PASS |
| **TC-REG-18** | TS-DUP-03 | 1. Send two simultaneous POST requests with identical new email | Identical payloads sent via `Promise.all` | Exactly 1 request completes with 200/201; 2nd request returns 409 Conflict. | PASS |