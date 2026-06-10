# Denial Types: Comprehensive Reference for Denials Doctor

## Overview

Denial management is the most critical revenue cycle domain for Denials Doctor. Denials represent lost revenue that must be systematically identified, appealed, and prevented. Understanding denial types is the foundation of any denial management strategy.

This document provides a complete reference on all denial categories, their root causes, denial codes, appeal strategies, and prevention techniques.

---

## 1. Medical Necessity Denials (~35-40% of all denials)

Medical necessity denials occur when a payer determines that a service, procedure, or level of care was not medically necessary for the patient's diagnosis or clinical presentation. This is the single largest category of denials.

### Root Causes

- **Insufficient documentation**: Medical records do not clearly support the medical necessity of the service
- **Diagnosis not supporting the procedure**: The documented diagnosis does not justify the procedure performed
- **Level of care mismatch**: Inpatient services when criteria for inpatient admission were not met (observation-level care would have been appropriate)
- **CMS LCD/NCD criteria not met**: Local Coverage Determination (LCD) or National Coverage Determination (NCD) requirements were not fulfilled
- **Experimental/investigational treatment**: The treatment is not widely accepted or does not meet standard of care
- **Failure to try conservative therapy first**: Payer requires step therapy or failed conservative management before advanced procedures
- **Frequency exceeded**: Service performed more frequently than medically necessary (e.g., physical therapy visits exceeded)
- **Screening vs. diagnostic confusion**: Payer considers the service screening when it was performed for diagnostic purposes

### Standard Denial Codes

| CARC | Description | Notes |
|------|-------------|-------|
| CO-50 | These are not covered under this medical benefit | Most common medical necessity code |
| CO-11 | The diagnosis is inconsistent with the procedure | Second most common |
| CO-48 | Charge for this service is outside of expected range | Frequency/volume issue |
| CO-96 | Non-covered charge | Service not a covered benefit |
| CO-119 | Benefit maximum for this service has been reached | Benefit limit denial |
| CO-198 | Prepayment review/preauthorization | Related to authorization requirements |
| N386 | This decision was based on documentation provided | RARC for medical necessity |
| N15 | This service/diagnosis is not payable | General non-coverage |

### Payer-Specific Medical Necessity Codes

- **UnitedHealthcare**: ClaimCheck, Optum Denial Code 600 (not medically necessary)
- **Aetna**: Aetna Code 16000 series for clinical denials
- **Cigna**: Cigna Code D0-D9 for medical necessity
- **Anthem/BCBS**: Anthem Code 100-199 range for clinical necessity

### How to Check LCD/NCD Criteria

The process for verifying LCD/NCD criteria is:

1. **Identify the procedure code (CPT/HCPCS)**: Determine the primary CPT code for the service
2. **Identify the ICD-10-CM diagnosis code(s)**: Determine the diagnosis codes submitted
3. **Access the applicable LCD**: Visit the Medicare contractor's website (e.g., Noridian, Novitas, Palmetto, WPS, NGS)
4. **Search LCD database**: Use the CMS Medicare Coverage Database at https://www.cms.gov/medicare-coverage-database
5. **Review LCD conditions**: Each LCD specifies covered diagnosis codes, frequency limits, documentation requirements
6. **Check NCD**: Verify national coverage policy exists (these override LCDs)
7. **Document compliance**: Ensure medical records document all required elements from the LCD

### Medical Necessity Appeal Strategy

When appealing a medical necessity denial:

1. **Review the specific denial reason**: Determine exactly why the payer denied (check denial code and remark codes)
2. **Gather supporting documentation**: Pull relevant medical records, physician notes, test results
3. **Map documentation to LCD/NCD criteria**: Create a table showing how each criterion is met
4. **Include peer-reviewed literature**: For controversial or advanced procedures, provide PubMed-indexed studies
5. **Include clinical guidelines**: Cite MCG, InterQual, UpToDate, specialty society guidelines
6. **Physician letter of medical necessity**: A detailed letter from the treating physician explaining why the service was necessary
7. **Submit within filing deadline**: Track the payer's appeal window carefully

### Prevention Strategies

- Pre-service medical necessity review before scheduling procedures
- Real-time eligibility and benefit verification with medical policy checking
- Use of prior authorization decision support tools
- Physician education on documentation requirements
- Automated claim edits that check procedure-diagnosis medical necessity before submission
- Peer-to-peer reviews before denial occurs

---

## 2. Coding Denials (~15-20% of all denials)

Coding denials result from errors in code selection, code assignment, or code reporting. These are often preventable with proper pre-submission editing.

### Root Causes

- **Invalid or missing diagnosis code**: ICD-10-CM code does not exist, is unspecified, or is inappropriate
- **Procedure code invalid for place of service**: CPT code is not payable in the setting where service was performed (e.g., surgical procedure in an office setting when required in an ASC)
- **Code unbundling**: Multiple CPT codes reported when a single comprehensive code should be used (code fragmentation)
- **Modifier missing or invalid**: Required modifier was omitted, or an invalid modifier was appended
- **NCCI edit failure**: National Correct Coding Initiative (NCCI) procedure-to-procedure (PTP) edit triggered
- **MUE exceeded**: Medically Unlikely Edit (MUE) threshold for number of units was exceeded
- **Invalid patient age**: Service/procedure not appropriate for patient's age
- **Invalid patient gender**: Procedure coded for wrong gender (e.g., prostate exam on a female patient)
- **Wrong code for service documented**: Code does not match the procedure documented in medical records
- **Upcoding**: Code billed represents a higher level of service than was actually performed
- **Downcoding**: Code billed may be incorrectly reduced by the payer (payer re-codes to a less specific code)
- **Incorrect code selection**: Wrong CPT, HCPCS, or ICD-10-CM code used for the service
- **Laterality missing**: Required laterality modifier (RT, LT, 50) not specified

### Standard Denial Codes

| CARC | Description | Common Scenarios |
|------|-------------|------------------|
| CO-4 | Procedure code inconsistent with modifier | Missing or invalid modifier |
| CO-16 | Claim/service lacks information needed for adjudication | Insufficient documentation |
| CO-97 | Service inconsistent with beneficiary/patient age | Age-related edit failure |
| CO-151 | Code not allowed by payer for this service | Payer-specific code restriction |
| CO-180 | Allowed amount has been reduced because the procedure code was invalid | Invalid CPT/HCPCS |
| CO-185 | The rendering provider is not eligible to perform this service | Provider-scope edit |
| CO-204 | Services/charges related to the treatment of this condition are not covered | Condition not covered |
| OA-100 | The service/equipment/drug is not covered | Non-covered item |
| N362 | The diagnosis code is incorrect | Diagnosis error |
| N4 | Procedure code inconsistent with place of service | POS code mismatch |
| N95 | This provider type/provider specialty may not bill this service | Scope-of-practice issue |

### NCCI Edit Types

There are three types of NCCI edits:

1. **Procedure-to-Procedure (PTP) Edits**: Two procedures that cannot be billed together. Edit has a column 1 (comprehensive) and column 2 (component) code. Both codes have a modifier indicator (0 or 1):
   - **Modifier 0**: Cannot use a modifier to bypass the edit under any circumstances
   - **Modifier 1**: A modifier can be used to bypass the edit if the procedure was distinct and separately identifiable

2. **Medically Unlikely Edits (MUE)**: Maximum units of service per day for each HCPCS/CPT code. Three types:
   - **Line edit**: Units on a single line cannot exceed the MUE
   - **Date of Service edit**: Total units for all lines on same DOS cannot exceed MUE
   - **Claim edit**: Total units on claim cannot exceed MUE

3. **Add-on Code Edits**: Primary procedure must be present when add-on code is billed

### Common Unbundling Scenarios

