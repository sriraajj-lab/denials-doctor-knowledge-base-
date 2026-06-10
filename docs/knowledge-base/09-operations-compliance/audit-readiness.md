# Audit Readiness for Denials Doctor RCM AI

## 1. Overview

Healthcare providers face a complex web of government and commercial audits, each with distinct requirements, timelines, and consequences. Denials Doctor must understand these audit programs to help clients prepare responses, manage documentation, and minimize financial risk. This document covers RAC audits, CERT audits, ZPIC/UPIC audits, TPE, ADR processes, Medicare appeals, internal audit preparation, fraud and abuse laws, and self-audit best practices.

---

## 2. RAC (Recovery Audit Contractor) Audits

### 2.1 Program Overview

The Medicare Recovery Audit Program, mandated by the Medicare Prescription Drug, Improvement, and Modernization Act of 2003 (MMA), is designed to identify and correct improper payments in the Medicare Fee-for-Service (FFS) program. RACs identify overpayments and underpayments on a contingency fee basis.

**Key Facts:**
- **Authorizing Statute:** Section 306 of the Medicare Prescription Drug, Improvement, and Modernization Act of 2003 (MMA)
- **Permanent Authority:** Section 302 of the Tax Relief and Health Care Act of 2006
- **CMS Management:** CMS oversees RACs through the Medicare Fee-for-Service Recovery Audit Program, now part of the larger Unified Program Integrity Contractor (UPIC) program since 2023

### 2.2 RAC Regions and Contractors

| Region | States | RAC Contractor | Transition |
|--------|--------|----------------|------------|
| Region 1 | CA, NV, AZ, HI, Pacific Territories | Performant Recovery | Transitioned to UPIC: Performant (Region 1 UPIC) |
| Region 2 | Midwest (IL, IN, KY, MN, MI, OH, WI, etc.) | Cotiviti | Transitioned to UPIC: Cotiviti (Region 2-5 UPIC) |
| Region 3 | South (TX, LA, AR, OK, etc.) | Cotiviti | Transitioned to UPIC: Cotiviti |
| Region 4 | Northeast (NY, NJ, PA, CT, MA, etc.) | Cotiviti | Transitioned to UPIC: Cotiviti |
| Region 5 | Southeast (FL, GA, AL, SC, NC, etc.) | Cotiviti | Transitioned to UPIC: Cotiviti |

**Important Transition:** Since 2023, CMS has been consolidating RAC, CERT, and MEDIC functions into Unified Program Integrity Contractors (UPICs). The traditional RAC program continues but operates under the broader UPIC structure. Denials Doctor should track UPIC contractor assignments in each region.

### 2.3 RAC Contingency Fees

RACs are paid contingency fees based on recoveries:
- **Overpayments:** 9-12% of the improper payment recovered
- **Underpayments:** Same percentage, paid from Medicare Trust Fund
- **No cap** on contingency fees per contractor

### 2.4 RAC Claim Lookback Period

- **Standard lookback:** 3 years from the date of service
- **Exceptions:** If fraud is suspected or if the provider failed to submit timely appeals
- RACs cannot look back at claims prior to the lookback date

### 2.5 RAC Focus Areas

RACs use data analytics to identify claims with high improper payment risk:

**Inpatient Short Stays (Observation vs. Inpatient):**
- CMS's "Two-Midnight Rule" (42 CFR 412.3): Inpatient admission is generally appropriate when the physician expects the patient to require a stay spanning at least two midnights
- RACs consistently audit inpatient claims where the patient was discharged before the second midnight
- If the admission is denied, it may be recategorized as outpatient observation, resulting in significant repayment (often $3,000-$10,000 per claim)

**Medical Necessity:**
- Whether services were reasonable and necessary for the diagnosis or treatment of the patient's condition (Social Security Act Section 1862(a)(1)(A))
- RACs audit for: procedures not supported by diagnosis codes, services exceeding frequency limits, and treatments not meeting standard of care

**DRG Validation:**
- RAC reviews medical records to verify that the assigned MS-DRG accurately reflects the documented diagnoses and procedures
- Targets include: DRG creep (upcoding), incorrect principal diagnosis, complication or comorbidity (CC)/major CC (MCC) validation

**Coding Errors:**
- Incorrect procedure code assignment
- Unbundling of comprehensive procedures
- Incorrect modifiers (especially modifier 25, 59)
- Evaluation and Management (E/M) coding errors

**Incorrect MS-DRG Assignment:**
- Wrong DRG based on documentation
- Missing or undocumented MCC/CC
- Principal diagnosis not meeting definition

### 2.6 RAC Audit Process

1. **Data Analysis:** RAC analyzes claims data to identify potential improper payments
2. **ADR (Additional Documentation Request):** RAC sends request for medical records to the provider
3. **Document Review:** RAC reviews submitted documentation
4. **Determination:** RAC makes a determination of overpayment, underpayment, or no change
5. **Appeals:** Provider may appeal the determination through the 5-level Medicare appeals process
6. **Recoupment:** If determination stands, CMS recoups the amount, plus interest

---

## 3. CERT (Comprehensive Error Rate Testing) Audits

### 3.1 Program Overview

The CERT program measures the Medicare FFS improper payment rate. CMS contracts with CERT contractors to randomly sample claims and determine whether payments were proper.

