# Medical Necessity

## Overview

Medical necessity is the fundamental requirement that healthcare services, procedures, and supplies must be clinically appropriate and reasonable for the diagnosis, treatment, or management of a patient's condition. Payers deny claims based on lack of medical necessity more than any other reason. Understanding medical necessity documentation requirements, coverage determinations, and liability rules is essential for preventing denials.

Medical necessity involves three core components:
1. **Diagnosis-to-procedure alignment**: The ICD-10 diagnosis code must support the CPT/HCPCS procedure code.
2. **Coverage policy compliance**: The service must be covered under the patient's benefit plan.
3. **Clinical documentation**: The medical record must support the level and type of service billed.

---

## 1. Local Coverage Determinations (LCDs)

### Definition

A Local Coverage Determination (LCD) is a decision by a Medicare Administrative Contractor (MAC) about whether a particular item or service is covered within the MAC's jurisdiction. LCDs are specific to each MAC's geographic region and define the diagnosis codes that support the medical necessity of specific procedure codes.

### How LCDs Work

- Each MAC publishes LCDs for procedures and services that have regional variation in coverage.
- LCDs include a list of ICD-10 diagnosis codes that are considered medically necessary for each procedure.
- LCDs may also include frequency limitations, documentation requirements, and coding guidelines.
- LCDs are binding on Medicare claims within that MAC's jurisdiction.
- Commercial payers may adopt LCDs or publish their own Local Coverage Articles.

### LCD Structure

| Component | Description |
|-----------|-------------|
| **LCD ID** | Unique identifier assigned by CMS |
| **Title** | Description of the covered service |
| **ICD-10 Codes** | List of covered diagnosis codes grouped into code lists |
| **CPT/HCPCS Codes** | Codes subject to the LCD |
| **Coverage Indications** | Clinical criteria that must be met |
| **Limitations** | Exclusions, frequency limits, or special requirements |
| **Documentation Requirements** | Records that must be maintained |
| **Revision History** | Dates of changes to the LCD |
| **Effective Date** | Date the LCD takes effect |
| **Retirement Date** | Date the LCD is retired |

### LCD Diagnosis Code Lists

| Group | Description | Example |
|-------|-------------|---------|
| **Group 1 Codes** | ICD-10 codes that support medical necessity | M17.0 (bilateral primary osteoarthritis of knee) for knee MRI |
| **Group 2 Codes** | ICD-10 codes that do NOT support medical necessity | M25.561 (pain in right knee) alone for knee MRI |
| **Non-covered Codes** | ICD-10 codes explicitly excluded from coverage | Z00.00 (general adult medical exam) for surgical procedure |

### Example LCD: Magnetic Resonance Imaging (MRI) of the Knee

| Covered Diagnoses (Group 1) | Non-Covered Diagnoses |
|----------------------------|----------------------|
| M17.0 (Bilateral primary OA of knee) | M25.561 (Pain in right knee) - insufficient |
| M23.51 (Chronic instability of knee, derangement) | Z00.00 (General medical exam) |
| S83.2 (Tear of meniscus, current injury) | Z01.89 (Encounter for other specified exam) |
| M22.2 (Patellofemoral disorders) | Z02.5 (Examination for participation in sport) |
| M24.45 (Recurrent dislocation of patella) | |

### MAC Jurisdictions and LCD Variability

Different MACs may have different LCDs for the same procedure. For example:
- **Novitas (Jurisdiction H)**: LCD for physical therapy requires at least 3 specific diagnosis codes.
- **Noridian (Jurisdiction E)**: LCD for echocardiography has specific frequency limitations.
- **NGS (Jurisdiction K)**: LCD for sleep studies requires documented failure of conservative therapy.

---

## 2. National Coverage Determinations (NCDs)

### Definition

A National Coverage Determination (NCD) is a policy established by CMS that applies to all Medicare beneficiaries across all MACs. NCDs define whether a particular item or service is covered nationally.

### Key Characteristics

- NCDs override LCDs when they exist for the same service.
- NCDs are published in the Medicare National Coverage Determinations Manual.
- NCDs apply uniformly across all MAC jurisdictions.
- NCDs can be national coverage (covered), national non-coverage (not covered), or coverage with conditions.
- Once CMS issues an NCD, MACs cannot create conflicting LCDs.

### Examples of NCDs

