# HIPAA Compliance for Denials Doctor RCM AI

## 1. Overview

The Health Insurance Portability and Accountability Act of 1996 (HIPAA) sets the national standard for protecting sensitive patient health information. As a revenue cycle management (RCM) AI platform, Denials Doctor handles Protected Health Information (PHI) on behalf of its healthcare provider clients and must maintain full HIPAA compliance. This document covers the Privacy Rule, Security Rule, HITECH Act, breach notification, Business Associate Agreements (BAAs), enforcement, state privacy laws, and AI-specific considerations.

---

## 2. HIPAA Privacy Rule (45 CFR Part 164, Subpart E, Sections 164.500-534)

### 2.1 Protected Health Information (PHI) Definition

PHI is individually identifiable health information held or transmitted by a covered entity or its business associate, in any form or medium (electronic, paper, or oral). The **18 HIPAA identifiers** that make health information identifiable are:

| # | Identifier | Example |
|---|-----------|---------|
| 1 | Names | Full name, initials |
| 2 | Geographic subdivisions smaller than a state | Street address, city, county, ZIP code (initial 3 digits of ZIP if population < 20,000 may be used) |
| 3 | Dates (except year) | Birth date, admission date, discharge date, date of death, exact age if over 89 |
| 4 | Telephone numbers | Any phone number |
| 5 | Fax numbers | Any fax number |
| 6 | Email addresses | Any email address |
| 7 | Social Security Numbers | Full SSN |
| 8 | Medical record numbers | MRN, account number |
| 9 | Health plan beneficiary numbers | Medicare ID, member ID |
| 10 | Account numbers | Bank or patient account numbers |
| 11 | Certificate/license numbers | License numbers |
| 12 | Vehicle identifiers | License plate, VIN |
| 13 | Device identifiers and serial numbers | Medical device serial numbers |
| 14 | Web URLs | Internet URLs |
| 15 | IP addresses | Internet Protocol addresses |
| 16 | Biometric identifiers | Fingerprints, voice prints |
| 17 | Full-face photographs and comparable images | Photos, videos |
| 18 | Any other unique identifying number, characteristic, or code | Unspecified unique identifiers |

**Note for Denials Doctor:** In the RCM context, PHI includes patient names, dates of birth, insurance member IDs, medical record numbers, account numbers, diagnosis codes, procedure codes, and clinical notes that accompany a claim.

### 2.2 Permitted Uses and Disclosures

HIPAA permits use and disclosure of PHI without patient authorization for three core activities:

- **Treatment:** The provision, coordination, or management of health care. (Not typically relevant for Denials Doctor as an RCM platform.)
- **Payment:** Activities to obtain reimbursement for health care services. This is the primary basis for Denials Doctor's processing of claims. Includes: billing, claims management, collections, eligibility verification, utilization review, and coding.
- **Operations:** Covered entity functions such as quality assessment, licensing, credentialing, medical review, auditing, and business planning. Denials Doctor uses PHI for denial analytics and reporting, which falls under healthcare operations.

**Other Permitted Disclosures (without authorization):**
- As required by law (public health activities, law enforcement, etc.)
- For public health activities (disease reporting, FDA adverse events)
- For health oversight activities (audits, investigations)
- For judicial and administrative proceedings
- For law enforcement purposes
- For research (with IRB waiver or limited data set)
- To avert serious threat to health or safety
- For workers' compensation

### 2.3 Minimum Necessary Standard (45 CFR 164.502(b), 164.514(d))

When using or disclosing PHI or when requesting PHI from another covered entity, a covered entity must make **reasonable efforts** to limit PHI to the **minimum necessary** to accomplish the intended purpose.

**Exceptions (minimum necessary does not apply):**
- Disclosures to or requests by a health care provider for treatment
- Disclosures to the individual who is the subject of the PHI
- Disclosures authorized by the individual
- Disclosures to the HHS Secretary for enforcement
- Uses or disclosures required by law
- Uses or disclosures for HIPAA compliance

**Denials Doctor Application:** The platform should only access and process the minimum PHI necessary for claim denial analysis and appeals generation. For example, if analyzing a coding-related denial, the platform should access the relevant diagnosis/procedure codes and clinical documentation but should not access unrelated sensitive information.

### 2.4 Patient Rights

HIPAA grants individuals the following rights regarding their PHI:

**Right of Access (45 CFR 164.524):**
- Patients have the right to inspect and obtain a copy of their PHI in a designated record set
- Covered entities must act on access requests within 30 days (one 30-day extension available)
- Reasonable cost-based fees may be charged for copies
- Denials must be in writing with review rights explained

**Right to Amendment (45 CFR 164.526):**
- Patients may request amendment to their PHI in a designated record set
- Covered entity must act within 60 days (one 30-day extension available)
- Denials must include basis and appeal rights

**Right to Accounting of Disclosures (45 CFR 164.528):**
- Patients may request an accounting of disclosures of their PHI made in the prior 6 years
- Excludes disclosures for treatment, payment, operations, and certain other categories
- First accounting in 12-month period is free

