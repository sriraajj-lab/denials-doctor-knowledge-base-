# Prior Authorization Requirements

## Overview

Prior authorization (also called pre-certification, pre-approval, or pre-authorization) is a utilization management process used by health insurance plans to determine if a prescribed medical service, procedure, or medication is medically necessary before it is rendered. In the revenue cycle management (RCM) workflow, prior authorization occurs after eligibility verification and before claim submission. Failure to obtain required prior authorization is one of the most common and preventable causes of claim denials.

---

## 1. What Requires Prior Authorization

The specific services requiring prior authorization vary by payer, plan type, and geographic region. The following table outlines common categories:

| Service Category | Examples | Typical Auth Required | Notes |
|---|---|---|---|
| **Inpatient Admissions** | All non-emergency inpatient stays | Yes | Medical necessity review required |
| **Major Surgeries** | Cardiac, orthopedic, neurosurgery, bariatric | Yes | CPT codes 27000-69999 range |
| **High-Cost Imaging** | MRI, CT, PET scans, nuclear cardiology | Yes | Usually above $500 threshold |
| **Durable Medical Equipment (DME)** | Wheelchairs, oxygen, CPAP, hospital beds | Yes | Over $150-$500 depending on payer |
| **Specialty Drugs** | Biologics, chemotherapy, IVIG, growth hormone | Yes | Often requires step therapy first |
| **Genetic Testing** | Whole exome sequencing, cancer panels | Yes | Typically >$500 test cost |
| **Physical Therapy / Occupational Therapy** | After initial visit limit (often 20-30 visits/year) | Yes | Once visit limit is exhausted |
| **Home Health Services** | Skilled nursing, home health aide, therapy at home | Yes | Face-to-face encounter required for Medicare |
| **Skilled Nursing Facility (SNF)** | Post-acute rehab, long-term care | Yes | 3-day prior hospitalization required for Medicare |
| **Elective Procedures** | Joint replacement, spine surgery, bariatric surgery | Yes | May require weight loss documentation for bariatric |
| **Behavioral Health** | Inpatient psychiatric, detox, residential treatment | Yes | Higher scrutiny for residential levels |
| **Transplants** | Kidney, liver, heart, bone marrow | Yes | Extensive clinical documentation required |
| **Pain Management** | Epidural steroid injections, nerve blocks, opioid therapy | Yes | Often requires recent imaging and failed conservative therapy |

### Payer-Specific Thresholds

- **Commercial payers** (UnitedHealthcare, Aetna, Cigna, BCBS): Auth required for most services >$500; some require auth for all outpatient surgery
- **Medicare**: Generally does NOT require prior authorization for most services (exceptions: home health, DME for certain items, chiropractic, and the Targeted Probe & Educate program)
- **Medicaid**: Varies by state; most require auth for all imaging, surgery, and inpatient stays
- **Workers' Compensation**: Typically requires auth for all services exceeding first visit
- **TRICARE**: Requires auth for all inpatient admissions, all surgeries, all high-cost imaging, and all DME >$200

---

## 2. Prior Authorization Types

### Standard Authorization

- Processing time: **7-15 business days** (commercial) or **14-21 days** (Medicare Advantage)
- Used for: Elective surgeries, routine imaging, scheduled procedures, DME
- Submission: Typically via portal, EDI 278, or fax
- Time of submission: At least 7-14 days before scheduled service date
- Consequences of delay: May necessitate rescheduling the procedure

### Urgent Authorization

- Processing time: **24-72 hours** (most payers); some require decision within 24 hours
- Used for: Emergency services, urgent surgeries, acute condition management
- Submission: Primarily via phone or expedited portal submission
- Documentation: Requires documentation justifying urgency
- Appeal rights: Expedited appeal available if denied

### Retrospective Authorization

- Processing time: 15-30 days (submitted after service date)
- Used for: Emergency services where auth could not be obtained in advance, unforeseen intraoperative findings requiring additional procedure
- Risk: Many payers do not guarantee payment for retro auth; may still deny
- Documentation: Must include reason auth was not obtained prospectively
- Payer limitations: Some payers (e.g., certain BCBS plans) do not accept retro auth at all

### Pre-Service vs. Post-Service Authorization