**Key Facts:**
- **Purpose:** To estimate the Medicare FFS improper payment rate as required by the Payment Integrity Information Act of 2019
- **Method:** Statistical random sampling of Medicare Part A and Part B claims
- **Outcome:** Annual Medicare FFS improper payment rate report to Congress

### 3.2 CERT Process

1. **Random Selection:** CERT contractor randomly selects claims for review (approximately 40,000 claims annually)
2. **Medical Record Request:** CERT sends ADR to the provider requesting medical records
3. **Document Review:** Physician reviewers evaluate whether services were medically necessary and correctly coded
4. **Determination:** Certifies claim as proper or improper (overpayment or underpayment)
5. **Extrapolation:** Results from the sample are extrapolated to estimate the overall improper payment rate

### 3.3 CERT Categories of Improper Payments

- **Insufficient Documentation:** Provider failed to submit requested documentation (50%+ of improper payments)
- **Medically Unnecessary:** Services not reasonable and necessary
- **Incorrect Coding:** Wrong procedure or diagnosis code
- **No Documentation:** Provider submitted no records

**Key Takeaway:** The single most important factor in avoiding CERT improper payment determinations is responding timely and completely to ADRs.

### 3.4 Provider Impact

- Individual CERT results are not used to recoup payments from the specific claim audited (the audit determines the error rate, not a recoupment)
- However, CMS may take administrative actions against providers with repeated failures
- High error rates can trigger targeted audits or TPE

---

## 4. ZPIC / UPIC (Unified Program Integrity Contractor) Audits

### 4.1 Overview

UPICs (formerly ZPICs -- Zone Program Integrity Contractors and PSCs -- Program Safeguard Contractors) are CMS contractors that investigate fraud, waste, and abuse in Medicare and Medicaid.

**Key Facts:**
- **Purpose:** Identify fraud, investigate suspicious billing patterns, and refer cases for prosecution or administrative action
- **Authority:** Section 1936 of the Social Security Act
- **Replaced ZPICs/PSCs:** UPICs consolidated the Medicare integrity contractor functions

### 4.2 UPIC vs. RAC Differences

| Feature | UPIC | RAC |
|---------|------|-----|
| Focus | Fraud investigation | Improper payments (errors) |
| Referral threshold | Higher (fraud indicators) | Lower (statistical likelihood) |
| Authority | Site visits, interviews, payment suspensions | Document review only |
| Scope | Medicare, Medicaid, dual-eligible | Medicare FFS only |
| Extrapolation | Yes, can extrapolate overpayments | Yes, can extrapolate |
| Civil/Criminal | Can refer for prosecution | No criminal referral authority |

### 4.3 UPIC Audit Process

1. **Data Mining:** UPIC uses sophisticated analytics to identify billing anomalies
2. **Document Request (Medical Records):** Initial ADR for specific claims
3. **Site Visit (Optional):** Unannounced or advance-notice site visit to inspect operations
4. **Interviews:** UPIC may interview providers, staff, and patients
5. **Payment Suspension:** UPIC can request CMS to suspend all payments to the provider
6. **Extrapolated Overpayment:** UPIC may use statistical sampling to extrapolate overpayment across the entire claims universe
7. **Referral:** Cases with fraud indicators are referred to OIG or DOJ

### 4.4 UPIC Red Flags (Triggers for Audit)

- Billing patterns significantly outside the norm for the specialty
- High volume of specific procedure codes
- Same-day billing by multiple providers
- Billing for services outside the provider's specialty
- Unusual place of service codes
- High number of denied or appealed claims
- Abrupt changes in billing patterns
- Billing for non-covered services
- Provider exclusions or sanctions reported by OIG

### 4.5 Responding to a UPIC Audit

1. **Immediate Legal Counsel:** Contact healthcare counsel immediately (UPIC audits carry fraud risk)
2. **Document Assembly:** Assemble all requested records within the deadline (typically 30-45 days)
3. **Documentation Integrity:** Submit complete, legible, authenticated medical records
4. **Cooperation:** Respond professionally without waiving legal rights
5. **Appeal Preparation:** Prepare for appeal if the determination is adverse

---

## 5. Targeted Probe and Educate (TPE)

### 5.1 Program Overview

TPE is CMS's medical review program designed to reduce claim denials and improper payments through education rather than purely punitive measures. Administered by Medicare Administrative Contractors (MACs) and Supplemental Medical Review Contractor (SMRC).

**Key Facts:**
- **Purpose:** Reduce claim denials through targeted education
- **Target:** Providers with high claim denial rates, unusual billing patterns, or new providers
- **Process:** Probe, education, re-probe, potential extrapolation

### 5.2 TPE Process

**Round 1 (Probe):**
- MAC selects 20-40 claims for review
- Provider submits medical records within 30-45 days
- MAC reviews and provides specific education on errors found
- Errors are categorized: documentation, coding, medical necessity, etc.

**Round 2 (Re-Probe):**
- If error rate exceeds threshold (typically 20-30%), another 20-40 claims are selected
- MAC reviews and provides focused education
- Goal: demonstrate improvement

**Round 3 (Final Probe):**
- If error rate remains high, a final round of 20-40 claims
- Education is more intensive
- If still not improved, case may proceed to extrapolation

