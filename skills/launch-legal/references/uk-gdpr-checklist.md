# United Kingdom — UK GDPR, DPA 2018 & PECR Compliance Checklist

> **Disclaimer:** This checklist is for informational and operational planning purposes only and does not constitute legal advice. Every product launch requires review by a qualified solicitor or legal practitioner admitted to practice in England and Wales, Scotland, or Northern Ireland before publication.

---

## Official Primary Sources

- **Legislation:** Data Protection Act 2018 (c. 12) (DPA 2018) & the UK General Data Protection Regulation (retained Regulation (EU) 2016/679 as amended by SI 2019/419)
- **Electronic Communications & Cookies:** The Privacy and Electronic Communications (EC Directive) Regulations 2003 (SI 2003/2426 as amended) (PECR)
- **Recent Enacted Amendments:** The Data (Use and Access) Act 2025 (DUAA 2025), amending UK GDPR, DPA 2018, and PECR
- **Supervisory Authority:** Information Commissioner's Office (ICO)
- **Official Guidance URLs:**
  - [ICO UK GDPR Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/) (Confirmed HTTP 200)
  - [ICO Lawful Basis Guide](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/) (Confirmed HTTP 200)
  - [ICO Consent Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/consent/) (Confirmed HTTP 200)
  - [ICO Guide to PECR](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/) (Confirmed HTTP 200)
  - [ICO Cookies and Similar Technologies](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/cookies-and-similar-technologies/) (Confirmed HTTP 200)
  - [ICO Children and UK GDPR Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/children-and-the-uk-gdpr/) (Confirmed HTTP 200)
  - [ICO Individual Rights Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/) (Confirmed HTTP 200)
  - [ICO International Transfers Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/) (Confirmed HTTP 200)
  - [ICO Legislation We Cover](https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/) (Confirmed HTTP 200)
  - [ICO DUAA 2025 Overview](https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/) (Confirmed HTTP 200)
  - [ICO DUAA 2025 Summary of Changes](https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/the-data-use-and-access-act-2025-duaa-summary-of-the-changes/) (Confirmed HTTP 200)
  - [ICO DUAA 2025 PECR Changes](https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/the-data-use-and-access-act-2025-duaa-summary-of-the-changes/privacy-and-electronic-communications/) (Confirmed HTTP 200)
  - [ICO DUAA 2025 Schedules (Cookie Exceptions)](https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/the-data-use-and-access-act-2025-duaa-summary-of-the-changes/schedules/) (Confirmed HTTP 200)
- **Statutory Repository Verification Status:** Direct automated HTTP requests to `legislation.gov.uk` encountered AWS WAF challenge (HTTP 202); statutory requirements, retained UK GDPR text, and DUAA amendments verified directly via official Information Commissioner's Office (ICO) regulatory publications.

---

## Practical Differences: UK GDPR vs EU GDPR for Small Web Apps

For a small web application or software product operating across both jurisdictions, note these key divergences:

1. **Supervisory Authority & Dispute Redress:**
   - In the UK, the sole supervisory authority is the **Information Commissioner's Office (ICO)** (`ico.org.uk`).
   - EU mechanisms like the European Data Protection Board (EDPB) and the "One-Stop-Shop" cross-border authority mechanism do not apply to UK processing.
