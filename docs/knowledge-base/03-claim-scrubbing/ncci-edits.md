# NCCI Edits (National Correct Coding Initiative)

## Overview

The National Correct Coding Initiative (NCCI) was developed by the Centers for Medicare & Medicaid Services (CMS) to promote correct coding and prevent improper payments. NCCI edits are automated claim edits that identify code pairs and code-to-unit combinations that should not be billed together or should not exceed certain service limits. Private payers commonly adopt NCCI edits or implement their own derivatives.

NCCI edits are divided into two main categories: Procedure-to-Procedure (PTP) edits and Medically Unlikely Edits (MUEs).

---

## 1. NCCI PTP (Procedure-to-Procedure) Edits

PTP edits define code pairs that cannot be reported together for the same patient on the same date of service by the same provider. Each edit consists of a Column 1 code (comprehensive/bundling code) and a Column 2 code (component code that is bundled into Column 1).

### Column 1 / Column 2 Structure

| Element | Description |
|---------|-------------|
| **Column 1 Code** | The comprehensive or primary procedure code. This code represents the more inclusive service. |
| **Column 2 Code** | The component or lesser procedure code. This code describes a service that is an integral part of the Column 1 code. |
| **Effective Date** | The date the edit becomes active. |
| **Deletion Date** | The date the edit is deleted (if applicable). |
| **Modifier Indicator** | 0 = Modifier cannot be used to bypass the edit. 1 = An allowed modifier may be used to bypass the edit. |

### Example PTP Edits

| Column 1 | Column 2 | Modifier Indicator | Rationale |
|----------|----------|--------------------|-----------|
| 27130 (Total Hip Arthroplasty) | 27236 (Open Treatment Femoral Fracture) | 0 | Femoral head removal is integral to hip replacement |
| 49505 (Repair Inguinal Hernia) | 49520 (Repair Recurrent Inguinal Hernia) | 0 | Cannot bill both primary and recurrent repair on same side |
| 93458 (Cardiac Cath with LHC) | 93453 (Combined RHC/LHC) | 0 | Comprehensive code includes the component |
| 93000 (ECG Complete) | 93005 (ECG Tracing Only) | 0 | 93000 = 93005 + 93010; components are bundled |

---

## 2. Medically Unlikely Edits (MUEs)

MUEs define the maximum number of units of service for a single CPT/HCPCS code that a provider can report for a single patient on a single date of service. MUEs are published by CMS and updated quarterly.

### MUE Categories

| Category | Description |
|----------|-------------|
| **Date-of-Service MUE** | Maximum units per patient per date of service. This is the most common type. |
| **Claim-Span/Stay MUE** | Maximum units across a span of dates (e.g., an inpatient stay). |
| **Patient-Specific MUE** | Maximum units per patient lifetime (rare, used for certain devices). |
| **Line-Level Edits** | Edits applied at the individual claim line rather than the claim header. |

### Example MUE Values

| CPT Code | Description | MUE | Rationale |
|----------|-------------|-----|-----------|
| 93005 | ECG Tracing | 1 | Only one ECG per day is medically reasonable |
| 97530 | Therapeutic Activities | 4 | Maximum 4 units per day for this timed service |
| 99213 | Office Visit, Level 3 | 1 | Only one E/M visit per provider per day |
| 12001 | Simple Repair of Laceration | 6 | Maximum laceration repairs per patient per day |
| 80048 | Basic Metabolic Panel | 1 | Only one panel per day |
| 96365 | IV Infusion Initial | 2 | Maximum 2 initial IV infusions per day |
| 93306 | Echo Complete | 1 | Only one echo per day |
| 93015 | Cardiovascular Stress Test | 1 | Only one stress test per day |

### MUE Adjudication Logic

When a claim is submitted with units exceeding the MUE for a code:

1. **Line-level adjudication**: Each claim line is evaluated independently. If a single line has units exceeding the MUE, the excess units are denied.
2. **Aggregate adjudication**: If multiple lines report the same CPT code, their total units are summed. If the total exceeds the MUE, some or all units may be denied.
3. **Date-of-service grouping**: Units are grouped by date of service. The MUE is applied per date, not per claim.

