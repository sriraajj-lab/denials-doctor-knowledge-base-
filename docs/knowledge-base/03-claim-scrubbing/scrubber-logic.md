# Scrubber Logic

## Overview

A claim scrubber is automated software that validates healthcare claims against a comprehensive set of editing rules before submission to a payer. Scrubber logic is the collection of rules, edits, and validations that the scrubber applies to detect errors, omissions, or inconsistencies that would result in denial. Effective scrubbing reduces denial rates, accelerates reimbursement, and minimizes rework.

Scrubbers operate at two levels:
1. **Pre-submission scrubbing**: Applied before the claim is sent to any payer.
2. **Payer-specific scrubbing**: Applied when routing the claim to a specific payer, using that payer's unique edit rules.

---

## 1. Pre-Submission Claim Scrubber Logic

### What It Checks

Pre-submission scrubber logic validates the claim against a comprehensive set of rules before it leaves the provider's system. These checks are typically organized into categories:

### Edit Category Hierarchy

| Priority | Category | Description |
|----------|----------|-------------|
| **Level 1** | Format Validation | X12 structure, required segments, data types |
| **Level 2** | Required Fields | Missing or invalid required data elements |
| **Level 3** | Code Validation | Valid CPT, HCPCS, ICD-10, NPI, taxonomy codes |
| **Level 4** | Code-to-Code Relationships | NCCI edits, diagnosis-to-procedure edits |
| **Level 5** | Modifier Validation | Valid modifier for code, modifier-to-procedure match |
| **Level 6** | Provider Validation | NPI active, taxonomy matches specialty, license valid |
| **Level 7** | Patient Validation | Eligibility, coverage dates, COB |
| **Level 8** | Payer-Specific Rules | Companion guide requirements, frequency limits |

---

## 2. Common Scrubber Edits

### 2.1 Missing or Invalid Diagnosis Codes

| Edit | Description | Error Message Example |
|------|-------------|-----------------------|
| Missing primary diagnosis | The claim does not contain a required ICD-10 diagnosis code | "Primary diagnosis code is required" |
| Invalid ICD-10 code | The diagnosis code is not valid in the current ICD-10 code set | "ICD-10 code A12.3 is not a valid code" |
| Invalid ICD-10 character | Wrong format, missing decimal, or invalid character | "ICD-10 codes must be 3-7 characters with one decimal" |
| Invalid ICD-10 age/gender | Diagnosis code is inconsistent with patient age or gender | "ICD-10 Z30.2 encounters for sterilization are not valid for this age" |
| Truncated diagnosis code | A 7-character ICD-10 code was submitted with fewer digits needed | "Diagnosis code S06.5X requires a 7th character" |
| Late-onset diagnosis | Diagnosis code's laterality is unspecified when a specific side is available | "Use right/left specific code instead of unspecified M17.9" |
| Manifestation code as primary | A manifestation-only code is used as the primary diagnosis | "Use E11.9 before E11.51 for diabetes with retinopathy" |

### 2.2 Diagnosis-to-Procedure Mismatch

| Edit | Description | Example |
|------|-------------|---------|
| Procedure not supported by diagnosis | The ICD-10 code does not support the medical necessity of the CPT code | CT cervical spine (72125) with M54.5 (low back pain) |
| E/M code with prevention-only diagnosis | E/M code billed but only preventive diagnosis codes present | 99213 with Z00.00 (general adult exam) only |
| Surgical code with medical diagnosis | Surgery code submitted with a diagnosis that describes a condition typically managed medically | 27130 (hip replacement) with M79.18 (myalgia) |

### 2.3 Missing Modifier

| Edit | Description | Example |
|------|-------------|---------|
| Bilateral procedure without modifier 50 | A code with bilateral surgery indicator requires modifier 50 for bilateral reporting | 27447 (TKA) performed bilaterally without modifier 50 |
| Multiple procedure without modifier 51 | Multiple surgical procedures without the appropriate modifier | Two procedures on same date, same session |
| Distinct service missing modifier | Codes with NCCI PTP edit indicator of 1 require a modifier | 27130 and 27236 both reported without modifier |
| Repeat procedure missing modifier 76/77 | Same procedure performed twice on same day without modifier | Two 93005 codes on same date without modifier |

### 2.4 Modifier-to-Procedure Mismatch

