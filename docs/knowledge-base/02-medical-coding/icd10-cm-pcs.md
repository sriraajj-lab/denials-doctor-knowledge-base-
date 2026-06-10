# ICD-10-CM and ICD-10-PCS: Diagnosis and Procedure Coding

## Overview

ICD-10-CM (Clinical Modification) is the official system of diagnosis codes used in the United States for all healthcare settings. ICD-10-PCS (Procedure Coding System) is used for inpatient hospital procedure coding.

- **ICD-10-CM**: ~72,000 codes for diagnoses, signs, symptoms, external causes
- **ICD-10-PCS**: ~80,000 codes for inpatient procedures only
- **Effective Date**: ICD-10 was implemented October 1, 2015 in the US
- **Updates**: CMS publishes updates each October 1 (annual), with quarterly updates for new codes

---

## ICD-10-CM Code Structure

An ICD-10-CM diagnosis code has 3-7 characters. The first character is always alphabetic, characters 2-7 can be alphabetic or numeric.

**Structure**: `[Category].[Etiology][Anatomy][Severity][Extension]`

```
S52.521A
│  │  │││
│  │  ││└── 7th character (A = initial encounter for fracture)
│  │  │└── Extension (1 = right radius)
│  │  └── Site (distal radius/ulna)
│  └── Category (fracture of forearm)
└── Chapter (Injury, poisoning)
```

**Character Positions**:
| Character | Meaning | Example |
|-----------|---------|---------|
| 1 | Chapter/category (alpha) | S = Injury |
| 2-3 | Category (numeric) | 52 = Forearm fracture |
| 4 | Etiology/site | 5 = Lower end of radius |
| 5 | Laterality/severity | 2 = Left side |
| 6 | Extension/detail | 1 = Type I fracture |
| 7 | Encounter type | A = Initial, D = Subsequent, S = Sequela |

---

## ICD-10-CM Chapter Breakdown

| Chapter | Code Range | Description |
|---------|------------|-------------|
| 1 | A00-B99 | Certain infectious and parasitic diseases |
| 2 | C00-D49 | Neoplasms |
| 3 | D50-D89 | Diseases of the blood and immune system |
| 4 | E00-E89 | Endocrine, nutritional, and metabolic diseases |
| 5 | F01-F99 | Mental and behavioral disorders |
| 6 | G00-G99 | Diseases of the nervous system |
| 7 | H00-H59 | Diseases of the eye and adnexa |
| 8 | H60-H95 | Diseases of the ear and mastoid |
| 9 | I00-I99 | Diseases of the circulatory system |
| 10 | J00-J99 | Diseases of the respiratory system |
| 11 | K00-K95 | Diseases of the digestive system |
| 12 | L00-L99 | Diseases of the skin and subcutaneous tissue |
| 13 | M00-M99 | Diseases of the musculoskeletal system |
| 14 | N00-N99 | Diseases of the genitourinary system |
| 15 | O00-O9A | Pregnancy, childbirth, and the puerperium |
| 16 | P00-P96 | Certain conditions originating in the perinatal period |
| 17 | Q00-Q99 | Congenital malformations |
| 18 | R00-R99 | Symptoms, signs, and abnormal clinical findings |
| 19 | S00-T88 | Injury, poisoning, and certain other consequences |
| 20 | V00-Y99 | External causes of morbidity |
| 21 | Z00-Z99 | Factors influencing health status and health services |

---

## Key Chapters in Detail

### Chapter 1: Infectious Diseases (A00-B99)

- A00-B99 covers bacterial, viral, fungal, and parasitic infections
- **Sepsis coding**: Requires a code for the underlying infection (e.g., A41.9 for sepsis) followed by the septic shock code (R65.21) if present. The organism causing sepsis is also coded.
- **COVID-19**: U07.1 (COVID-19, virus identified)
- **HIV**: B20 (HIV disease) for symptomatic, Z21 (asymptomatic HIV)
- **MRSA**: B95.62 (MRSA as cause of disease classified elsewhere)

### Chapter 2: Neoplasms (C00-D49)