| NCD Topic | Coverage Decision |
|-----------|-------------------|
| Cardiac Rehabilitation (NCD 20.10) | Covered for specific conditions post-MI, CABG, etc. |
| Lung Cancer Screening (NCD 210.1) | Covered with low-dose CT for high-risk patients meeting specific criteria |
| Cochlear Implantation (NCD 50.3) | Covered for specific hearing loss thresholds |
| PET Scans for Cancer (NCD 220.6) | Covered for specified cancer types with conditions |
| Bariatric Surgery (NCD 100.1) | Covered for patients with BMI >= 35 and obesity-related conditions |
| Home Oxygen Therapy (NCD 240.2) | Covered with specific blood gas or oximetry criteria |

### NCD vs LCD Decision Hierarchy

```
NCD Exists?
  |-- YES: NCD applies (LCD cannot override)
  |-- NO: Check for LCD
       |-- YES: LCD applies within that MAC
       |-- NO: No local or national policy (carrier discretion)
```

---

## 3. Advance Beneficiary Notice of Noncoverage (ABN)

### Definition

The Advance Beneficiary Notice of Noncoverage (ABN), CMS Form R-131, is a standardized form that a Medicare provider gives to a beneficiary before providing a service when the provider believes Medicare may not cover the service.

### Purpose

- Shifts financial liability from the provider to the beneficiary when Medicare denies a service.
- Obtains the patient's informed consent to pay out of pocket if Medicare denies coverage.
- Documents that the patient was warned the service may not be covered.
- Is required only for Medicare Part B services that may be denied.

### ABN Form Layout (CMS-R-131)

| Section | Content |
|---------|---------|
| **Header** | Patient name, Medicare number, form identifier |
| **Section A** | Notifier (provider name, description of items/services) |
| **Section B** | List of items/services that may not be covered |
| **Section C** | Reason Medicare may not pay |
| **Section D** | Estimated cost (optional) |
| **Section E** | Patient options and signature |

### Patient Options on ABN

| Option | Patient Action | Financial Consequence |
|--------|---------------|----------------------|
| **Option 1** | I want the service. I will pay if Medicare denies. | Patient liable if denied |
| **Option 2** | I want the service. I will appeal if Medicare denies. | Patient liable if appeal fails |
| **Option 3** | I do not want the service. | No service provided |

### ABN-Related Modifiers

| Modifier | Definition | When to Use |
|----------|------------|-------------|
| **GA** | Waiver of liability statement issued as required by payer policy | On the claim line when an ABN was signed (patient chose Option 1 or 2) |
| **GX** | Notice of liability issued, voluntary under payer policy | On the claim line when an ABN was signed but not required by payer policy |
| **GY** | Item or service statutorily excluded or does not meet the definition of a Medicare benefit | On the claim line when the service is known to be non-covered (no ABN needed) |
| **GZ** | Item or service expected to be denied as not reasonable and necessary | On the claim line when the provider expects denial but did not obtain an ABN |

### When an ABN Is Required

- Service is likely to be denied for medical necessity.
- Service is not considered reasonable and necessary for the specific diagnosis.
- Frequency limits have been met or exceeded.
- Service is experimental or investigational.

### When an ABN Is NOT Required

- Service is statutorily excluded (use modifier GY).
- Emergency care.
- Inpatient hospital services (different notice, the Important Message from Medicare).
- Services that are never covered by Medicare regardless of circumstances.

### ABN Failure Consequences

| Scenario | Outcome |
|----------|---------|
| ABN signed, modifier GA appended, Medicare denies | Patient is financially responsible |
| ABN not signed, no modifier appended, Medicare denies | Provider cannot bill patient; provider writes off service |
| ABN not signed, modifier GZ appended, Medicare denies | Provider cannot bill patient; waiver of liability granted to patient |
| Service statutorily excluded, modifier GY appended | Beneficiary is liable if they signed a voluntary ABN |

---

## 4. Medical Necessity Denials

### Why Medical Necessity Denials Occur

Medical necessity denials are the most common type of claim denial. Key causes include:

1. **Insufficient diagnosis codes**: The ICD-10 code does not support the procedure.
2. **Diagnosis-to-procedure mismatch**: No clinically valid relationship between the diagnosis and the procedure.
3. **Missing supporting documentation**: The medical record does not document the clinical rationale.
4. **Frequency exceeded**: Service performed more often than the payer allows.
5. **Level of care not supported**: Higher level of service billed but lower level documented.
6. **Experimental/investigational**: Service is not yet accepted standard of care.
7. **Not medically necessary per policy**: Service does not meet payer-specific criteria.