| Edit | Description | Example |
|------|-------------|---------|
| Modifier not valid for code | A modifier is appended to a code that does not support it | Modifier 50 on a code with bilateral indicator 0 |
| Modifier 25 without E/M code | Modifier 25 can only be used with E/M codes | Modifier 25 appended to 27130 (THA) |
| Modifier 59 used unnecessarily | Modifier 59 on codes that do not have NCCI edits | 99213 with modifier 59 (no edit exists) |
| Modifier 59 with modifier indicator 0 | A modifier cannot bypass a PTP edit with indicator 0 | Modifier 59 on 27130/27236 PTP edit |
| Multiple modifiers conflict | Incompatible modifiers on the same line | Modifier 50 and modifier LT on same line |

### 2.5 Invalid NPI

| Edit | Description | Example |
|------|-------------|---------|
| Invalid NPI format | NPI does not pass checksum validation | 10-digit number failing Luhn algorithm |
| Deactivated NPI | NPI is listed as deactivated in NPPES | Provider NPI terminated |
| NPI/TIN mismatch | NPI is not associated with the TIN on the claim | Individual NPI under a different group TIN |
| NPI not enrolled with payer | Provider is not credentialed with the billing payer | NPI not in payer's provider directory |

### 2.6 Invalid Taxonomy Code

| Edit | Description | Example |
|------|-------------|---------|
| Missing taxonomy | No taxonomy code on the claim when required | Claim for professional service without taxonomy |
| Invalid taxonomy format | Taxonomy codes must be 10 characters (alphanumeric) | "207R00000X" format violation |
| Taxonomy not matching specialty | The taxonomy code does not match the provider's enrolled specialty | Internal medicine taxonomy on a cardiologist's claim |
| Multiple taxonomies on same claim | Conflicting taxonomy codes on different lines of same claim | 207R (Internal Medicine) on line 1 and 207L (Anesthesiology) on line 2 |

### Common Taxonomy Codes

| Taxonomy Code | Description |
|---------------|-------------|
| **207R00000X** | Internal Medicine |
| **207L00000X** | Anesthesiology |
| **207P00000X** | Emergency Medicine |
| **207Q00000X** | Family Medicine |
| **207V00000X** | Obstetrics & Gynecology |
| **207X00000X** | Orthopaedic Surgery |
| **208D00000X** | General Practice |
| **2085R0202X** | Diagnostic Radiology |
| **207RC0000X** | Cardiovascular Disease |
| **363L00000X** | Nurse Practitioner |
| **363A00000X** | Physician Assistant |
| **208000000X** | Pediatrics |

### 2.7 Invalid Place of Service (POS)

| Edit | Description | Example |
|------|-------------|---------|
| POS missing | No place of service code on the claim | Claim without POS for professional service |
| POS invalid | POS code does not exist in the CMS POS code set | POS code 99 on a professional claim |
| POS/CPT mismatch | Procedure code not typically performed at that POS | 99221 (initial inpatient care) with POS 11 (office) |
| POS/Provider mismatch | Provider cannot bill for services at that POS | Provider not credentialed at hospital POS 21 |

### CMS Place of Service Codes

| POS Code | Description | Typical Services |
|----------|-------------|-----------------|
| **11** | Office | Outpatient E/M, procedures in office |
| **12** | Home | Home health, DME |
| **21** | Inpatient Hospital | Inpatient surgery, hospital visits |
| **22** | Outpatient Hospital | Outpatient surgery, ER visits |
| **23** | Emergency Room - Hospital | ER encounters |
| **24** | Ambulatory Surgical Center | Outpatient surgeries |
| **25** | Birthing Center | Obstetric services |
| **26** | Military Treatment Facility | Services by uniformed providers |
| **31** | Skilled Nursing Facility | SNF care |
| **32** | Nursing Facility | Custodial nursing care |
| **34** | Hospice | Hospice care |
| **41** | Ambulance - Land | Ground ambulance transport |
| **51** | Inpatient Psychiatric Facility | Inpatient psych care |
| **54** | Intermediate Care Facility/IDD | ICF for intellectual disabilities |
| **55** | Residential Substance Abuse Facility | Rehab for substance abuse |
| **56** | Psychiatric Residential Treatment Center | Residential psych care |
| **61** | Comprehensive Inpatient Rehab | Inpatient rehab |
| **65** | End-Stage Renal Disease Treatment Facility | Dialysis center |
| **71** | State or Local Public Health Clinic | Public health services |
| **72** | Rural Health Clinic | RHC services |
| **81** | Independent Laboratory | Lab specimens drawn |
| **99** | Other Place of Service | Not elsewhere classified |

### POS Code to Code Type Validation