- **C00-C96**: Malignant neoplasms (cancer)
- **C7A**: Malignant neuroendocrine tumors
- **C80.1**: Malignant (primary) neoplasm, unspecified
- **D00-D09**: In situ neoplasms
- **D10-D36**: Benign neoplasms
- **D37-D48**: Neoplasms of uncertain behavior
- **D49**: Neoplasms of unspecified behavior

**Coding guidance for neoplasms**:
- Primary malignancy: C-code for the primary site
- Secondary malignancy: C77-C79 codes for metastatic sites
- Personal history of malignancy: Z85 code
- If patient is being treated for the primary malignancy, code the primary malignancy
- If patient is being treated for a complication or different condition, still code the malignancy if it affects management

### Chapter 4: Endocrine (E00-E89)

- **E08-E13**: Diabetes mellitus codes are the most commonly used
- **Fifth character for diabetes**: 0=not stated as uncontrolled, 1=uncontrolled (hyperglycemia), 9=no complications
- **Combination codes**: E10-E13 include the manifestation within the code

### Chapter 9: Circulatory (I00-I99)

- **I10**: Essential (primary) hypertension
- **I11**: Hypertensive heart disease
- **I12**: Hypertensive chronic kidney disease
- **I13**: Hypertensive heart and chronic kidney disease
- **I20-I25**: Ischemic heart diseases
- **I48**: Atrial fibrillation and flutter (I48.0 = paroxysmal, I48.1 = persistent, I48.2 = chronic)
- **I50**: Heart failure (I50.2 = systolic, I50.3 = diastolic, I50.4 = combined)

### Chapter 10: Respiratory (J00-J99)

- **J03.90**: Acute tonsillitis, unspecified
- **J18.9**: Pneumonia, unspecified organism
- **J44.9**: COPD, unspecified
- **J45**: Asthma codes with severity and exacerbation status
- **J96**: Respiratory failure (J96.0 = acute, J96.1 = chronic, J96.2 = acute and chronic)

### Chapter 11: Digestive (K00-K95)

- **K21.9**: GERD without esophagitis
- **K35.80**: Acute appendicitis without perforation
- **K40-K46**: Hernias (inguinal, femoral, umbilical, ventral)
- **K56.69**: Other intestinal obstruction
- **K57.3**: Diverticulosis of large intestine

### Chapter 13: Musculoskeletal (M00-M99)

- **M05-M06**: Rheumatoid arthritis
- **M16**: Osteoarthritis of hip
- **M17**: Osteoarthritis of knee
- **M25.51**: Pain in shoulder
- **M54.5**: Low back pain
- **M79.60**: Pain in limb, unspecified

### Chapter 19: Injury and Trauma (S00-T88)

- Fracture codes require 7th character extensions
- **Burns**: T20-T25 with fourth character for percentage of body surface
- **Poisonings**: T36-T50 by drug type
- **Adverse effects**: T78-T88

---

## Laterality

ICD-10-CM uses specific characters to indicate laterality:

| Digit | Meaning | Example |
|-------|---------|---------|
| 1 | Right | M17.11 (Unilateral OA, right knee) |
| 2 | Left | M17.12 (Unilateral OA, left knee) |
| 9 | Unspecified | M17.10 (Unilateral OA, unspecified knee) |
| 0 | Bilateral | M17.0 (Bilateral OA of knee) |

**Not all codes have laterality**. Some conditions are inherently bilateral or unspecified.

---

## 7th Character Extensions

Seventh characters are required for specific code categories, particularly:

| Category | 7th Char | Description |
|----------|----------|-------------|
| Fractures (S02, S12, S22, S32, S42, S52, S62, S72, S82, S92) | A | Initial encounter for closed fracture |
| | B | Initial encounter for open fracture |
| | D | Subsequent encounter for routine healing |
| | G | Subsequent encounter for delayed healing |
| | K | Subsequent encounter for nonunion |
| | P | Subsequent encounter for malunion |
| | S | Sequela |
| Injuries (S00-S99, T01-T14) | A | Initial encounter |
| | D | Subsequent encounter |
| | S | Sequela |
| External causes | A | Initial encounter |
| | D | Subsequent encounter |
| | S | Sequela |
| OB encounters (O00-O99) | 0 | Not applicable or unspecified |
| | 1 | Delivered |
| | 2 | Delivered with postpartum complication |
| | 3 | Antepartum condition with delivery |
| | 4 | Postpartum condition with delivery |
| Burns (T20-T32) | A | Initial encounter |
| | D | Subsequent encounter |
| | S | Sequela |