**Extrapolation:**
- If all three rounds show high error rates, the MAC may extrapolate the error rate to the entire claims universe
- The provider must repay the extrapolated overpayment (which can be substantial)
- Providers can appeal extrapolation

### 5.3 TPE Tips for Providers

- Respond to all ADRs timely (within deadline)
- Prepare for TPE when selected; assign a dedicated team member
- Address all educational feedback from each round
- Consider a temporary reduction in billing in the targeted area until performance improves
- If extrapolation is threatened, consider a voluntary repayment or corrective action plan

---

## 6. Additional Documentation Request (ADR) Process

### 6.1 What is an ADR?

An Additional Documentation Request is a formal request from a Medicare contractor (MAC, RAC, UPIC, CERT, TPE reviewer) for medical records and supporting documentation to verify the medical necessity and coding accuracy of a claim.

### 6.2 ADR Response Timeline

| Auditor Type | Standard Response Time | Extension Available? |
|-------------|------------------------|---------------------|
| MAC / TPE | 30 days from request date | Rarely |
| RAC | 45 calendar days | Yes, one 15-day extension |
| CERT | 30 calendar days | Yes, one 15-day extension |
| UPIC | 30-45 calendar days | Case-by-case |
| Private payer audit | 30-45 days (contract-dependent) | Per contract terms |

**Critical:** Failure to respond within the deadline results in automatic claim denial. There is no grace period. The claim is denied for "no documentation."

### 6.3 ADR Response Process

1. **Log and Track:** Assign a tracking number and deadline in a system of record
2. **Identify the Claim:** Match the ADR to the specific claim in the practice management system
3. **Assemble Medical Records:** Gather all relevant records:
   - History and physical (H&P)
   - Progress notes
   - Operative/procedure reports
   - Lab and imaging reports
   - Physician orders
   - Nursing notes
   - Admission orders
   - Discharge summary
   - (For RAC DRG review, the complete medical record)
4. **Review for Completeness:** Ensure records are legible, authenticated (signed and dated), and complete
5. **Submit Within Deadline:** Send via fax, secure portal, or mail per the reviewer's instructions
6. **Confirm Receipt:** Obtain confirmation of receipt and document in the tracking system

### 6.4 Common ADR Mistakes

- **Late submission:** Most common cause of denial
- **Incomplete records:** Missing pages, illegible copies
- **Unauthenticated records:** Missing signatures or dates
- **Wrong records submitted:** Sending records for the wrong encounter or patient
- **Fax transmission errors:** Pages out of order, missing, or illegible
- **No cover sheet:** Lack of identification information on submissions

---

## 7. Appeals of Audit Findings

### 7.1 Standard 5-Level Medicare Appeal Process

| Level | Body | Description | Timeframe to Appeal | Amount in Controversy |
|-------|------|-------------|--------------------|-----------------------|
| Level 1 | Redetermination | First-level appeal by the MAC | 120 days from claim determination | No minimum |
| Level 2 | Reconsideration | Second-level appeal by a Qualified Independent Contractor (QIC) | 180 days from Level 1 decision | No minimum |
| Level 3 | Administrative Law Judge (ALJ) Hearing | Hearing before an HHS ALJ | 60 days from Level 2 decision | $180 (2024 threshold) |
| Level 4 | Medicare Appeals Council (MAC) | HHS Departmental Appeals Board review | 60 days from Level 3 decision | No minimum |
| Level 5 | Federal District Court | Judicial review | 60 days from Level 4 decision | $1,840 (2024 threshold) |

### 7.2 Appeal Strategies

**Level 1 (Redetermination):**
- Fastest track; most appeals should start here
- Submit complete medical records with a concise written argument
- Focus on documentation that supports medical necessity and correct coding
- MAC must issue a decision within 60 days (extended to 90 days for Medicare Part B)

**Level 2 (Reconsideration):**
- QIC conducts de novo review (independent, not deferential to Level 1)
- Submit all documentation plus new evidence if available
- QIC must issue a decision within 60 days
- If QIC does not decide within 60 days, the provider may escalate to Level 3

**Level 3 (ALJ Hearing):**
- Most time-consuming but highest success rate (historically 50-70% of appeals are granted at this level)
- May be in person, by video, or by telephone
- Submit pre-hearing brief and evidence
- Expert witness testimony may be presented
- Long wait times (historically 2-4 years due to backlog, though CMS has reduced this)

**Level 4 (Medicare Appeals Council):**
- Reviews ALJ decision for errors of law or fact
- Limited new evidence
- Written decision (no hearing)

**Level 5 (Federal Court):**
- Most expensive and time-consuming
- Must have minimum Amount in Controversy ($1,840 in 2024)
- File complaint in U.S. District Court

### 7.3 Appeals Timelines

- Each level has a strict deadline; missed deadlines result in dismissal
- If a deadline is missed, the provider may request an appeal for "good cause" shown
- Appeals deadlines are counted from the date of the determination letter (not the date of claim)
- Denials Doctor should integrate appeal deadline tracking into its workflows

### 7.4 Private Payer Appeals

Commercial insurance appeals follow contract-specific processes:
- Typically 2-3 internal appeal levels
- External independent review (if internal appeals are exhausted)
- State-mandated external review for certain denials
- ERISA plans have specific appeal requirements (timing, content, right to review)
- No uniform process -- Denials Doctor must know each payer's requirements