Example: If CPT 99304 (nursing facility initial care) has an MUE of 1, submitting a claim with 2 units will result in 1 unit being denied.

### Patient-Specific MUEs

Some MUEs are defined per patient lifetime rather than per date of service. These are rare and typically apply to implants or devices. For example, CPT 33227 (insertion of pacemaker pulse generator) has a patient-specific MUE of 1 because a patient would only have one initial insertion.

---

## 3. NCCI Modifier Indicators

Modifier indicators determine whether a PTP edit can be bypassed using an appropriate modifier.

### Modifier Indicator 0

- **No modifier is allowed** to bypass the edit.
- The Column 2 code is considered an integral component of the Column 1 code.
- If both codes are reported, the Column 2 code will be denied.
- Example: CPT 27130 (THA) and 27236 (femoral fracture treatment) -- modifier indicator 0, cannot be bypassed.

### Modifier Indicator 1

- An **allowed modifier may be used** to bypass the edit.
- The provider must document that the two procedures were performed at distinct anatomical sites, separate encounters, by different practitioners, or in unusual circumstances.
- Common modifiers: 59, XE, XS, XP, XU, 76, 77, 91, 99
- Example: CPT 27447 (Total Knee Arthroplasty) and 27360 (Partial Excision of Femur) -- modifier indicator 1, can be bypassed if on opposite legs.

### Modifier 59 -- Distinct Procedural Service

Modifier 59 is used to identify procedures that are not normally reported together but are appropriate under the circumstances. CMS considers modifier 59 a "last resort" modifier that should only be used when no more specific modifier describes the relationship.

Proper use of modifier 59 requires documentation of one of the following:

1. **Different anatomical site**: The two procedures were performed on different organs or different anatomical regions.
2. **Different encounter**: The two procedures occurred during separate patient encounters on the same day.
3. **Different procedure**: The two procedures are distinctly different and not integral to each other.
4. **Separate incision/excision**: The two procedures required separate incisions or excisions.

### X{EPSU} Modifiers (CMS 2017)

CMS introduced these modifiers in 2017 to provide more specific alternatives to modifier 59:

| Modifier | Description | When to Use |
|----------|-------------|-------------|
| **XE** | Separate Encounter | A service that is distinct because it occurred during a separate encounter |
| **XS** | Separate Structure | A service that is distinct because it was performed on a separate organ/structure |
| **XP** | Separate Practitioner | A service that is distinct because it was performed by a different practitioner |
| **XU** | Unusual Non-Overlapping Service | A service that is distinct because it does not overlap usual components of the main service |

Priority order for using X{EPSU} modifiers:

1. Use XE, XS, XP, or XU when the circumstances match the specific definition.
2. Use modifier 59 only when none of the X{EPSU} modifiers apply.

### Other Modifiers Used to Bypass NCCI Edits

| Modifier | Description | Use Case |
|----------|-------------|----------|
| **76** | Repeat Procedure by Same Physician | Same procedure, same day, different session |
| **77** | Repeat Procedure by Different Physician | Same procedure, same day, different provider |
| **78** | Unplanned Return to OR | Related procedure during postoperative period |
| **79** | Unrelated Procedure | Unrelated procedure during postoperative period |
| **91** | Repeat Clinical Diagnostic Lab Test | Same lab test, same day, different specimen |
| **99** | Multiple Modifiers | Used when more than four modifiers are needed |

---

## 4. Add-on Code Editing

Add-on codes (indicated with a "+" symbol in CPT) describe services that are performed in addition to a primary procedure. They **cannot be reported without the primary code**.

### Add-on Code Rules

1. The primary code must be reported on the same claim.
2. Add-on codes themselves do not have NCCI PTP edits with their primary code.
3. Add-on codes may have MUE values.
4. Some add-on codes can be reported multiple times (e.g., +69990 for microsurgical microscope).
5. Example: CPT +22610 (interbody fusion at L5-S1) cannot be reported without 22612 (posterior lumbar fusion) or similar primary fusion code.

### Example Add-on Codes and Their Primary Codes