**Right to Request Restrictions (45 CFR 164.522):**
- Patients may request restrictions on uses/disclosures of their PHI
- Covered entity is not required to agree except for disclosures to a health plan if the patient paid out of pocket in full

**Right to Confidential Communications (45 CFR 164.522(b)):**
- Patients may request alternative means or locations for communications about their PHI

### 2.5 Notice of Privacy Practices (NPP) (45 CFR 164.520)

Covered entities must provide a Notice of Privacy Practices that:
- Describes how PHI may be used and disclosed
- States the covered entity's duties to protect PHI
- Describes individual rights with respect to PHI
- Provides contact information for complaints
- States that the entity is required to notify individuals following a breach
- Must be provided at first service delivery and posted prominently

### 2.6 Breach Notification Rule (45 CFR 164.400-414)

See Section 5 (Breach Notification) below for detailed coverage.

---

## 3. HIPAA Security Rule (45 CFR Part 164, Subpart C, Sections 164.300-318)

The Security Rule establishes national standards for protecting electronic PHI (ePHI) that is created, received, used, or maintained by a covered entity or business associate. Unlike the Privacy Rule, the Security Rule is **technology-neutral** and **scalable** -- requirements vary based on the entity's size, complexity, and capabilities.

### 3.1 Administrative Safeguards (45 CFR 164.308)

| Standard | Required vs Addressable | Description |
|----------|------------------------|-------------|
| Security Management Process (Risk Analysis) | **Required** | Conduct accurate and thorough assessment of potential risks and vulnerabilities to the confidentiality, integrity, and availability of ePHI |
| Security Management Process (Risk Management) | **Required** | Implement security measures sufficient to reduce risks and vulnerabilities to a reasonable and appropriate level |
| Security Management Process (Sanction Policy) | **Required** | Apply appropriate sanctions against workforce members who fail to comply with security policies |
| Security Management Process (Information System Activity Review) | **Required** | Regularly review records of information system activity (audit logs, access reports) |
| Assigned Security Responsibility | **Required** | Identify the security official responsible for developing and implementing security policies |
| Workforce Security (Authorization/Supervision) | **Addressable** | Authorize and supervise workforce members who work with ePHI |
| Workforce Security (Workforce Clearance Procedure) | **Addressable** | Determine appropriate access levels based on job function |
| Workforce Security (Termination Procedures) | **Addressable** | Terminate access when workforce member leaves |
| Information Access Management (Isolating Health Care Clearinghouse Functions) | **Required** | If a clearinghouse, ensure firewall between clearinghouse and other business units |
| Information Access Management (Access Authorization) | **Addressable** | Establish policies for granting access to ePHI |
| Information Access Management (Access Establishment and Modification) | **Addressable** | Establish procedures for modifying or terminating access |
| Security Awareness and Training (Security Reminders) | **Addressable** | Periodic security updates for workforce |
| Security Awareness and Training (Protection from Malicious Software) | **Addressable** | Procedures for guarding against malware |
| Security Awareness and Training (Log-in Monitoring) | **Addressable** | Procedures for monitoring log-in attempts |
| Security Awareness and Training (Password Management) | **Addressable** | Procedures for creating, changing, and safeguarding passwords |
| Security Incident Procedures | **Required** | Identify and respond to suspected or known security incidents |
| Contingency Plan (Data Backup Plan) | **Required** | Establish and implement procedures to create retrievable exact copies of ePHI |
| Contingency Plan (Disaster Recovery Plan) | **Required** | Establish procedures to restore any loss of ePHI |
| Contingency Plan (Emergency Mode Operation Plan) | **Required** | Establish procedures to enable continuation of critical business processes while operating in emergency mode |
| Contingency Plan (Testing and Revision) | **Addressable** | Periodically test contingency plans |
| Contingency Plan (Applications and Data Criticality Analysis) | **Addressable** | Assess criticality of specific applications and data |
| Evaluation | **Required** | Periodically evaluate technical and nontechnical security measures |
| Business Associate Contracts or Other Arrangements | **Required** | Obtain satisfactory assurances (BAA) from business associates |

### 3.2 Physical Safeguards (45 CFR 164.310)

| Standard | Required vs Addressable | Description |
|----------|------------------------|-------------|
| Facility Access Controls (Contingency Operations) | **Addressable** | Establish procedures to enable facility access during an emergency |
| Facility Access Controls (Facility Security Plan) | **Addressable** | Implement policies to safeguard the facility and equipment from unauthorized access, tampering, or theft |
| Facility Access Controls (Access Control and Validation Procedures) | **Addressable** | Implement procedures to control and validate access to facilities based on role/function |
| Facility Access Controls (Maintenance Records) | **Addressable** | Document repairs and modifications to security-related physical components |
| Workstation Use | **Required** | Specify proper functions and physical attributes of workstations that access ePHI |
| Workstation Security | **Required** | Implement physical safeguards for workstations accessing ePHI |
| Device and Media Controls (Disposal) | **Required** | Implement policies for disposal of hardware and electronic media containing ePHI |
| Device and Media Controls (Media Re-use) | **Required** | Procedures for removal of ePHI before media reuse |
| Device and Media Controls (Accountability) | **Addressable** | Track movement of hardware and electronic media |
| Device and Media Controls (Data Backup and Storage) | **Addressable** | Create retrievable exact copies of ePHI before moving equipment |