| Unbundled Codes | Comprehensive Code | Notes |
|-----------------|-------------------|-------|
| 12001 + 12002 | 13100 | Wound repair complexity |
| 59400 + 59409 + 59410 | 59400 | Global OB package |
| 27130 + 27132 | 27447 | Total hip arthroplasty |
| 49505 + 49507 | 49507 | Hernia repair |
| 99203 + 99213 | Single E&M | Same-day visits |
| 93015 + 93017 | 93015 | Cardiovascular stress test |

### Coding Denial Appeal Strategy

1. **Verify the coding error**: Confirm whether the denial is accurate or the payer made an error
2. **Document the correct codes**: Ensure medical records support the codes billed
3. **Provide supporting documentation**: Operative reports, procedure notes, or progress notes
4. **Cite coding references**: CPT Assistant, AHA Coding Clinic, specialty-specific coding guidelines
5. **Explain the use of modifiers**: When a modifier bypass was used, explain the clinical rationale
6. **Demonstrate medical necessity**: Even if the coding is correct, the service must be medically necessary

### Prevention Strategies

- Pre-submission claim scrubbing with NCCI/MUE editing
- Certified coders (CPC, CCS, COC) reviewing all coding before submission
- Regular coding audits and feedback
- Use of Computer-Assisted Coding (CAC) tools
- Automated payer-specific code validation
- Modifier validation rules
- Place of service code validation

---

## 3. Prior Authorization Denials (~10-15% of all denials)

Prior authorization (pre-authorization, pre-certification, precert) denials occur when required authorization for a service was not obtained, was obtained incorrectly, or has issues with its validity.

### Root Causes

- **No authorization obtained**: Service was performed without obtaining prior authorization
- **Authorization expired**: Authorization was obtained but expired before the service was rendered
- **Authorization for different service**: Authorization was obtained for a different CPT code, different procedure, or different level of care
- **Authorization amount exceeded**: Actual service charges exceeded the authorized amount
- **Services performed after authorization window**: Service rendered after the authorization effective period
- **Wrong patient**: Authorization obtained for a different patient
- **Wrong provider**: Authorization obtained for a different rendering provider or facility
- **Authorization not linked to claim**: Payer's system does not link the authorization to the claim
- **Authorization not on file**: Payer claims no authorization exists (may be due to data entry error)
- **Emergency services without authorization**: Some payers require post-service authorization for emergency care
- **Partial authorization**: Payer authorized only part of the requested service
- **Authorization not documented**: Authorization number was not recorded or attached to the claim
- **Retroactive authorization denied**: Retroactive authorization request was denied

### Standard Denial Codes

| CARC | Description |
|------|-------------|
| CO-31 | Patient cannot be identified as our insured |
| CO-197 | Preauthorization/Precertification/Utilization review required |
| CO-198 | Prepayment review/preauthorization |
| OA-23 | Services denied because authorization was not obtained |
| OA-107 | The associated claim was paid as a result of the provider not accepting an assignment |
| PR-16 | Claim/service lacks information needed for adjudication |

### Authorization vs. Pre-certification vs. Notification

| Term | Meaning | When Required |
|------|---------|---------------|
| Prior Authorization (Pre-Auth) | Full clinical review and approval | High-cost procedures, surgery, imaging |
| Pre-certification (Pre-cert) | Verification that admission/service is covered | Inpatient admissions, elective surgery |
| Notification | Notice to payer but no clinical review | Emergency admissions, observation |
| Referral | PCP directed patient to specialist | Specialist visits in HMO plans |
| Concurrent Review | Ongoing review during hospitalization | Extended inpatient stays |

### Authorization-Related Appeal Strategy

**If authorization was obtained:**
1. Search for the authorization record (portal, phone recording, fax confirmation)
2. Provide the authorization number, effective dates, and authorized CPT codes
3. Submit proof that the service rendered matches the authorization
4. Request the payer to attach the authorization to the claim

**If authorization was NOT obtained:**
1. Determine if an exception applies (emergency services, retroactive authorization)
2. Submit a retroactive authorization request (some payers allow this within a specific window)
3. If denied, appeal showing medical necessity (appeal based on clinical need, not authorization)
4. Some states have laws requiring payers to cover emergency services without prior authorization

**If authorization was partial:**
1. Determine if the additional services were medically necessary
2. Submit medical records showing why the expanded service was required
3. Request reconsideration based on clinical changes after authorization

### Prevention Strategies

- Real-time authorization checking before scheduling
- Automated authorization verification integrated with EHR
- Authorization tracking with automated expiration alerts
- Standardized authorization request workflow with documentation
- Confirmation number capture and documentation at time of service
- Pre-service authorization checklist
- Training on payer-specific authorization requirements
- Use of prior authorization clearinghouses (e.g., CoverMyMeds for pharmacy, Navinet for medical)

---

## 4. Timely Filing Denials (~10% of all denials)

Timely filing denials occur when a claim or appeal is submitted after the payer's specified deadline. These are entirely administrative — the clinical validity of the claim is not considered.

### Root Causes

- **Claim submitted after filing deadline**: Initial or corrected claim not filed within the payer's window
- **Appeal submitted after appeal deadline**: Appeal not filed within the payer's appeal window
- **Late submission from the billing service**: The billing company or service bureau submitted late
- **Provider did not receive timely filing notification**: Staff missed the deadline
- **Clearinghouse delay**: Claim filed to clearinghouse on time but not forwarded to payer in time
- **Incorrect filing date**: Payer uses date received, not date submitted
- **Missing or invalid secondary claim**: Secondary claim not filed within secondary payer's window
- **No proof of timely submission**: Cannot produce evidence that the claim was filed on time

### Filing Windows by Payer

| Payer | Initial Claim Filing Window | Appeal Filing Window |
|-------|---------------------------|---------------------|
| Medicare Part A/B | 12 months from DOS | 120 days from remittance |
| Medicare Part C (Advantage) | Varies by plan (90-365 days) | Varies (60-180 days) |
| Medicare Part D | 12 months from DOS | Varies by PDP |
| Medicaid (state varies) | 90-365 days from DOS | 30-180 days |
| UnitedHealthcare | 180 days from DOS | Varies by state |
| Cigna | 180 days from DOS | 180 days from denial |
| Aetna | 180 days from DOS | 180 days from denial |
| Anthem/BCBS | Varies by state (90-365 days) | 60-180 days |
| Humana | 180 days from DOS | 180 days from denial |
| Tricare | 365 days from DOS | 90 days from denial |
| Workers Comp (state varies) | Varies (30-365 days) | Varies (30-90 days) |
| Self-funded/ERISA plans | Plan document determines | Plan document determines |

### Standard Denial Codes

| CARC | Description |
|------|-------------|
| CO-29 | The time limit for filing has expired |
| CO-197 | Timely filing (sometimes used for appeal deadline) |
| OA-29 | The time limit for filing this claim has expired (other payer) |

### Proof of Timely Filing

Documentation that can prove timely filing:

1. **Clearinghouse submission log**: Date and time stamp from the claims clearinghouse
2. **997 Functional Acknowledgment**: Electronic acknowledgment from the payer's system
3. **277CA Claim Status Response**: Shows claim received date from payer
4. **TA1 Interchange Acknowledgment**: Confirms electronic transaction was accepted
5. **Fax transmission confirmation**: Date-stamped fax confirmation page
6. **Certified mail receipt**: For paper claims sent via certified mail
7. **Portal submission confirmation**: Screenshot or PDF from payer portal
8. **Phone log**: Record of phone call with the payer confirming submission
9. **Clearinghouse report**: Monthly clearinghouse reconciliation showing submission dates
10. **Billing system records**: Date-stamped records from the practice management system

### Good Cause Extensions

CMS allows "good cause" extensions for timely filing in specific circumstances:

- **Catastrophic illness or death** of the provider or immediate family member
- **Natural disaster** (hurricane, flood, earthquake, wildfire)
- **Fire, flood, or other casualty** destroying business records
- **Provider was incapacitated** due to physical or mental condition
- **Substantial clerical error** on the part of the provider (not the billing service)
- **CMS instruction error** or misinformation from CMS/MAC
- **System failure** (PMS or clearinghouse failure), with supporting documentation

For commercial payers, good cause exceptions vary widely. Most commercial payers do not recognize good cause exceptions.

### How to Calculate Filing Deadlines

**From Date of Service:**
- Service date = 01/15/2025
- Medicare deadline: 01/15/2025 + 12 months = 01/15/2026
- UHC deadline: 01/15/2025 + 180 days = 07/14/2025

**From Date of Discharge:**
- Inpatient admission 01/10/2025 to 01/15/2025
- Most payers use discharge date for filing deadline calculation
- Medicare: 01/15/2025 + 12 months = 01/15/2026
- Some payers use date of service (last date in the billing period)

**From Remittance Date (Appeals):**
- Remittance date: 03/01/2025
- Medicare appeal deadline: 03/01/2025 + 120 days = 06/29/2025

### State-Specific Timely Filing Laws

Some states have laws that mandate minimum timely filing periods:

| State | Minimum Filing Period | Law/Regulation |
|-------|---------------------|----------------|
| California | 90 days (minimum for certain plans) | Cal. Code Regs. tit. 10, § 2695.7 |
| New York | 120 days | NY Insurance Law § 3224-a |
| Texas | 95 days | 28 TAC § 21.2802 |
| Florida | 90 days | Various insurance regulations |
| Illinois | 180 days | 215 ILCS 5/370a |

Note: State laws typically apply to fully-insured plans. Self-funded ERISA plans are governed by federal law and plan documents.

### Timely Filing Appeal Strategy

1. **Confirm the deadline**: Verify the exact timely filing deadline for the specific payer and plan
2. **Gather evidence**: Collect all proof of timely filing documentation
3. **If filed timely**: Submit all supporting documentation showing the claim was submitted within the deadline
4. **If not filed timely**: Determine if a good cause exception applies
5. **Written explanation**: Prepare a detailed timeline of events leading to the late filing
6. **Request good cause exception**: For Medicare, complete the good cause exception request
7. **Escalate if appropriate**: Some payers have an escalation process for timely filing exceptions

### Prevention Strategies

- Automated timely filing deadline tracking in the practice management system
- Claims aging reports run weekly to identify claims approaching deadlines
- Automated alerts for claims within 30 days of the filing deadline
- Daily clearinghouse reconciliation to identify unsubmitted claims
- Batch submission with same-day verification
- Calendar tracking for all payers with different timelines
- Integration of filing deadlines into the billing workflow
- Secondary claims tracked from primary payment date, not original DOS

---

## 5. Benefit Limit Denials (~5-10% of all denials)

Benefit limit denials occur when the patient has exhausted their insurance benefits for a particular service type, or the service is not a covered benefit under their plan.

### Root Causes

- **Maximum visits exceeded**: Annual or lifetime limit on visits reached (physical therapy, occupational therapy, speech therapy, chiropractic, mental health)
- **Dollar maximum reached**: Annual or lifetime dollar maximum for a service category exhausted
- **Lifetime maximum exhausted**: Overall lifetime benefit limit reached on the plan
- **Plan excludes this service**: The specific service is not covered under the patient's benefit plan
- **Frequency limit exceeded**: Service can only be performed a certain number of times per period (e.g., once per year)
- **Calendar year limit**: Service limit is based on calendar year (January-December)
- **Plan year limit**: Service limit based on the plan year (may not align with calendar year)
- **Pre-existing condition limitation**: Service related to a pre-existing condition with limited coverage
- **Out-of-network benefit limit**: Out-of-network services subject to separate, lower limits

### Standard Denial Codes

| CARC | Description |
|------|-------------|
| CO-96 | Non-covered charges |
| CO-119 | Benefit maximum for this service/benefit category has been reached |
| CO-149 | Lifetime benefit maximum has been reached |
| CO-180 | Allowed amount reduced because service is not covered |
| PR-25 | Payment reduced or denied based on benefit limit |
| PR-27 | Expenses incurred during a non-covered benefit period |

### Common Service-Specific Limits

| Service Type | Typical Limit | Most Common Payer |
|--------------|---------------|-------------------|
| Physical Therapy | 20-30 visits per year | Most commercial plans |
| Occupational Therapy | 20-30 visits per year | Most commercial plans |
| Chiropractic | 12-24 visits per year | Most commercial plans |
| Speech Therapy | 20-30 visits per year | Most commercial plans |
| Mental Health Visits | 20-30 visits per year | Varies (mental health parity) |
| Cardiac Rehabilitation | 36 sessions per 12 months | Medicare |
| Pulmonary Rehabilitation | 36 sessions per 12 months | Medicare |
| ESRD-Related Services | Varies | Medicare |
| Skilled Nursing Facility | 100 days per benefit period | Medicare Part A |
| Home Health Services | Varies | Medicare Part A/B |

### Benefit Limit Appeal Strategy

1. **Verify remaining benefits**: Check the patient's benefit summary to confirm the limit
2. **Determine if limit is accurate**: Payer systems sometimes show incorrect remaining benefits
3. **Request additional benefits**: Some payers allow exception requests for additional visits:
   - Submit clinical justification for additional visits
   - Show functional improvement and goals not yet met
   - Provide a treatment plan with expected outcomes
4. **Appeal based on medical necessity**: Even if the limit is technically correct, argue that medical necessity should override the limit (success rate varies)
5. **Check for mental health parity**: If the benefit limit applies to mental health, check that it is not more restrictive than medical/surgical limits (Mental Health Parity and Addiction Equity Act)
6. **Patient financial responsibility**: If the appeal fails, the patient may be responsible for the cost

### Prevention Strategies

- Verify remaining benefits at each visit
- Track benefit utilization against plan limits
- Alert patients when benefits are approaching exhaustion
- Pre-service authorization for services approaching limits
- Document functional status and improvement goals from the first visit
- Plan treatment to maximize available benefits
- Consider alternative billing methods when benefits are exhausted

---

## 6. Non-Covered / Excluded Service Denials (~5%)

These denials occur when the service is specifically excluded from the patient's insurance policy, regardless of medical necessity.

### Root Causes

- **Service specifically excluded from policy**: The policy document explicitly excludes the service
- **Cosmetic vs. reconstructive**: Payer determines the procedure is cosmetic (not reconstructive/medically necessary)
- **Investigational/experimental**: Treatment not proven effective or not widely accepted
- **Routine dental excluded**: Medical plan excludes routine dental services
- **Routine vision excluded**: Medical plan excludes routine vision exams or eyewear
- **Hearing services excluded**: Medical plan excludes hearing aids or hearing exams
- **Weight loss surgery or treatment**: Plan excludes bariatric surgery or obesity treatment
- **Infertility treatment**: Plan excludes IVF or fertility treatments
- **Foot care (routine)**: Plan excludes routine foot care (ingrown toenails, calluses)
- **Alternative medicine**: Plan excludes acupuncture, chiropractic, naturopathy
- **Educational or habilitative services**: Not considered medical treatment

### Standard Denial Codes

| CARC | Description |
|------|-------------|
| CO-86 | Service not covered by this policy |
| CO-87 | Service not covered because the service is not a benefit of the policy |
| CO-88 | Service not covered because the service was not deemed medically necessary |
| CO-96 | Non-covered charge |
| CO-119 | Benefit maximum for this service/benefit category has been reached |
| CO-204 | Service/charge related to treatment of this condition is not covered |
| OA-100 | Service/equipment/drug not covered |

### Cosmetic vs. Reconstructive Determination

The key distinction is:

- **Cosmetic surgery**: Performed to improve appearance, not function. Typically excluded.
- **Reconstructive surgery**: Performed to correct a functional impairment or congenital anomaly. Typically covered.

To appeal a cosmetic determination:
1. Document the functional impairment (not just the appearance issue)
2. Include photographs showing the medical problem
3. Provide operative notes describing the reconstructive nature of the procedure
4. Cite the applicable insurance policy definition of reconstructive surgery
5. Include medical literature supporting reconstruction as standard of care

### Experimental/Investigational Appeal Strategy

1. **Determine payer's definition of "experimental"**: Most payers use specific criteria
2. **Gather evidence**:
   - FDA approval (if applicable)
   - Published, peer-reviewed literature
   - Specialty society guidelines endorsing the treatment
   - Medicare NCD/LCD if applicable
   - Clinical trials (Phase III or IV data)
3. **Show standard of care**: Demonstrate that the treatment is widely accepted
4. **Request peer-to-peer review**: A clinical peer review with a physician in the same specialty
5. **Cite the "prudent layperson" standard** if applicable (emergency services)

### Prevention Strategies

- Benefit verification before services to identify exclusions
- Pre-service coverage review for high-cost or likely-excluded services
- Patient waivers (Advance Beneficiary Notice - ABN for Medicare, Commercial ABN for non-Medicare)
- Clear documentation of medical necessity for services that could be considered cosmetic
- Patient education on plan exclusions before services are rendered

---

## 7. Coordination of Benefits (COB) Denials (~3-5%)

COB denials occur when claims are filed incorrectly regarding multiple insurance coverage.

### Root Causes

- **Other insurance primary**: Claim filed to the wrong payer (the secondary payer was billed as primary)
- **COB not processed**: Primary payer paid, but secondary claim not processed by secondary payer
- **Claim sent to wrong payer**: Billed to the wrong insurance company entirely
- **No other insurance information**: Provider does not have the patient's other insurance information
- **Primary payer denied wrong reason**: Primary denied for a non-covered service, but secondary expects primary to process first
- **Patient did not disclose dual coverage**: Patient has two insurance plans but did not tell the provider
- **COB pending**: Payer is still determining COB coordination, delaying payment

### Standard Denial Codes

| CARC | Description |
|------|-------------|
| CO-22 | This payment may be adjusted if other insurance is identified |
| CO-23 | Payment adjusted because this service was paid by another payer |
| CO-24 | Payment adjusted because charges have been covered by another payer |
| CO-166 | Balance is from the same payer as the primary payer |
| OA-22 | Other insurance coordination of benefits |

### COB Determination Rules

The NAIC (National Association of Insurance Commissioners) model rules determine which plan is primary:

1. **Dependent vs. Subscriber**: The plan covering the patient as a subscriber is primary; the plan covering them as a dependent is secondary
2. **Birthday Rule**: For dependent children covered by both parents, the plan of the parent whose birthday comes first in the calendar year is primary (month and day only, not year)
3. **Active vs. COBRA**: Active employee coverage is primary; COBRA continuation coverage is secondary
4. **No-COB rules**: Medicare is primary for patients 65+ with employer coverage unless employer has fewer than 20 employees
5. **Medicare and Medicaid**: Medicare always pays first; Medicaid pays last
6. **Workers Comp**: Workers Comp is always primary for work-related conditions

### COB Denial Appeal Strategy

1. **Determine the correct COB order**: Verify which insurance should be primary based on COB rules
2. **Bill the correct primary payer first**: The primary must process the claim before secondary can be billed
3. **Verify secondary payer information**: Confirm the secondary payer has the correct EOB/RA from primary
4. **Submit primary EOB with secondary claim**: Attach the primary payer's EOB/RA to the secondary claim
5. **Update patient insurance records**: Correct the insurance order in the practice management system
6. **Contact the COB department**: Some payers have dedicated COB departments for coordination issues

### Prevention Strategies

- Collect complete insurance information at every patient visit
- Verify COB status through eligibility checks
- Ask patients about other insurance coverage at each visit
- Use the NAIC Birthday Rule to determine dependent coverage order
- Document which insurance was billed and when
- Automated COB checking in the clearinghouse before adjudication

---

## 8. Other Denial Categories

### Duplicate Claim Denials (CO-18)

- **Definition**: Claim is identical to a previously processed claim
- **Root Causes**: Resubmission of the same claim, system double-submission, incorrect date of service
- **Resolution**: Confirm the original claim was processed, verify there is no payment issue on the original
- **If original was denied**: Appeal the original denial rather than resubmitting
- **Correction**: If the resubmission was intentional (for a corrected claim), add the appropriate frequency code (7 for replacement)

### Patient Ineligibility Denials (PR-5, PR-8)

- **PR-5**: Patient is not covered on the date of service (no active coverage)
- **PR-8**: Claim/service not covered when the patient has no coverage
- **Root Causes**: Patient coverage ended before DOS, patient not enrolled on DOS, waiting period not over
- **Resolution**: 
  1. Verify patient eligibility on the actual date of service
  2. If coverage WAS active, provide proof of coverage (screenshot, eligibility verification number)
  3. If coverage was NOT active, the patient is financially responsible
- **Prevention**: Verify eligibility 24-48 hours before every appointment

### Non-Participating Provider Denials (CO-174)

- **CO-174**: The provider is not participating in this plan/network
- **Root Causes**: Out-of-network provider, provider not in plan's network directory, terminated contract
- **Resolution**:
  - If the provider was in-network on DOS, provide proof of network participation
  - If out-of-network, check if the patient has OON benefits
  - Check for continuity of care provisions (patient in active treatment)
  - Consider a gap-fill or single-case agreement

### Technical Denials

These are administrative/business rule denials:

| Issue | Common Cause | Resolution |
|-------|-------------|------------|
| Invalid NPI | NPI not on file, wrong NPI used | Correct NPI and resubmit |
| Invalid TIN | TIN not matched to NPI | Verify TIN, correct and resubmit |
| Missing taxonomy | Taxonomy code required but missing | Add taxonomy code, resubmit |
| Invalid provider address | Address not on file with payer | Update provider file, resubmit |
| Missing referring provider | Referring/ordering provider required | Add referring provider info |
| Invalid servicing provider | Servicing provider not credentialed | Credential provider or correct codes |
| Missing prior auth number | Auth number required but missing | Add auth number and resubmit |

### Deductible, Coinsurance, Copayment Denials (PR-1, PR-2, PR-3)

These are technically not denials but patient financial responsibility adjustments:

| CARC | Description |
|------|-------------|
| PR-1 | Deductible amount |
| PR-2 | Coinsurance amount |
| PR-3 | Copayment amount |
| PR-27 | Non-covered benefit period expenses |

These amounts are patient responsibility and should be billed to the patient.

---

## Denial Type Interaction Matrix

Denials rarely occur in isolation. Common denial combinations:

| Primary Denial | Often Accompanied By | Impact |
|----------------|---------------------|--------|
| Medical Necessity (CO-50) | Missing documentation (N386) | Need both clinical and admin appeal |
| Prior Auth (CO-197) | Medical Necessity (CO-50) | Need auth plus clinical support |
| Coding Error (CO-4) | Medical Necessity (CO-11) | Fix codes and document necessity |
| Timely Filing (CO-29) | No proof of submission | Find proof or good cause |
| Benefit Limit (CO-119) | Patient liability (PR-25) | Can be patient or provider responsibility |

---

## Denial Prevention: Root Cause Analysis Framework

For each denial received, document:

1. **Denial type**: Primary and secondary categories
2. **Denial code**: CARC, RARC, and payer-specific codes
3. **Payer**: Specific payer and plan type
4. **Service**: CPT/HCPCS codes involved
5. **Root cause**: Why the denial occurred (not just the code)
6. **Prevention action**: What process change would prevent this denial
7. **Responsible party**: Who should take the prevention action
8. **Tracking**: Is this a recurring issue or one-time error?