| Add-on Code | Description | Typical Primary Codes |
|-------------|-------------|----------------------|
| +22552 | Additional Cervical Interspace | 22551 (Anterior Cervical Discectomy & Fusion) |
| +22632 | Additional Posterior Lumbar Segment | 22630 (Posterior Lumbar Interbody Fusion) |
| +69990 | Operating Microscope | Various surgical codes |
| +36218 | Additional Extremity Artery Cath | 36200, 36216, 36217 |
| +47563 | Lap Cholecystectomy with Cholangiogram | 47562 (Lap Cholecystectomy) |

---

## 5. Mutually Exclusive Edits

Mutually exclusive edits identify code pairs that cannot be reported together because they describe procedures that cannot reasonably be performed on the same patient on the same date of service.

### Examples

| Code 1 | Code 2 | Rationale |
|--------|--------|-----------|
| 27130 (Total Hip Arthroplasty) | 27236 (Open Treatment Femoral Fracture) | Cannot do both on same hip |
| 44950 (Appendectomy) | 44960 (Appendectomy with Abscess) | Cannot do both on same appendix |
| 47562 (Lap Cholecystectomy) | 47600 (Open Cholecystectomy) | Cannot do both laparoscopic and open |
| 93000 (Complete ECG) | 93010 (ECG Interpretation Only) | Comprehensive includes component |

Mutually exclusive edits have modifier indicator 0 -- modifiers cannot be used to bypass them.

---

## 6. Gender Edits

Gender edits flag procedure codes that are incompatible with the patient's gender as recorded in the claim.

### Examples

| CPT Code | Description | Valid Gender |
|----------|-------------|--------------|
| 58661 | Laparoscopy for removal of adnexal structures | Female |
| 76856 | Pelvic ultrasound | Female (non-obstetric use) |
| 84163 | AMH (Anti-Mullerian Hormone) | Female |
| 84154 | PSA Total | Male |
| 76817 | Transvaginal ultrasound | Female |
| 55821 | Prostatectomy | Male |

### Handling Gender Edit Failures

- A gender edit failure typically requires correcting the patient gender in the system or verifying that the code assignment is correct.
- Certain gender edits can be overridden if the patient is transgender and the procedure is medically necessary for the documented diagnosis.
- Some payers allow modifier KX (requirements met) to indicate medical policy requirements have been satisfied.

---

## 7. Age Edits

Age edits flag procedure codes that are inappropriate for the patient's age.

### Examples

| CPT Code | Description | Typical Age Restriction |
|----------|-------------|------------------------|
| 99381 | Preventive visit, newborn | Under 1 year |
| 99382 | Preventive visit, 1-4 years | 12-47 months |
| 99391 | Preventive visit, 5-11 years | 5-11 years |
| 99397 | Preventive visit, 65+ | 65 years and older |
| 93306 | Echo complete | Generally age 0+ but some payers restrict to 2+ |
| 27130 | Total Hip Arthroplasty | Rarely performed under age 18 |
| 47562 | Lap Cholecystectomy | Rarely performed under age 1 |

### Handling Age Edit Failures

- Age edit failures may require documentation of medical necessity for the age group.
- Some age edits are payer-specific guidelines, not absolute denials.
- Providing appropriate diagnosis codes that justify the service for the patient's age may resolve the edit.

---

## 8. Bundling vs Unbundling

### Definitions

- **Bundling**: Combining multiple component services into a single comprehensive code. This is the correct coding practice when a single code describes the entire procedure.
- **Unbundling (Inappropriate)**: Separating a comprehensive procedure into component parts and billing each component separately. This results in higher reimbursement than the comprehensive code allows.

### Examples of Inappropriate Unbundling

| Inappropriate Unbundling | Correct Coding | Savings to Payer |
|--------------------------|----------------|------------------|
| 27130 + 27236 (Total hip + femoral head removal separately) | 27130 only | 27236 denied |
| 49505 + 49507 (Inguinal hernia repair + initial/recurrent) | 49505 or 49507 | Both cannot be billed together |
| 93005 + 93010 (Tracing + interpretation separately) | 93000 (Complete ECG) | Bundled saves ~\$10-15 |
| 47562 + 47563 (Lap chole + lap chole with cholangiogram) | 47563 only | Cannot bill both |
| 27447 + 27580 (TKA + knee fusion) | 27447 only | Mutually exclusive |