---

## Combination Codes

ICD-10-CM has numerous combination codes that capture two conditions or a condition and its manifestation in a single code. These reduce the total number of codes needed.

**Examples**:

| Code | Meaning | Components Captured |
|------|---------|---------------------|
| E10.51 | Type 1 DM with diabetic retinopathy with macular edema | Diabetes + retinopathy + macular edema |
| I25.110 | ASCVD of native coronary artery with unstable angina pectoris | ASCVD + unstable angina |
| J44.0 | COPD with acute lower respiratory infection | COPD + acute infection |
| K57.30 | Diverticulosis of large intestine without perforation or abscess | Diverticulosis + site + no complication |

**Coding rule**: When a combination code exists that fully describes the condition, do NOT code the individual components separately.

---

## Z Codes (Factors Influencing Health Status)

Z codes (Z00-Z99) are used for encounters for reasons other than illness or injury, or for conditions that influence the patient's health status but are not a current illness.

| Code Range | Category | Examples |
|------------|----------|----------|
| Z00-Z13 | Encounters for medical exams | Z00.00 (Well child), Z12.11 (Mammogram screening) |
| Z20-Z28 | Exposure/contact with communicable diseases | Z20.09 (Contact with COVID-19) |
| Z30-Z39 | Reproductive health encounters | Z30.013 (Initiation of IUD), Z34.00 (Prenatal visit, first trimester) |
| Z40-Z53 | Encounters for specific procedures/aftercare | Z48.02 (Removal of internal fixation device) |
| Z55-Z65 | Social determinants of health | Z59.0 (Homelessness), Z59.5 (Extreme poverty) |
| Z66-Z76 | Other specific health factors | Z68 (BMI codes), Z72.0 (Tobacco use) |
| Z77-Z99 | Family/personal history | Z85.3 (Personal history of breast cancer), Z92.82 (Status post COVID-19 vaccination) |

**Important rules for Z codes**:
- Z codes can be primary or secondary depending on the encounter
- Z68 BMI codes: Must be appended to the primary diagnosis (e.g., E66.01 for morbid obesity followed by Z68.41 for BMI 40.0-44.9, adult)
- Z79 codes for long-term drug therapy (e.g., Z79.01 for long-term anticoagulant use)

---

## External Cause Codes (V00-Y99)

External cause codes describe the cause of injury, poisoning, or adverse effect. They are **secondary codes only**.

**Structure**: V (transport accidents), W (falls, exposure), X (assault, intentional self-harm, venomous animals), Y (complications, legal intervention, war)

- **W01.XXXA**: Fall on same level from slipping
- **V43.52XA**: Car driver injured in collision with pick-up truck
- **Y92.00**: Place of occurrence, home
- **Y93.A1**: Activity, walking, marching, hiking

**Requirements**:
- Report external cause codes for all injuries, poisonings, and specific conditions
- Provide at minimum: mechanism, place of occurrence, activity, intent (unintentional/self-harm/assault)

---

## Present on Admission (POA) Indicator

POA is a requirement for inpatient claims to identify conditions present at admission vs. hospital-acquired.

| POA Code | Meaning |
|----------|---------|
| Y | Present at time of inpatient admission |
| N | Not present (developed during admission) |
| U | Documentation insufficient to determine |
| W | Clinically undetermined |
| 1 | Unreported/not used (CMS) |

**Impact**: Medicare will not pay for hospital-acquired conditions (HACs) -- these are conditions coded with POA=N and on the HAC list (e.g., stage 3-4 pressure ulcers, catheter-associated UTI, central line-associated bloodstream infection).

---

## ICD-10-PCS (Inpatient Procedure Coding)

