# California CCPA / CPRA — Privacy Compliance Checklist

> **Disclaimer:** This checklist is for informational and operational planning purposes only and does not constitute legal advice. Every product launch requires review by a qualified attorney admitted to practice in California or the United States before publication.

---

## Official Primary Sources

- **Legislation:** California Consumer Privacy Act of 2018 (CCPA), as amended by Proposition 24, the California Privacy Rights Act of 2020 (CPRA) (Cal. Civ. Code § 1798.100 et seq.)
- **Enforcement & Oversight Agencies:** California Privacy Protection Agency (CPPA) & Office of the Attorney General (OAG), California Department of Justice
- **Official OAG CCPA Portal:** [California DOJ CCPA Overview](https://oag.ca.gov/privacy/ccpa) (Confirmed HTTP 200)
- **Official OAG Global Privacy Control Guidance:** [California DOJ GPC](https://oag.ca.gov/privacy/ccpa/gpc) (Confirmed HTTP 200)
- **Official CPPA Regulations Portal:** [CPPA Regulations](https://cppa.ca.gov/regulations/consumer_privacy_act.html) (Confirmed HTTP 200)
- **Official CPPA Regulations Text:** [CPPA Final Regulations Text PDF](https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf) (Title 11, Division 6, California Code of Regulations; Confirmed HTTP 200, 515,569 bytes)
- **Official CPPA FAQs:** [CPPA Frequently Asked Questions](https://cppa.ca.gov/faq.html) (Confirmed HTTP 200)
- **Statutory Repository Verification Status:** Direct automated requests to California Legislative Information (`leginfo.legislature.ca.gov`) encountered Cloudflare automated challenges (HTTP 403); statutory sections (Cal. Civ. Code § 1798.100 et seq.) verified through California DOJ OAG publications and CPPA regulatory texts.

---

## Statutory Requirements Checklist

### 1. Scope & Statutory Application Thresholds
- [ ] **Threshold Assessment:** Applies to any for-profit business collecting personal information of California consumers, determining processing purposes/means, doing business in California, and meeting **any one** of three statutory thresholds:
  1. *Gross Annual Revenue:* Generated gross annual revenue exceeding $25 million in the preceding calendar year (adjusted for inflation to $26.625 million effective January 1, 2025; Cal. Civ. Code § 1798.140(d)(1)(A)).
  2. *Data Volume Threshold:* Annually buys, sells, or shares the personal information of 100,000 or more California consumers or households (Cal. Civ. Code § 1798.140(d)(1)(B)).
  3. *Revenue Percentage Threshold:* Derives 50% or more of its annual revenue from selling or sharing California consumers' personal information (Cal. Civ. Code § 1798.140(d)(1)(C)).
  - *Citation:* Cal. Civ. Code § 1798.140(d)(1); 11 CCR § 7002.
  - *Source:* [CPPA FAQ](https://cppa.ca.gov/faq.html)
- [ ] **Exemptions & Expired Relief:**
  - Non-profits and government agencies are generally exempt (Cal. Civ. Code § 1798.140(d)).
  - Statutory exemptions for employee personal information and business-to-business (B2B) communications expired on December 31, 2022 (Cal. Civ. Code § 1798.145(m)-(n); CPPA FAQ).

### 2. Notice at Collection of Personal Information
- [ ] **Timing & Visibility:** Notice at collection is provided to consumers at or before the point of personal information collection (prominently linked on website homepage, account creation screens, and mobile app download/settings).
  - *Citation:* Cal. Civ. Code § 1798.100(a); 11 CCR § 7012(a)-(c).
  - *Source:* [California DOJ CCPA](https://oag.ca.gov/privacy/ccpa), [CPPA Final Regs PDF p. 17](https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf#page=17)
- [ ] **Mandatory Disclosure Contents:**
  1. Specific categories of personal information to be collected.
  2. The specific operational/business purpose for each category collected.
  3. Clear statement whether each category of personal information is "sold" or "shared" (for cross-context behavioral advertising).
  4. Explicit disclosure of categories of Sensitive Personal Information (SPI) collected, their intended purposes, and whether sold or shared.
  5. Concrete retention criteria or periods for each category (data cannot be retained longer than reasonably necessary for the disclosed purpose).
  6. A direct link to the business's full Privacy Policy and a link to the "Do Not Sell or Share My Personal Information" mechanism if selling or sharing.
  - *Citation:* Cal. Civ. Code § 1798.100(a)(1)-(3); 11 CCR § 7012(e).
  - *Source:* [CPPA Final Regs PDF p. 17-19](https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf#page=17)

### 3. Consumer Privacy Rights Workflows
- [ ] **Right to Know (Access):** Consumers can request disclosure of (1) categories of PI collected, (2) categories of sources, (3) business or commercial purpose, (4) categories of third parties to whom PI was disclosed/shared, and (5) specific pieces of personal information collected in the preceding 12+ months (up to twice a year, free of charge).
  - *Citation:* Cal. Civ. Code §§ 1798.110, 1798.115, 1798.130(a); 11 CCR § 7024.
  - *Source:* [California DOJ CCPA](https://oag.ca.gov/privacy/ccpa), [CPPA FAQ](https://cppa.ca.gov/faq.html)
- [ ] **Right to Delete:** Consumers can request deletion of personal information collected by the business, requiring the business to delete the data and instruct service providers, contractors, and third parties to delete (subject to narrow statutory exceptions under § 1798.105(d) such as legal compliance, completing transactions, or security debugging).
  - *Citation:* Cal. Civ. Code § 1798.105; 11 CCR § 7022.
  - *Source:* [California DOJ CCPA](https://oag.ca.gov/privacy/ccpa)
- [ ] **Right to Correct:** Consumers can request the correction of inaccurate personal information maintained by the business.
  - *Citation:* Cal. Civ. Code § 1798.106; 11 CCR § 7023.
  - *Source:* [California DOJ CCPA](https://oag.ca.gov/privacy/ccpa), [CPPA FAQ](https://cppa.ca.gov/faq.html)
- [ ] **Right to Opt-Out of Sale or Sharing:** Consumers have the continuous right to opt-out of the "sale" of personal information (for monetary or other valuable consideration) or "sharing" of personal information (for cross-context behavioral advertising).
  - *Citation:* Cal. Civ. Code § 1798.120; 11 CCR § 7026.
  - *Source:* [California DOJ CCPA](https://oag.ca.gov/privacy/ccpa)
- [ ] **Right to Limit Use of Sensitive Personal Information:** Consumers can direct the business to limit the use of Sensitive Personal Information strictly to that necessary to perform services or provide goods reasonably requested.
  - *Citation:* Cal. Civ. Code § 1798.121; 11 CCR § 7027.
  - *Source:* [California DOJ CCPA](https://oag.ca.gov/privacy/ccpa), [CPPA FAQ](https://cppa.ca.gov/faq.html)
- [ ] **Right to Non-Discrimination:** Prohibits denying goods/services, charging different prices, or providing different quality to consumers who exercise CCPA rights, unless differences are reasonably related to the value of the consumer's data under a valid notice of financial incentive.
  - *Citation:* Cal. Civ. Code § 1798.125; 11 CCR § 7080-7081.
  - *Source:* [California DOJ CCPA](https://oag.ca.gov/privacy/ccpa)
- [ ] **Response Timelines:**
  - Requests to Know, Delete, and Correct must be fulfilled within **45 calendar days** (extendable once by an additional 45 days upon providing written notice and explanation within the initial 45-day window).
  - Requests to Opt-Out of Sale/Sharing and Requests to Limit Sensitive Personal Information must be acted upon within **15 business days**.
  - *Citation:* Cal. Civ. Code § 1798.130(a)(2); 11 CCR § 7021(a), § 7026(f), § 7027(g).
  - *Source:* [California DOJ CCPA](https://oag.ca.gov/privacy/ccpa), [CPPA Final Regs PDF p. 27, 42, 46](https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf#page=27)

### 4. Opt-Out Architecture & Global Privacy Control (GPC)
- [ ] **"Do Not Sell or Share My Personal Information" Link:** Clear and conspicuous link in website footers and within the privacy policy allowing immediate submission of opt-out requests without requiring account creation.
  - *Citation:* Cal. Civ. Code § 1798.135(a)(1); 11 CCR § 7013, § 7015.
  - *Source:* [California DOJ CCPA](https://oag.ca.gov/privacy/ccpa)
- [ ] **Mandatory Global Privacy Control (GPC) Recognition:** Online services must treat user-enabled opt-out preference signals (such as GPC sent via HTTP headers `Sec-GPC` or browser settings in Brave, Firefox, DuckDuckGo) as valid requests to opt-out of sale and sharing.
  - Must operate seamlessly without charging fees, requiring account login, or overriding user preferences with dark patterns.
  - *Citation:* 11 CCR § 7025; Cal. Civ. Code § 1798.135(e).
  - *Source:* [California DOJ GPC](https://oag.ca.gov/privacy/ccpa/gpc), [CPPA Final Regs PDF p. 35-40](https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf#page=35)
- [ ] **12-Month Opt-In Moratorium:** Once a consumer submits an opt-out request, the business must wait at least 12 months before asking the consumer to opt back into the sale or sharing of their personal information.
  - *Citation:* Cal. Civ. Code § 1798.135(c)(4); 11 CCR § 7028.
  - *Source:* [California DOJ CCPA](https://oag.ca.gov/privacy/ccpa)

### 5. Sensitive Personal Information (SPI) Protections
- [ ] **Statutory Scope of SPI:** Includes Social Security numbers, driver's licenses, state IDs, financial account credentials with passwords, precise geolocation, racial or ethnic origin, religious or philosophical beliefs, union membership, contents of non-recipient mail/email/texts, genetic data, and biometric/health/sexual orientation data.
  - *Citation:* Cal. Civ. Code § 1798.140(ae).
  - *Source:* [CPPA FAQ](https://cppa.ca.gov/faq.html)
- [ ] **"Limit the Use of My Sensitive Personal Information" Mechanism:** If SPI is used or disclosed for purposes other than performing requested services/goods or permitted business operations under 11 CCR § 7027(m), the business must provide a dedicated link or opt-out mechanism to limit use.
  - *Citation:* Cal. Civ. Code § 1798.135(a)(2); 11 CCR § 7014, § 7027.
  - *Source:* [CPPA Final Regs PDF p. 23, 44-47](https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf#page=23)

### 6. Children's Privacy Protections (< 16 Years)
- [ ] **Absolute Ban on Sale/Sharing Without Opt-In:** Businesses cannot sell or share personal information of consumers known to be under 16 years of age without affirmative authorization ("opt-in").
  - *Citation:* Cal. Civ. Code § 1798.120(c); 11 CCR § 7070-7072.
  - *Source:* [California DOJ CCPA](https://oag.ca.gov/privacy/ccpa)
- [ ] **Under 13 Parental Consent:** For children under 13 years of age, affirmative opt-in consent must be obtained from the child's parent or legal guardian using verifiable methods (consistent with COPPA).
  - *Citation:* Cal. Civ. Code § 1798.120(c); 11 CCR § 7070.
  - *Source:* [CPPA Final Regs PDF p. 58](https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf#page=58)
- [ ] **Ages 13 to 15 Child Consent:** For children at least 13 and under 16 years of age, affirmative opt-in consent must be obtained directly from the minor consumer.
  - *Citation:* Cal. Civ. Code § 1798.120(c); 11 CCR § 7071.
  - *Source:* [CPPA Final Regs PDF p. 59](https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf#page=59)
- [ ] **Treble Statutory Penalties for Minor Violations:** Civil penalties of up to $7,500 per violation (the statutory figure; the CPPA adjusts these amounts for inflation every two years, so check the current number at cppa.ca.gov before quoting it) apply to any intentional violation or any violation involving the personal information of consumers known to be under 16 years of age.
  - *Citation:* Cal. Civ. Code § 1798.155(a).
  - *Source:* [California DOJ CCPA](https://oag.ca.gov/privacy/ccpa)

### 7. Service Provider & Contractor Contractual Governance
- [ ] **Mandatory Binding Contracts:** All third-party vendors processing personal information on behalf of the business must execute written contracts binding them to:
  1. Prohibit selling or sharing personal information.
  2. Prohibit retaining, using, or disclosing personal information for any purpose other than the specific business purposes specified in the contract.
  3. Prohibit retaining, using, or disclosing personal information outside the direct business relationship.
  4. Grant the business audit and monitoring rights to verify compliance.
  - *Citation:* Cal. Civ. Code § 1798.140(ag), (j); 11 CCR § 7051.
  - *Source:* [CPPA Final Regs PDF p. 50-52](https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf#page=50)

### 8. Private Right of Action & Security Safeguards
- [ ] **Reasonable Security Procedures:** Implement and maintain reasonable security procedures and practices appropriate to the nature of personal information.
  - *Citation:* Cal. Civ. Code § 1798.100(e).
- [ ] **Data Breach Statutory Damages:** Consumers have a private right of action if nonencrypted and nonredacted personal information is subject to unauthorized access, exfiltration, theft, or disclosure due to a business's violation of the duty to maintain reasonable security.
  - *Statutory Damages:* $100 to $750 per consumer per incident, or actual damages, whichever is greater.
  - *Citation:* Cal. Civ. Code § 1798.150(a)(1).
  - *Source:* [California DOJ CCPA](https://oag.ca.gov/privacy/ccpa)