### Common Unbundling Scenarios

1. **Fragmenting a colonoscopy**: Billing 45378 (diagnostic colonoscopy) + 45380 (with biopsy) + 45384 (with snare) when the entire service is described by 45385 (colonoscopy with polypectomy).
2. **Separating a surgical package**: Billing the surgical code plus individual components of the surgical package (e.g., billing 49505 for hernia repair plus 12031 for skin closure when closure is included).
3. **Billing global period components**: Billing E/M visits unrelated to the surgery within the global period without modifier 24.
4. **Multiple endoscopy rules**: Reporting multiple endoscopic procedures on the same day without applying the multiple endoscopy reduction rules.

---

## 9. Coding Edits Specific to Modifier Usage

### Modifier 51 (Multiple Procedures)

- Modifier 51 is an informational modifier used to identify multiple procedures performed during the same surgical session.
- The primary (highest RVU) procedure is paid at 100%.
- Subsequent procedures are typically paid at 50% of the allowable amount.
- Medicare does not require modifier 51 on claims, but some commercial payers do.

### Modifier 50 (Bilateral Procedure)

- Used when a procedure is performed bilaterally (both sides) during the same session.
- Some codes have a bilateral surgery indicator (1 or 3) in the Medicare Physician Fee Schedule.
- Indicator 1: Can be billed with modifier 50.
- Indicator 0: Bilateral surgery is not allowed.
- Indicator 2: Bilateral payment rule does not apply (e.g., diagnostic tests).
- Indicator 3: Modifier 50 not required -- the code itself describes the bilateral service.

### Modifier 22 (Increased Procedural Service)

- Used when a procedure required substantially greater work than typically required.
- Requires supporting documentation.
- Payer may increase payment by 20-40%.
- Often denied if supporting documentation is insufficient.

### Modifier 25 (Significant, Separately Identifiable E/M Service)

- Used with E/M codes when a significant, separately identifiable E/M service is performed on the same day as a procedure.
- Requires separate documentation of the E/M component.
- One of the most frequently audited modifiers.

---

## 10. NCCI Quarterly Updates

CMS releases updated NCCI edit files quarterly. Providers must stay current with these updates to avoid denials.

### Update Schedule

| Quarter | Release Date | Effective Date |
|---------|-------------|----------------|
| Q1 (January) | Mid-December | January 1 |
| Q2 (April) | Mid-March | April 1 |
| Q3 (July) | Mid-June | July 1 |
| Q4 (October) | Mid-September | October 1 |

### What Changes Quarterly

1. **New PTP edits**: New code pairs are added as new CPT codes are introduced.
2. **Deleted PTP edits**: Some edits are removed when codes become obsolete.
3. **Changed modifier indicators**: Some edits change from indicator 0 to 1 or vice versa.
4. **Updated MUE values**: Some MUE values are adjusted based on claims data.
5. **New MUEs**: New CPT codes receive MUE values.
6. **Deleted MUEs**: MUEs are removed when CPT codes are deleted.

### Impact of Quarterly Updates

- Claims submitted for dates of service after the effective date must comply with the new edits.
- Claims submitted before the effective date are governed by the old edits.
- Providers should update their claim scrubbing software quarterly.
- Failure to update can result in claims that should pass edits being denied or claims that should fail edits being accepted.

---

## 11. Payer-Specific Code Edits

While NCCI edits apply to Medicare claims, commercial payers often have additional or modified edits.

### Types of Payer-Specific Edits

| Edit Type | Description | Payer Example |
|-----------|-------------|---------------|
| **Payer PTP Edits** | Additional procedure pairs that cannot be billed together | Some payers have more restrictive PTP edits than Medicare |
| **Payer MUEs** | Reduced maximum units compared to Medicare MUEs | A payer may set MUE = 2 for a code where Medicare allows 4 |
| **Diagnosis-to-Procedure Edits** | Specific ICD-10 codes required for certain CPT codes | Many payers require specific diagnosis codes for advanced imaging |
| **Site-of-Service Edits** | Certain procedures only payable in specific sites | Some procedures only covered in outpatient, not office |
| **Frequency Edits** | Limits on how often a procedure can be performed | DME supplies often have frequency limits |
| **Preauthorization Edits** | Services that require prior authorization | High-cost imaging, surgeries, specialty drugs |