---

## 8. Internal Audit Preparation

### 8.1 Documentation Integrity Check

Before submitting any claim or responding to an audit, verify:
- **All records are legible:** Illegible documentation may be treated as no documentation
- **All records are authenticated:** Signed and dated by the treating provider
- **All records are complete:** No gaps in the clinical story
- **Records support the billed codes:** Clinical documentation supports medical necessity
- **Timeliness:** Records are created within appropriate timeframes (e.g., H&P within 24 hours of admission, operative report immediately or within 24 hours, discharge summary within 30 days)

### 8.2 Coding Compliance Review

Verify:
- **Diagnosis codes match documentation:** ICD-10-CM codes must accurately reflect documented diagnoses
- **Procedure codes match documentation:** CPT/HCPCS codes must be supported by the procedure note
- **Modifiers are correctly applied:** Modifier 25 (significant, separately identifiable E/M), modifier 59 (distinct procedural service), modifier 76 (repeat procedure by same physician), etc.
- **DRG assignment is accurate:** Principal diagnosis definition, CC/MCC capture
- **Site of service is correct:** Facility vs. non-facility place of service codes
- **Units of service are appropriate:** No unbundling, correct units per RVU calculation

### 8.3 Medical Records Complete Before Submission

A complete medical record for a claim should include:
- Patient identification on every page
- Date of service on every page
- Legible entries
- Appropriate signatures with credentials
- Clinical data supporting all billed services
- Chief complaint or reason for encounter
- History of present illness
- Review of systems (if applicable)
- Past medical, family, social history (if applicable)
- Physical examination
- Assessment/medical decision-making
- Plan of care
- Time spent (if time-based coding)

---

## 9. Upcoding vs. Downcoding Risk

### 9.1 Upcoding

**Definition:** Billing a higher-level service than supported by the medical record.

**Risks:**
- Fraud and Abuse liability (False Claims Act)
- RAC/UPIC audit target
- Overpayment recoupment with interest
- Exclusion from Medicare/Medicaid
- Civil monetary penalties

**Common Upcoding Scenarios:**
- E/M leveling: Billing Level 4 or 5 E/M when documentation supports Level 2 or 3
- DRG upcoding: Adding CC or MCC not supported by documentation
- Modifier misuse: Using modifier 25 to bill an E/M with a procedure when not separately identifiable
- unbundling: Billing individual components of a comprehensive procedure

### 9.2 Downcoding

**Definition:** Billing a lower-level service than the documentation supports.

**Risks:**
- Lost revenue (underpayment)
- Underpayment (if payer would have paid more)
- Potential compliance concern if patterns suggest systematic undercoding

**Common Downcoding Scenarios:**
- Physician under-documentation (billing based on documented level, not actual services)
- Overly conservative coding practices
- Lack of awareness of new or revised coding guidelines

### 9.3 Best Practice

- Audit both upcoding and downcoding in internal reviews
- Encourage complete and accurate documentation
- Use a consistent, evidence-based coding approach
- Educate providers on documentation requirements for each billed code

---

## 10. Self-Audit Best Practices

### 10.1 Purpose

Proactive self-audits allow providers to identify and correct issues before external auditors find them. Self-audits demonstrate good faith compliance, which is a mitigating factor in False Claims Act cases.

### 10.2 Self-Audit Program Design

**Frequency:**
- Quarterly random sample (minimum)
- Monthly for high-risk areas
- Targeted audits based on risk assessment

**Sample Size:**
- 10-20 claims per provider per review cycle
- Larger samples for providers with known issues or new services
- Statistical sampling (e.g., 95% confidence level, 5% margin) for overpayment estimation

**Scope:**
- Coding accuracy (E/M leveling, CPT/HCPCS codes, ICD-10-CM codes, modifiers)
- Medical necessity documentation
- DRG validation (inpatient)
- Site of service accuracy
- Compliance with payer-specific requirements

### 10.3 Self-Audit Methodology

1. **Select the Sample:** Random selection, focused on specific service types or providers
2. **Obtain Medical Records:** Pull records corresponding to the selected claims
3. **Independent Review:** Coding review by an auditor who did not perform the original coding (independent auditor)
4. **Score Each Claim:**
   - Appropriate (compliant)
   - Minor error (documentation deficiency, no payment impact)
   - Major error (incorrect code, payment impact)
   - Critical error (no medical necessity, fraud concern)
5. **Calculate Error Rate:** Percentage of claims with significant errors
6. **Identify Patterns:** Common errors, provider-specific issues, payer-specific trends
7. **Report Findings:** Present to compliance committee or leadership
8. **Develop Corrective Action Plan:** Training, policy updates, workflow changes
9. **Re-Audit:** Verify that corrective actions are effective

### 10.4 Self-Audit Documentation

Maintain records of:
- Audit plan and methodology
- Selection criteria and sample
- Review findings (each claim scored)
- Aggregate error rates and trends
- Corrective actions implemented
- Effectiveness of corrective actions
- Communication with providers and leadership

### 10.5 Self-Disclosure

If self-audit reveals significant overpayments:
- **Repayment:** Refund overpayments within 60 days of identification (Affordable Care Act 60-day repayment rule, 42 U.S.C. 1320a-7k(d))
- **Self-Disclosure Options:**
  - OIG Self-Disclosure Protocol
  - CMS Self-Referral Disclosure Protocol (Stark Law)
  - DOJ voluntary disclosure (False Claims Act)