| CPT Code Range | Valid POS | Invalid POS |
|----------------|-----------|-------------|
| 99201-99215 (Office/Outpatient E/M) | 11, 22 | 21 |
| 99221-99239 (Hospital E/M) | 21, 22 | 11, 12 |
| 99281-99285 (ED E/M) | 23 | 11, 21, 22 |
| 99304-99310 (Nursing Facility) | 31, 32 | 11, 21 |
| 99324-99337 (Nursing Facility) | 31, 32 | 11, 21 |
| 99341-99350 (Home) | 12 | 11, 21 |
| 10021-69990 (Surgical) | 11, 21, 22, 23, 24 | Varies by procedure |

### 2.8 Referring Provider Validation

| Edit | Description |
|------|-------------|
| Missing referring provider | Required for certain services (e.g., imaging, lab, therapy) |
| Referring provider NPI invalid | NPI fails validation |
| Referring provider deactivated | NPI deactivated in NPPES |
| Referring provider not enrolled | Provider not credentialed with the billing payer |
| Referring/ordering mismatch | Ordering provider differs from referring when order is required |

### When Referring Provider Is Required

- Diagnostic imaging services (radiology, MRI, CT, ultrasound)
- Laboratory services
- Physical, occupational, and speech therapy
- Durable medical equipment
- Home health services
- Specialty referral consultations
- Radiation oncology

---

## 3. Place of Service (POS) Code Reference

### Full POS Code Table

| Code | Name | Description |
|------|------|-------------|
| 01 | Pharmacy | A facility where drugs and medicines are dispensed |
| 02 | Telehealth | Services provided via telecommunications, patient not present |
| 03 | School | Services provided in an educational setting |
| 04 | Homeless Shelter | Services in a shelter for homeless individuals |
| 05 | Indian Health Service | Free-standing facility operated by IHS |
| 06 | Indian Health Service - Provider-based | Provider-based location operated by IHS |
| 07 | Tribal 638 Facility | Facility operated by tribe under P.L. 93-638 |
| 08 | Mobile Unit | Services in a vehicle designed for care |
| 09 | Correctional Facility | Services in a prison or jail |
| 11 | Office | Provider's office or clinic |
| 12 | Home | Patient's residence |
| 13 | Assisted Living Facility | Residential setting with supportive services |
| 14 | Group Home | Residential home for specific populations |
| 15 | Mobile Unit (Alternate) | Temporary mobile unit |
| 16 | Temporary Lodging | Temporary housing for treatment |
| 17 | Walk-in Retail Health Clinic | Retail clinic in pharmacy or store |
| 18 | Place of Employment - Worksite | Services at employer location |
| 19 | Off Campus - Outpatient Hospital | Hospital outpatient at non-hospital location |
| 20 | Urgent Care Facility | Walk-in urgent care |
| 21 | Inpatient Hospital | Hospital inpatient |
| 22 | Outpatient Hospital | Hospital outpatient department |
| 23 | Emergency Room - Hospital | Hospital emergency department |
| 24 | Ambulatory Surgical Center | Free-standing surgery center |
| 25 | Birthing Center | Free-standing birthing center |
| 26 | Military Treatment Facility | Military medical facility |
| 27 | Satellite/Federally Qualified Health Center | FQHC satellite |
| 28 | Community Mental Health Center | CMHC facility |
| 29 | VA Facility | Veterans Affairs facility |
| 30 | Comprehensive Outpatient Rehab | CORF facility |
| 31 | Skilled Nursing Facility | SNF (Medicare-certified) |
| 32 | Nursing Facility | Nursing facility (non-SNF) |
| 33 | Custodial Care Facility | Custodial care |
| 34 | Hospice | Freestanding hospice facility |
| 35 | Adult Day Care | Day program for adults |
| 36 | Urgent Care - Hospital Based | Hospital-based urgent care |
| 37 | Psychiatric Day Treatment | Partial hospitalization program |
| 38 | Psychiatric Residential Treatment | Residential treatment center |
| 39 | Federally Qualified Health Center | FQHC main site |
| 40 | Indian Health Service - Hospital | IHS hospital |
| 41 | Ambulance - Land | Ground ambulance |
| 42 | Ambulance - Air or Water | Air or water ambulance |
| 49 | Independent Clinic | Free-standing clinic |
| 50 | Outpatient Rehabilitation | Facility-based rehab |
| 51 | Inpatient Psychiatric Facility | Psychiatric hospital |
| 52 | Psychiatric Facility - Partial Hospitalization | PHP |
| 53 | Community Mental Health Center | CMHC |
| 54 | Intermediate Care Facility/IDD | ICF for intellectual disabilities |
| 55 | Residential Substance Abuse Facility | Substance abuse residential |
| 56 | Psychiatric Residential Treatment | Psychiatric residential treatment |
| 57 | Non-residential Substance Abuse Facility | Substance abuse non-residential |
| 58 | Non-residential Opioid Treatment Facility | Opioid treatment program |
| 60 | Mass Immunization Center | Mass vaccine clinic |
| 61 | Comprehensive Inpatient Rehabilitation | Inpatient rehabilitation hospital |
| 62 | Comprehensive Outpatient Rehabilitation | CORF |
| 65 | ESRD Treatment Facility | Dialysis center |
| 71 | Public Health Clinic | State/local public health clinic |
| 72 | Rural Health Clinic | RHC |
| 81 | Independent Laboratory | Independent lab |
| 99 | Other Place of Service | Other |