### Payer Edit File Sources

1. **Payer fee schedules**: Available on payer portals.
2. **Companion guides**: Published by payers with their X12 requirements.
3. **Payer bulletins**: Periodic updates about coding policy changes.
4. **Clearinghouse edit summaries**: Some clearinghouses provide payer-specific edit reports.

---

## 12. CCI Edit Tables and File Formats

CMS publishes NCCI edit files in specific formats:

### File Naming Convention

- `PT` prefix = PTP edits
- `MUE` prefix = Medically Unlikely Edits
- `Anesthesia` prefix = Anesthesia PTP edits (for anesthesia codes only)
- Suffix indicates version and year

### File Format (PTP Edits)

| Field | Position | Description |
|-------|----------|-------------|
| Column 1 Code | 1-5 | The comprehensive code |
| Column 2 Code | 6-10 | The component code |
| Modifier Indicator | 11 | 0 or 1 |
| Effective Date | 12-19 | Format CCYYMMDD |
| Deletion Date | 20-27 | Format CCYYMMDD, blank if active |

### Accessing NCCI Files

- CMS publishes NCCI files at: https://www.cms.gov/medicare/coding/ncci
- Files are in Excel, CSV, and text formats.
- Medicare contractors also publish CCI edits in their local coverage resources.

---

## 13. Agent Training: Q&A Pairs for NCCI Edits

**Q: What is the difference between NCCI PTP edits and MUEs?**

**A:** NCCI PTP (Procedure-to-Procedure) edits define code pairs that should not be billed together on the same date of service. PTP edits identify unbundling -- billing a comprehensive procedure and its component parts separately. MUEs (Medically Unlikely Edits) define the maximum units of service for a single CPT or HCPCS code per patient per day. PTP edits address code pair relationships, while MUEs address per-code service volume.

---

**Q: What does a modifier indicator of 0 mean in an NCCI PTP edit?**

**A:** A modifier indicator of 0 means no modifier can be used to bypass the edit. The Column 2 code (component procedure) is considered an integral part of the Column 1 code (comprehensive procedure). If both codes are submitted, the Column 2 code will be denied. There is no documentation or circumstance that would justify separate billing of both codes.

---

**Q: What does a modifier indicator of 1 mean in an NCCI PTP edit?**

**A:** A modifier indicator of 1 means a modifier can be used to bypass the edit if the clinical circumstances justify separate reporting. The provider must append an appropriate modifier (such as 59, XE, XS, XP, XU, 76, 77, 91, or 99) to the Column 2 code and maintain documentation supporting the distinct nature of the service. The modifier indicates the two procedures were performed at different anatomical sites, during different encounters, by different providers, or in other non-overlapping circumstances.

---

**Q: When should modifier XS be used instead of modifier 59?**

**A:** Modifier XS (Separate Structure) should be used when a service is distinct because it was performed on a separate organ, anatomical site, or structure. CMS prefers X{EPSU} modifiers over modifier 59 because they are more specific. For example, if a patient has bilateral knee injections, modifier XS more accurately describes the situation (same encounter, same practitioner, but separate anatomical structure) than modifier 59. Modifier 59 should only be used when none of the X{EPSU} modifiers (XE, XS, XP, XU) apply.

---

**Q: What is the MUE for CPT 93005 (ECG tracing)?**

**A:** The MUE for CPT 93005 (ECG tracing) is 1. Only one ECG tracing is medically reasonable per patient per date of service. If a claim is submitted with 2 units of 93005 for the same patient on the same date, one unit will be denied. If a complete ECG (93000) was performed, the tracing component (93005) is bundled and cannot be separately billed.

---

**Q: Can add-on codes be reported without a primary procedure code?**