ICD-10-PCS is used only for **inpatient hospital procedures** (not physician office or outpatient). Each code has exactly **7 alphanumeric characters**.

### Code Structure

**Example: `0DBB0ZX` (Excision of right lobe of liver, open approach, diagnostic)**

| Position | Value | Meaning |
|----------|-------|---------|
| 1: Section | 0 | Medical and Surgical |
| 2: Body System | D | Hepatobiliary System and Pancreas |
| 3: Root Operation | B | Excision |
| 4: Body Part | B | Right Lobe of Liver |
| 5: Approach | 0 | Open |
| 6: Device | Z | No Device |
| 7: Qualifier | X | Diagnostic |

### Sections

| Section Value | Description |
|:---:|-------------|
| 0 | Medical and Surgical |
| 1 | Obstetrics |
| 2 | Placement |
| 3 | Administration |
| 4 | Measurement and Monitoring |
| 5 | Extracorporeal Assistance and Performance |
| 6 | Extracorporeal Therapies |
| 7 | Osteopathic |
| 8 | Other Procedures |
| 9 | Chiropractic |
| B | Imaging |
| C | Nuclear Medicine |
| D | Radiation Oncology |
| F | Physical Rehabilitation and Diagnostic Audiology |
| G | Mental Health |
| H | Substance Abuse Treatment |
| X | New Technology |

### Root Operations (Section 0 - Medical/Surgical)

| Root Operation | Description | Example |
|----------------|-------------|---------|
| B | Excision | Cutting out/off a portion of a body part |
| 0 | Alteration | Modifying for cosmetic purposes |
| 1 | Bypass | Creating a new route for flow |
| 2 | Change | Exchanging a device |
| 3 | Control | Stopping bleeding |
| 4 | Creation | Creating a new body part |
| 5 | Destruction | Eradicating tissue |
| 6 | Detachment | Cutting off all/part of an extremity |
| 7 | Dilation | Expanding an orifice/lumen |
| 8 | Division | Separating a body part |
| 9 | Drainage | Taking/letting out fluids |
| B | Excision | Cutting out a portion |
| C | Extirpation | Taking out solid matter |
| D | Extraction | Pulling out/off a structure |
| F | Fragmentation | Breaking solid matter into pieces |
| G | Fusion | Joining body parts |
| H | Insertion | Putting in a device |
| J | Inspection | Visual and/or manual exploration |
| K | Map | Determining electrical impulses |
| L | Occlusion | Closing off an orifice/lumen |
| M | Reattachment | Putting back a detached body part |
| N | Release | Freeing a body part from constraint |
| P | Removal | Taking out a device |
| Q | Repair | Restoring to normal function |
| R | Replacement | Putting in a prosthesis |
| S | Resection | Cutting out all of a body part |
| T | Resection, Destructive | |
| V | Restriction | Partially closing an orifice/lumen |
| W | Revision | Correcting a malfunctioning device |
| X | Transfer | Moving to new location |
| Y | Transplantation | Putting a non-biological substitute |

### Approaches (Character 5)

| Approach | Description | Example |
|----------|-------------|---------|
| 0 | Open | Incision through skin and underlying tissue |
| 3 | Percutaneous | Needle puncture through skin |
| 4 | Percutaneous Endoscopic | Scope through skin |
| 7 | Via Natural/Artificial Opening | Scope through natural orifice |
| 8 | Via Natural/Artificial Opening Endoscopic | Scope through natural orifice with endoscopic visualization |
| F | Via Natural/Artificial Opening with Percutaneous Endoscopic Assistance | Combination approach |
| X | External | Direct visualization without incision |

### Devices (Character 6)

| Device Value | Category | Example |
|:---:|----------|---------|
| 0 | Drainage Device | Surgical drain |
| 1 | Radioactive Element | Seeds, radioactive band |
| 2 | Monitoring Device | Foley catheter |
| 3 | Infusion Device | Port-a-cath |
| 4 | Pacemaker | Cardiac pacemaker |
| 5 | Autologous Tissue Substitute | Skin graft |
| 6 | Synthetic Substitute | Mesh, prosthetic |
| 7 | Nonautologous Tissue Substitute | Cadaver graft |
| 8 | Intraluminal Device | Stent |
| 9 | Extraluminal Device | External fixator |
| J | Tissue Bank | Allograft |
| K | Bone Bank | Bone allograft |