| Aspect | Pre-Service Authorization | Post-Service Authorization |
|---|---|---|
| **When obtained** | Before service is rendered | After service has been provided |
| **Risk level** | Low risk for payment if auth is approved | High risk for denial |
| **Common use** | Elective services, scheduled procedures | Emergency services, oversight |
| **Payment certainty** | High (if all requirements met) | Low |
| **Appeal difficulty** | Easier to appeal prospectively | More difficult to overturn post-service |

---

## 3. Auth Validity Periods

Authorization approvals are only valid for a limited time window. The provider must render services within this window or the authorization expires.

| Service Type | Typical Validity Period | Notes |
|---|---|---|
| **Surgery** | 30 days | Extended 60 days for some orthopaedic |
| **Imaging (MRI/CT/PET)** | 60 days | Some payers give 30 days for CT |
| **Physical Therapy (series)** | 1 year | Specifies number of visits within the year |
| **Inpatient Admission** | Admission-based | Valid for duration of medically necessary stay |
| **DME** | 90 days to 1 year | Depends on equipment type |
| **Specialty Drugs** | 30-90 days | Often requires re-auth for each cycle |
| **Home Health** | 60-day episode | Medicare home health certification period |
| **Skilled Nursing** | Length of stay | CMS 100-day benefit period |
| **Genetic Testing** | Single order | Valid only for the specific test ordered |

### Auth-to-Claim Matching Rules

For a claim to pay correctly, the following must match between the authorization and the claim:

1. **Auth number present on claim**: The authorization number (obtained from the payer) must be submitted in the appropriate claim field (Loop 2300 REF02 with REF01=G1 in 837P, or Loop 2400 REF02 with REF01=9F for service line auth references)
2. **Procedure code match**: The CPT/HCPCS code on the claim must match the authorized code or be within an authorized range
3. **Date of service within auth window**: All dates of service on the claim must fall within the authorization's valid from/to dates
4. **Units/renderings match**: The quantity billed must not exceed the authorized quantity
5. **Rendering provider match**: Some auths are provider-specific; using a different rendering provider may cause denial
6. **Place of service match**: Facility vs office location may need to match (POS 21 vs 11)

### Common Auth-to-Claim Mismatch Scenarios

| Scenario | Issue | Resolution |
|---|---|---|
| **Wrong auth number on claim** | Submitted billing NPI's auth instead of rendering NPI's auth | Correct the auth number and resubmit |
| **DOS outside auth window** | Service performed after auth expiration | Request auth extension or new auth |
| **Units exceeded** | PT billed 12 visits but auth approved 8 | Write off excess or obtain additional auth |
| **Modifier mismatch** | Auth for 29881, claim billed 29880 (wrong scope) | Rebill with correct code or get revised auth |
| **Multiple procedures, single auth number** | Auth covers only one of multiple procedures | Get separate auth for each unique procedure |

---

## 4. Auth Not Obtained Denials

### Handling Emergency Services When Auth Could Not Be Obtained

**The Prudent Layperson Standard**: Under the Affordable Care Act (ACA), health plans cannot require prior authorization for emergency services. If a patient presents with emergency symptoms, the plan must cover emergency care even without auth. However, documentation must support that the visit was truly an emergency.

**Process for unauthed emergency claims:**

1. **Attach the emergency modifier**: Append modifier **ET** (Emergency Services) to the primary CPT code on the claim
2. **Use appropriate place of service**: POS 23 (Emergency Room - Hospital) must be used
3. **Document the emergency**: Clinical documentation must support the emergent nature (e.g., chest pain, difficulty breathing, acute trauma)
4. **Appeal with Prudent Layperson Standard**: If denied for no auth, appeal citing the ACA provision
5. **Condition Code 41** (Medicare): Used to indicate an emergency when billing Medicare Part B for emergency services

### ACA Emergency Exception Rules

- Health plans cannot require prior authorization for emergency services
- Cannot impose any administrative barriers (e.g., higher copays) for out-of-network emergency services
- Coverage must be provided without regard to whether the provider is in-network
- Plans cannot require pre-certification for emergency department visits
- Exception applies to fully insured and self-insured group health plans and individual health insurance

### Non-Emergency Unauthed Services

If a non-emergency service is performed without required authorization:

1. **Provider writes off** the charges if the payer will not pay without auth (common for commercial payers)
2. **Patient responsibility**: Check if the patient signed an ABN (Advance Beneficiary Notice) or similar waiver; if so, the patient may be responsible
3. **Retrospective auth**: Submit for retrospective authorization, but many plans will not honor it
4. **Good faith attempt**: Document any attempts to obtain authorization (phone logs, portal screenshots)
5. **Appeal**: Submit clinical documentation supporting medical necessity with a letter of medical necessity

---

## 5. Medicare-Specific Authorization Rules

### Medicare Part A (Inpatient)

- **Does NOT require prior authorization** for most inpatient admissions
- **Condition Code 44**: Used when a physician determines an inpatient admission should have been outpatient observation. Required before the patient is discharged; otherwise, Medicare may deny the entire stay
- **2-Midnight Rule**: Inpatient admission is presumed appropriate if the physician expects the patient to require a hospital stay spanning two midnights
- **Medical review**: May still be subject to post-service medical review by a Quality Improvement Organization (QIO)
- **Targeted Probe & Educate (TPE)**: CMS program that pre-claims review for providers with high denial rates

### Medicare Part B (Outpatient)

- **No prior auth** for most outpatient services (routine blood work, imaging, most procedures)
- **Exceptions requiring auth**:
  - Home health services (must have face-to-face encounter and plan of care)
  - Certain DME items (coded KX modifier indicates medical necessity documentation on file)
  - Chiropractic services (limited to manual manipulation of the spine)
  - Hyperbaric oxygen therapy
  - Cochlear implants
  - Lung volume reduction surgery
  - Proton beam therapy

### Medicare Advantage (Part C)

- **Can require prior authorization** for services that Original Medicare does not require
- Commercial payers administering Medicare Advantage plans have their own auth requirements
- CMS regulations: Medicare Advantage plans must have "gold carding" programs for providers with consistent compliance
- Denial rates: Medicare Advantage plans have higher prior authorization denial rates than Original Medicare

---

## 6. Hospital Admission Authorization

### Medicare Part A vs. Observation Status

| Aspect | Medicare Part A (Inpatient) | Observation Status |
|---|---|---|
| **Coverage** | Hospital stay, nursing, therapies | Outpatient services in hospital |
| **Authorization required** | None (Medicare); varies (commercial) | Typically none for Medicare |
| **Beneficiary cost** | Deductible + coinsurance after day 60 | Part B 20% coinsurance per service |
| **SNF eligibility** | Qualifies for SNF coverage after 3-day stay | Does NOT qualify for SNF coverage |
| **Duration limit** | No set limit (must be medically necessary) | Typically <24-48 hours per CMS |
| **CMS rule** | 2-Midnight Rule applies | Benchmark for "inpatient" vs "observation" |

### Condition Code 44

Condition Code 44 is used to change a patient's status from inpatient to outpatient when:

1. The physician ordered inpatient admission
2. The patient has not been discharged
3. The utilization review committee determines the stay does not meet inpatient criteria
4. The patient agrees to the change

**CC 44 process:**
- Must be initiated BEFORE discharge
- Requires physician concurrence
- Claims should be billed as outpatient with Condition Code 44
- If not applied before discharge, the entire claim may be denied

### Hospital Authorization for Commercial Payers

- Most commercial payers require auth for ALL inpatient admissions
- Some require auth for observation stays >24 hours
- Auth is typically obtained from the insurance company's utilization management department
- If auth is denied, the hospital may still admit under a "member appeal" or "grace period"
- Many payers have "delegated credentialing" where the hospital's UR committee can certify admission

---

## 7. Payer-Specific Authorization Processes

### UnitedHealthcare
- Requires auth for all inpatient admissions, surgeries, advanced imaging, sleep studies, and cardiac testing
- Uses UnitedHealthcare Pre-Certification List
- Auth via UHC Provider Portal or EDI 278
- Standard processing: 5-7 business days
- Urgent: 24-72 hours

### Aetna
- Auth for inpatient, observation >24 hours, surgeries, advanced imaging, genetic testing
- Aetna Precertification Notification Unit
- Auth via Aetna Provider Portal or Navinet
- Standard: 5-10 business days
- Urgent: 24-72 hours

### Cigna
- Auth for inpatient, all surgical procedures, advanced imaging, sleep studies, cardiac testing
- Cigna Pre-Certification List
- Auth via Cigna for Health Care Professionals portal
- Standard: 7-10 business days
- Urgent: 24 hours