### Medical Necessity Denial Data Flow

```
Claim Submitted
  |
  v
Payer Edits (NCCI, MUE, diagnosis-to-procedure)
  |
  v
Medical Necessity Review
  |-- ICD-10 supports CPT/HCPCS? --> YES --> Process normally
  |-- ICD-10 does not support CPT/HCPCS? --> NO --> Denial
  |
  v
Adjudication: Group Code = CO (Contractual) or PR (Patient)
               CAS Reason Code = 50 / 11 / 96
```

### Common Medical Necessity Denial Reason Codes

| CARC Code | Description | Typical Scenarios |
|-----------|-------------|-------------------|
| **50** | Service not medically necessary | Procedure not supported by diagnosis |
| **11** | Diagnosis inconsistent with procedure | ICD-10 does not match CPT |
| **96** | Non-covered service | Procedure not covered by benefit plan |
| **119** | Benefit maximum exceeded | Therapy cap reached |
| **179** | Service not covered when performed in this setting | POS mismatch with policy |
| **180** | Procedure code not valid for patient age | Age edit failure |
| **181** | Procedure code not valid for patient gender | Gender edit failure |

### Medical Necessity Denial Appeal Strategy

1. **Review the specific denial reason**: Identify the CARC, RARC, and payer denial details.
2. **Obtain complete medical records**: Progress notes, test results, operative reports, referrals.
3. **Map documentation to denial reason**: Show where the record supports medical necessity.
4. **Identify the correct diagnosis code**: Ensure the ICD-10 code accurately reflects the documented condition.
5. **Draft an appeal letter**: Reference the specific denial, include supporting evidence, cite relevant LCD/NCD.
6. **Submit within timely filing deadline**: Most payers allow 30-180 days for appeals.

---

## 5. Medically Unlikely vs Medically Unnecessary

### Key Distinction

| Concept | Definition | Example |
|---------|------------|---------|
| **Medically Unlikely (MUE)** | The number of units of service exceeds what could reasonably be performed per day | 5 units of CPT 97530 (therapeutic activities) when MUE = 4 |
| **Medically Unnecessary** | The service is not clinically appropriate or reasonable for the patient's condition | CPT 72125 CT cervical spine for complaint of "headache" |

### Comparison Table

| Aspect | Medically Unlikely | Medically Unnecessary |
|--------|--------------------|-----------------------|
| **Edit Type** | NCCI MUE (unit limits) | Medical necessity review |
| **Focus** | Quantity of service | Appropriateness of service |
| **Override** | Based on documentation | Based on clinical evidence |
| **ABN Required?** | Rarely | Usually, if known in advance |
| **Common Appeal Route** | Line-level correction | Appeal with medical records |
| **Result** | Excess units denied | Entire line denied |

---

## 6. Diagnosis-to-Procedure Edit Validation

### What It Validates

Diagnosis-to-procedure edits confirm that the ICD-10 diagnosis code on the claim is clinically consistent with the procedure code. This is a critical medical necessity check.

### Validation Logic

```
Is the ICD-10 code an acceptable diagnosis for the CPT/HCPCS code?
  |-- YES: Proceed to next edit
  |-- NO: Check patient-specific circumstances
       |-- Documentation supports the procedure? --> Appeal with records
       |-- Documentation does not support the procedure --> Correct coding/ABN
```

### Examples

| CPT Code | Procedure | ICD-10 Supports | ICD-10 Does Not Support |
|----------|-----------|-----------------|------------------------|
| 99283 | Emergency Department Visit, Level 3 | I10 (Hypertension), R10.9 (Abdominal pain), J45.909 (Asthma) | Z00.00 (General exam) |
| 70450 | CT Head without Contrast | S06.9X9A (Head Injury), R51 (Headache), G40.909 (Seizure) | M54.5 (Low back pain) |
| 72052 | MRI Spine, Complete | M51.26 (Disc displacement lumbar), S33.8XXA (Sprain lumbar) | J45.909 (Asthma) |
| 81001 | Urinalysis with microscopy | N39.0 (UTI), R31.9 (Hematuria), R35 (Polyuria) | E11.9 (Diabetes without complication) |