---

## 4. Coordination of Benefits (COB) in Scrubber

### How Scrubbers Handle COB

Coordination of Benefits validation ensures the correct payer is billed in the correct order. The scrubber checks:

| Check | Description |
|-------|-------------|
| **Primary Payer Identification** | Is the payer being billed the correct primary payer? |
| **Secondary Claim Logic** | Has the primary claim been processed? Does the secondary claim show primary payment? |
| **COB Field Validation** | Are COB fields (other insurance information) populated correctly? |
| **MSP (Medicare Secondary Payer) Validation** | Is Medicare correctly designated as primary or secondary? |
| **EGHP/ESRD Verification** | Is the patient's employer group health plan the primary payer for ESRD? |
| **GHP/LTSS Verification** | Is the patient's group health plan the primary payer for disability? |
| **Auto/No-fault/Liability** | Is there third-party liability that should be primary? |
| **Workers' Compensation** | Is there a workers' comp claim that should be primary? |

### COB Determination Logic

```
Step 1: Does the patient have other insurance?
  |-- YES:
       Step 2: Determine primary payer using NAIC coordination rules
         |-- Patient is covered by employer group plan > Medicare? -> GHP is primary
         |-- Patient has ESRD and COB period has passed? -> Medicare is primary
         |-- Patient has auto/liability claim? -> Auto/liability is primary
         |-- Patient has workers' comp? -> Workers' comp is primary
         |-- Patient has primary and secondary commercial plans? -> Oldest plan is primary
       Step 3: Validate the claim is being submitted to the correct order
  |-- NO: Proceed as primary claim submission
```

### MSP (Medicare Secondary Payer) Working Aged

For patients aged 65+ with employer group health plan (EGHP) coverage:

| Scenario | Primary | Secondary |
|----------|---------|-----------|
| Patient 65+, active employee, EGHP >= 20 employees | EGHP | Medicare |
| Patient 65+, active employee, EGHP < 20 employees | Medicare | EGHP |
| Patient 65+, retired, no EGHP | Medicare | N/A |
| Patient 65+, covered by spouse's EGHP >= 20 employees | EGHP | Medicare |

---

## 5. Claim Scrubber Workflow

### Standard Scrubbing Process

```
Claim Created in EHR/Practice Management System
  |
  v
Level 1: Format Validation
  |-- X12 structure valid?
  |-- Required segments present?
  |-- Data types correct (dates, amounts, codes)?
  |
  v
Level 2: Required Field Validation
  |-- Provider NPI present and valid?
  |-- Patient demographics complete?
  |-- Diagnosis codes present?
  |-- Procedure codes present?
  |-- Dates of service present?
  |-- POS present?
  |
  v
Level 3: Code Validation
  |-- CPT/HCPCS codes valid and active?
  |-- ICD-10 codes valid and active?
  |-- Modifiers valid for codes?
  |-- NPI checksum valid?
  |-- Taxonomy code valid?
  |
  v
Level 4: Code-to-Code Validation
  |-- NCCI PTP edits checked
  |-- NCCI MUE edits checked
  |-- Diagnosis-to-procedure match
  |-- Add-on code with primary code present
  |-- Mutually exclusive code check
  |
  v
Level 5: Provider Validation
  |-- NPI active in NPPES
  |-- Taxonomy matches specialty
  |-- License status valid
  |-- Provider enrolled with payer
  |
  v
Level 6: Patient Validation
  |-- Eligibility verified (if available)
  |-- Coverage dates valid
  |-- COB determined correctly
  |
  v
Level 7: Payer-Specific Validation
  |-- Payer-specific CPT/HCPCS coverage
  |-- Payer-specific MUE values
  |-- Payer-specific modifier requirements
  |-- Companion guide rules applied
  |
  v
Scrubber Report Generated
  |-- Errors (must fix before submission)
  |-- Warnings (may cause denial)
  |-- Passed (ready for submission)
```

---

## 6. Scrubber Types and Features

### Desktop Scrubber