### 3.3 Technical Safeguards (45 CFR 164.312)

| Standard | Required vs Addressable | Description |
|----------|------------------------|-------------|
| Access Control (Unique User Identification) | **Required** | Assign unique names/numbers to identify and track user identity |
| Access Control (Emergency Access Procedure) | **Required** | Establish procedures for obtaining necessary ePHI during an emergency |
| Access Control (Automatic Logoff) | **Addressable** | Implement electronic procedures that terminate an electronic session after a predetermined time of inactivity |
| Access Control (Encryption and Decryption) | **Addressable** | Implement mechanisms to encrypt and decrypt ePHI |
| Audit Controls | **Required** | Record and examine information system activity |
| Integrity Controls | **Addressable** | Implement policies to protect ePHI from improper alteration or destruction |
| Person or Entity Authentication | **Required** | Verify that a person or entity seeking access is the one claimed |
| Transmission Security (Integrity Controls) | **Addressable** | Ensure that ePHI is not improperly modified during transmission |
| Transmission Security (Encryption) | **Addressable** | Implement encryption for ePHI transmitted over electronic networks |

### 3.4 Required vs Addressable Implementation Specifications

- **Required:** Must be implemented as stated; no discretion.
- **Addressable:** Must assess whether the specification is a reasonable and appropriate safeguard. If it is, implement it. If not, document why and implement an equivalent alternative measure if reasonable and appropriate. **Addressable does not mean optional.**

**Example for Denials Doctor:** Encryption of ePHI at rest is addressable. However, given the nature of the platform (cloud-based, processing sensitive claim data), encryption at rest (AES-256) and in transit (TLS 1.2+) should be standard.

---

## 4. HITECH Act (Health Information Technology for Economic and Clinical Health Act of 2009)

The HITECH Act, enacted as part of the American Recovery and Reinvestment Act of 2009, strengthened HIPAA privacy and security enforcement.

### 4.1 Key Provisions

- **Business Associate Direct Liability:** Business associates (like Denials Doctor) are now **directly liable** for HIPAA Privacy and Security Rule compliance, not just through contractual obligations. Before HITECH, BA liability was only through BAA contracts.
- **Increased Penalties:** Raised civil monetary penalties significantly (see Section 7: Enforcement).
- **Breach Notification Requirements:** Created the Breach Notification Rule requiring covered entities and business associates to notify affected individuals, HHS, and (in some cases) media.
- **Accounting of Disclosures for EHR:** Expanded right to an accounting of disclosures for electronic health records.
- **Marketing and Sale Restrictions:** Restricted use of PHI for marketing and prohibited sale of PHI without authorization.
- **HIPAA Enforcement Rule (2013 Omnibus Rule):** The HITECH Act was fully implemented through the 2013 HIPAA Omnibus Final Rule, which extended many requirements to business associates.

### 4.2 Denials Doctor Obligations Under HITECH

As a business associate, Denials Doctor must:
- Comply directly with the Security Rule's administrative, physical, and technical safeguards
- Comply with the Breach Notification Rule (notify covered entity of breaches)
- Enter into BAAs with subcontractors who handle ePHI
- Comply with the Privacy Rule provisions applicable to business associates
- Not use or disclose PHI in a manner prohibited by the Privacy Rule

---

## 5. Breach Notification

### 5.1 Breach Definition (45 CFR 164.402)

A **breach** is the acquisition, access, use, or disclosure of PHI in a manner not permitted by the Privacy Rule that compromises the security or privacy of the PHI.

**Exceptions (not a breach):**
- Unintentional acquisition, access, or use by a workforce member if in good faith, within the scope of authority, and does not result in further impermissible use
- Inadvertent disclosure between authorized persons at the same entity
- Disclosure to an unauthorized person if the entity has a good faith belief that the unauthorized person would not have been able to retain the information

### 5.2 Risk Assessment (Four-Factor Test)

To determine if a breach occurred and notification is required, entities must conduct a risk assessment considering:

1. **The nature and extent of the PHI involved:** What types of identifiers were exposed? Likelihood of re-identification?
2. **The unauthorized person who used the PHI or to whom the disclosure was made:** Did the recipient have a previous relationship? Are there obligations to protect PHI?
3. **Whether the PHI was actually acquired or viewed:** Evidence of actual acquisition or viewing?
4. **The extent to which the risk to the PHI has been mitigated:** Has the PHI been returned? Has the recipient agreed to destroy it?

If there is a **low probability** that the PHI has been compromised (based on the four-factor test), no breach notification is required. This determination must be documented in writing.