---

## Agent Q&A Pairs for Training

**Q: What is the most common type of denial, and approximately what percentage of all denials does it represent?**
**A:** Medical necessity denials are the most common type, representing approximately 35-40% of all denials. These occur when the payer determines that the service, procedure, or level of care was not medically necessary for the patient's diagnosis or clinical condition. The primary denial code for this is CO-50 (these are not covered under this medical benefit/part/maximum). Second most common is CO-11 (the diagnosis is inconsistent with the procedure).

**Q: A claim was denied with CO-50. What does this mean and what should I do?**
**A:** CO-50 means "These are not covered under this medical benefit/part/maximum" — it is a medical necessity denial. The payer determined your service was not medically necessary for the patient's condition. To appeal: (1) review the specific denial reason in the remark codes, (2) gather supporting clinical documentation, (3) map your documentation to the payer's medical necessity criteria (LCD, NCD, or clinical policy), (4) include a letter of medical necessity from the treating physician, and (5) submit within the appeal window.

**Q: What is the difference between an LCD and an NCD?**
**A:** NCD (National Coverage Determination) is a nationwide CMS policy that applies to all Medicare claims nationally. There are approximately 300+ NCDs covering major treatments and technologies. LCD (Local Coverage Determination) is a coverage policy established by each Medicare Administrative Contractor (MAC) for their specific jurisdiction. LCDs apply only within that MAC's region. An NCD always overrides an LCD. When checking coverage for a Medicare service, first check for an applicable NCD, then check the local MAC's LCD for any additional requirements.

**Q: A claim was denied with CO-4. What does this mean and what could be the cause?**
**A:** CO-4 means "The procedure code is inconsistent with the modifier used or a required modifier is missing." This is a coding denial. Common causes: (1) an invalid modifier was appended to a CPT code, (2) a required modifier (like RT, LT, 50 for laterality) was missing, (3) a modifier that the payer does not recognize was used, (4) a modifier was used to bypass an NCCI edit when the modifier indicator is 0 (cannot be bypassed). To fix: review the correct coding guidelines for the procedure, verify which modifiers are valid for the payer, and resubmit with the correct modifier.

**Q: How do NCCI edits work and what are the modifier indicators?**
**A:** NCCI (National Correct Coding Initiative) edits prevent improper coding. There are three types: (1) Procedure-to-Procedure (PTP) edits that prevent billing two codes together when one is comprehensive, (2) Medically Unlikely Edits (MUE) that cap maximum units per day, (3) Add-on code edits requiring the primary code. Modifier indicators: 0 means no modifier can bypass this edit even if the procedures were separate; 1 means a modifier CAN bypass the edit if the procedures were distinct and separately identifiable. When appealing an NCCI edit denial, if the modifier indicator is 1, explain why the procedures were distinct and document this clinically.

**Q: What is the timely filing deadline for Medicare Part A/B?**
**A:** Medicare Part A and Part B claims must be filed within 12 months (365 days) from the date of service. This is one of the most generous filing windows. Important exceptions: (1) Medicare Part C (Medicare Advantage) plans set their own deadlines, typically 90-365 days, and (2) Medicare as a secondary payer (MSP) has different filing rules. Appeals for Medicare denials must be filed within 120 days from the date of the remittance advice.

**Q: My claim was denied with CO-29 for timely filing, but I submitted it on time. What proof do I need?**
**A:** You need documentation showing the claim was filed within the payer's timely filing window. Acceptable proof includes: (1) clearinghouse submission log showing date and time stamps, (2) 997 Functional Acknowledgment from the payer confirming receipt, (3) 277CA Claim Status Response showing the payer's received date, (4) fax transmission confirmation with date/time stamp, (5) certified mail receipt for paper claims, or (6) payer portal screenshot showing the submission timestamp. Submit the strongest evidence available with a written explanation of when and how the claim was submitted.

**Q: What is a good cause exception for timely filing?**
**A:** A good cause exception allows a provider to file a claim or appeal after the standard timely filing deadline when circumstances beyond their control caused the delay. CMS recognizes good cause for: catastrophic illness or death of the provider, natural disaster (hurricane, flood, fire), destruction of records, provider incapacitation, substantial clerical error by the provider (not the billing service), CMS instruction error, or system failure. The provider must submit a written request explaining the circumstances with supporting documentation. Commercial payers generally do not recognize good cause exceptions, though some states have laws requiring exceptions for certain circumstances.

**Q: How do I check if a service requires prior authorization for a specific patient?**
**A:** There are several ways: (1) Use the payer's online provider portal to check authorization requirements — most major payers (UHC Optum, Cigna, Aetna, BCBS) have eligibility and benefit tools that show authorization requirements, (2) Use the patient's eligibility and benefit (270/271) transaction to check service-level authorization requirements, (3) Call the payer's provider services line and ask specifically about the CPT/HCPCS code, (4) Use a third-party authorization tool like Navinet or Availity, (5) Check the payer's medical policy website for their authorization requirements list. Always document the verification method, confirmation number, date, and representative name.

**Q: A claim was denied with OA-23. What does this mean?**
**A:** OA-23 means "Services denied because authorization was not obtained" — this is a prior authorization denial (OA = Other Adjustment, meaning the adjustment is for reasons other than contractual or patient responsibility). The payer is saying that you did not obtain required prior authorization for the service. To resolve: (1) if authorization WAS obtained, provide proof (authorization number, dates, approved CPT codes), (2) if authorization was NOT obtained, determine if an exception applies (emergency services, retroactive authorization option), (3) file an appeal demonstrating medical necessity to overcome the authorization requirement.

**Q: What is the Medicare 5-level appeal process?**
**A:** Medicare has a 5-level appeals process for Part A and Part B: Level 1 — Redetermination by the MAC (120 days to file, 60-day decision), Level 2 — Reconsideration by a QIC (180 days to file, 30-60 day decision), Level 3 — Hearing by an Administrative Law Judge (ALJ) (60 days to file, minimum $180 controversy, 90-day decision), Level 4 — Medicare Appeals Council review (60 days to file, no minimum controversy), Level 5 — Judicial review in Federal District Court (minimum $1,830 controversy for 2024). Most claims are resolved at Level 1 or 2. ALJ hearings (Level 3) have the highest success rate at 60-70%.

**Q: What is an MUE and how does it affect claim payment?**
**A:** MUE stands for Medically Unlikely Edit. It is a CMS edit that sets the maximum number of units of service for a HCPCS/CPT code per day (or per claim for certain codes). If you bill more units than the MUE, the additional units are denied. There are three types: line edit (units on a single line cannot exceed MUE), date of service edit (total units for all lines on same DOS cannot exceed MUE), and claim edit (total units on claim cannot exceed MUE). Example: If CPT 99233 has an MUE of 4, you cannot bill more than 4 units of 99233 per day. If the medical record supports more units, you can appeal with clinical documentation.

**Q: My claim was denied with CO-18 (duplicate claim). What should I do?**
**A:** CO-18 means the payer believes you already submitted this claim and it was processed. First, check your practice management system to see if the original claim was paid. If it was paid, do nothing (this is a duplicate). If the original was denied, you need to appeal the original denial — do not resubmit as a duplicate. If you need to send a corrected claim, use frequency code 7 (replacement) on the corrected submission. If the original claim was lost or never received by the payer, call the payer to explain and request they locate the original or accept a corrected submission with appropriate documentation.

**Q: How do I determine which insurance is primary when a patient has two plans?**
**A:** Follow NAIC Coordination of Benefits rules: (1) If the patient is covered as an employee/subscriber under one plan and as a dependent under another, the plan covering them as the subscriber is primary. (2) For dependent children covered by both parents, use the Birthday Rule — the parent whose birthday (month/day only, not year) comes first in the calendar year has the primary plan. (3) Active employee coverage is primary over COBRA. (4) Medicare is primary for patients 65+ with employer coverage of 20+ employees; employer coverage is primary for fewer than 20 employees. (5) Medicare is always primary to Medicaid. (6) Workers Comp is always primary for work-related conditions.