**A:** No. Add-on codes (identified with a "+" in CPT) describe supplemental services that are performed in addition to a primary procedure. They cannot be reported without the primary code on the same claim. For example, CPT +22632 (additional posterior lumbar segment) cannot be reported without the primary fusion code such as 22630. If an add-on code is submitted without its primary code, the add-on code will be denied.

---

**Q: What is the difference between bundling and unbundling?**

**A:** Bundling is the correct coding practice of reporting a single comprehensive code that describes the entire service performed. Unbundling (specifically inappropriate unbundling) is the incorrect practice of reporting multiple component codes separately when a single comprehensive code covers the same service. For example, billing 93005 (ECG tracing) plus 93010 (ECG interpretation) separately instead of 93000 (complete ECG) is unbundling. Unbundling often results in higher total reimbursement than the comprehensive code and is considered a form of improper coding that can trigger audits.

---

**Q: How often does CMS update NCCI edits?**

**A:** CMS updates NCCI edits quarterly. The effective dates are January 1 (Q1), April 1 (Q2), July 1 (Q3), and October 1 (Q4). Update files are typically released by CMS approximately two weeks before the effective date. Providers should update their claim scrubbing systems before each quarter to stay current with new PTP edits, changed modifier indicators, and updated MUE values.

---

**Q: What is a mutually exclusive edit?**

**A:** A mutually exclusive edit identifies two procedure codes that describe services that cannot reasonably be performed on the same patient on the same date of service. For example, CPT 44950 (appendectomy) and 44960 (appendectomy with abscess drainage) are mutually exclusive because the appendix can only be removed once. These edits typically have a modifier indicator of 0, meaning no modifier can bypass them.

---

**Q: How do commercial payers handle NCCI edits?**

**A:** Commercial payers may adopt CMS NCCI edits directly, modify them, or create their own proprietary edit sets. Many payers use NCCI as a baseline and add additional edits specific to their payment policies. For example, a commercial payer may have stricter MUE values for certain high-cost procedures or additional PTP edits for codes not covered by NCCI. Providers should consult each payer's fee schedule and companion guide for payer-specific edit policies.

---

**Q: What happens when a claim line exceeds the MUE value?**

**A:** When a claim line's units exceed the MUE value for that CPT code, the payer's system will deny the excess units. The adjudication logic varies by payer. Typically, if a claim line has 3 units of a code with MUE = 2, the system will pay 2 units and deny 1 unit. In some cases, if multiple lines report the same code, the system sums the units across lines and applies the MUE to the total. The denied units receive a claim adjustment reason code indicating the MUE exceeded.

---

**Q: What is the MUE for CPT 99213 (established patient office visit)?**

**A:** The MUE for CPT 99213 is 1. A patient can only have one E/M office visit per provider per date of service. If two visits with the same provider on the same date are medically necessary, the provider should use modifier 25 on the first visit E/M code and document both encounters separately. However, reporting two 99213 codes on the same date would trigger the MUE and result in a denial of the second unit.

---

**Q: How should a provider handle a gender edit failure?**

**A:** A gender edit failure occurs when a procedure code is submitted for a patient whose recorded gender is incompatible with the procedure (e.g., CPT 84154 for PSA on a patient recorded as female). The provider should verify the patient's gender in the system. If the gender is incorrect, correct it and resubmit. If the gender is correct (e.g., the patient is transgender), some payers allow modifier KX (requirements met) to indicate that medical policy requirements have been satisfied. The provider should also verify that the diagnosis code supports medical necessity.

---

**Q: What is the difference between an age edit and a gender edit?**

**A:** An age edit flags procedure codes that are inappropriate for the patient's age (e.g., CPT 99382 for preventive visit ages 1-4 submitted for a 10-year-old patient). A gender edit flags procedure codes incompatible with the patient's gender (e.g., CPT 76817 transvaginal ultrasound for a male patient). Both are pre-submission claim edits that can result in denial if not resolved. Age edits can sometimes be overridden with supporting documentation, while gender edits for non-transgender patients typically require data correction.

---

**Q: Can modifier 51 be used to bypass NCCI edits?**

