# EU GDPR & ePrivacy Directive — Compliance Checklist

> **Disclaimer:** This checklist is for informational and operational planning purposes only and does not constitute legal advice. Every product launch requires review by a qualified legal professional admitted in an EU jurisdiction before publication.

---

## Official Primary Sources

- **Legislation:** Regulation (EU) 2016/679 of the European Parliament and of the Council (General Data Protection Regulation - GDPR)
- **Official Text URL:** [EUR-Lex CELEX:32016R0679](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679) (Confirmed HTTP 200, 1,069,042 bytes)
- **ePrivacy Directive:** Directive 2002/58/EC of the European Parliament and of the Council (as amended by Directive 2009/136/EC)
- **Official Text URL:** [EUR-Lex CELEX:32002L0058](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32002L0058) (Confirmed HTTP 200)

---

## Statutory Requirements Checklist

### 1. Legal Basis for Processing
- [ ] **Documented Lawful Basis:** For every single processing purpose, a lawful basis under Article 6(1) is formally documented:
  - *Consent (Art. 6(1)(a)):* Freely given, specific, informed, and unambiguous.
  - *Contract Performance (Art. 6(1)(b)):* Strictly necessary to fulfill core service requested by user.
  - *Legal Obligation (Art. 6(1)(c)):* Necessary to comply with EU/Member State laws (e.g., invoice/tax record retention).
  - *Vital Interests (Art. 6(1)(d)):* To protect life/health.
  - *Public Task (Art. 6(1)(e)):* Official authority.
  - *Legitimate Interests (Art. 6(1)(f)):* Requires a documented Legitimate Interests Assessment (LIA) balancing test; cannot override data subject rights, cannot be used for children's data or direct marketing.
  - *Citation:* Article 6(1)(a)-(f).
  - *Source:* [EUR-Lex 32016R0679](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679)

### 2. Consent Conditions (When Consent is the Basis)
- [ ] **Burden of Proof:** Controller is capable of demonstrating that the data subject consented (audit log of consent event).
  - *Citation:* Article 7(1).
- [ ] **Distinguishable & Clear:** Request for consent is clearly distinguishable from terms of service, in intelligible and plain language.
  - *Citation:* Article 7(2).
- [ ] **Withdrawal as Easy as Giving:** The data subject can withdraw consent at any time; withdrawing consent must be as easy as giving it (e.g., self-serve account toggle).
  - *Citation:* Article 7(3).
- [ ] **Freely Given (No Bundling):** Service provision must not be conditioned on consent to process data unnecessary for that contract.
  - *Citation:* Article 7(4).
  - *Source:* [EUR-Lex 32016R0679](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679)

### 3. Cookies & Terminal Equipment (ePrivacy Directive)
- [ ] **Prior Informed Opt-In for Non-Essential Cookies:** Analytics, tracking, advertising, and third-party cookies/local storage must NOT load or set cookies until the user clicks affirmative opt-in consent.
  - *Citation:* Directive 2002/58/EC Article 5(3) (as amended by Directive 2009/136/EC).
  - *Source:* [EUR-Lex 32002L0058](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32002L0058)
- [ ] **No Pre-Ticked Boxes or Cookie Walls:** Pre-ticked consent toggles and cookie walls (blocking service access unless user accepts tracking) are non-compliant.
- [ ] **Exemption for Strictly Necessary Cookies:** Only technical cookies strictly necessary to provide the service requested by the user (auth session tokens, load balancing, shopping cart) are exempt from prior consent.

### 4. Privacy Notice Transparency Disclosures
Every privacy notice provided at data collection must state:
- [ ] **Controller & Representative Details:** Legal entity name, registered office address, and contact email.
  - *Citation:* Article 13(1)(a).
- [ ] **Data Protection Officer (DPO):** Contact details of DPO if designated.
  - *Citation:* Article 13(1)(b) & Article 37.
- [ ] **Purposes & Legal Basis:** Specific purpose paired with exact legal basis under Article 6(1).
  - *Citation:* Article 13(1)(c).
- [ ] **Legitimate Interests (if applicable):** Specific interests pursued if relying on Art. 6(1)(f).
  - *Citation:* Article 13(1)(d).
- [ ] **Recipients of Personal Data:** Specific third-party recipients or categories (cloud providers, payment processors, customer support SDKs).
  - *Citation:* Article 13(1)(e).
- [ ] **Cross-Border Transfers:** Details on data transfers outside the EEA, including adequacy decisions (Article 45) or Standard Contractual Clauses (SCCs, Article 46) and where copies may be obtained.
  - *Citation:* Article 13(1)(f) & Articles 44-49.
- [ ] **Retention Periods:** Concrete storage durations for each data category, or specific objective criteria used to determine retention.
  - *Citation:* Article 13(2)(a).
- [ ] **Data Subject Rights Enumeration:** Explicitly listing rights to access, rectification, erasure, restriction, objection, and data portability.
  - *Citation:* Article 13(2)(b).
- [ ] **Right to Withdraw Consent:** Explicit mention of right to withdraw consent at any time without affecting prior lawful processing.
  - *Citation:* Article 13(2)(c).
- [ ] **Right to Lodge Complaint:** Informing users of their statutory right to lodge a complaint with an EU Member State Data Protection Authority (Supervisory Authority).
  - *Citation:* Article 13(2)(d).
- [ ] **Automated Decision-Making & Profiling:** Disclosing existence, logic involved, and anticipated consequences if profiling or automated decisions are made.
  - *Citation:* Article 13(2)(f) & Article 22.
  - *Source:* [EUR-Lex 32016R0679](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679)

### 5. Data Subject Rights Workflows
- [ ] **1-Month Response Window:** Workflow in place to handle and respond to Data Subject Access Requests (DSARs) without undue delay and within 1 calendar month.
  - *Citation:* Article 12(3).
- [ ] **Right of Access (Art. 15):** User can download/receive copy of personal data and processing metadata.
- [ ] **Right to Rectification (Art. 16):** Mechanism to update or correct inaccurate profile information.
- [ ] **Right to Erasure / "Right to be Forgotten" (Art. 17):** Mechanism to request permanent account and data deletion across all systems and backup schedules.
- [ ] **Right to Restriction (Art. 18):** Capability to freeze data processing while disputes/accuracy are verified.
- [ ] **Right to Data Portability (Art. 20):** Ability to export user data in a structured, commonly used, machine-readable format (e.g., JSON or CSV).
- [ ] **Right to Object (Art. 21):** Immediate opt-out from direct marketing (absolute right) or legitimate interest processing.

### 6. Processor Agreements & Security
- [ ] **Article 28 Data Processing Agreements (DPAs):** Written, binding contracts executed with all subprocessors (AWS, Supabase, Stripe, Sendgrid, PostHog, etc.) enforcing Article 28 obligations.
  - *Citation:* Article 28(1)-(3).
- [ ] **Security Measures (Art. 32):** Technical and organizational safeguards including TLS in transit, encryption at rest, role-based least-privilege access, audit logging, and vulnerability management.
  - *Citation:* Article 32(1)(a)-(d).

### 7. Data Breach Notification
- [ ] **Supervisory Authority Notification (72 Hours):** Established procedure to notify competent EU supervisory authority within 72 hours of becoming aware of a personal data breach, unless unlikely to risk individuals' rights.
  - *Citation:* Article 33(1).
- [ ] **Communication to Affected Individuals:** Procedure to communicate high-risk breaches directly to affected individuals without undue delay in plain language.
  - *Citation:* Article 34(1)-(2).
  - *Source:* [EUR-Lex 32016R0679](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679)