**Q: A claim was denied with PR-5. What does this mean and what do I do?**
**A:** PR-5 means "The patient is not covered on the date of service" — this is an eligibility denial (PR = patient responsibility). The payer is saying the patient had no active coverage on the DOS. First, re-verify eligibility for the exact date of service using a 270/271 transaction. If coverage WAS active: (1) provide the payer with proof of coverage (screenshot of eligibility response, eligibility verification number), (2) ask the payer to research their eligibility records. If coverage was NOT active: (1) notify the patient, (2) collect payment from the patient, (3) consider whether the patient can retroactively enroll or if a different payer should have been billed.

**Q: What is a Medicare Advance Beneficiary Notice (ABN) and when should I use it?**
**A:** An ABN (CMS-R-131) is a waiver that Medicare providers give to Medicare beneficiaries before providing a service that Medicare is likely to deny as not medically necessary or not covered. The ABN informs the patient that Medicare may not pay and that they will be financially responsible. Use an ABN when: (1) the service may be denied by Medicare for medical necessity or frequency, (2) the service is not a covered benefit, (3) Medicare may deny based on a statutory exclusion, (4) you plan to bill for a service that Medicare usually covers but may deny in this specific case. Without a valid ABN (signed before the service), you cannot bill the patient for denied charges.

**Q: What is a commercial ABN and how does it differ from a Medicare ABN?**
**A:** A commercial ABN (also called a Notice of Non-Coverage or Financial Responsibility Agreement) serves the same purpose as a Medicare ABN but for non-Medicare insurance plans. Key differences: (1) No CMS-mandated form — each provider typically creates their own version, (2) State laws vary on whether and how commercial ABNs must be worded, (3) Some commercial payers explicitly prohibit providers from balance billing patients even with a signed waiver (in-network providers), (4) The scope is wider — commercial ABNs can address any potential denial reason (not just medical necessity), (5) Enforcement is less standardized than Medicare. Always check your provider contracts before balance billing patients.

**Q: What is the success rate for Level 1 appeals? Level 2? Level 3?**
**A:** Level 1 (Redetermination for Medicare, standard appeal for commercial): 50-60% success rate. This is the best chance for a successful appeal because the MAC or payer's internal reviewers will do a fresh review. Level 2 (Reconsideration for Medicare through QIC): 15-25% success rate. The QIC (Qualified Independent Contractor) is more rigorous. Level 3 (ALJ hearing for Medicare): 60-70% success rate. ALJ hearings are the most favorable level for Medicare because they provide an independent review. For commercial payers, success rates vary widely but generally decrease at each level.

**Q: A claim was denied for an invalid NPI. What should I check?**
**A:** CO-180 or a technical denial for invalid NPI can have several causes: (1) the NPI was entered incorrectly on the claim (transposition error), (2) the NPI is not enrolled with the specific payer — the provider must be credentialed/contracted, (3) the NPI/TIN combination does not match the payer's provider file, (4) you used the wrong NPI (Entity Type 1 individual vs. Entity Type 2 organization), (5) the NPI was deactivated. Fix: verify the NPI in the NPPES registry, ensure it matches your TIN in the payer's system, correct the claim, and resubmit. If the provider just enrolled with the payer, allow 30-60 days for the enrollment to process.

**Q: What is the difference between CO, PR, OA, and PI adjustment groups?**
**A:** These are the adjustment group codes in the ANSI X12 835 transaction: CO (Contractual Obligation) — adjustments the provider agreed to contractually, usually write-offs. The provider cannot bill the patient for these amounts. PR (Patient Responsibility) — amounts the patient is responsible for (deductibles, coinsurance, copays). The provider can bill the patient. OA (Other Adjustment) — adjustments for reasons OTHER than contractual or patient responsibility. This can include prior authorization denials (OA-23), COB issues (OA-22), etc. PI (Payer Initiated) — adjustments that may be reduced or reversed later. CR (Corrections and Reversals) — used when a previous payment is being corrected or reversed.

**Q: How do I appeal a denial for experimental/investigational treatment?**
**A:** Investigational denials require a strong clinical appeal: (1) Determine the payer's specific definition of "experimental" and "medically necessary" from their policy, (2) Gather FDA approval documentation if applicable, (3) Collect peer-reviewed published literature from indexed journals (PubMed), (4) Include specialty society guidelines, clinical practice guidelines, and consensus statements, (5) Show that the treatment is the standard of care in the medical community, (6) Include case studies if the condition is rare and large studies do not exist, (7) Submit a detailed letter from the treating specialist explaining why the treatment is appropriate, (8) Request a peer-to-peer review with a physician in the same specialty. Some payers have a specific "experimental/investigational" appeal process.

**Q: A claim for an inpatient admission was denied as "not medically necessary" and the level of care was reduced to observation. How do I appeal?**
**A:** This is a common Medicare denial (typically from a MAC or Recovery Auditor/RAC). To appeal: (1) Confirm the specific admission criteria that were not met (review the LCD or MCG/InterQual criteria for the diagnosis), (2) Gather all clinical documentation including admission orders, progress notes, nursing notes, vital signs, lab results, and consultant notes, (3) Document specific clinical findings that justified inpatient status (not observation), such as: vital sign instability, need for IV medications beyond observation capabilities, complex comorbidities requiring inpatient management, (4) Create a timeline showing why the patient needed inpatient-level care, (5) Include the physician's admission order and note explaining inpatient necessity, (6) Submit within 120 days for Medicare. For concurrent denials (before discharge), use the Medicare Beneficiary and Family Centered Care Quality Improvement Organization (BFCC-QIO) process.