- Runs locally in practice management software
- Checks standard edits (NCCI, gender, age, invalid codes)
- Does not have access to real-time payer data
- Lower cost, limited features

### Cloud/Web-Based Scrubber

- Runs on clearinghouse or vendor server
- Checks standard edits plus payer-specific rules
- May include real-time eligibility checks
- Regular updates from clearinghouse
- Higher cost, more comprehensive

### Embedded Scrubber (EHR Module)

- Built into the EHR or practice management system
- Checks edits in real-time as the claim is created
- May integrate with clearinghouse for payer-specific checks
- Lower learning curve for providers

### Clearinghouse Scrubber

- Applied when the claim is sent to the clearinghouse
- Payer-specific editing based on companion guides
- Real-time 999/277CA response processing
- Can catch errors before they reach the payer
- Most comprehensive for multi-payer providers

---

## 7. Agent Training: Q&A Pairs for Scrubber Logic

**Q: What is the purpose of a pre-submission claim scrubber?**

**A:** A pre-submission claim scrubber validates healthcare claims against a comprehensive set of editing rules before they are sent to a payer. Its purpose is to detect errors, omissions, and inconsistencies that would result in claim denials. By catching these issues before submission, the scrubber reduces denial rates, accelerates reimbursement, minimizes administrative rework, and improves revenue cycle efficiency.

---

**Q: What is the difference between a scrubber error and a scrubber warning?**

**A:** A scrubber error is a critical issue that will likely result in a claim rejection or denial if the claim is submitted without correction. An error must be fixed before the claim can be submitted. A scrubber warning is a potential issue that may or may not result in a denial, depending on the payer's specific policies. Warnings should be reviewed and addressed but do not necessarily prevent submission. For example, a missing modifier on a code that may need one is a warning, while an invalid NPI is an error.

---

**Q: What POS code should be used for a service performed in the hospital emergency department?**

**A:** POS 23 (Emergency Room - Hospital) should be used for services performed in the hospital emergency department. This includes both professional E/M services (99281-99285) and procedures performed in the ED setting. Using the wrong POS, such as POS 11 (Office) or POS 22 (Outpatient Hospital), for ED services can result in denial or incorrect payment.

---

**Q: Why would a claim be rejected for a "missing taxonomy code"?**

**A:** A claim can be rejected for a missing taxonomy code because many payers require the taxonomy code to identify the provider's specialty for reimbursement purposes. The taxonomy code is a 10-character alphanumeric code (e.g., 207R00000X for Internal Medicine) that classifies the provider by specialty, license type, and practice setting. Payers use taxonomy codes to determine which fee schedule applies, validate provider credentials, and apply specialty-specific editing rules. Without the taxonomy code, the payer cannot accurately process the claim.

---

**Q: What is the Luhn algorithm in the context of NPI validation?**

**A:** The Luhn algorithm (also known as the "modulus 10" or "mod 10" algorithm) is a checksum formula used to validate National Provider Identifiers (NPIs). An NPI is a 10-digit number. The Luhn algorithm verifies that the NPI is mathematically valid by checking the sum of the digits against a known check digit. If the NPI fails the Luhn check, it is not a valid NPI. The scrubber applies the Luhn algorithm to catch accidental keystroke errors or invalid NPIs before the claim is submitted.

---

**Q: What should a provider do if a scrubber flags a "diagnosis-to-procedure mismatch"?**

**A:** When a scrubber flags a diagnosis-to-procedure mismatch, the provider should: verify that the correct ICD-10 diagnosis code is selected (is there a more appropriate code?), confirm the CPT code is correct for the service performed (was the wrong code chosen?), check whether the diagnosis code is in the LCD's covered codes list for that CPT/HCPCS code, review the medical record to ensure the diagnosis-to-procedure relationship is clinically valid, and if the diagnosis code is correct and clinical support exists, document the reasoning and proceed with submission (or add a supporting diagnosis code). If the mismatch is real, the code should be corrected before submission.

---

**Q: How does a scrubber validate Coordination of Benefits (COB)?**