- **Legal Counsel:** Consult healthcare counsel before self-disclosure

---

## 11. OIG Work Plan

### 11.1 Overview

The HHS Office of Inspector General (OIG) annually publishes a Work Plan that identifies areas of focus for audits, evaluations, and investigations in the coming year. The Work Plan signals areas of heightened scrutiny.

### 11.2 Typical OIG Work Plan Focus Areas

- Telehealth services (post-PHE)
- Home health services
- Durable medical equipment (DME)
- Part B drugs
- Skilled nursing facility (SNF) services
- Inpatient psychiatric facility services
- Outpatient therapy services
- Hospice services
- Evaluation and Management (E/M) services
- Medicare Advantage (Part C) risk adjustment
- Medicaid managed care
- Opioid prescribing and monitoring
- COVID-19-related fraud

### 11.3 Using the OIG Work Plan

- Review the annual Work Plan and identify applicable areas
- Focus internal audit resources on identified risk areas
- Develop preventive measures for services likely to be targeted
- Monitor for enforcement actions and settlements in identified areas
- Track ongoing OIG audits and their outcomes

### 11.4 OIG Exclusion List

The OIG maintains a list of individuals and entities excluded from participating in federal healthcare programs (Medicare, Medicaid, all federal healthcare programs). Providers must:
- Screen employees and contractors monthly against the OIG exclusion list
- Exclude payments to excluded individuals
- Report any excluded individuals discovered in the organization

---

## 12. Fraud and Abuse Laws

### 12.1 False Claims Act (31 U.S.C. Sections 3729-3733)

The False Claims Act (FCA) is the government's primary civil enforcement tool against healthcare fraud.

**Key Provisions:**
- **Liability:** Any person who knowingly submits, or causes another to submit, a false or fraudulent claim to the federal government is liable
- **"Knowing" Defined:** Actual knowledge, deliberate ignorance, or reckless disregard -- specific intent to defraud is NOT required
- **Per Claim Penalty:** $11,803 to $23,607 per claim (adjusted periodically for inflation)
- **Treble Damages:** Three times the amount of damages sustained by the government
- **Qui Tam (Whistleblower):** Private individuals (relators) may file FCA lawsuits on behalf of the government and receive 15-30% of the recovery

**Healthcare FCA Examples:**
- Upcoding (billing a higher-level service than provided)
- Billing for medically unnecessary services
- Unbundling (billing components separately when a comprehensive code exists)
- Billing for services not provided
- Billing for non-covered services
- False certification of compliance
- Violation of the Anti-Kickback Statute or Stark Law (creating an FCA violation through a "tainted" claim)

**Mitigating Factors:**
- Voluntary disclosure
- Cooperation with government investigation
- Corrective action implementation
- Effective compliance program

### 12.2 Stark Law (Physician Self-Referral Law) (42 U.S.C. Section 1395nn)

**General Prohibition:**
A physician may not refer Medicare patients to an entity for "designated health services" (DHS) if the physician (or an immediate family member) has a financial relationship with the entity, unless an exception applies.

**Designated Health Services (DHS):**
- Clinical laboratory services
- Physical therapy, occupational therapy, and speech-language pathology
- Radiology and imaging services
- Radiation therapy services and supplies
- Durable medical equipment (DME)
- Parenteral and enteral nutrients, equipment, and supplies
- Prosthetics, orthotics, and prosthetic devices
- Home health services
- Outpatient prescription drugs
- Inpatient and outpatient hospital services

**Financial Relationship Includes:**
- Ownership or investment interest (direct or indirect)
- Compensation arrangement (direct or indirect)

**Strict Liability:** No intent requirement -- even a technical, inadvertent violation creates liability

**Key Exceptions:**
- **In-office Ancillary Services:** Services provided personally by the referring physician or under supervision in the same office
- **Group Practice:** Services provided by a member of the group practice
- **Fair Market Value:** Compensation arrangements that are at fair market value, not based on volume or value of referrals
- **Personal Services:** Bona fide employment or independent contractor arrangements
- **Rental of Office Space:** Office space leases at fair market value
- **Physician Recruitment:** Recruiting new physicians to underserved areas

**Penalties:**
- Denial of payment for all DHS provided pursuant to a prohibited referral
- Refund of amounts collected
- Civil monetary penalties (up to $15,000 per service)
- CMP for circumvention schemes (up to $100,000)
- False Claims Act liability

### 12.3 Anti-Kickback Statute (42 U.S.C. Section 1320a-7b)

**General Prohibition:**
Criminal penalties for knowingly and willfully offering, paying, soliciting, or receiving remuneration (anything of value) to induce or reward referrals for items or services payable by a federal healthcare program.

**Key Elements:**
- "Knowingly and willfully" -- one-party knowledge sufficient (does not require both giver and receiver to know)
- "Remuneration" -- anything of value, including cash, gifts, discounts, free services, excessive compensation, below-market leases
- "Induce or reward referrals" -- one purpose sufficient (even if other legitimate purposes exist)

**Criminal Penalties:**
- Felony
- Up to $100,000 per violation
- Up to 10 years imprisonment
- Mandatory exclusion from federal healthcare programs