---

## Official Coding Guidelines

### Acute vs. Chronic Conditions

- Code both acute and chronic when documented
- Acute usually sequenced first
- Example: "Acute exacerbation of COPD" = J44.1 (COPD with acute exacerbation)

### Combination Codes

- Use when a single code captures two conditions or a condition and manifestation
- Do NOT code components separately
- **Example**: E11.51 (Type 2 DM with retinopathy with macular edema) includes both conditions; do not add E11.3 and H35.30 separately

### Uncertain Diagnoses ("Rule Out")

- Diagnoses described as "rule out," "suspected," "possible," or "probable" in the outpatient setting should NOT be coded as confirmed
- Code the symptoms or signs that prompted the encounter
- Example: "Rule out MI" in outpatient = code chest pain (R07.9), not I21.x (MI)

### Multiple Conditions

- Sequence the condition that required the most resources first
- Code all documented conditions that affect patient management
- Do not code conditions that are integral to another condition (e.g., don't code "nausea" with "gastritis" unless separately clinically significant)

### Laterality and Specificity

- Use the most specific code available
- Use laterality codes when documented
- Use unspecified codes (e.g., M25.50 Pain in unspecified joint) only when documentation does not support a more specific code
- "Unspecified" should be avoided whenever possible

### Coding for Sepsis and SIRS

1. First: Code the underlying infection (e.g., pneumonia, UTI)
2. Second: Code R65.20 (severe sepsis without septic shock) or R65.21 (severe sepsis with septic shock)
3. Third: Code the organ dysfunction (e.g., acute kidney failure, acute respiratory failure)

**Example**: Pneumonia (J15.9) with severe sepsis with septic shock (R65.21) and acute respiratory failure (J96.00)

### Coding for Diabetes

- Use E08-E13 codes based on diabetes type
- Use the fourth character for complication type
- Always code the manifestation within the combination code
- Use additional codes for manifestations not included
- **Example**: E10.610 (Type 1 DM with diabetic neuropathic arthropathy) plus M14.60 (Charcot's joint) would be incorrect -- E10.610 already includes the arthropathy

### Coding for Hypertension

- Essential hypertension: I10
- Hypertensive heart disease: I11.0 (with heart failure) or I11.9 (without heart failure)
- Hypertensive CKD: I12.0 (with CKD stage 5/ESRD) or I12.9 (with CKD stage 1-4)
- Combined hypertensive heart and CKD: I13 codes
- **Important**: Do not code I10 with I11-I13; they are mutually exclusive

### Coding for Pregnancy

- Use O codes for pregnancy-related conditions
- Use Z3A codes for weeks of gestation (added in 2016)
- Sequence: O-code first, then any additional codes for complications
- Trimester is specified in O codes: 0=unspecified, 1=first, 2=second, 3=third
- Always use the appropriate 7th character for delivery encounters

### Coding for Poisonings, Adverse Effects, and Underdosing

- **Poisoning (overdose)**: T36-T50 with the appropriate 7th character and intent (accidental, intentional self-harm, assault, undetermined)
- **Adverse effect**: T36-T50 with the correct drug causing the effect, plus code for the nature of the adverse effect
- **Underdosing**: T36-T50 with 7th character 6

**Example**: Patient accidentally takes too much warfarin and develops bleeding. Code T45.511A (Poisoning by anticoagulants, accidental, initial encounter) and K92.0 (Hematemesis).

---

## Q&A Pairs

**Q:** A patient presents with chest pain. The physician documents "Rule out myocardial infarction" in the outpatient setting. What ICD-10-CM code should be used?

**A:** In the outpatient/ED setting, use the symptom code for chest pain (R07.9). Do NOT code a suspected or "rule out" diagnosis as if it were confirmed. The coding guidelines for outpatient encounters state that diagnoses documented as "possible," "probable," "rule out," or "suspected" should be coded as if they do not exist -- instead, code the signs, symptoms, or findings that prompted the encounter.

---

**Q:** What is the correct code for a patient with Type 2 diabetes with diabetic retinopathy and macular edema?

**A:** E11.31 (Type 2 diabetes mellitus with unspecified diabetic retinopathy with macular edema) if the retinopathy type is not specified, or E11.351 (Type 2 diabetes with proliferative diabetic retinopathy with macular edema) or E11.331 (Type 2 diabetes with nonproliferative diabetic retinopathy with macular edema) depending on the retinopathy type. This is a combination code -- do NOT separately code diabetes, retinopathy, and macular edema.

---

**Q:** A patient has a fracture of the left distal radius that is currently healing and is coming for a follow-up visit. What 7th character should be used?

**A:** Use 7th character "D" (Subsequent encounter for closed fracture with routine healing). For the specific code S52.532D (Other fracture of left distal radius, subsequent encounter for closed fracture with routine healing). The 7th character D is used for routine follow-up visits during healing. If the fracture is not healing properly, use G (delayed healing), K (nonunion), or P (malunion) as appropriate.

---

**Q:** When is a code from Chapter 20 (External Causes V00-Y99) required?

**A:** External cause codes are required for:
- Injury encounters (S00-T88)
- Poisonings
- Adverse effects of drugs
- Any encounter where an external cause (accident, fall, assault, etc.) is documented

At minimum, report the mechanism of injury, intent (unintentional, self-harm, assault), place of occurrence, and activity. However, for injury-related inpatient and outpatient encounters, reporting the mechanism (e.g., fall from bed W06.XXXA) is strongly recommended but may not be required by all payers -- check specific payer policies.

---

**Q:** A patient with COPD (J44.9) develops acute bronchitis (J20.9). What is the correct coding?

**A:** Code J44.0 (COPD with acute lower respiratory infection). This combination code includes both conditions. Do not code J44.9 and J20.9 separately unless the documentation specifically states a different relationship. The combination code takes precedence.

---

**Q:** What is the difference between ICD-10-CM and ICD-10-PCS in terms of usage?

**A:** 
- **ICD-10-CM**: Used by ALL providers (physicians, hospitals, clinics) in ALL settings (inpatient, outpatient, ED, nursing home) for DIAGNOSIS coding
- **ICD-10-PCS**: Used ONLY by hospitals for INPATIENT PROCEDURE coding. Physicians use CPT codes for procedures in all settings. Outpatient hospital departments use CPT, not PCS.

---

**Q:** A patient with essential hypertension (I10) also has chronic kidney disease stage 3 (N18.3). What is the correct coding?

**A:** Code I12.9 (Hypertensive chronic kidney disease with stage 1 through stage 4 chronic kidney disease, or unspecified chronic kidney disease). The combination code I12.9 captures both hypertension and CKD when documented together. If the CKD stages are 5 or ESRD, use I12.0. Do NOT separately code I10 and N18.3 when there is a relationship between hypertension and CKD.

---

**Q:** A patient has a pressure ulcer on the sacrum that is documented as stage 3. How is this coded?

**A:** Use L89.153 (Pressure ulcer of sacral region, stage 3). Pressure ulcer codes require:
1. Anatomic site (sacrum, heel, buttock, etc.)
2. Stage (1-4, unspecified, or unstageable)
3. Laterality (for extremities) or midline site

If the documentation does not specify a stage, use the unspecified stage code. If the ulcer is unstageable (covered with eschar), use the unstageable code.

---

**Q:** A patient is admitted for an inpatient procedure. The physician documents "possible sepsis" but the patient has clear signs of systemic inflammatory response syndrome (SIRS). What code should be used?

**A:** In the inpatient setting, uncertain diagnoses ("possible," "probable," "suspected") CAN be coded as if confirmed. If the physician documents "possible sepsis," code the sepsis (A41.9) and the SIRS. However, for outpatient/ED encounters, do NOT code uncertain diagnoses -- use symptom codes instead. The difference in coding guidelines between inpatient and outpatient is critical.

---

**Q:** What is a "POA indicator" and why does it matter?

**A:** POA (Present on Admission) indicates whether a condition was present at the time of inpatient admission. It matters because:
1. Medicare will not pay for hospital-acquired conditions (HACs) identified by POA=N
2. POA affects hospital quality metrics and public reporting
3. Incorrect POA assignment can result in claim denials or overpayment recoupment
4. POA=N for certain conditions (pressure ulcers stage 3/4, falls with trauma, certain infections) can reduce DRG payment

---

**Q:** A patient is brought to the ED after a motor vehicle accident. They have a traumatic brain injury (S06.9X9A), rib fractures (S22.3XXA), and a femur fracture (S72.90XA). How should these be sequenced?

**A:** Sequence the most severe/life-threatening condition first. Usually this would be the traumatic brain injury (S06.9X9A) followed by the femur fracture and rib fractures. The external cause code for the MVA (V-series code such as V43.52XA) should also be reported as a secondary code. The actual sequencing depends on the resources utilized and clinical focus of the encounter.

---

**Q:** How do you code for a patient receiving long-term anticoagulation therapy with warfarin?

**A:** Use Z79.01 (Long-term [current] use of anticoagulants). This Z code is reported as a secondary diagnosis. Additionally, if the patient develops a complication from the anticoagulation (e.g., bleeding), code the complication separately (e.g., D68.32 for hemorrhage due to extrinsic circulating anticoagulants).

---

**Q:** What is the difference between a "fracture" and a "stress fracture" in coding?

**A:** 
- **Traumatic fracture**: S-codes (e.g., S52.521A). These require 7th character extensions.
- **Stress fracture**: M84.3- (Stress fracture, not elsewhere classified). These also require 7th character extensions.
- **Pathological fracture due to neoplasm**: M84.5- (Pathological fracture in neoplastic disease)
- **Pathological fracture due to osteoporosis**: M80 codes

The distinction matters because stress fractures and pathological fractures have different underlying causes and follow different coding rules.

---

**Q:** A patient has diabetes (E11.9), hypertension (I10), hyperlipidemia (E78.5), and GERD (K21.9). What is the correct sequencing?

**A:** The primary diagnosis should be the condition that required the most resources during the encounter. If the visit was primarily for diabetes management, sequence E11.9 first, followed by I10, E78.5, and K21.9. If the visit was for HTN management, sequence I10 first. There is no mandatory sequencing order for these conditions -- it depends on the reason for the encounter.

---

**Q:** What is the correct code for a patient with sepsis due to E. coli UTI?

**A:** 
1. N39.0 (Urinary tract infection, site not specified)
2. A41.51 (Sepsis due to Escherichia coli [E. coli])
3. If the patient has severe sepsis, add R65.20 (severe sepsis without septic shock)
4. If the patient has septic shock, add R65.21 (severe sepsis with septic shock)

Alternatively, if the patient meets the criteria for urosepsis with organ dysfunction, code the infection and sepsis appropriately.

---

**Q:** What is the correct way to code for a patient who has both acute and chronic respiratory failure?

**A:** Use code J96.21 (Acute and chronic respiratory failure). This combination code captures both acute and chronic respiratory failure in a single code. Do not code J96.00 and J96.10 separately. Code documentation must clearly state "acute on chronic" respiratory failure.

---

**Q:** A patient with breast cancer (C50.912) develops bone metastases requiring treatment. What codes should be reported?

**A:** The primary diagnosis depends on the reason for the encounter:
- If the visit is for the bone metastases: C79.51 (Secondary malignant neoplasm of bone) as primary
- C50.912 (Malignant neoplasm of unspecified site of left female breast) as secondary
- If the visit is primarily for the breast cancer management, sequence C50.912 first

When a patient has active malignancy with metastases, both the primary and metastatic sites must be coded. The sequencing depends on the focus of care.

---

**Q:** A patient is seen for a routine physical with a BMI of 32.4. What codes should be reported?

**A:** For a routine physical:
- Z00.00 (Encounter for general adult medical examination without abnormal findings)
- Z68.34 (Body mass index [BMI] 32.0-32.9, adult)

If the exam finds an abnormality, use Z00.01 (with abnormal findings). BMI codes (Z68) should be appended to the primary diagnosis code when the BMI information is documented. Do not use Z68 codes alone.

---

**Q:** How do you code for an encounter for removal of internal fixation hardware (e.g., plate and screws from ankle)?

**A:** Use Z47.31 (Aftercare following explantation of internal fixation device). This code replaces the older practice of using status codes. If the hardware is being removed for a specific reason (e.g., infection, nonunion), code the complication or reason as the primary diagnosis and Z47.31 as secondary.

---

**Q:** A patient has an adverse reaction to a prescribed medication (non-opioid analgesic). What is the correct coding approach?

**A:** 
1. Code the nature of the adverse effect first (e.g., rash L27.0, nausea R11.2)
2. Code the adverse effect of the drug (T39.8X5A = Adverse effect of nonopioid analgesics, initial encounter)
3. The T39.8X5A captures the drug causing the effect

Do NOT use the "poisoning" code (accidental overdose) for adverse effects -- use the "adverse effect" 7th character (5).

---

**Q:** What is the BMI Z-code for a patient with a BMI of 35.0?

**A:** Z68.35 (BMI 35.0-35.9). Z68 codes are in 0.9-range increments, always using the lower bound of the range. For BMI 35.0-35.9, use Z68.35. For adult BMI, use Z68.3x (30-39 range) or Z68.4x (40+ range). For pediatric patients, use Z68.5x codes.

---

**Q:** A patient is admitted for total knee replacement (CPT 27447). The diagnosis is osteoarthritis of the knee. How should this be coded?

**A:** 
- **ICD-10-CM**: M17.9 (Osteoarthritis of knee, unspecified) if laterality is not documented, or M17.11 (Right) / M17.12 (Left) if laterality is documented. Always use the most specific code.
- **ICD-10-PCS** (inpatient): 0SRD0J9 (Replacement of left knee joint with synthetic substitute, cement, open approach) or 0SRC0J9 (right knee).
- Do not code the surgical approach, the indication for surgery, or the complications as a diagnosis unless they are present and affect management.

---

**Q:** A patient with a history of colon cancer is seen for a screening colonoscopy. What codes should be reported?

**A:** The appropriate coding depends on whether the screening is for surveillance:
- If the colon cancer was completely resected with no recurrence and the screening is for surveillance: Z08 (Encounter for follow-up examination after completed treatment for malignant neoplasm) plus Z85.038 (Personal history of malignant neoplasm of colon)
- If the patient had a history and the screening is for early detection: Z12.11 (Encounter for screening for malignant neoplasm of colon) plus Z85.038

A screening colonoscopy for a patient with personal history of cancer is typically reported with Z11.x (Encounter for screening for malignant neoplasms) rather than Z08.

---

**Q:** What is the correct way to code for a patient with anemia due to chronic kidney disease (CKD)?

**A:** 
- Code CKD first (N18.x with appropriate stage)
- Code anemia secondary to CKD (D63.1 = Anemia in chronic kidney disease)
- D63.1 is a manifestation code (etiology/manifestation pairing) and must be reported secondary to the underlying CKD

Do NOT code D63.1 first. It is always secondary. Also, do NOT code D50.9 (iron deficiency anemia) unless specifically documented as iron deficiency.

---

**Q:** A patient has a fracture of the femoral neck. The 7th character A, D, and S: what is the difference?

**A:** 
- **A** (Initial encounter): Active treatment for the fracture. Used during the acute phase, ER visit, initial surgery, or definitive treatment. Also used for open fractures.
- **D** (Subsequent encounter): Routine follow-up care during healing phase. Cast checks, medication adjustments, physical therapy. Use when the fracture is progressing normally.
- **S** (Sequela): Late effects or residual conditions from the healed fracture. Examples: malunion, nonunion, chronic pain, limited range of motion after healing.

The same fracture code with different 7th characters can be reported multiple times over the patient's care course as the encounter type changes.