### Blue Cross Blue Shield
- Requirements vary significantly by state/plan
- BCBS FEP (Federal Employee): Auth for all inpatient and surgical services
- BCBS Association: Auth via Availity portal
- Many BCBS plans have different requirements for HMO vs PPO products
- Standard: 7-15 business days depending on plan

### Medicaid (State-Specific)
- Every state Medicaid program has different auth requirements
- Most require auth for non-emergency inpatient admissions, all surgeries, and advanced imaging
- Many states use a fiscal intermediary for auth processing
- Some have "standing referrals" for ongoing care

---

## 8. Auth Workflow in RCM

### Typical Auth Workflow Steps

```
Step 1: Schedule Appointment
   |
Step 2: Verify Benefits — Check auth requirements for the specific service
   |
Step 3: Gather Clinical Documentation — Notes, labs, imaging, referrals
   |
Step 4: Submit Auth Request — Via portal, EDI 278, phone, or fax
   |
Step 5: Track Auth Status — Follow up at day 5, day 10, day 14 if needed
   |
Step 6: Receive Auth Decision — Approved, denied, or pended
   |
Step 7: Log Auth Details — Auth number, valid dates, approved services, units
   |
Step 8: Notify Provider and Patient — Auth is in place for scheduled service
   |
Step 9: Submit Claim — Include auth number on claim at header or line level
   |
Step 10: Verify Payment — Ensure claim pays correctly; appeal if auth-related denial
```

### Key Performance Indicators (KPIs)

| Metric | Target | What It Measures |
|---|---|---|
| **Auth obtained rate** | >90% | Percentage of services with auth obtained before service |
| **Auth denial rate** | <10% | Percentage of auth requests denied |
| **Auth turnaround time** | <5 business days | Average days from request to decision |
| **Auth-related claim denial rate** | <2% | Claims denied due to auth issues |
| **Appeal overturn rate** | >60% | Auth denials overturned on appeal |

---

## 9. Technology Integration

### Electronic Prior Authorization (ePA)
- **EDI 278**: Standard electronic format for auth request and response
- **CoverMyMeds**: Widely used for prescription prior authorization
- **Zocdoc, HealthSherpa**: Consumer platforms with integrated auth
- **Clearinghouses**: Many (e.g., Change Healthcare, Availity, Navinet) offer ePA services
- **Provider portals**: Each major payer has its own provider portal for auth

### API-Based Prior Authorization
- Newer approach using HL7 FHIR standard
- Da Vinci Project Prior Authorization Support (PAS) IG
- Enables real-time auth determination for straightforward cases
- Reduces average auth time from days to minutes for simple requests
- Adoption increasing among major payers (UnitedHealthcare Optum, Aetna)

### Automation Considerations

| Task | Automation Potential | Tools |
|---|---|---|
| Checking auth requirements | High | RPA + payer lookup tables |
| Submitting standard auths | High | EDI 278 batch, API |
| Gathering clinical documentation | Medium | EHR integration |
| Tracking auth status | High | Automated status checks |
| Appeals for auth denials | Low (requires clinical reasoning) | AI-assisted drafting |
| Communicating auth # to billing | High | EHR-PMS integration |

---

## 10. Q&A Pairs for Agent Training

**Q:** What is the difference between standard and urgent prior authorization processing timeframes?
**A:** Standard prior authorization typically processes within 7-15 business days for commercial payers, while urgent authorizations process within 24-72 hours. The clinical documentation submitted must justify the urgency. Urgent auth is appropriate when the standard timeline would seriously jeopardize the patient's life, health, or ability to regain maximum function.

**Q:** Does Medicare require prior authorization for most services?
**A:** No. Original Medicare (Part A and Part B) does not require prior authorization for most services. Exceptions include home health services, certain DME items, chiropractic services, hyperbaric oxygen therapy, cochlear implants, and lung volume reduction surgery. Medicare Advantage plans (Part C) can impose prior authorization requirements that differ from Original Medicare.

**Q:** What happens if a claim is submitted without a required authorization number?
**A:** The claim will likely be denied with reason code indicating missing or invalid authorization. The denial may come through as an EDI 835 with CAS segment indicating patient responsibility or contractual adjustment. The provider must either obtain retrospective authorization (if the plan accepts it), write off the charges, bill the patient (if a valid waiver was signed), or appeal with clinical documentation.