### 5.3 Notification Timeline and Requirements

**For Breaches Affecting 500 or More Individuals:**
- **Notify affected individuals:** Without unreasonable delay, no later than 60 calendar days from discovery of the breach
- **Notify HHS:** Simultaneously with individual notification (through the OCR breach portal)
- **Notify media:** Prominent media outlets serving the state or jurisdiction

**For Breaches Affecting Fewer Than 500 Individuals:**
- **Notify affected individuals:** Without unreasonable delay, no later than 60 calendar days from discovery
- **Notify HHS:** Within 60 days after the end of the calendar year in which the breach occurred (annual reporting via OCR portal)

### 5.4 Notification Content

The notification must include:
- Brief description of the breach (date of breach, date of discovery)
- Description of the types of PHI involved
- Steps individuals should take to protect themselves
- Brief description of the entity's investigation and mitigation actions
- Contact information for questions (toll-free number, email, website)

### 5.5 Breach Discovery

A breach is **discovered** on the first day the breach is known or, by exercising reasonable diligence, would have been known. The 60-day clock starts from discovery.

### 5.6 Business Associate Breach Obligations

When Denials Doctor (as a business associate) discovers a breach:
1. Notify the covered entity (client) without unreasonable delay, no later than 60 calendar days
2. Provide the identification of the individual whose PHI was breached
3. Provide any other available information needed for the covered entity to fulfill its notification obligations
4. Maintain documentation of all breach notifications

---

## 6. Business Associate Agreements (BAA)

### 6.1 Definition and Requirement

A **Business Associate** (BA) is a person or entity that creates, receives, maintains, or transmits PHI on behalf of a covered entity for a function or activity regulated by HIPAA. Denials Doctor, as an RCM AI platform, is a **business associate** of its healthcare provider clients.

A **Business Associate Agreement (BAA)** is the contract required between a covered entity and a business associate. It must be in place before PHI is shared with the BA.

### 6.2 Required BAA Provisions (45 CFR 164.504(e))

The BAA must:
- Describe the permitted and required uses of PHI by the BA
- Prohibit the BA from using or disclosing PHI other than as permitted by the BAA or as required by law
- Require the BA to use appropriate safeguards to prevent impermissible uses/disclosures
- Require the BA to report to the covered entity any breach of unsecured PHI
- Require the BA to ensure subcontractors agree to the same restrictions
- Require the BA to make PHI available for individual access (if the BA holds the designated record set)
- Require the BA to make PHI available for amendment
- Require the BA to make internal practices, books, and records available to HHS for investigation
- Require the BA to return or destroy PHI at termination of the contract (if feasible)
- Authorize termination of the BAA if the BA violates a material term

### 6.3 BAA with Cloud Providers