**Safe Harbors:**
OIG has identified practices that are not subject to prosecution (the "safe harbors"). Compliance with all elements of a safe harbor provides protection:
- **Investment interests** (large publicly traded companies, small entities)
- **Space rental** (written, signed, fair market value, term at least 1 year)
- **Equipment rental** (same requirements as space rental)
- **Personal services and management contracts** (written, signed, fair market value, term at least 1 year)
- **Employment** (bona fide employment relationships)
- **Referral services**
- **Discounts** (properly disclosed and reported)
- **Group purchasing organizations**
- **Waiver of beneficiary coinsurance and deductible amounts**
- **Managed care safe harbors** (including risk-sharing arrangements)
- **Electronic health records** (donation of interoperable EHR software)
- **Accountable care organizations** (shared savings programs)

**OIG Advisory Opinions:**
Providers may request a formal OIG Advisory Opinion on whether a proposed arrangement violates the Anti-Kickback Statute or qualifies for a safe harbor. The opinion is binding on OIG and the requesting party.

### 12.4 Civil Monetary Penalties Law (42 U.S.C. Section 1320a-7a)

Civil Monetary Penalties (CMPs) may be imposed for:
- Presenting a claim the person knows or should know is false or fraudulent
- Offering remuneration to Medicare/Medicaid beneficiaries (inducements)
- Violating the Anti-Kickback Statute
- Excluding an individual from participation in federal healthcare programs
- Failing to grant OIG access to records
- Violations of Stark Law

---

## 13. Agent Q&A Pairs

**Q: What is a RAC audit and how is the RAC compensated?**

**A:** A RAC (Recovery Audit Contractor) audit reviews Medicare Part A and Part B claims to identify improper payments. RACs are paid on a contingency fee basis -- they receive 9-12% of the improper payment amount recovered (both overpayments and underpayments). This creates a financial incentive for RACs to identify as many overpayments as possible. RACs have been consolidated into the broader UPIC program since 2023.

**Q: What is the claim lookback period for RAC audits?**

**A:** RACs can review claims dating back 3 years from the date of service (not the date of payment). RACs cannot look back at claims older than 3 years unless fraud is suspected or the provider failed to submit timely appeals.

**Q: How should a provider respond to an Additional Documentation Request (ADR)?**

**A:** The provider must respond within the specified timeline (typically 30-45 days depending on the auditor). Response steps: (1) Log and track the request with a deadline, (2) Identify the claim in the practice management system, (3) Assemble complete medical records (H&P, progress notes, operative report, labs, imaging, orders, discharge summary), (4) Review for completeness and authentication, (5) Submit within deadline via the auditor's preferred method, (6) Confirm receipt and document in the tracking system. Failure to respond within the deadline results in automatic denial.

**Q: What is the Targeted Probe and Educate (TPE) program?**

**A:** TPE is CMS's medical review program administered by MACs. It involves three rounds: Round 1 (probe of 20-40 claims with education), Round 2 (re-probe 20-40 claims with focused education), Round 3 (final probe 20-40 claims with intensive education). If all three rounds show high error rates, the MAC may extrapolate the error rate to the entire claims universe, requiring the provider to repay substantial amounts.

**Q: What are the 5 levels of the Medicare appeals process?**

**A:** Level 1: Redetermination by the MAC (120 days to appeal, 60 days to decide). Level 2: Reconsideration by a QIC (180 days to appeal, 60 days to decide). Level 3: ALJ Hearing before an HHS ALJ (60 days to appeal, $180 minimum amount in controversy). Level 4: Medicare Appeals Council review (60 days to appeal). Level 5: Federal District Court (60 days to appeal, $1,840 minimum amount in controversy).

**Q: What is the False Claims Act and how does it apply to healthcare billing?**

**A:** The False Claims Act (31 U.S.C. Sections 3729-3733) prohibits knowingly submitting or causing the submission of a false or fraudulent claim to the federal government. "Knowing" includes actual knowledge, deliberate ignorance, or reckless disregard -- specific intent is not required. Penalties are $11,803-$23,607 per claim plus treble damages. Qui tam (whistleblower) provisions allow private individuals to sue on behalf of the government and receive 15-30% of the recovery. Healthcare examples include upcoding, billing for medically unnecessary services, unbundling, and billing for services not provided.

**Q: What is the difference between RAC and UPIC audits?**

**A:** RAC audits focus on identifying improper payments (errors) and are paid contingency fees. UPIC audits focus on fraud investigation and have broader authority including site visits, interviews, payment suspensions, and criminal referrals. UPIC can extrapolate overpayments and refer cases for prosecution, while RACs cannot. UPICs have largely replaced the separate RAC, ZPIC, and PSC programs since 2023.

**Q: What is the Stark Law, and what are designated health services?**

**A:** The Stark Law (42 U.S.C. Section 1395nn) prohibits physicians from referring Medicare patients to an entity for Designated Health Services (DHS) if the physician or an immediate family member has a financial relationship with the entity, unless an exception applies. DHS includes: clinical lab services, PT/OT/speech therapy, radiology, radiation therapy, DME, prosthetics, home health, outpatient drugs, and inpatient/outpatient hospital services. Stark Law is strict liability -- no intent requirement. Penalties include denial of payment, refunds, civil monetary penalties up to $15,000 per service, and FCA liability.