**A:** A scrubber validates COB by checking the patient's insurance information on file to determine whether the payer being billed is the correct primary payer. It checks for other insurance on record, evaluates the patient's employment status, age, and eligibility for other coverage, applies the NAIC coordination rules (e.g., the birthday rule, Medicare secondary payer rules, workers' compensation priority), and verifies that submitted COB fields match the expected order. If the claim is being submitted to the wrong payer or in the wrong order, the scrubber flags it for correction.

---

**Q: What is an NPI/TIN mismatch and why does it cause denials?**

**A:** An NPI/TIN mismatch occurs when the National Provider Identifier (NPI) submitted on a claim is not associated with the Tax Identification Number (TIN) on the same claim. This can happen when a provider changes groups, a provider's NPI is under a different tax ID than the billing TIN, or the provider's enrollment information is outdated. Payers validate NPI-to-TIN relationships. If the NPI and TIN do not match in the payer's system, the claim is denied or rejected. This is a common issue when providers work at multiple locations under different tax IDs.

---

**Q: Can a claim be scrubbed and accepted by the clearinghouse but denied by the payer?**

**A:** Yes. Clearinghouse scrubbing checks formatting, required fields, and standard edit rules, but cannot catch all payer-specific issues. A claim can pass the clearinghouse scrub (format and basic edits are correct) but still be denied by the payer for medical necessity, benefit limitations, or policy-specific coverage decisions. Additionally, some payer-specific edits are not available in the clearinghouse scrubber database. Clearinghouse acceptance means the claim is formatted correctly and passes standard edits, not that the claim will be paid.

---

**Q: What is the difference between a clearinghouse rejection and a payer rejection?**

**A:** A clearinghouse rejection occurs when the claim fails the clearinghouse's format or edit validation before being transmitted to the payer. The clearinghouse returns the claim with an error report (often a 999 rejection or a clearinghouse-specific error). The claim never reaches the payer. A payer rejection occurs after the claim is accepted by the clearinghouse and submitted to the payer. The payer's system rejects the claim due to format errors, missing data, or invalid codes. The payer returns a 999 or 277CA rejection. Clearinghouse rejections are typically easier to fix (format/EDI issues), while payer rejections may require more complex corrections.

---

**Q: What is the correct taxonomy code for a Nurse Practitioner?**

**A:** The correct taxonomy code for a Nurse Practitioner is **363L00000X**. The taxonomy should match the provider's enrolled specialty and license type. Using a different taxonomy code (e.g., 363A00000X for Physician Assistant) on a Nurse Practitioner's claim can result in incorrect payment rates or denial. The taxonomy code must be the full 10-character alphanumeric code, including the check digit (the final "X").

---

**Q: Why does POS 11 (Office) cause a scrubber error for CPT 99221?**

**A:** POS 11 (Office) causes a scrubber error for CPT 99221 because 99221 is an initial inpatient hospital care E/M code. Initial inpatient care codes (99221-99223) are designed for services performed in a hospital inpatient setting. Billing an inpatient care code with an office POS is a mismatch. The correct POS for 99221 is POS 21 (Inpatient Hospital). If the service was actually performed in the office, the provider should use an office/outpatient E/M code (99201-99215) instead.

---

**Q: What is the purpose of the Medicare Secondary Payer (MSP) validation in a scrubber?**

**A:** The Medicare Secondary Payer (MSP) validation in a scrubber ensures that the claim is being submitted to the correct payer in the correct order. MSP rules determine whether Medicare is the primary or secondary payer based on the patient's other insurance coverage. The scrubber checks whether the patient has group health plan coverage from current employment (GHP), employer group health plan via a working spouse, or other insurance that should be primary (auto, liability, no-fault, workers' compensation). If Medicare is incorrectly billed as primary, the claim will be denied.

---

**Q: What is the maximum number of units of CPT 97530 (therapeutic activities) per day?**

**A:** The MUE (Medically Unlikely Edit) for CPT 97530 (therapeutic activities) is 4 units per patient per date of service. However, the scrubber checks this against the CMS MUE. Some commercial payers may have lower limits. The provider should check both the CMS MUE and the specific payer's MUE value. If the claim is submitted with 5 units, the scrubber should flag it for review. If the claim is submitted to Medicare with 5 units, 4 units will be paid (if medically necessary) and 1 unit will be denied as exceeding the MUE.

---

**Q: How is a referring provider validated in the claim scrubber?**

**A:** The referring provider is validated by checking: that the referring provider's NPI is present and passes Luhn algorithm validation; that the NPI is active in NPPES (not deactivated, not deceased); that the referring provider's taxonomy is appropriate for the service ordered; that the referring provider is enrolled with the billing payer; and that the referring provider has an active license. For certain services like imaging, lab, and therapy, a valid referring provider is mandatory. Missing or invalid referring provider NPI will result in a denial.

---

**Q: What does a scrubber check when validating modifiers on a claim?**

**A:** When validating modifiers, the scrubber checks: whether the modifier is valid for the specific CPT/HCPCS code; whether the modifier is used correctly (e.g., modifier 25 only with E/M codes); whether the modifier bypasses NCCI edits correctly (modifier indicator 0 vs 1); whether multiple modifiers on the same line are compatible; whether modifier 50 is used for bilateral procedures when appropriate; whether modifier 59 is used as a last resort (XE/XS/XP/XU preferred); and whether modifier 76/77 is used for repeat procedures.