---

## 7. Documentation Requirements for Medical Necessity

### Key Documentation Elements

1. **Chief Complaint**: The patient's reason for the visit in their own words.
2. **History of Present Illness**: Chronological description of the condition.
3. **Review of Systems**: Documented systems review relevant to the complaint.
4. **Physical Examination**: Objective findings that support the diagnosis.
5. **Assessment/Diagnosis**: The medical diagnosis coded in ICD-10.
6. **Plan**: The treatment plan including ordered procedures, medications, and follow-up.
7. **Medical Decision Making**: Complexity of diagnosis, data reviewed, and risk of complications.

### Why Diagnosis Codes Alone Are Not Enough

Payers do not rely solely on the ICD-10 code; they also evaluate whether the medical record supports the diagnosis-to-procedure relationship. Even if the correct ICD-10 code is used, the claim can be denied if:

- The physical examination does not document findings consistent with the diagnosis.
- The history does not describe the progression or nature of the condition.
- There is no documented evidence that conservative treatment failed before advanced imaging was ordered.
- The treatment plan does not match the diagnosis.

### Documentation Best Practices

1. **Be specific**: Document the exact anatomical location, severity, and chronicity.
2. **Link diagnosis to procedure**: Explain why the procedure is necessary for the diagnosis.
3. **Document failed conservative therapy**: Especially important for surgery and advanced imaging.
4. **Include pertinent negatives**: Document what was ruled out.
5. **Sign and date all entries**: Timely documentation carries more weight.
6. **Use templates appropriately**: Customized documentation is better than generic templates.
7. **Document medical necessity at the time of service**: Retrospective documentation is less credible.

---

## 8. Commercial Payer Medical Necessity

Commercial payers may have different medical necessity criteria than Medicare. Key differences include:

| Aspect | Medicare | Commercial |
|--------|----------|------------|
| **Coverage Authority** | LCDs and NCDs | Plan-specific medical policies |
| **ABN Equivalent** | CMS-R-131 (formal ABN) | Voluntary waiver of liability |
| **Denial Rate** | Varies by MAC | Generally higher |
| **Appeal Level 1** | Redetermination (MAC) | Internal peer review |
| **Appeal Level 2** | Reconsideration (QIC) | External independent review |
| **Appeal Timeline** | 120 days for redetermination | Varies (30-180 days typical) |
| **Medical Policy** | Published on cms.gov | Published on payer portal |

### Common Commercial Payer Medical Necessity Policies

| Payer | Policy Area | Typical Requirements |
|-------|-------------|---------------------|
| UnitedHealthcare | Imaging | Specific clinical criteria for each study |
| Anthem/BCBS | Surgery | Failed conservative therapy documentation |
| Aetna | Physical Therapy | Functional improvement documented |
| Cigna | Sleep Studies | Home sleep test before in-lab study |
| Humana | Cardiac Testing | Specific risk factors required |

---

## 9. Agent Training: Q&A Pairs for Medical Necessity

**Q: What is the difference between an LCD and an NCD?**

**A:** A Local Coverage Determination (LCD) is a coverage policy set by a specific Medicare Administrative Contractor (MAC) for its jurisdiction. LCDs vary by region and define which diagnosis codes support the medical necessity of specific procedures within that MAC's geographic area. A National Coverage Determination (NCD) is a coverage policy set by CMS that applies uniformly to all Medicare beneficiaries across all MAC jurisdictions. NCDs override LCDs when both exist for the same service, and MACs cannot create LCDs that conflict with NCDs.

---

**Q: When is an Advance Beneficiary Notice (ABN) required?**

**A:** An ABN (CMS Form R-131) is required when a Medicare provider believes a service may not be covered by Medicare due to medical necessity reasons. This includes situations where the service is not reasonable and necessary, frequency limits have been met, or the service may be denied as custodial care. The ABN must be presented to the beneficiary before the service is provided, and the beneficiary must sign it. After signing, the provider appends modifier GA to the claim line. The ABN shifts financial liability to the beneficiary if Medicare denies the claim.

---

**Q: What is the difference between modifier GA and modifier GZ?**