2. **Age of Minor Consent for Online Services:**
   - Under Section 9 of the Data Protection Act 2018, the age of consent for information society services in the UK is **13 years old** (compared to the EU default of 16 under EU GDPR Art. 8, unless individual Member States set a lower age).
   - In addition, services likely to be accessed by individuals under 18 must comply with the statutory **Age Appropriate Design Code (Children's Code)** under DPA 2018 Section 123 (privacy-by-default, geo-tracking off by default, no nudge techniques).
3. **Cross-Border Transfers & Transfer Mechanisms:**
   - Standard EU Standard Contractual Clauses (EU SCCs) cannot be used standalone for exports of personal data originating from the UK.
   - UK exporters must execute either:
     - The UK **International Data Transfer Agreement (IDTA)**, OR
     - The UK **Addendum to the EU Commission Standard Contractual Clauses**.
   - For transfers to US recipients: Exporters rely on the UK Extension to the EU-US Data Privacy Framework (requires self-certified US recipient under the UK extension) or the IDTA/Addendum with a Transfer Risk Assessment (TRA) / Data Protection Test.
4. **UK Representative Requirement (Article 27 UK GDPR):**
   - Web applications established outside the UK that regularly offer goods or services to UK residents or monitor their behaviour must formally appoint a UK representative (unless processing is occasional, low risk, and does not include special category data).
5. **Annual Data Protection Fee to the ICO:**
   - Under the Data Protection (Charges and Information) Regulations 2018, businesses processing personal data as controllers must pay an annual data protection fee to the ICO (Tier 1 micro-organisations / small businesses: £40/year, or £35 if paying via direct debit) unless an explicit statutory exemption applies.
6. **Cookie Rules & The Data (Use and Access) Act 2025 [VERIFY]:**
   - *Baseline Rule:* Under PECR Regulation 6, prior affirmative consent is required before storing or accessing information on a user's terminal equipment (cookies, local storage, SDKs) for non-essential purposes like third-party tracking, heatmaps, and advertising.
   - *DUAA Amendment:* Schedule 12 of the Data (Use and Access) Act 2025 inserts new exceptions into PECR permitting storage/access without prior consent for (i) sole purpose of collecting information for statistical purposes about how an online service is used (first-party analytics), and (ii) adapting appearance or functions to user preferences.
   - *[VERIFY with Lawyer]:* While the DUAA has been enacted, specific secondary commencement regulations, phased timeline dates, and ministerial guidance are being rolled out. Web apps **must verify** with UK legal counsel before disabling cookie banners for analytics tools. Until affirmatively verified for your specific tool, retain affirmative opt-in consent for all non-essential analytics and tracking.

---

## Statutory Requirements Checklist

### 1. Lawful Basis for Processing (UK GDPR Art. 6)
- [ ] **Documented Lawful Basis:** Every personal data processing activity is mapped to a specific lawful basis under UK GDPR Article 6(1):
  - *Consent (Art. 6(1)(a)):* Affirmative, freely given, specific, and informed.
  - *Contract Performance (Art. 6(1)(b)):* Necessary to deliver the requested service or take pre-contractual steps.
  - *Legal Obligation (Art. 6(1)(c)):* Necessary to comply with UK statutory obligations (e.g. HMRC tax record retention).
  - *Vital Interests (Art. 6(1)(d)):* Necessary to protect life.
  - *Public Task (Art. 6(1)(e)):* Official authority or public interest.
  - *Legitimate Interests (Art. 6(1)(f)):* Supported by a formal 3-part Legitimate Interests Assessment (LIA) (Purpose, Necessity, Balancing test). Note: DUAA 2025 Schedule 4 introduces a recognized legitimate interests list for public security, crime prevention, and emergencies.
  - *Citation:* UK GDPR Article 6(1)(a)-(f); DPA 2018 Section 8.
  - *Source:* [ICO Lawful Basis Guide](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/)

### 2. Consent Standards (UK GDPR Art. 7)
- [ ] **Affirmative Indication (No Bundling):** Consent requires a clear affirmative action (unticked checkboxes; pre-ticked boxes are non-compliant).
  - *Citation:* UK GDPR Article 7(2), 7(4).
- [ ] **Withdrawal as Easy as Giving:** Clear mechanism for data subjects to withdraw consent at any time (e.g. self-serve account toggle).
  - *Citation:* UK GDPR Article 7(3).
  - *Source:* [ICO Consent Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/consent/)

### 3. Cookies & Terminal Equipment (PECR Reg. 6)
- [ ] **Prior Consent for Non-Essential Cookies:** Analytics, tracking pixels, and advertising cookies/local storage must NOT load or fire before the user provides affirmative opt-in consent.
  - *Citation:* PECR Regulation 6(1)-(2); ICO Cookies Guidance.
  - *Source:* [ICO Cookies and Similar Technologies](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/cookies-and-similar-technologies/)
- [ ] **Strictly Necessary Exemption:** Exemption from consent applies only to cookies strictly necessary to provide the service requested by the user (auth session tokens, load balancing, shopping cart, CSRF protection).
  - *Citation:* PECR Regulation 6(4).
- [ ] **DUAA 2025 Analytics Exception [VERIFY]:** DUAA Schedule 12 creates an exception for first-party statistical analytics cookies. Have legal counsel verify whether this exception has formally commenced and applies to your specific analytics configuration before relying on it.
  - *Source:* [ICO DUAA Schedules](https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/the-data-use-and-access-act-2025-duaa-summary-of-the-changes/schedules/)

### 4. Direct Marketing & Electronic Mail (PECR Reg. 22)
- [ ] **Opt-in for Marketing Emails:** Direct marketing emails sent to individual subscribers require prior consent, unless the statutory "soft opt-in" criteria are met:
  1. Contact details obtained directly during a sale or negotiations for a sale of a product/service;
  2. Marketing only related to similar products/services; and
  3. A clear, simple opportunity to opt out provided at collection and in every subsequent email.
  - *Citation:* PECR Regulation 22(1)-(3).
  - *Source:* [ICO Guide to PECR](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/)

### 5. Children's Information & Age-Appropriate Design (< 18 Years)
- [ ] **Age of Consent (13 Years):** For online information society services relying on consent, parental consent is required if the child is under 13 years of age.
  - *Citation:* DPA 2018 Section 9; UK GDPR Article 8.
- [ ] **Children's Code (Age Appropriate Design Code):** If the service is likely to be accessed by children under 18, implement the 15 statutory design standards:
  1. Best interests of the child as primary consideration.
  2. High-privacy default settings (no profiling, no geolocation tracking by default).
  3. Data minimization: Only collect personal data necessary to provide core service.
  4. No nudge techniques encouraging children to weaken privacy settings.
  - *Citation:* DPA 2018 Section 123; ICO Children's Code.
  - *Source:* [ICO Children and UK GDPR Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/children-and-the-uk-gdpr/)

### 6. Individual Rights Workflows (UK GDPR Art. 12-22)
- [ ] **1-Month Response Window:** Workflow to respond to individual rights requests without undue delay and within 1 calendar month.
  - *Citation:* UK GDPR Article 12(3).
- [ ] **Right of Access (Art. 15):** Provide copies of personal data and processing purposes free of charge.
- [ ] **Right to Rectification (Art. 16):** Mechanism to update or correct inaccurate profile records.
- [ ] **Right to Erasure (Art. 17):** Mechanism to delete user data upon request across systems and backups.
- [ ] **Right to Restriction of Processing (Art. 18):** Ability to freeze data processing while disputes are evaluated.
- [ ] **Right to Data Portability (Art. 20):** Ability to export user data in structured, machine-readable format (JSON/CSV).
- [ ] **Right to Object (Art. 21):** Immediate cessation of direct marketing processing (absolute right).
- [ ] **Automated Decision-Making & Profiling (Art. 22):** Safeguards against solely automated decisions producing legal effects.
  - *Source:* [ICO Individual Rights Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/)

### 7. Processor Agreements & Security (UK GDPR Art. 28 & 32)
- [ ] **Written Data Processing Agreements (DPAs):** Mandatory written contracts with all cloud providers, database hosts, payment processors, and analytics vendors satisfying UK GDPR Article 28(3).
  - *Citation:* UK GDPR Article 28(1)-(3).
- [ ] **Technical & Organisational Safeguards:** TLS in transit, encryption at rest, principle of least privilege access, automated backups, and vulnerability patching.
  - *Citation:* UK GDPR Article 32.

### 8. International Data Transfers (UK GDPR Art. 44-46)
- [ ] **Restricted Transfer Verification:** For transfers of personal data outside the UK:
  - Confirm recipient country has a UK adequacy regulation; OR
  - Execute the UK International Data Transfer Agreement (IDTA) or UK Addendum to EU SCCs; OR
  - Confirm recipient participates in the UK Extension to the EU-US Data Privacy Framework (for US transfers); AND
  - Complete a Transfer Risk Assessment (TRA) / Data Protection Test.
  - *Citation:* UK GDPR Articles 44-46; DPA 2018 Sections 17A-17C.
  - *Source:* [ICO International Transfers Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/)

### 9. Personal Data Breach Management
- [ ] **72-Hour ICO Breach Notification:** Established incident response procedure to notify the ICO within 72 hours of becoming aware of a personal data breach posing risk to individuals.
  - *Citation:* UK GDPR Article 33(1).
- [ ] **Communication to Data Subjects:** Direct plain-language communication to affected individuals without undue delay if breach poses high risk to rights and freedoms.
  - *Citation:* UK GDPR Article 34(1)-(2).

### 10. Statutory Penalties & Criminal Offences
- [ ] **UK GDPR Administrative Fines:** Fines up to £17.5 million or 4% of total worldwide annual turnover, whichever is higher.
  - *Citation:* UK GDPR Article 83; DPA 2018 Section 157.
- [ ] **PECR Enforcement Alignment (DUAA 2025):** Maximum monetary penalties under PECR increased from £500,000 to align with UK GDPR (£17.5m or 4% of global turnover).
  - *Citation:* DUAA 2025 Schedule 13.
  - *Source:* [ICO DUAA Schedules](https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/the-data-use-and-access-act-2025-duaa-summary-of-the-changes/schedules/)
- [ ] **Statutory Criminal Offence (DPA 2018 Sec. 170):** Unlawful obtaining, disclosing, or retaining of personal data without controller consent is a criminal offence.
  - *Citation:* DPA 2018 Section 170.