---

**Q: What triggers a scrubber warning for "modifier 59 used unnecessarily"?**

**A:** A scrubber warning for "modifier 59 used unnecessarily" is triggered when modifier 59 is appended to a CPT code that does not appear in any NCCI PTP edit pair with the other codes on the claim. Modifier 59 signals that a service is distinct and separate from other services on the same date. If there is no underlying edit requiring separation, the modifier is unnecessary and may trigger payer audit risk. Some payers view unnecessary modifier 59 use as a red flag and may review the claim for inappropriate billing.

---

**Q: How does the birthday rule apply in COB validation?**

**A:** The birthday rule is a NAIC standard for determining which parent's insurance is primary for a dependent child. Under the birthday rule, the parent whose birthday (month and day only, not year) falls earlier in the calendar year is the primary insured. For example, if the mother's birthday is May 15 and the father's birthday is November 20, the mother's insurance is primary. The birthday rule applies when both parents have coverage for the child. The scrubber validates the COB fields to ensure the claim is submitted to the correct primary payer based on this rule.

---

**Q: What is the correct taxonomy code for a diagnostic radiologist?**

**A:** The correct taxonomy code for a Diagnostic Radiologist is **2085R0202X** (Radiology - Diagnostic Radiology). This is distinct from 2085U0001X (Radiology - Ultrasound), 2085B0000X (Radiology - Body Imaging), or 2085N0700X (Radiology - Neuroradiology). Using the wrong radiology subspecialty taxonomy can result in incorrect reimbursement or denial. The taxonomy must match the provider's enrolled specialty and the type of service billed.

---

**Q: What happens when a claim passes the scrubber but is later denied for medical necessity?**

**A:** If a claim passes the scrubber but is later denied for medical necessity, this typically means the scrubber's standard edits (format, code validation, NCCI) were passed, but the claim failed the payer's clinical review. Scrubbers validate coding and formatting rules, not necessarily clinical judgment. To reduce medical necessity denials, the provider's pre-submission workflow should include a medical necessity check, typically by comparing the diagnosis code against the relevant LCD or payer medical policy. Some advanced scrubbers include this check; others do not.

---

**Q: What is an "invalid NPI format" error?**

**A:** An "invalid NPI format" error means the NPI submitted on the claim does not pass the standard NPI format requirements. NPIs are 10-digit numbers (the last digit is a check digit). The first digit must be 1 (for individual providers) or 2 (for organizational providers). The NPI must pass the Luhn checksum algorithm. Common causes of invalid NPI format errors include: entering a 9-digit number, entering the NPI with leading zeros removed, typing the wrong number, entering a TIN instead of an NPI, or using an expired/old NPI.

---

**Q: How does a scrubber handle add-on code validation?**

**A:** When validating add-on codes (identified by the "+" symbol in CPT), the scrubber checks: that a valid primary code is present on the same claim; that the primary code is appropriate for the add-on code (the scrubber maintains a list of valid primary-add-on pairings); and that the add-on code units do not exceed the MUE. If an add-on code is submitted without its primary code, the scrubber flags it as an error. The add-on code cannot be paid without the primary code.

---

**Q: What is the difference between an NPI/TIN mismatch and an NPI not enrolled with the payer?**

**A:** An NPI/TIN mismatch occurs when the NPI and Tax Identification Number on the claim do not match the pair on file with the payer's enrollment database. The NPI is valid and the TIN is valid, but they are not associated with each other. "NPI not enrolled with the payer" means the NPI (or the NPI/TIN pair) does not exist in the payer's provider directory at all. The provider may not have completed credentialing with that payer, or credentialing may have lapsed. Both will result in denial, but the root cause and solution are different.

---

**Q: How can a provider use scrubber reports to reduce denial rates?**

**A:** Providers can use scrubber reports to reduce denial rates by: reviewing the most common scrubber errors across all claims and identifying patterns; training providers and billers on the top error types; adding missing fields (like taxonomy codes, referring provider NPI) to EHR templates; updating fee schedules and modifier usage rules; performing regular scrubber rule updates (quarterly for NCCI, as needed for payer rules); creating worklists for scrubber warnings that require manual review; and tracking scrubber error trends over time to measure the impact of improvements.

---

**Q: What is the role of the scrubber in billing for services requiring a referring provider?**