**Q: What is the Anti-Kickback Statute and what are its safe harbors?**

**A:** The Anti-Kickback Statute (42 U.S.C. Section 1320a-7b) prohibits knowingly and willfully offering, paying, soliciting, or receiving remuneration to induce or reward referrals for items or services payable by a federal healthcare program. Violation is a felony (up to $100,000 fine and 10 years imprisonment). Safe harbors include: space rental, equipment rental, personal services contracts, employment relationships, discounts, group purchasing organizations, and managed care arrangements. To qualify for a safe harbor, all elements of the safe harbor regulation must be met.

**Q: How should a provider conduct a self-audit?**

**A:** Best practices: (1) Quarterly random sample of 10-20 claims per provider, (2) Larger samples for high-risk areas, (3) Independent reviewer (who did not perform the original coding), (4) Score each claim as appropriate/minor error/major error/critical error, (5) Calculate error rate and identify patterns, (6) Present findings to compliance committee, (7) Develop corrective action plan (training, policy updates, workflow changes), (8) Re-audit to verify effectiveness. Maintain documentation of all audits.

**Q: What happens if a provider fails to respond to an ADR within the deadline?**

**A:** The claim is automatically denied for "no documentation." There is no grace period and no opportunity to submit late documentation at the initial review level. The claim must be appealed through the standard appeals process, which is significantly more burdensome than submitting documentation timely. This is the single most common reason for claim denials in audit situations.

**Q: What is the CERT program and how does it affect providers?**

**A:** CERT (Comprehensive Error Rate Testing) is a CMS program that randomly samples approximately 40,000 Medicare claims annually to measure the Medicare FFS improper payment rate. CERT results are not used to recoup payments from the specific sampled claim, but high error rates at the national level lead to increased scrutiny, targeted audits, and TPE for providers in high-error categories. The most common CERT error is insufficient documentation.

**Q: What are the elements of an effective compliance program?**

**A:** The OIG recommends seven elements: (1) Written compliance policies and procedures, (2) Designated compliance officer and compliance committee, (3) Effective training and education, (4) Accessible communication lines for reporting concerns, (5) Enforcement of standards through disciplinary guidelines, (6) Internal monitoring and auditing, and (7) Prompt response to detected offenses and corrective action.

**Q: What is the 60-day repayment rule?**

**A:** The Affordable Care Act (42 U.S.C. Section 1320a-7k(d)) requires a person who has received an overpayment from Medicare or Medicaid to report and return the overpayment within 60 days of the date the overpayment was identified. "Identified" means when the person has or should have known of the overpayment through the exercise of reasonable diligence. Failure to return an overpayment within 60 days creates liability under the False Claims Act.

**Q: What is qui tam and how does it apply to healthcare?**

**A:** Qui tam is a provision of the False Claims Act that allows a private individual (called a relator or whistleblower) to file a lawsuit on behalf of the government alleging fraud. The relator receives 15-30% of the government's recovery. In healthcare, qui tam actions are commonly filed by current or former employees who become aware of upcoding, billing for unnecessary services, or other fraud. The government may intervene in the case or the relator may pursue it independently.

**Q: What are the upcoding red flags that trigger audit?**

**A:** Common upcoding red flags include: (1) Higher-than-average E/M level distribution (e.g., 90%+ at Level 4-5 for a specialty), (2) Significant increase in E/M coding levels year-over-year, (3) High volume of modifier 25 usage with established patients, (4) High CC/MCC capture rate compared to peers, (5) High volume of specific high-reimbursement procedure codes, (6) Billing patterns inconsistent with specialty norms, (7) Unbilled or under-billed lower-level codes.

**Q: What is the role of the OIG Exclusion List?**

**A:** The OIG maintains a list of individuals and entities excluded from participating in federal healthcare programs. Providers must screen all employees, independent contractors, and vendors monthly against this list. Hiring or contracting with an excluded individual can result in CMP liability and exclusion. Payments made to excluded individuals for items or services covered by federal healthcare programs cannot be billed.

**Q: What is the difference between an overpayment and an extrapolated overpayment?**

**A:** An overpayment is a specific overpayment calculated on a specific claim (e.g., the provider was paid $500 for a Level 4 E/M but documentation supported Level 3 E/M, so the overpayment is $200). An extrapolated overpayment is when an auditor reviews a sample of claims, calculates the error rate in the sample, and applies (extrapolates) that error rate to the entire universe of similar claims to calculate a total overpayment. Extrapolation can result in very large overpayment demands.

**Q: What should a provider do immediately upon receiving a UPIC document request?**

**A:** (1) Engage healthcare legal counsel immediately (UPIC has fraud investigation authority and may refer for prosecution), (2) Do not alter, destroy, or remove any records, (3) Assemble all requested documentation within the deadline, (4) Submit complete, legible, authenticated records, (5) Cooperate with the investigation without waiving legal rights (e.g., Fifth Amendment), (6) Prepare for potential site visit or interviews, (7) Prepare to challenge extrapolation if the UPIC demands an extrapolated overpayment.

**Q: How does the Two-Midnight Rule affect inpatient admission audits?**