Cloud service providers that store, process, or transmit ePHI on behalf of a covered entity are business associates. Key considerations:
- Cloud provider must sign a BAA
- The BAA must address the cloud provider's specific services
- Data location, encryption responsibilities, and incident response must be specified
- Subcontractor disclosures (cloud provider's downstream vendors)

### 6.4 BAAs with Subcontractors

If Denials Doctor engages a subcontractor that will handle PHI (e.g., a data analytics provider, a cloud hosting service), Denials Doctor must:
1. Enter into a BAA with the subcontractor
2. Ensure the subcontractor agreement includes the same or equivalent restrictions as those in the Denials Doctor-client BAA
3. Monitor the subcontractor's compliance

### 6.5 BAAs with Clearinghouses

Healthcare clearinghouses (e.g., claim scrubbing, electronic transaction processing) are generally covered entities but may operate as business associates for certain functions. BAAs must clearly define the clearinghouse's role.

---

## 7. HIPAA Enforcement

### 7.1 OCR (Office for Civil Rights)

The HHS Office for Civil Rights (OCR) is responsible for enforcing HIPAA Privacy, Security, and Breach Notification Rules. OCR:
- Investigates complaints
- Conducts compliance reviews
- Performs audits (phase 2 audits began in 2016)
- Provides technical assistance and guidance
- Imposes civil monetary penalties

### 7.2 Penalty Tiers (as adjusted for inflation)

| Tier | Culpability | Minimum Penalty per Violation | Maximum Penalty per Violation | Annual Cap per Violation Category |
|------|-------------|-------------------------------|-------------------------------|-----------------------------------|
| Tier 1 | Did not know and would not have known by exercising reasonable diligence | $127 | $63,973 | $1,919,173 |
| Tier 2 | Reasonable cause (knew or should have known, but not willful neglect) | $1,280 | $63,973 | $1,919,173 |
| Tier 3 | Willful neglect -- corrected within 30 days | $12,794 | $63,973 | $1,919,173 |
| Tier 4 | Willful neglect -- not corrected within 30 days | $63,973 | $1,919,173 | $1,919,173 |

**Note:** Penalties are adjusted annually for inflation. Figures above reflect recent adjustments. Each day a violation continues may constitute a separate violation.

### 7.3 Criminal Penalties

In addition to civil penalties, HIPAA includes criminal penalties (enforced by DOJ):
- **Knowingly obtaining/disclosing PHI:** Up to $50,000 and 1 year imprisonment
- **Under false pretenses:** Up to $100,000 and 5 years imprisonment
- **With intent to sell, transfer, or use for personal gain:** Up to $250,000 and 10 years imprisonment

### 7.4 Resolution Agreements and Corrective Action Plans (CAPs)

OCR often resolves investigations through Resolution Agreements that include:
- Monetary settlement
- Corrective Action Plan (CAP) requiring specific remedial steps
- Independent monitor oversight
- Periodic reporting to OCR

---

## 8. State Privacy Laws

### 8.1 CCPA/CPRA (California Consumer Privacy Act / California Privacy Rights Act)

The CCPA (effective 2020), as amended by the CPRA (effective 2023), provides California residents with:
- Right to know what personal information is collected
- Right to delete personal information
- Right to opt out of sale of personal information
- Right to non-discrimination for exercising rights
- Private right of action for data breaches

**Interaction with HIPAA:** Medical information governed by HIPAA is generally exempt from CCPA when maintained by a covered entity or business associate for HIPAA-covered purposes. However, Denials Doctor must confirm applicability for non-HIPAA data processing.

### 8.2 Other State Privacy Laws

| State | Law | Effective | Key Provisions |
|-------|-----|-----------|----------------|
| Virginia | VCDPA | January 2023 | Consumer data rights, controller obligations |
| Colorado | CPA | July 2023 | Universal opt-out, data protection assessments |
| Connecticut | CTDPA | July 2023 | Similar to Virginia and Colorado |
| Utah | UCPA | December 2023 | More business-friendly approach |
| Texas | Texas Data Privacy and Security Act | July 2024 | Expanded biometric data protections |

### 8.3 State Health Privacy Laws

Several states have passed or enhanced health-specific privacy laws:
- **Washington My Health My Data Act:** Expansive definition of consumer health data, private right of action, geofencing prohibitions around healthcare facilities
- **Nevada:** Enhanced health data requirements
- **Connecticut:** Expanded health data provisions

### 8.4 Preemption

HIPAA **preempts** state laws that are contrary to HIPAA (less protective). However, state laws that are **more protective** of patient privacy than HIPAA are NOT preempted. This means:
- Covered entities must comply with both HIPAA and any stricter state laws
- Denials Doctor must know the states where its clients operate and any additional state requirements

---

## 9. HIPAA and AI

### 9.1 De-Identification Methods

De-identified health information is not PHI and is not subject to HIPAA Privacy Rule requirements. Two methods:

**Safe Harbor Method (45 CFR 164.514(b)):**
Remove all 18 identifiers:
1. Names
2. Geographic subdivisions smaller than a state (except initial 3 ZIP digits if population > 20,000)
3. All elements of dates (except year) directly related to an individual (birth date, admission date, discharge date, date of death, age over 89)
4. Telephone numbers
5. Fax numbers
6. Email addresses
7. Social Security Numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers and serial numbers, including license plate numbers
13. Device identifiers and serial numbers
14. Web Universal Resource Locators (URLs)
15. Internet Protocol (IP) addresses
16. Biometric identifiers, including finger and voice prints
17. Full-face photographic images and any comparable images
18. Any other unique identifying number, characteristic, or code

Plus: The covered entity must have no actual knowledge that the remaining information could be used alone or in combination to identify an individual.

**Expert Determination Method (45 CFR 164.514(b)(1)):**
A person with appropriate knowledge of and experience with generally accepted statistical and scientific principles and methods for rendering information not individually identifiable:
- Determines that the risk is very small that the information could be used by anticipated recipients to identify the individual
- Documents the methods and results of analysis

### 9.2 Limited Data Set (45 CFR 164.514(e))

A limited data set is PHI that excludes the following 16 direct identifiers (but may include dates and geographic information):
- All identifiers listed above (items 1-18), except dates and geographic information

A **Data Use Agreement** is required between the covered entity and the limited data set recipient.

### 9.3 Data Use Agreement

Required for limited data set disclosures:
- Establishes permitted uses and disclosures
- Identifies who may use or receive the data
- Prohibits re-identification of the data subjects
- Requires appropriate safeguards
- Requires reporting of any breach of unsecured data

### 9.4 AI-Specific Considerations for Denials Doctor

**Training Data:**
- If AI models are trained on PHI, the training data must be de-identified (safe harbor or expert determination)
- If training data contains PHI, a BAA is required between the developer/trainer and the covered entity
- Synthetic data generation is an alternative to using real PHI for training

**LLM Prompting with PHI:**
- Prompting a large language model (LLM) with PHI constitutes a disclosure
- A BAA must be in place with the LLM provider (e.g., OpenAI, Anthropic, Azure OpenAI)
- Not all LLM providers will sign BAAs; verify before use
- Denials Doctor must ensure its LLM provider (if any) signs a BAA

**AI Risk Management:**
- Re-identification risk: AI models can potentially re-identify de-identified data; expert determination must account for this
- Model inversion attacks: AI models trained on PHI may inadvertently memorize and reproduce PHI
- Data minimization: Only send the minimum PHI necessary for the specific AI task
- Audit trail: Maintain logs of all PHI sent to AI models and the outputs received

---

## 10. OCR HIPAA Right of Access Initiative

OCR has made enforcement of the Right of Access a priority. Since 2019, OCR has pursued numerous enforcement actions against covered entities that fail to provide patients timely access to their PHI.

### 10.1 Key Enforcement Actions

- Penalties range from $3,500 to $160,000+ for failure to provide access
- Typical violations: charging excessive fees, failing to provide access within 30 days, failing to provide records in requested format

### 10.2 Denials Doctor's Role

While Denials Doctor is not a covered entity, it may hold PHI in a "designated record set" on behalf of clients. The BAA should specify whether Denials Doctor must:
- Respond directly to patient access requests (if it controls the designated record set)
- Forward access requests to the covered entity
- Provide PHI to the covered entity for access fulfillment

---

## 11. Telehealth and HIPAA

### 11.1 Enforcement Discretion During PHE

During the COVID-19 Public Health Emergency (PHE), OCR exercised enforcement discretion, allowing telehealth providers to use non-compliant platforms (e.g., FaceTime, Zoom) without penalty. This discretion has largely ended post-PHE (May 11, 2023).

### 11.2 Current Telehealth Requirements

- Telehealth platforms must be HIPAA-compliant
- A BAA must be in place with the telehealth vendor
- End-to-end encryption is expected
- Patient consent and notice requirements apply

---

## 12. Agent Q&A Pairs

**Q: What is the primary legal basis for Denials Doctor to process patient health information?**

**A:** Denials Doctor processes PHI under the "payment" and "healthcare operations" provisions of the HIPAA Privacy Rule (45 CFR 164.502). Payment includes billing, claims management, and collections. Healthcare operations includes quality assessment, medical review, and business planning. As a business associate, Denials Doctor may only use PHI as permitted by its BAA with the covered entity.

**Q: What constitutes a HIPAA breach, and what is the notification timeline?**

**A:** A breach is the acquisition, access, use, or disclosure of PHI not permitted by the Privacy Rule that compromises the security or privacy of the PHI. For breaches affecting 500+ individuals, notification to affected individuals and HHS must occur within 60 calendar days of discovery, plus media notification. For breaches affecting fewer than 500 individuals, individual notification within 60 days and HHS notification within 60 days after the end of the calendar year.

**Q: What are the 18 HIPAA identifiers that must be removed for safe harbor de-identification?**

**A:** The 18 identifiers are: (1) names, (2) geographic subdivisions smaller than a state, (3) dates (except year), (4) telephone numbers, (5) fax numbers, (6) email addresses, (7) SSNs, (8) medical record numbers, (9) health plan beneficiary numbers, (10) account numbers, (11) certificate/license numbers, (12) vehicle identifiers, (13) device identifiers/serial numbers, (14) web URLs, (15) IP addresses, (16) biometric identifiers, (17) full-face photographs, (18) any other unique identifying number, characteristic, or code. Plus no actual knowledge that the data could re-identify an individual.

**Q: What is the difference between a "required" and "addressable" implementation specification under the HIPAA Security Rule?**

**A:** "Required" means the specification must be implemented as stated with no discretion. "Addressable" does not mean optional; it means the entity must assess whether the specification is reasonable and appropriate. If it is, implement it. If not, document why and implement an equivalent alternative measure if reasonable and appropriate. The determination must be documented.

**Q: Does Denials Doctor need a BAA with its cloud provider?**

**A:** Yes. Any cloud provider that stores, processes, or transmits ePHI on behalf of Denials Doctor is a subcontractor business associate. A BAA must be in place before any ePHI is shared with the cloud provider. The BAA must include all required provisions under 45 CFR 164.504(e) and must flow down the same restrictions that apply to Denials Doctor.

**Q: What is the HITECH Act's significance for business associates?**

**A:** The HITECH Act made business associates directly liable for HIPAA Privacy and Security Rule compliance. Before HITECH, business associates were only indirectly liable through contractual BAA obligations. After HITECH, business associates face direct civil monetary penalties, must comply with the Security Rule, and must comply with the Breach Notification Rule.

**Q: What is the four-factor test for breach risk assessment?**

**A:** The four factors are: (1) the nature and extent of the PHI involved (what types of identifiers were exposed), (2) the unauthorized person who used the PHI or to whom the disclosure was made (trustworthiness, obligations to protect), (3) whether the PHI was actually acquired or viewed, and (4) the extent to which the risk to the PHI has been mitigated. If there is a low probability of compromise, no notification is required. The assessment must be documented.

**Q: What are the four penalty tiers under HIPAA?**

**A:** Tier 1: did not know and would not have known (min $127/violation). Tier 2: reasonable cause (min $1,280/violation). Tier 3: willful neglect, corrected within 30 days (min $12,794/violation). Tier 4: willful neglect, not corrected (min $63,973/violation). Annual cap per violation category is approximately $1.9M. Penalties are adjusted annually for inflation.

**Q: What is the minimum necessary standard, and does it apply to treatment disclosures?**

**A:** The minimum necessary standard requires reasonable efforts to limit PHI to the minimum necessary to accomplish the intended purpose. However, it does NOT apply to: disclosures to a healthcare provider for treatment, disclosures to the individual, disclosures authorized by the individual, disclosures required by law, or disclosures to HHS for enforcement.

**Q: When is a BAA required between Denials Doctor and its clients?**

**A:** A BAA is required whenever a covered entity (healthcare provider) discloses PHI to Denials Doctor for the performance of a function or activity regulated by HIPAA (claims processing, denial management, revenue cycle analytics). The BAA must be in place BEFORE any PHI is shared. It must describe permitted uses, prohibit impermissible uses, require safeguards, and include breach notification and subcontractor requirements.

**Q: Can Denials Doctor use client PHI to train its AI models?**

**A:** Only if the PHI has been de-identified using either the safe harbor method (removing all 18 identifiers) or expert determination method. If PHI is used for training, a BAA with the training partner is required, and the training must comply with the minimum necessary standard. Synthetic data generation is recommended as an alternative. The use must also be permitted under the BAA with the client.

**Q: Does the CCPA apply to Denials Doctor's processing of medical information?**

**A:** Medical information governed by HIPAA and maintained by a covered entity or business associate is generally exempt from the CCPA. However, Denials Doctor should confirm applicability for any non-HIPAA data processing activities and for California residents' data that falls outside the HIPAA exemption. State-specific legal advice is recommended.

**Q: What is OCR's Right of Access Initiative?**

**A:** Starting in 2019, OCR made enforcement of the HIPAA Right of Access a priority. OCR has imposed significant penalties (ranging from $3,500 to $160,000+) on covered entities that fail to provide patients timely access to their PHI, charge excessive fees, or fail to respond within 30 days. While Denials Doctor is not a covered entity, it must support its clients' access obligations under the BAA.

**Q: What are the criminal penalties for HIPAA violations?**

**A:** Criminal penalties (enforced by DOJ) include: knowingly obtaining/disclosing PHI (up to $50,000 and 1 year), under false pretenses (up to $100,000 and 5 years), and with intent to sell/transfer/use for personal gain (up to $250,000 and 10 years). Criminal penalties apply to both covered entities and business associates.

**Q: What must be included in a breach notification to affected individuals?**

**A:** The notification must include: (1) brief description of the breach (date, discovery date), (2) types of PHI involved, (3) steps individuals should take to protect themselves, (4) brief description of investigation and mitigation, and (5) contact information (toll-free number, email, website). The notification must be written in plain language.

**Q: What is a limited data set, and what is required to use one?**

**A:** A limited data set is PHI that excludes all 18 identifiers EXCEPT dates and geographic information. A Data Use Agreement is required between the covered entity and the recipient, specifying permitted uses, identifying authorized users, prohibiting re-identification, requiring safeguards, and requiring breach reporting.

**Q: What happens if Denials Doctor discovers a breach?**

**A:** Denials Doctor must notify the covered entity (client) without unreasonable delay and no later than 60 calendar days from discovery. The notification must identify the affected individuals and provide all available information the covered entity needs to fulfill its notification obligations. Denials Doctor must also maintain documentation of the breach and its response.

**Q: What are the requirements for a Notice of Privacy Practices (NPP)?**

**A:** Covered entities must provide an NPP describing how PHI may be used/disclosed, the entity's duties to protect PHI, individual rights, complaint contact information, and breach notification obligation. The NPP must be provided at first service delivery and posted prominently. Business associates are not required to have their own NPP but must comply with the covered entity's NPP.

**Q: What is the difference between the Privacy Rule and the Security Rule?**

**A:** The Privacy Rule (45 CFR 164.500-534) governs how PHI can be used and disclosed in any form (oral, paper, electronic) and establishes patient rights. The Security Rule (45 CFR 164.300-318) specifically governs electronic PHI (ePHI) and requires administrative, physical, and technical safeguards to protect confidentiality, integrity, and availability.

**Q: Can Denials Doctor use a subcontractor that handles PHI?**

**A:** Yes, but Denials Doctor must: (1) Enter into a BAA with the subcontractor that includes the same or equivalent restrictions as the Denials Doctor-client BAA, (2) Ensure the subcontractor agrees to appropriate safeguards, breach notification, and compliance monitoring, and (3) Reasonably monitor the subcontractor's performance. Denials Doctor remains liable for subcontractor violations.

**Q: What is OCR's audit protocol?**

**A:** OCR conducts periodic audits of covered entities and business associates to assess HIPAA compliance. The audits use a comprehensive protocol covering Privacy Rule, Security Rule, and Breach Notification Rule requirements. Phase 2 audits began in 2016 (pilot), with full implementation ongoing. Audits may be for-cause (based on a complaint) or for-compliance (random selection).

**Q: Does HIPAA preempt California's stricter privacy laws?**

**A:** No. HIPAA preempts state laws that are less protective of patient privacy. However, state laws that are MORE protective are NOT preempted. California's medical privacy laws, the Washington My Health My Data Act, and other stricter state laws remain in effect. Covered entities and business associates must comply with both HIPAA and any stricter state requirements.

**Q: What are the contingency plan requirements under the Security Rule?**

**A:** The Security Rule's contingency plan (45 CFR 164.308(a)(7)) requires: (1) Data backup plan (required) -- create retrievable exact copies of ePHI, (2) Disaster recovery plan (required) -- restore any loss of ePHI, (3) Emergency mode operation plan (required) -- continue critical business processes during emergency, (4) Testing and revision (addressable) -- periodically test, and (5) Applications and data criticality analysis (addressable) -- assess criticality of specific applications.

**Q: How should Denials Doctor handle patient access requests?**

**A:** The BAA should specify the process. Generally: if Denials Doctor maintains PHI in a designated record set on behalf of the covered entity, it must: (1) Make the PHI available to the covered entity within a reasonable timeframe to allow the covered entity to meet the 30-day access requirement, or (2) Respond directly to the access request if specified in the BAA. Denials Doctor should not respond directly to patient requests unless explicitly authorized in the BAA.

**Q: What are the encryption requirements under the Security Rule?**

**A:** Encryption of ePHI is an addressable implementation specification under both Access Control (164.312(a)(2)(iv)) and Transmission Security (164.312(e)(2)(ii)). While addressable, encryption is considered a standard safeguard. Denials Doctor should implement AES-256 for data at rest and TLS 1.2+ for data in transit. If encryption is not implemented, the reason must be documented and equivalent alternative measures must be in place.

**Q: What is a Resolution Agreement and Corrective Action Plan?**

**A:** A Resolution Agreement is a settlement between OCR and a covered entity or business associate to resolve a HIPAA violation investigation. It typically includes a monetary payment and a Corrective Action Plan (CAP) requiring specific remedial steps such as: revising policies, conducting workforce training, implementing new technical safeguards, performing risk assessments, and submitting to independent monitoring and periodic reporting to OCR.

**Q: What steps should Denials Doctor take if it receives a subpoena or court order for PHI?**

**A:** Denials Doctor must: (1) Immediately notify the covered entity (client) as required by the BAA, (2) Verify the subpoena is valid and properly served, (3) Determine whether the covered entity will object to the disclosure, (4) Ensure disclosure is limited to the minimum necessary, and (5) Document the disclosure for accounting of disclosures purposes. Denials Doctor should not disclose PHI in response to a subpoena without first notifying the covered entity unless otherwise required by law.

**Q: What are the specific HIPAA obligations for Denials Doctor's workforce training?**

**A:** Under the Security Rule (164.308(a)(5)), Denials Doctor must provide security awareness and training for all workforce members, including: (1) periodic security reminders (addressable), (2) protection from malicious software (addressable), (3) log-in monitoring (addressable), and (4) password management (addressable). Training should be provided at hire, annually, and when policies change. Documentation of training must be maintained.

**Q: What is a designated record set, and why does it matter for Denials Doctor?**

**A:** A designated record set is a group of records maintained by or for a covered entity that includes: (1) medical records and billing records about an individual, (2) enrollment, payment, claims adjudication, and case or medical management record systems, and (3) records used to make decisions about individuals. Claims data and denial analytics processed by Denials Doctor may constitute part of the client's designated record set, triggering patient access and amendment obligations.

**Q: How does the HIPAA Omnibus Rule (2013) affect Denials Doctor?**

**A:** The 2013 Omnibus Rule: (1) Made business associates directly liable for HIPAA violations (implementing HITECH), (2) Expanded the definition of business associate to include subcontractors, (3) Required BAAs with subcontractors, (4) Modified the breach notification standard (from "significant risk of harm" to "low probability of compromise" four-factor test), (5) Expanded individuals' rights to request electronic copies of PHI, and (6) Prohibited the sale of PHI without authorization.

---

## 13. References

- 45 CFR Part 160 (General Administrative Requirements)
- 45 CFR Part 164, Subpart E (Privacy Rule)
- 45 CFR Part 164, Subpart C (Security Rule)
- 45 CFR Part 164, Subpart D (Breach Notification)
- HITECH Act (ARRA Title XIII, Division A, and Title IV)
- 2013 HIPAA Omnibus Final Rule (78 Fed. Reg. 5566)
- OCR HIPAA Guidance: https://www.hhs.gov/hipaa/for-professionals/index.html
- NIST Special Publication 800-66 (HIPAA Security Rule Implementation)
- HHS Breach Notification Portal: https://ocrportal.hhs.gov/