**A:** No. Modifier 51 (Multiple Procedures) is not recognized by CMS as a modifier that can bypass NCCI PTP edits. Modifier 51 is an informational modifier used to indicate multiple procedures performed during the same operative session. It does not indicate that two procedures are distinct from each other. Only the specific bypass modifiers (59, XE, XS, XP, XU, 76, 77, 91, 99) can be used to bypass PTP edits with a modifier indicator of 1.

---

**Q: What are the X{EPSU} modifiers and when were they introduced?**

**A:** CMS introduced the X{EPSU} modifiers (XE, XS, XP, XU) in 2017 as more specific alternatives to modifier 59. XE = separate encounter, XS = separate structure, XP = separate practitioner, XU = unusual non-overlapping service. CMS encourages providers to use these specific modifiers instead of modifier 59 whenever the circumstances match the definition. Modifier 59 should be reserved as a "last resort" when none of the X{EPSU} modifiers apply.

---

**Q: What is the standard MUE for CPT 97530 (therapeutic activities)?**

**A:** The MUE for CPT 97530 (therapeutic activities) is 4 units per patient per date of service. This is a timed service code (each unit typically represents 15 minutes). A provider could report up to 4 units (60 minutes) of therapeutic activities for a patient on a single date of service. If more than 4 units are reported, the excess will be denied. Providers should document the total treatment time to support the units billed.

---

**Q: What documentation is needed to support modifier 59 or modifier XS?**

**A:** For modifier 59 (Distinct Procedural Service) or XS (Separate Structure), the documentation must clearly indicate that the two procedures were performed at different anatomical sites. Examples include: specifying "right knee" and "left knee" in separate operative notes; documenting separate incision sites; describing distinct organs or anatomical regions; or providing separate procedure notes for each service. CMS auditors will look for explicit documentation in the medical record that supports the separate nature of the services. Vague documentation like "also performed" is insufficient.

---

**Q: What is an inappropriate unbundling example involving surgical packages?**

**A:** A common inappropriate unbundling example is billing CPT 49505 (repair inguinal hernia) and separately billing CPT 12031 (layered skin closure of wound) for the incision closure. The skin closure in an inguinal hernia repair is an integral part of the surgical procedure and is included in the global surgical package. Billing these separately constitutes unbundling. The correct coding is to report only 49505, which includes the closure.

---

**Q: How do Medicare global surgery periods relate to NCCI editing?**

**A:** Medicare assigns global surgery periods to surgical codes: 0 days (no global period), 10 days (minor surgery), or 90 days (major surgery). During the global period, related E/M services and most postoperative care are included in the surgical payment and cannot be separately billed. NCCI PTP edits do not enforce global period rules directly, but the Correct Coding Initiative also includes edits for global surgery package components. Reporting a related procedure within the global period requires modifier 78 (unplanned return to OR) or 79 (unrelated procedure).

---

**Q: Can an add-on code be reported multiple times?**

**A:** Some add-on codes can be reported multiple times, but not all. For example, CPT +69990 (operating microscope) can typically be reported only once per surgical session regardless of the number of procedures performed. However, CPT +22552 (additional cervical interspace fusion) can be reported for each additional vertebral interspace fused beyond the primary level. The MUE for each add-on code determines how many units can be reported. Providers should check the specific code descriptor and MUE value for each add-on code.

---

**Q: What happens if a provider bills a patient for a service denied by NCCI edits?**

**A:** If a service is denied due to NCCI edits and the provider has not obtained an Advance Beneficiary Notice (ABN) from the patient, the provider generally cannot bill the patient. For Medicare, if a service is denied as bundled under NCCI, the patient is not liable for payment. The provider must write off the denied amount. For commercial payers, the patient's liability depends on the payer's policy and whether the patient signed a waiver. It is important to note that NCCI denials are typically considered a provider billing error, not a service that the patient should pay for.

---

**Q: What is the NCCI for anesthesia services?**

**A:** CMS publishes a separate set of NCCI edits for anesthesia services. These edits identify code pairs specific to anesthesia coding, including edits between anesthesia codes and surgical/procedural codes. The anesthesia NCCI file has a different naming convention from the standard PTP file. Anesthesia providers should use the anesthesia-specific NCCI edits to validate their claims. Common anesthesia NCCI edits include restrictions on reporting multiple anesthesia codes for overlapping time periods.