**Q: What is the Birthday Rule in Coordination of Benefits?**
**A:** The Birthday Rule is the NAIC standard for determining which parent's insurance is primary for a dependent child when both parents cover the child. The parent whose birthday (month and day ONLY — the year does not matter) comes first in the calendar year has the primary plan. Example: Parent A's birthday is March 15. Parent B's birthday is July 22. Parent A's plan is primary because March comes before July. If both parents share the same birthday, the plan that has covered the parent longer is primary. If the parents are divorced, court orders determine primary coverage (typically the custodial parent's plan is primary).

**Q: How do I appeal a denial for a service that was not properly authorized when the patient had an emergency?**
**A:** Emergency services have special protections: (1) The Emergency Medical Treatment and Labor Act (EMTALA) requires hospitals to provide stabilizing emergency treatment regardless of insurance, (2) Most states have laws requiring coverage of emergency services without prior authorization, (3) The "prudent layperson" standard defines an emergency as symptoms that a reasonable person would believe require immediate medical attention. To appeal: (1) Cite EMTALA if a hospital emergency department was involved, (2) Cite the state's emergency services law, (3) Cite the "prudent layperson" standard in the patient's policy, (4) Provide clinical documentation showing the emergency nature of the visit from the patient's presentation. The appeal should focus on the legal obligation to cover emergency services, not on the authorization deficiency.

**Q: What is a peer-to-peer review and when should I request one?**
**A:** A peer-to-peer (P2P) review is a conversation between the patient's treating physician and a medical director or physician reviewer at the insurance company. Use P2P: (1) Before a formal denial is issued (proactive), particularly for high-cost services like surgery, imaging, or injectable medications, (2) After an adverse determination but before filing a formal appeal (many payers allow this), (3) For medical necessity denials where clinical documentation tells the story better than written words. Prepare by: (a) Having the treating physician (not the billing staff) make the call, (b) Reviewing the denial reason and having the patient's chart ready, (c) Preparing specific clinical facts that support medical necessity, (d) Being ready to cite medical literature or guidelines if needed. P2P reviews are most effective when the physician can clearly articulate the clinical rationale.

**Q: My claim was denied with CO-97. What does this mean?**
**A:** CO-97 means "Service is inconsistent with the beneficiary's/patient's age." This is a coding/clinical edit that flags when the procedure code is not appropriate for the patient's age. Examples: (1) Newborn hearing screening on a 50-year-old patient, (2) Geriatric assessment on a 10-year-old patient, (3) Maternity care on a 72-year-old patient, (4) Pediatric immunization on an adult. To fix: (1) Verify the correct age was used on the claim, (2) Confirm the CPT code is appropriate for the patient's age, (3) If the procedure IS appropriate despite the age mismatch, provide medical necessity documentation explaining why, (4) Resubmit the corrected claim.

**Q: What should I do when a payer says "authorization amount exceeded" (CO-197)?**
**A:** This means the services billed exceeded the dollar amount or number of units that were authorized. Steps: (1) Compare the billed services against the authorization — check CPT codes, units/days, allowed amount, (2) If the billed amount exceeds the authorization, request an amendment or additional authorization from the payer, (3) If the payer cannot increase the authorization, appeal based on medical necessity showing why the additional services were needed, (4) If the billed amount is within the authorization but the payer says it exceeds, provide documentation showing the authorized amount and billed charges side by side, (5) Check if the authorization was incorrectly entered in the payer's system.

**Q: What is a 277CA and how is it different from a 997?**
**A:** Both are electronic acknowledgments but serve different purposes: The 997 (Functional Acknowledgment) confirms that the electronic file was received and accepted by the payer or clearinghouse at the technical level — it confirms the X12 format was valid. The 277CA (Health Care Claim Acknowledgment) is a more detailed acknowledgment that shows claim-level status — it tells you which specific claims in the batch were accepted, rejected, or pended, with specific error codes. When proving timely filing, the 277CA is stronger evidence than the 997 because it shows the payer processed the specific claim. Ideally, keep both as proof.

**Q: What is a modifier and when is it required?**
**A:** A modifier is a two-character code appended to a CPT/HCPCS code to provide additional information about the service. Common reasons to use modifiers: (1) To show a service was performed on a specific side of the body (RT, LT), (2) To show bilateral procedures (50), (3) To show multiple procedures by the same provider (51), (4) To show a distinct procedural service (59, XE, XS, XP, XU), (5) To reduce the value of a service (52, 53), (6) To show the service was increased (22), (7) To identify the level of a professional or technical component (26, TC), (8) To show a staged or related procedure (58, 78, 79), (9) To indicate a repeat procedure by the same physician (76) or a different physician (77). Use modifiers only when supported by the clinical documentation.

**Q: How do I handle a denial for a service that was bundled into another procedure?**
**A:** When the payer bundles a service (the component code) into another procedure (the comprehensive code), this is an NCCI edit. To handle: (1) Check the NCCI edit table to confirm the edit exists and the modifier indicator, (2) If the modifier indicator is 1 and the procedures were truly distinct and separate, append the appropriate modifier (typically 59 or an X{EPSU} modifier), (3) If the modifier indicator is 0, you cannot bypass the edit with a modifier — bill only the comprehensive code, (4) If the payer incorrectly applied an edit, appeal with documentation showing the procedures were distinct, (5) If the procedures were performed on different body sites or through separate incisions, document this clearly.

**Q: A Medicare claim was denied for an unspecified diagnosis code. What should I do?**
**A:** CMS requires specific diagnosis codes for Medicare claims; unspecified codes (e.g., M54.9 Dorsalgia, unspecified) are often denied. To fix: (1) Review the medical record for a more specific diagnosis, (2) Use the highest level of specificity available for the condition, (3) Do NOT use unspecified codes unless the medical record truly does not support a more specific code, (4) Some payers reject unspecified codes outright while others accept them under certain conditions (e.g., initial visit before workup is complete), (5) If the medical record supports the unspecified code, document why no more specific code is available, (6) Resubmit the corrected claim with a specific diagnosis code.

**Q: What is the difference between a CO-45 and a CO-50 denial?**
**A:** CO-45 means "Charge exceeds fee schedule/maximum allowable or contracted/legislated fee arrangement" — this is a payment adjustment, not a denial. The payer is saying the allowed amount is less than the billed amount based on their fee schedule or contract. This is expected and the difference is a contractual write-off. CO-50 means "These are not covered under this medical benefit/part/maximum" — this IS a denial. The payer is denying the entire service as not medically necessary or not covered. A CO-45 is routine and expected; a CO-50 requires an appeal.

**Q: A claim for physical therapy services was denied with CO-119 (benefit maximum reached). How do I appeal?**
**A:** CO-119 means the patient has exhausted their benefit limit for this service category. Appeal options: (1) Verify the benefit limit — ask the payer for a detailed benefit summary showing remaining visits, (2) Check for errors — sometimes payer systems incorrectly show benefits as exhausted, (3) Request an exception — some payers allow additional visits with clinical justification showing functional improvement and ongoing need, (4) Appeal based on medical necessity — submit a treatment plan, functional assessment scores, and physician referral showing why additional visits are medically necessary, (5) Consider mental health parity — if the limit applies to mental health, check that it is not more restrictive than medical/surgical limits, (6) If the appeal fails, the patient may be financially responsible with a signed waiver.

**Q: What is a TAR (Treatment Authorization Request) and when is it used?**
**A:** A TAR (Treatment Authorization Request) is used primarily by Medi-Cal (California Medicaid) to request prior authorization for specific services, drugs, supplies, or devices. TARs are required for: (1) Certain high-cost or restricted drugs, (2) Durable medical equipment (DME), (3) Specific medical supplies, (4) Certain procedures with utilization limits, (5) Out-of-network services, (6) Services exceeding frequency limits. The TAR must include specific medical justification, the diagnosis code, and supporting clinical information. Without an approved TAR, the claim will be denied.

**Q: How do I handle a denial from a Workers' Compensation claim?**
**A:** Workers' Compensation denials follow state-specific processes. General approach: (1) Understand the denial reason — common WC denials include "not work-related," "condition not compensable," "no authorization," or "utilization review denial," (2) For "not work-related" — gather documentation linking the injury to the work activity (accident reports, witness statements, supervisor reports, first report of injury), (3) For "no authorization" — file a utilization review (UR) request through the WC UR process, (4) For utilization review denials — file an appeal with the state WC board or commission, (5) Most states have specific forms and deadlines for WC appeals (state-specific, typically 20-60 days), (6) Consider an independent medical examination (IME) if the defense challenges the medical necessity, (7) Unlike commercial insurance, WC also covers permanent disability, temporary disability, and vocational rehabilitation — appeal those separately if benefits are denied.

**Q: What is the difference between a corrected claim and an appeal?**
**A:** A corrected claim (submitted with frequency code 7) is used to fix minor data errors such as incorrect diagnosis code, incorrect modifier, or missing information — before or after adjudication, as long as the claim is not already denied. An appeal is a formal request for reconsideration of a claim that has been denied. Use a corrected claim when: (1) A coding error is identified before payment, (2) The claim needs administrative correction. Use an appeal when: (1) The claim was already adjudicated and denied, (2) The payer made an error in adjudication, (3) You need to provide additional clinical documentation, (4) The denial is for medical necessity, prior authorization, or benefit limits. Generally, if the claim has been denied, always appeal rather than submitting a corrected claim.

**Q: What is the 3-day payment window rule for Medicare?**
**A:** The 3-day payment window rule (also called the "DRG packaging rule") states that outpatient diagnostic and non-diagnostic services provided to a Medicare inpatient within 3 days (72 hours) prior to admission are considered related to the inpatient stay and must be bundled into the inpatient DRG payment. If you bill these services separately as outpatient claims, they will be denied. The 3 days is a calendar day count (not business days), and it includes the date of admission as day 1. The rule applies regardless of diagnosis — the services are presumed related. The only exception is for services provided in an emergency department or outpatient observation that are unrelated to the admission. This rule does NOT apply to Part B services for Part A excluded services.

**Q: A claim for an emergency department visit was denied for a non-covered condition. What are my options?**
**A:** First, determine the specific condition the payer is saying is not covered and the basis for the denial (policy exclusion, medical necessity, etc.). Options: (1) Appeal based on the prudent layperson standard — argue that given the patient's presenting symptoms, a reasonable person would believe emergency care was needed, (2) Many states have laws requiring health plans to cover emergency services based on symptoms, not final diagnosis — cite the applicable state law, (3) EMTALA requires hospitals to provide screening and stabilizing treatment regardless of insurance status — while EMTALA does not guarantee payment, it establishes the standard for when emergency care is appropriate, (4) If the denial is based on a specific policy exclusion, check whether the exclusion truly applies to the patient's symptoms, (5) Submit the full ED record, triage notes, and discharge instructions showing the patient's presenting symptoms.

**Q: What is CO-204 and what does it mean?**
**A:** CO-204 means "Services/charges related to the treatment of this condition are not covered." This denial code is used when the payer's policy specifically excludes coverage for the diagnosed condition. Common conditions with exclusion clauses include: (1) Obesity/weight-related treatments, (2) Infertility treatments, (3) Cosmetic procedures, (4) Foot care (routine), (5) Dental services, (6) Hearing services, (7) Experimental/investigational treatments. To appeal: (1) Check the specific policy language to understand the exclusion, (2) Determine if there is an exception or rider that covers the service, (3) If the exclusion should not apply (e.g., reconstructive surgery denied as cosmetic), provide documentation proving the service is covered, (4) If the exclusion legitimately applies, the patient may be financially responsible with a signed waiver.

**Q: How do I determine if a denial should be appealed or written off?**
**A:** Use this decision framework: (1) Is there a valid clinical or coding reason for the denial that can be corrected? If yes, appeal. (2) Was the denial an error by the payer (incorrect code application, wrong patient, etc.)? If yes, appeal. (3) Is the denial amount significant enough to justify the appeal effort? Consider the cost of the appeal vs. the expected reimbursement. (4) Is the appeal deadline still open? If the deadline has passed, you may be unable to appeal. (5) Is there a pattern of similar denials from this payer? If yes, appeal to establish precedent. (6) Is the denial contractual (CO-45 fee schedule adjustment)? Write off — this is expected. (7) Is the service truly not covered under the policy (CO-96, CO-86, CO-87)? Check for exceptions, but this may be a patient responsibility with a valid waiver. (8) If the appeal effort will cost more than the expected reimbursement, consider writing off for business efficiency.

**Q: What is the "all reasonable effort" standard for appealing denied claims?**
**A:** The "all reasonable effort" standard is a billing and collections concept that requires providers to make genuine attempts to resolve denied claims before writing them off or billing the patient. For Medicare, this is particularly important — if you do not make all reasonable efforts to resolve a denied claim (including appeals), you generally cannot bill the patient. For commercial payers, provider contracts often require "good faith efforts" to resolve denials. This means: (1) You should appeal every valid denial through at least one appeal level, (2) You should track and follow up on appeals, (3) You should document all appeal efforts, (4) You should not automatically write off all denials as "cost of doing business" if you have a basis for appeal. For medical necessity denials where you did not obtain a valid ABN, you especially need to appeal before considering patient billing.

**Q: What is the difference between a standard appeal and an expedited appeal?**
**A:** A standard appeal follows the normal processing timeline (60 days for Medicare Level 1, 30-45 days for most commercial). An expedited appeal (also called an urgent or fast-track appeal) is used when delaying the decision could seriously jeopardize the patient's life, health, or ability to regain maximum function. Expedited appeals: (1) Must be requested by the patient, provider, or patient's representative, (2) Are typically decided within 72 hours, (3) Require a specific justification showing urgency, (4) Can be requested verbally by phone for Medicare, (5) Are available at all appeal levels (1-5) for Medicare. Commercial payers also offer expedited reviews, typically with a 24-72 hour decision window. Use expedited appeals only for truly urgent situations; the expedited process is not appropriate for retrospective denials.

**Q: What is a RAC (Recovery Audit Contractor) and what types of denials do they typically issue?**
**A:** A RAC (Recovery Audit Contractor) is a CMS contractor that identifies Medicare overpayments and underpayments through post-payment audits. RACs generate denials/recovery demands for: (1) Medical necessity — inpatient admissions that should have been outpatient/observation (one of the most common RAC issues), (2) Incorrect coding — DRG validation errors, incorrect discharge status codes, unbundling, (3) Duplicate payments — claims paid multiple times, (4) Non-covered services — services billed that are not covered, (5) Medical records not submitted — failure to submit requested medical records. RAC denials follow the standard Medicare 5-level appeal process. Most RAC audits allow 45 days to submit medical records. If records are not submitted or do not support the claim, the overpayment is demanded with interest.

**Q: How do I handle a denial for a "never event" or hospital-acquired condition?**
**A:** "Never events" (also called Serious Reportable Events) and Hospital-Acquired Conditions (HACs) are serious, preventable adverse events that Medicare and many commercial payers will not pay for. Examples: (1) Surgery on the wrong body part, (2) Surgery on the wrong patient, (3) Wrong surgery performed, (4) Foreign object left in patient after surgery, (5) Air embolism, (6) Blood incompatibility, (7) Catheter-associated urinary tract infections, (8) Pressure ulcers (Stage III or IV) acquired after admission, (9) Falls with injury, (10) Vascular catheter-associated infections. For these denials: (1) Accept that payment will typically be denied — most have no appeal path for the "never event" itself, (2) Ensure the denial is indeed for the correct never event category, (3) For HACs, verify the condition was truly hospital-acquired (not present on admission - POA), (4) Document POA indicators correctly on all claims, (5) Focus on prevention rather than appeal, (6) Do not bill the patient for never events — most states prohibit this practice.

**Q: A claim was denied with OA-100. What does this mean?**
**A:** OA-100 means "The service/equipment/drug is not covered" — an OTHER adjustment. Unlike CO-86/87/88 (contractual non-coverage), OA-100 is used when the service is not covered for reasons that are not purely contractual. Common scenarios: (1) The drug/device does not have a valid HCPCS code, (2) The service is not a benefit under the patient's specific plan, (3) The FDA-approved indication does not match the condition being treated, (4) The dosage/formulation is not covered. To resolve: (1) Determine the specific reason for OA-100 by checking the accompanying RARC codes, (2) If it is a non-covered benefit, check if an exception applies, (3) If it is a coding issue (no valid HCPCS), use a valid code or a not-otherwise-classified (NOC) code, (4) Submit an appeal with clinical justification.

**Q: What is the appeals process for self-funded/ERISA plans?**
**A:** Self-funded (ERISA) plans follow federal ERISA regulations: Level 1 — Internal appeal with the plan administrator (minimum 60 days to file, 30-45 day decision for urgent, 30-60 day for standard). Level 2 — Second internal appeal (many plans require this before external review). Level 3 — External independent review (required by most states for fully-insured but optional for self-funded; however, many self-funded plans voluntarily participate in external review). Level 4 — Federal lawsuit under ERISA Section 502(a). Key ERISA rules: (1) Claims and appeals must be decided within strict timeframes, (2) Plan must provide specific reasons for denials, (3) Claimants have the right to review the complete file and submit additional information, (4) Denials must be decided by someone who was not involved in the initial decision, (5) Plans must have a process for urgent care appeals with 72-hour decision timeframes. Self-funded plans are governed by federal ERISA law, not state insurance laws.