**A:** Modifier GA indicates that the provider issued an Advance Beneficiary Notice (ABN) to the patient, the patient signed it, and understands they may be financially responsible if Medicare denies the claim. If Medicare denies the claim, the patient can be billed. Modifier GZ indicates the provider expects the service will be denied as not reasonable and necessary but did NOT obtain an ABN. If Medicare denies a claim with modifier GZ, the provider cannot bill the patient and must absorb the loss. Modifier GZ is considered a compliance risk and may trigger medical review.

---

**Q: What is the most common reason for medical necessity denials?**

**A:** The most common reason for medical necessity denials is insufficient diagnosis-to-procedure alignment. The ICD-10 diagnosis code submitted on the claim does not adequately support the medical necessity of the procedure performed. For example, billing CPT 72125 (CT cervical spine) with diagnosis M54.5 (low back pain) would be denied because cervical spine imaging is not medically necessary for lumbar symptoms. Other common reasons include lack of supporting clinical documentation, failure to document failed conservative therapy, and exceeding established frequency limits.

---

**Q: Can an LCD be used to appeal a commercial payer denial?**

**A:** Possibly, but LCDs technically apply only to Medicare claims within a specific MAC's jurisdiction. However, some commercial payers adopt Medicare LCDs as part of their medical policies, or they may reference them in their coverage criteria. When appealing a commercial payer denial, the provider should primarily reference the payer's own medical policy. The LCD can be referenced as supporting evidence or as a secondary argument, but it is not binding on commercial payers. The provider should check the specific payer's medical policy for the most relevant coverage criteria.

---

**Q: What is the difference between a Group 1 code and Group 2 code in an LCD?**

**A:** In an LCD, Group 1 codes list the ICD-10 diagnosis codes that do support medical necessity for the specified procedure. If the claim's diagnosis code falls in Group 1, the procedure passes the medical necessity check. Group 2 codes list diagnosis codes that do NOT support medical necessity for the procedure. If the claim's diagnosis code falls in Group 2, the procedure fails the medical necessity check and will be denied unless additional clinical criteria are documented and met. Some LCDs also have Group 3 codes that are conditionally covered.

---

**Q: What modifiers relate to the Advance Beneficiary Notice (ABN)?**

**A:** There are four ABN-related modifiers: GA (waiver of liability statement issued as required by payer policy -- ABN signed, patient liable if denied), GX (notice of liability issued voluntarily -- ABN signed but not required), GY (item or service statutorily excluded or does not meet the definition of a Medicare benefit -- no ABN needed), and GZ (item or service expected to be denied as not reasonable and necessary -- no ABN obtained, provider cannot bill patient). Each modifier communicates a different liability scenario to Medicare.

---

**Q: How does "medically unlikely" differ from "medically unnecessary"?**

**A:** "Medically unlikely" refers to the number of units of a procedure exceeding what could reasonably be performed per patient per day. This is governed by Medically Unlikely Edits (MUEs). For example, submitting 5 units of CPT 97530 (therapeutic activities) when the MUE is 4. "Medically unnecessary" refers to the clinical appropriateness of the service itself. For example, performing a CT scan of the cervical spine for low back pain. MUE denials are about quantity; medical necessity denials are about appropriateness. Both require different appeal strategies.

---

**Q: What should a provider do if a service is statutorily excluded from Medicare coverage?**

**A:** If a service is statutorily excluded from Medicare coverage (such as most dental services, cosmetic surgery, or routine foot care), the provider should use modifier GY on the claim line and may obtain a voluntary ABN from the patient. Modifier GY indicates the item or service is statutorily excluded or does not meet the definition of a Medicare benefit. The patient can be informed in advance and asked to sign a voluntary waiver if they agree to pay. No formal ABN is required for statutorily excluded services because Medicare never covers them under any circumstances.

---

**Q: What is the role of a Local Coverage Determination in claim scrubbing?**

**A:** In claim scrubbing, LCDs are used to validate that the diagnosis code on the claim supports the medical necessity of the procedure code. The scrubber checks whether the ICD-10 code falls within the covered diagnosis code list in the relevant LCD. If the diagnosis code is not in the covered list, the scrubber flags the claim for review. Some advanced scrubbers also check whether the documentation requirements specified in the LCD are met. This pre-submission validation reduces the risk of medical necessity denials.

---

**Q: What are the four options a patient has when presented with an ABN?**