**Q:** What is Condition Code 44 and when is it used?
**A:** Condition Code 44 is a Medicare billing code used to change a patient's hospital status from inpatient to outpatient when the physician ordered inpatient admission but the utilization review committee later determines the stay does not meet inpatient criteria. It must be applied BEFORE the patient is discharged. The patient must agree to the change. The provider bills as outpatient services with Condition Code 44 on the claim.

**Q:** How long is a prior authorization typically valid for surgery?
**A:** Surgery authorizations are typically valid for 30 days from the date of approval, though some payers (especially for orthopaedic surgery) may grant 60-day validity periods. If the surgery does not occur within the valid window, a new authorization request must be submitted.

**Q:** What is the Prudent Layperson Standard?
**A:** The Prudent Layperson Standard is a provision of the Affordable Care Act (ACA) that requires health plans to cover emergency services without requiring prior authorization. If a patient presents with symptoms that would lead a "prudent layperson" to believe emergency care is needed, the plan must cover the services regardless of whether authorization was obtained. The modifier ET appended to the CPT code and proper documentation of the emergency symptoms are required for this exception.

**Q:** Can a prior authorization be used for multiple procedures performed on the same day?
**A:** It depends. Some authorizations are procedure-specific and cover only the CPT code(s) listed. If multiple distinct procedures are performed, each may require its own authorization. However, some payers issue authorization for an "encounter" covering all services during a specified date range. The 837 claim submission should reference the auth number at the appropriate level: the header (Loop 2300 REF segment) if it covers the entire encounter, or at the service line level (Loop 2400 REF) if auths are procedure-specific.

**Q:** What is the 2-Midnight Rule?
**A:** The 2-Midnight Rule is a CMS regulation stating that inpatient admission is presumed medically appropriate if the physician expects the patient to require a hospital stay spanning at least two midnights. Services expected to last less than two midnights are generally considered outpatient observation. This rule is for Medicare beneficiaries and is used to determine inpatient vs. observation status.

**Q:** How should a provider handle a situation where auth was obtained but the claim still denies for "no authorization"?
**A:** Common causes include: (1) the auth number was omitted from the claim, (2) the auth number was entered incorrectly, (3) the auth was for a different procedure code, (4) the dates of service fall outside the auth window, (5) the rendering provider is different from the auth-approved provider. Investigation should start with verifying the auth details, then checking the submitted claim data. If the auth was correctly included and valid, the provider should appeal with the supporting documentation.

**Q:** What is the difference between pre-service and post-service authorization?
**A:** Pre-service authorization is obtained before the service is rendered, providing payment certainty if approved. Post-service authorization is obtained after the service has already been performed, typically for emergency services or situations where advance auth was not feasible. Pre-service auth carries low payment risk; post-service auth carries high payment risk. Many payers do not guarantee payment for post-service authorization.

**Q:** What is retrospective authorization and when is it appropriate?
**A:** Retrospective authorization is a request for authorization submitted after the service date. It is typically used for emergency services where authorization could not be obtained in advance, or for unforeseen intraoperative findings that necessitated additional procedures. Not all payers accept retrospective authorization. The provider must document the reason authorization was not obtained prospectively.

**Q:** How does the auth-to-claim matching process work in the 837 transaction?
**A:** In the 837 professional claim, the authorization number is placed in Loop 2300 with REF01 segment qualifier "G1" (Prior Authorization Number) and the auth number in REF02. If authorization is procedure-specific, it is placed at the service line level in Loop 2400 with REF01 qualifier "G1" as well. The payer's claims processing system validates that the procedure code, modifier, date of service, quantity, and rendering provider on the claim match the authorization on file.

**Q:** What is a "gold carding" program for prior authorization?
**A:** Gold carding is a program under CMS regulations where Medicare Advantage plans exempt certain high-performing providers from prior authorization requirements. Providers with consistently low denial rates and high compliance are "gold carded," allowing them to receive payment for services without obtaining prior authorization in advance. CMS has required Medicare Advantage plans to implement gold carding programs starting in 2024.

**Q:** What modifiers are commonly used to indicate authorization status?
**A:** Common modifiers related to authorization include: Modifier ET (Emergency Services) - indicates the service was provided in an emergency and auth could not be obtained; Modifier GX (Notice of Liability Issued) - indicates an ABN was issued; Modifier GY (Statutorily Excluded) - indicates item or service is statutorily non-covered; Modifier KX (Medical Policy Meets Requirements) - indicates requirements specified in the medical policy have been met, often used for DME.