---

**Q: How does a provider check if a new CPT code has NCCI edits?**

**A:** When a new CPT code is introduced (typically in January), CMS may not publish NCCI edits for it in the first quarter. The code may receive edits in a subsequent quarterly update after CMS has had time to analyze the code's relationship to other codes. Providers should check the CMS NCCI webpage when updates are released. Commercial payers may implement edits for new codes on their own schedule. Until edits are published, providers should use clinical judgment and coding guidelines to determine when procedures should not be billed together.

---

**Q: What is the MUE for CPT 93015 (cardiovascular stress test)?**

**A:** The MUE for CPT 93015 (cardiovascular stress test, complete) is 1. Only one stress test is medically reasonable per patient per date of service. The code bundle includes the stress test procedure, ECG monitoring, and physician supervision. Submitting multiple units of 93015 on the same date of service will result in the additional units being denied under MUE adjudication.

---

**Q: What is the difference between a date-of-service MUE and a patient-specific MUE?**

**A:** A date-of-service MUE limits the number of units per patient per date of service. This is the standard MUE type for most CPT codes. For example, CPT 93005 has a date-of-service MUE of 1 (one ECG tracing per day). A patient-specific MUE limits the number of units per patient over their entire lifetime. These are rare and apply to certain implants, devices, or one-time procedures. For example, CPT 33227 (insertion of pacemaker pulse generator) has a patient-specific MUE of 1 because a patient would typically only have one initial insertion.

---

**Q: How do quarterly NCCI updates affect prior authorizations?**

**A:** When NCCI edits change quarterly, prior authorizations obtained before the effective date may be affected. If a new edit makes two codes unbundlable starting April 1, but the prior authorization was obtained in March, the claim submitted after April 1 may be denied. Providers should check for NCCI changes before submitting claims, even if a prior authorization was already obtained. Ideally, the prior authorization should reflect the coding rules in effect on the date of service.

---

**Q: What is the CMS multiple endoscopy rule?**

**A:** The CMS multiple endoscopy rule applies when multiple endoscopic procedures are performed in the same family through the same incision, orifice, or surgical approach. The highest-valued endoscopic procedure is paid at 100%, and subsequent procedures are paid at the difference between the comprehensive code and the base endoscopic code value. For example, if a colonoscopy with polypectomy (45385) and a diagnostic colonoscopy (45378) are performed on the same day, 45385 is paid at 100% and 45378 is paid at 0% because 45378 is included in 45385. NCCI edits enforce this bundling.

---

**Q: Can a payer-specific MUE be stricter than the CMS MUE?**

**A:** Yes. Commercial payers can and often do set MUE values that are stricter (lower) than the CMS MUE. For example, CMS may have an MUE of 4 for CPT 97140 (manual therapy techniques), but a commercial payer might set their MUE at 2. In such cases, the provider must follow the payer-specific MUE, not the CMS MUE. The payer's MUE is typically documented in the payer's fee schedule or companion guide. Clearinghouses that offer payer-specific scrubbers can catch these differences before submission.

---

**Q: What is the appropriate modifier to use when a different provider performs the same procedure on the same day?**

**A:** The appropriate modifier is modifier 77 (Repeat Procedure by Different Physician). This modifier is reported on the repeated procedure code and indicates that the same service was performed by a different provider on the same date of service. For example, if one radiologist performs a diagnostic ultrasound and another radiologist performs a repeat ultrasound for a different indication, the second procedure would be reported with modifier 77. Modifier 77 has a modifier indicator of 1 for most eligible PTP edits and can bypass the edit.

---

**Q: What is the significance of Column 1 and Column 2 in NCCI PTP edits?**

**A:** In NCCI PTP edits, Column 1 contains the comprehensive (bundling) code -- the primary or more extensive procedure. Column 2 contains the component code that is considered an integral part of the Column 1 procedure. When both codes are submitted for the same patient on the same date of service, the Column 2 code is denied unless a valid modifier is appended. The Column 1 code is the comprehensive service, and the Column 2 code is the component that is bundled into it.