**A:** The patient has three options. Option 1: "I want the service. I will pay if Medicare denies." The patient accepts financial responsibility. Option 2: "I want the service. I will appeal if Medicare denies." The patient accepts financial responsibility if the appeal fails. Option 3: "I do not want the service." The service is not provided. There is no Option 4. If the patient chooses Option 1 or 2, the provider appends modifier GA to the claim lines.

---

**Q: What is a diagnosis-to-procedure mismatch denial?**

**A:** A diagnosis-to-procedure mismatch denial occurs when the ICD-10 diagnosis code on the claim is not clinically consistent with the CPT or HCPCS procedure code billed. The payer's system evaluates whether the diagnosis code supports the medical necessity of the procedure. For example, billing CPT 93000 (complete ECG) with a diagnosis of M25.561 (pain in right knee) would be flagged as a mismatch because an ECG is not medically necessary for knee pain. The provider must either correct the diagnosis code or supplement the claim with documentation that establishes the medical necessity.

---

**Q: How does a provider know which MAC's LCD applies to their claim?**

**A:** The applicable MAC is determined by the state where the service is performed (not the provider's home state or the patient's residence). CMS divides the United States into MAC jurisdictions by state and territory. The provider can check the CMS MAC Jurisdiction map or the Noridian/Palmetto/NGS/WPS/First Coast/CGS/Novitas jurisdiction listings. For example, a provider in Texas is under Novitas jurisdiction J-E and must follow Novitas LCDs. A provider in Illinois is under NGS (Part A) or WPS (Part B) jurisdiction J-K.

---

**Q: What is the liability consequence if a provider performs a medically unnecessary service without an ABN?**

**A:** If a provider performs a service that Medicare denies as not medically necessary and no ABN was obtained, the provider cannot bill the patient for the service. The provider must absorb the loss as a write-off. The provider would use modifier GZ on the claim to indicate they expected the denial but did not obtain an ABN. This outcome is unfavorable for the provider, which is why obtaining a signed ABN before providing services that may be denied is so important.

---

**Q: Can a commercial payer require an ABN-equivalent form?**

**A:** Yes. While the formal ABN (CMS-R-131) is a Medicare-specific form, commercial payers may have their own waiver of liability procedures. Some commercial payers have voluntary waiver forms that the patient can sign to accept financial responsibility for services that may not be covered. These commercial waivers function similarly to the Medicare ABN but are payer-specific. Providers should check each commercial payer's policy regarding advance notification of non-coverage.

---

**Q: What should a provider document in the medical record to support medical necessity for advanced imaging?**

**A:** For advanced imaging (CT, MRI, PET), the provider should document: the specific clinical signs and symptoms that prompted the imaging, relevant history including duration and progression of symptoms, physical examination findings that localize the problem, results of any prior imaging or diagnostic tests, attempts at conservative therapy and their outcomes (for non-emergent conditions), the specific clinical question the imaging is intended to answer, and how the results will change clinical management. This comprehensive documentation supports the medical necessity determination if the claim is audited or appealed.

---

**Q: How long does a Medicare beneficiary have to file a redetermination appeal?**

**A:** A Medicare beneficiary (or their provider on their behalf) has 120 calendar days from the date of the redetermination notice to file an appeal. The redetermination is the first level of appeal for Medicare Part B claims. The appeal must be submitted in writing to the MAC. After the redetermination, the next levels are reconsideration by a Qualified Independent Contractor (QIC), hearing by an Administrative Law Judge (ALJ), review by the Medicare Appeals Council, and finally judicial review in federal district court. Each level has its own filing deadline and amount-in-controversy requirements.

---

**Q: What is a Local Coverage Article (LCA)?**

**A:** A Local Coverage Article (LCA), also known as a "Billing and Coding Article," provides additional guidance on how to implement an LCD. LCAs include coding instructions, documentation requirements, and frequently asked questions. While the LCD defines coverage policy, the LCA explains how to apply it when submitting claims. LCAs are not separately appealable but provide critical guidance for compliant billing. Some MACs use LCAs to provide updated diagnosis code lists between LCD revisions.

---

**Q: How do NCDs interact with LCDs when both exist?**

**A:** When a National Coverage Determination (NCD) exists for a service, it takes precedence over any Local Coverage Determination (LCD). MACs cannot issue LCDs that conflict with NCDs. If an NCD covers a service, the MAC cannot issue an LCD that non-covers the same service. If an NCD sets specific conditions for coverage, the MAC's LCD must be consistent with those conditions. However, the MAC may issue an LCD that adds additional requirements not mentioned in the NCD, as long as those requirements do not conflict with the NCD.