**Q:** How does the authorization process differ for physical therapy vs. surgery?
**A:** Physical therapy authorizations typically authorize a block of visits (e.g., 12-20 visits over a 1-year period) rather than a single procedure. Surgery authorizations are typically for a single procedure on a specific date (or a range of dates). PT auths require tracking of remaining visits against the auth limit, while surgery auths are one-time approvals.

**Q:** What is a "pending" authorization and how should it be handled?
**A:** A pending authorization (status code 2 in the 278 response) means the payer needs additional information before making a decision. The provider should respond promptly with the requested clinical documentation. Common reasons for pending status include: insufficient clinical data, missing lab results, need for peer-to-peer review, or additional diagnostic information. The provider should track pending auths to ensure they do not expire while awaiting decision.

**Q:** What are the consequences of billing a claim with an expired authorization?
**A:** If the claim date of service falls outside the authorization's valid date range, the payer will deny the claim. Common denial codes include CO 197 (Prior Authorization Information Missing/Invalid) or CO 204 (Authorization Expired). The solution is to request an extension from the payer or submit a new authorization request covering the actual date of service. The provider cannot simply change the date of service on the claim to match the auth range.

**Q:** What steps should a provider take if an authorization is denied?
**A:** (1) Review the denial reason carefully - was it a clinical necessity denial, administrative error, or policy exclusion? (2) For clinical necessity denials, gather additional supporting documentation and submit a letter of medical necessity. (3) Request a peer-to-peer review with the plan's medical director. (4) File a formal appeal following the plan's appeal process, typically within 180 days. (5) Consider a state external review or independent medical review. (6) If all appeals are exhausted, consider whether to write off the service or bill the patient under a signed waiver.

**Q:** What is a managed care "authorization requirement grid"?
**A:** An authorization requirement grid is a comprehensive reference document maintained by provider organizations that lists every payer and product line (HMO, PPO, POS, EPO, Medicare Advantage, Medicaid) along with which specific CPT/HCPCS codes require prior authorization. It includes details such as: auth submission method, required clinical documentation, processing times, auth validity periods, and phone numbers for urgent requests. This grid is essential for RCM teams to verify auth requirements before each procedure.

**Q:** How does the EDI 278 transaction differ from portal-based auth submission?
**A:** The EDI 278 is a standardized electronic format (X12 HIPAA-compliant) that allows direct system-to-system submission of authorization requests and responses. Portal-based submission requires manual data entry into a web interface. EDI 278 is faster, more efficient for high-volume providers, and reduces manual data entry errors. However, portal-based submission may offer more detailed guidance and real-time feedback for complex cases. Many providers use EDI 278 for routine auths and portals for complex or first-time requests.

**Q:** What is the process for changing a patient from inpatient to observation status (Condition Code 44)?
**A:** The physician must first concur with the status change. The utilization review committee must document that the inpatient admission does not meet medical necessity criteria. The patient must be notified and agree to the change. The change must be made BEFORE the patient is discharged. The claim is then submitted with outpatient revenue codes and Condition Code 44 indicating the status change. If not completed before discharge, the provider cannot retroactively change status and may face full claim denial.

**Q:** How should an RCM team handle Medicare Targeted Probe & Educate (TPE) reviews?
**A:** TPE is a CMS program that pre-claims review for providers with high denial rates. Under TPE: (1) The provider is selected based on claim denial rates. (2) CMS reviews up to 20-40 claims per review round. (3) If denial rate exceeds threshold after two rounds, the provider is placed in pre-payment review. (4) After three rounds with high denial rate, CMS may extrapolate overpayments. RCM teams should: maintain robust medical necessity documentation, respond to ADRs within 30 days, track TPE results and denial reasons, and implement corrective action plans.

**Q:** What is a "crossover authorization" for a dependent patient?
**A:** In EDI 278, when the patient is a dependent (not the subscriber), the authorization request uses Loop 2000C (Dependent Level). The subscriber's information is in Loop 2000B and the dependent patient information (including unique subscriber-dependent identifier) is in Loop 2000C. The authorization approval is specific to that dependent patient and cannot be transferred to another family member even if the subscriber is the same.