**A:** For services requiring a referring provider (such as diagnostic imaging, lab tests, and therapy), the scrubber validates that: the claim includes a referring/ordering provider NPI in the appropriate loop (Loop 2317B for referring provider); the referring provider's NPI passes format validation; the referring provider's NPI is active in NPPES; and the referring provider is enrolled with the billing payer. If the referring provider information is missing or invalid, the scrubber generates an error that must be resolved before the claim can be submitted.

---

**Q: Can a scrubber validate that a procedure was pre-authorized?**

**A:** Some advanced scrubbers can validate pre-authorization requirements by checking: whether the CPT/HCPCS code requires pre-authorization per the payer's medical policy; whether a valid pre-authorization number is entered for the claim; whether the pre-authorization number is in the correct format; and whether the pre-authorization is still valid (not expired, not exhausted). However, not all scrubbers have this capability. Providers may need to manually verify pre-authorization requirements or use a separate pre-authorization management tool.

---

**Q: What POS code should be used for telehealth services?**

**A:** For telehealth services, POS 02 (Telehealth) should be used. This POS code was introduced to identify encounters where the patient is not physically present with the provider. Using POS 02 instead of the actual patient location (e.g., POS 11 for a patient at home) ensures proper payment for telehealth services. Some payers and timeframes require specific telehealth modifiers (95 or GT) in addition to POS 02. The scrubber should validate that the POS 02 is used with appropriate telehealth codes and modifiers.

---

**Q: Why does a scrubber flag repeated use of the same CPT code on the same date?**

**A:** The scrubber flags repeated use of the same CPT code on the same date because it may indicate unbundling, duplicate billing, or MUE violations. For example, two lines of CPT 93005 (ECG tracing) on the same date would be flagged because the MUE is 1. Two lines of CPT 97530 (therapeutic activities) on the same date would be flagged for review even if the total units do not exceed the MUE, because the provider should submit a single line with the total units rather than multiple lines with partial units. The scrubber checks for both MUE violations and proper claim formatting.

---

**Q: Can a claim pass the scrubber with a "modifier 25" used correctly?**

**A:** Yes. Modifier 25 (Significant, Separately Identifiable E/M Service) is a valid modifier when a significant, separately identifiable E/M service is provided on the same day as a procedure. The scrubber checks that modifier 25 is appended only to an E/M code (99201-99499 range), that the date of service has both an E/M code with modifier 25 and a procedure code, and that the documentation supports the separate E/M service. When used correctly, the claim passes the scrubber. Incorrect modifier 25 use (e.g., on a procedural code or without an associated procedure) will trigger a scrubber error.

---

**Q: How is place of service verified for professional claims?**

**A:** Place of service (POS) is verified for professional claims by checking: POS code is present and valid (must be in CMS POS code set); POS code is valid for date of service (some POS codes changed historically); POS code matches the CPT/HCPCS code type (e.g., inpatient POS with inpatient E/M codes); and POS code is consistent with the rendering provider's practice setting. The scrubber may also check for common mismatches, such as POS 24 (Ambulatory Surgical Center) with E/M codes, or POS 21 (Inpatient Hospital) with office visit codes (99201-99215).

---

**Q: What is the role of the scrubber in preventing duplicate claim submissions?**

**A:** The scrubber prevents duplicate claim submissions by: checking whether a claim with the same patient, provider, date of service, and CPT/HCPCS code has already been submitted; flagging potential duplicates for manual review; preventing automatic resubmission of previously submitted claims; and tracking the submission status of each claim in the billing system. This prevents the provider from unknowingly submitting a duplicate claim that would be denied or result in an overpayment that must be refunded.

---

**Q: How does the scrubber handle CMS quarterly NCCI update integration?**

**A:** The scrubber handles CMS quarterly NCCI updates by: downloading or receiving the updated NCCI edit files from CMS; applying new PTP edits, revised modifier indicators, and updated MUE values; removing deleted edits; validating that the update is complete and consistent; and applying new edits to all pending and future claims. Providers should update their scrubber software before each quarter's effective date (January 1, April 1, July 1, October 1). Failure to update can result in passing claims that should fail edits, or failing claims that should pass edits.

---

**Q: Can a scrubber detect unbundling of surgical packages?**

**A:** Yes. Advanced scrubbers can detect unbundling of surgical packages by checking: whether component codes of a surgical package are being billed separately instead of the comprehensive code; whether E/M services are billed within the global period without appropriate modifiers (24, 25, 57); and whether procedures integral to the surgery are billed separately (e.g., skin closure, surgical approach, exploration). The scrubber references both NCCI PTP edits and payer-specific surgical package policies to detect unbundling. These edits help prevent the overpayment that results from fragmented billing.