---

**Q: Why do medical necessity denials often result in patient liability?**

**A:** Medical necessity denials often result in patient liability because the provider has a mechanism to inform the patient in advance -- the Advance Beneficiary Notice (ABN). If the provider obtains a signed ABN before performing a service that may be denied and appends modifier GA to the claim, the patient has agreed to accept financial responsibility if Medicare denies the claim. For commercial payers, similar waiver arrangements may apply. Without a signed waiver or ABN, the provider cannot bill the patient and must write off the denied service.

---

**Q: What is a "not reasonable and necessary" denial?**

**A:** A "not reasonable and necessary" denial is Medicare's most common medical necessity denial. It is based on Section 1862(a)(1)(A) of the Social Security Act, which states that Medicare will only pay for items and services that are "reasonable and necessary for the diagnosis or treatment of illness or injury." The denial reason code is typically CARC 50 or 96. This means the payer determined that the service was not appropriate, not effective, or not needed for the patient's condition as documented on the claim. The provider must appeal with supporting clinical documentation to overturn this denial.

---

**Q: Can a provider override a medical necessity denial without appealing?**

**A:** In some limited circumstances, a provider can correct and resubmit a claim rather than appeal. This is possible when the denial was due to a coding error rather than a true medical necessity issue. For example, if the wrong ICD-10 code was submitted and the correct code supports medical necessity, the provider can correct the code and resubmit (if within timely filing limits). However, if the denial was based on a clinical review of the medical records, a full appeal with supporting documentation is required. The provider should check the specific payer's policies on corrected claims versus appeals.

---

**Q: What is the difference between a "covered service" and a "medically necessary service"?**

**A:** A "covered service" is a service included in the patient's benefit plan. For example, physical therapy is a covered service under most Medicare Part B plans. A "medically necessary service" is a specific instance of that covered service that is clinically appropriate for the patient's condition. Even if a service is covered (generally included in the benefit plan), a specific instance may be denied as not medically necessary (not appropriate for this particular patient/diagnosis). Coverage is a benefit issue; medical necessity is a clinical issue.

---

**Q: How often are LCDs updated?**

**A:** LCDs are updated as needed. There is no fixed schedule like the quarterly NCCI update cycle. CMS requires that each active LCD be reviewed at least annually. Updates may include changes to the covered diagnosis code lists, revised documentation requirements, or new coverage conditions. Providers should monitor their MAC's LCD website for updates. When an LCD is revised, it has an effective date and may have a grace period for implementation. Providers should update their claim scrubbing logic when LCDs change.

---

**Q: What should be included in an appeal letter for a medical necessity denial?**

**A:** A medical necessity appeal letter should include: the patient's name and Medicare/claim number, the date of service, the specific CPT/HCPCS and ICD-10 codes billed, the date of the denial notice, the specific denial reason (CARC code and description), a narrative explaining why the service was medically necessary, references to relevant LCDs, NCDs, or medical policies, specific citations from the medical record that support the procedure, a copy of the relevant medical records, any relevant test results or imaging reports, the ordering provider's statement of medical necessity, and a request for specific relief (overturn denial and process payment). The letter should be concise but complete.

---

**Q: Can the same service be denied for medical necessity for one diagnosis but covered for another?**

**A:** Yes. Medical necessity is diagnosis-dependent. For example, CPT 70450 (CT head without contrast) would be covered for a diagnosis of S06.9X9A (head injury with loss of consciousness) but denied for M54.5 (low back pain). The same procedure code can be covered or denied depending entirely on the diagnosis code submitted and whether that diagnosis code supports the medical necessity of the procedure. This is why correct diagnosis code selection is critical for claim acceptance.

---

**Q: What is the role of medical necessity in outpatient therapy denials?**

**A:** In outpatient therapy, medical necessity is evaluated based on whether the therapy is expected to improve the patient's condition, maintain the patient's current functional status to prevent decline, or slow deterioration in a progressive condition. Therapy for "maintenance only" is generally not covered by Medicare unless there is a specific skilled need. The therapist must document functional limitations, measurable goals, and clinical progress. Medical necessity denials in therapy often occur when the documentation does not show objective improvement or when the treatment appears custodial rather than skilled.