**A:** The Two-Midnight Rule (42 CFR 412.3) provides that inpatient admission is generally appropriate when the admitting physician expects the patient to require a medically necessary hospital stay spanning at least two midnights. Admissions with expected stays of less than two midnights are generally considered outpatient observation (even if the patient stays overnight). RACs aggressively audit inpatient claims with stays under two midnights. If denied, the claim is recategorized as outpatient, and the provider must repay the difference between inpatient and outpatient reimbursement.

**Q: What is the TPE extrapolation threshold?**

**A:** While specific thresholds vary by MAC, providers whose error rate remains above approximately 20-30% after all three rounds of TPE may face extrapolation. The MAC will issue a notice of extrapolation, and the provider can appeal this determination. If extrapolation goes forward, the MAC reviews a random sample and applies the error rate to all paid claims in the relevant category for a specified time period.

**Q: What are common CERT audit findings and how can providers avoid them?**

**A:** The most common CERT findings are: (1) Insufficient documentation (50%+ of improper payments) -- avoid by responding to ALL ADRs with COMPLETE medical records, (2) Medical necessity -- ensure clinical documentation supports the reason for the service, (3) Incorrect coding -- verify accurate code assignment. The key to avoiding CERT errors is to respond to ADRs timely and completely, not to ignore them because they are "random."

**Q: What is the Affordable Care Act 60-day overpayment rule?**

**A:** The ACA requires providers to report and return any identified overpayment from Medicare or Medicaid within 60 days of identification (42 U.S.C. Section 1320a-7k(d)). "Identification" means actual knowledge or when the provider should have known through reasonable diligence. The statute of limitations for FCA actions is 6 years, but the overpayment itself must be returned within 60 days. Failure to return an overpayment within 60 days creates FCA liability.

**Q: What are the differences between the Anti-Kickback Statute and the Stark Law?**

**A:** Key differences: (1) AKS prohibits ANY referral for federal program business if remuneration is involved; Stark Law covers only referrals for Designated Health Services to Medicare patients. (2) AKS requires "knowing and willful" intent; Stark Law is strict liability (no intent needed). (3) AKS is a criminal statute (felony prosecution); Stark Law is civil. (4) AKS covers anyone (physicians, hospitals, labs, DME suppliers); Stark Law applies only to physicians. (5) AKS safe harbors are voluntary; Stark Law exceptions are absolute requirements.

**Q: What is self-disclosure, and when should a provider consider it?**

**A:** Self-disclosure is the voluntary reporting of potential fraud or regulatory violations to the government. Options include OIG Self-Disclosure Protocol, CMS Self-Referral Disclosure Protocol, and DOJ voluntary disclosure. Providers should consider self-disclosure when: (1) A self-audit reveals significant overpayments, (2) A potential Stark Law or AKS violation is identified, (3) An excluded individual was employed and claims were submitted, (4) Billing errors suggest patterns of false claims. Legal counsel should be consulted before any self-disclosure.

**Q: How does Denials Doctor help clients with audit readiness?**

**A:** Denials Doctor helps clients by: (1) Analyzing denial patterns to identify services and providers at high risk of audit, (2) Integrating ADR tracking and deadline management into the workflow, (3) Providing documentation templates that support coding and medical necessity, (4) Analyzing claims data for upcoding/downcoding patterns, (5) Generating reports on payer-specific denial and audit history, (6) Supporting appeal generation for audit-related denials, (7) Providing analytics that identify areas for internal audit focus.

**Q: What are the penalties for Stark Law violations?**

**A:** Stark Law penalties include: (1) Denial of payment for ALL designated health services provided pursuant to a prohibited referral, (2) Refund of all amounts collected for prohibited services, (3) Civil monetary penalties of up to $15,000 per service, (4) CMP of up to $100,000 for circumvention schemes, (5) False Claims Act liability for claims submitted in violation of Stark Law (treble damages plus per-claim penalties). There is no criminal penalty under Stark Law.

**Q: What is the TPE "educational" component, and is it useful?**

**A:** Yes, the TPE educational component is valuable. After each round, the MAC provides specific, actionable feedback on errors found, categorized by type (documentation, coding, medical necessity, etc.). Providers should assign a dedicated team member to review this feedback, develop corrective action plans, and implement changes before the next round. Many providers successfully reduce their error rates through TPE education and avoid extrapolation.

---

## 14. References

- 31 U.S.C. Sections 3729-3733 (False Claims Act)
- 42 U.S.C. Section 1320a-7b (Anti-Kickback Statute)
- 42 U.S.C. Section 1395nn (Stark Law)
- 42 U.S.C. Section 1320a-7k(d) (60-day overpayment rule)
- 42 CFR Part 412 (Hospital Inpatient Prospective Payment System, Two-Midnight Rule)
- 42 CFR Part 405, Subpart I (Medicare Appeals)
- CMS Recovery Audit Program: https://www.cms.gov/medicare/medicare-fee-for-service-payment/recovery-audit-program
- CMS Targeted Probe and Educate: https://www.cms.gov/research-statistics-data-systems/medicare-fee-service-compliance-program/targeted-probe-and-educate
- OIG Work Plan: https://oig.hhs.gov/reports-and-publications/workplan/
- OIG Exclusion List: https://oig.hhs.gov/exclusions/
- HHS Office of Inspector General: https://oig.hhs.gov/
- OIG Compliance Program Guidance: https://oig.hhs.gov/compliance/compliance-guidance/