# Modifiers: CPT and HCPCS Modifier Reference

## Overview

Modifiers are two-character codes appended to CPT or HCPCS Level II codes to provide additional information about the service or procedure performed. They indicate that a service has been altered in some way without changing the fundamental definition of the code.

**Purpose of modifiers**:
- Identify anatomical location
- Indicate bilateral or multiple procedures
- Show reduced or discontinued services
- Describe surgical care components
- Differentiate professional vs. technical components
- Report assistant surgeon services
- Indicate special circumstances (staged, repeat, unrelated)

---

## Anatomical Modifiers

### LT and RT -- Left and Right

| Modifier | Description |
|----------|-------------|
| LT | Left side (used when a procedure is performed on the left side of the body) |
| RT | Right side (used when a procedure is performed on the right side of the body) |

**Use**: Required when a procedure is performed on a paired organ, extremity, or bilateral structure. Many payers require LT/RT for claims processing. When both sides are performed, use modifier 50 (bilateral) instead of LT and RT on separate lines.

**Example**: Knee arthroscopy right knee -- 29881-RT

### Eyelid Modifiers (E1-E4)

| Modifier | Description |
|----------|-------------|
| E1 | Upper left eyelid |
| E2 | Lower left eyelid |
| E3 | Upper right eyelid |
| E4 | Lower right eyelid |

**Example**: Excision of chalazion, left upper eyelid -- 67801-E1

### Finger Modifiers (FA-F9)

| Modifier | Description |
|----------|-------------|
| FA | Left hand, thumb |
| F1 | Left hand, second digit |
| F2 | Left hand, third digit |
| F3 | Left hand, fourth digit |
| F4 | Left hand, fifth digit |
| F5 | Right hand, thumb |
| F6 | Right hand, second digit |
| F7 | Right hand, third digit |
| F8 | Right hand, fourth digit |
| F9 | Right hand, fifth digit |

**Example**: Trigger finger release, left ring finger -- 26055-F3

### Toe Modifiers (TA-T9)

| Modifier | Description |
|----------|-------------|
| TA | Left foot, great toe |
| T1 | Left foot, second digit |
| T2 | Left foot, third digit |
| T3 | Left foot, fourth digit |
| T4 | Left foot, fifth digit |
| T5 | Right foot, great toe |
| T6 | Right foot, second digit |
| T7 | Right foot, third digit |
| T8 | Right foot, fourth digit |
| T9 | Right foot, fifth digit |

### Cardiac Modifiers

| Modifier | Description |
|----------|-------------|
| LC | Left circumflex coronary artery |
| LD | Left anterior descending coronary artery |
| RC | Right coronary artery |

**Example**: Stent placement in LAD -- 92928-LD

### Vascular Modifiers

| Modifier | Description | Use |
|----------|-------------|-----|
| LM | Left main coronary artery | Used for stent placement, angioplasty |
| RI | Ramus intermedius coronary artery | Used when the target vessel is the ramus |

---

## Global Surgery Modifiers

### Modifier 24 -- Unrelated E/M During Postoperative Period

**Description**: An evaluation and management service provided by the same physician during the postoperative period of a surgery, when the service is unrelated to the surgery.

**Example**: A patient is 3 weeks post cholecystectomy (90-day global) and presents with a UTI. The surgeon performs an office visit. Append modifier 24 to the E/M code (e.g., 99213-24).

**Documentation**: The medical record must clearly demonstrate the E/M is for a completely unrelated condition.

### Modifier 25 -- Significant, Separately Identifiable E/M

**Description**: A significant, separately identifiable evaluation and management service by the same physician on the same day of a procedure or other service.

**Example**: Patient presents for hypertension follow-up. During the visit, the physician also removes a skin tag. Bill 99213-25 (E/M for HTN) and 11200 (skin tag removal).

**Key rules**:
- The E/M must be above and beyond the pre-procedure work
- Do not use modifier 25 with minimal E/M codes (99211)
- Documentation must clearly separate the E/M work from the procedure decision

### Modifier 57 -- Decision for Surgery

**Description**: An evaluation and management service that results in the initial decision to perform major surgery (typically 90-day global period).

**Use**: Append modifier 57 to the E/M code when the decision for major surgery is made during the visit.

**Example**: A patient is seen in the office for hip pain, and based on history, exam, and X-ray findings, the physician decides to recommend total hip arthroplasty. The office visit is reported as 99204-57.

**Important**: Modifier 57 is for **major surgery** (90-day global). For minor surgeries (0-10 day global), use modifier 25 instead. Medicare considers procedures with a 90-day global period as major for modifier 57 purposes.

### Modifier 54 -- Surgical Care Only

**Description**: When one physician performs the surgical procedure and another provides preoperative and/or postoperative management.

**Use**: The surgeon appends modifier 54 to indicate they are billing only for the intraoperative portion of the global surgical package.

**Example**: A surgeon performs an emergency appendectomy but the post-op care is managed by the hospitalist. The surgeon bills 47562-54.

**Payment**: The surgeon receives a percentage of the global fee based on the portion of care provided (typically 70-80% depending on payer).

### Modifier 55 -- Postoperative Management Only

**Description**: When a physician provides only the postoperative management of a surgical patient during the global period.

**Example**: A patient is transferred to a different surgeon for post-op care after a hip replacement. The receiving surgeon bills 27447-55.

### Modifier 56 -- Preoperative Management Only

**Description**: When a physician provides only the preoperative care for a surgical patient.

**Example**: An anesthesiologist manages pre-operative optimization of a complex medical patient before surgery. Bill the appropriate E/M with modifier 56.

### Modifier 58 -- Staged or Related Procedure During Postoperative Period

**Description**: A procedure or service that was:
1. Staged or planned (e.g., staged burn débridement)
2. More extensive than the original procedure
3. For therapy following diagnostic surgical procedure

**Example**: A patient who underwent a mastectomy (19303) requires a staged tissue expander placement (19357). The expander placement is in the global period but was planned. Bill 19357-58.

**Key distinction**: Modifier 58 vs. modifier 78:
- **58**: Planned or staged procedure (related but anticipated)
- **78**: Unplanned return to OR for complication

### Modifier 79 -- Unrelated Procedure During Postoperative Period

**Description**: An unrelated procedure performed by the same physician during the postoperative period of a different surgery.

**Example**: Two weeks after an inguinal hernia repair (49505), the patient falls and fractures their wrist, requiring ORIF (25609). The same surgeon performs both. Bill 25609-79.

---

## Professional and Technical Component Modifiers

### Modifier 26 -- Professional Component

**Description**: The professional component of a service, including the physician's interpretation and report.

**Use**: When a physician interprets a test but does not own the equipment or employ the technician.

**Example**: A radiologist interprets a CT scan performed at a hospital. Bill 74150-26 (CT abdomen, professional component only).

**Payment**: The professional component is typically 30-40% of the global service fee schedule amount.

### Modifier TC -- Technical Component

**Description**: The technical component of a service, including the equipment, supplies, and technician time.

**Use**: When a facility (hospital, imaging center) performs the test but does not interpret it.

**Example**: The hospital performs the CT scan. Bill 74150-TC (technical component only).

**Payment**: The technical component is typically 60-70% of the global service fee schedule amount.

**Note**: Modifier TC is a HCPCS Level II modifier, not a CPT modifier. Some payers accept -26 and -TC on CPT codes, while others require the global (no modifier) approach.

---

## Payment Modifiers

### Modifier 50 -- Bilateral Procedure

**Description**: Bilateral procedure performed on both sides of the body during the same operative session.

**Use**: Append modifier 50 to the CPT code when the same procedure is performed on paired organs or symmetrical body parts (both arms, both legs, both eyes, both ears).

**Example**: Bilateral knee arthroscopy -- 29881-50

**Medicare Payment Rule**: 
- For bilateral indicator 1 or 2: pay 150% of the fee schedule (one line, modifier 50)
- For bilateral indicator 0: use two lines with RT and LT separately
- For bilateral indicator 3: always bilateral by definition, pay 100%

**Private payer variation**: Some commercial payers require two lines with 50% each rather than one line with modifier 50.

### Modifier 51 -- Multiple Procedures

**Description**: Multiple procedures performed during the same surgical session (by the same physician).

**Use**: Medicare recommends appending modifier 51 to second and subsequent procedures. However, Medicare's multiple procedure payment reduction is applied automatically by their system.

**Example**: Three procedures are performed: 27130 (hip replacement), 29881-51 (knee arthroscopy), 20670-51 (hardware removal).

**Payment adjustment**: 100% for highest value, 50% for second, 25% for third and subsequent.

**Exception**: Modifier 51 is NOT used with:
- E/M services
- Add-on codes
- Preventive services
- Physical medicine services

### Modifier 52 -- Reduced Services

**Description**: When a service is partially reduced or eliminated at the physician's discretion, without impacting the quality of the service provided.

**Example**: A physician performs a consultation but the patient leaves before the examination is complete. Bill 99244-52.

**Documentation**: The medical record must explain why the service was reduced and what portions were completed.

### Modifier 53 -- Discontinued Procedure

**Description**: When a procedure is terminated due to extenuating circumstances or those that threaten the patient's well-being.

**Example**: During a colonoscopy, the patient develops respiratory distress and the procedure is stopped. Bill 45378-53.

**Key distinction**: Modifier 52 (reduced) vs. modifier 53 (discontinued):
- **52**: Service was voluntarily reduced but completed as modified
- **53**: Service was terminated due to medical necessity (patient safety)

### Modifier 59 -- Distinct Procedural Service

**Description**: Indicates that a procedure or service was distinct or independent from other services performed on the same day.

**Use**: This is the most commonly used modifier for unbundling. It is used when two normally bundled procedures are performed:

1. **Different session** (e.g., diagnostic endoscopy and surgical endoscopy)
2. **Different procedure** (e.g., colonoscopy and EGD)
3. **Different site/organ system** (e.g., cataract surgery with lid lesion removal)
4. **Separate incision/excision** (e.g., excision of two separate lesions)
5. **Separate lesion** (e.g., removal of multiple skin lesions)
6. **Separate injury** (e.g., repair of multiple lacerations)

**Example**: NCCI edits bundle diagnostic colonoscopy (45378) with colonoscopy with polypectomy (45385). If both were truly performed in separate sessions, append modifier 59 to 45378.

**CMS "-X" modifiers** (preferred over 59):

| Modifier | Description | When to Use |
|----------|-------------|-------------|
| XE | Separate encounter | Different encounter on different date |
| XS | Separate structure | Different anatomic site/organ |
| XP | Separate practitioner | Different provider |
| XU | Unusual non-overlapping | Service not normally part of the code combination |

**Preference**: CMS strongly prefers the -X{EPSU} modifiers over modifier 59 because they provide greater specificity.

### Modifier 62 -- Co-Surgery

**Description**: Two surgeons (typically from different specialties) perform distinct parts of a single surgical procedure.

**Use**: Both surgeons bill the same CPT code with modifier 62.

**Example**: A neurosurgeon and an ENT surgeon perform a skull base tumor resection together. Both bill the same code with modifier 62 (e.g., 61580-62).

**Payment**: Each surgeon receives 62.5% of the fee schedule amount (total 125%).

### Modifier 66 -- Surgical Team

**Description**: When a highly complex procedure requires the concurrent services of several physicians, often of different specialties, plus supporting personnel.

**Use**: The primary surgeon bills with modifier 66.

**Example**: Organ transplantation (e.g., liver transplant 47135-66), conjoined twin separation.

**Payment**: Determined on a case-by-case basis by the Medicare Administrative Contractor (MAC).

### Modifier 74 -- Discontinued Outpatient/ASC Procedure

**Description**: When an outpatient or ambulatory surgery center (ASC) procedure is terminated after the induction of anesthesia or the initiation of the procedure.

**Use**: The facility/appends modifier 74 to indicate the procedure was started but not completed.

**Example**: A patient is anesthetized for cataract surgery, but the patient becomes hemodynamically unstable and the procedure is cancelled. The ASC bills 66984-74.

### Modifier 76 -- Repeat Procedure by Same Physician

**Description**: When the same physician repeats a procedure on the same day.

**Example**: A radiologist performs a CT scan that is technically inadequate due to patient motion. A repeat scan is performed. Bill 74150-76.

### Modifier 77 -- Repeat Procedure by Different Physician

**Description**: When a different physician repeats a procedure on the same day.

**Example**: An emergency physician performs a lumbar puncture that results in a traumatic tap. Later, the neurologist repeats the LP. The neurologist bills 62270-77.

### Modifier 78 -- Return to OR for Related Procedure

**Description**: An unplanned return to the operating room by the same physician during the postoperative period for a related procedure.

**Example**: A patient who had a hip replacement develops a hematoma on post-op day 3 requiring evacuation. The surgeon returns to the OR. Bill 27345-78 (arthrotomy for hip drainage).

**Payment**: Medicare pays approximately 80% of the fee schedule for 090-day global procedures with modifier 78.

### Modifier 80 -- Assistant Surgeon

**Description**: A physician assistant during surgery.

**Example**: A general surgeon performs a Whipple procedure (48150) and another surgeon assists. The assistant bills 48150-80.

**Payment**: 20% of the fee schedule for the primary procedure.

### Modifier 81 -- Minimum Assistant Surgeon

**Description**: When a minimum assistant surgeon is required for a procedure.

**Payment**: Typically 10-15% of the fee schedule.

### Modifier 82 -- Assistant Surgeon (Resident Unavailable)

**Description**: When a teaching hospital's qualified resident is not available to assist, and another surgeon assists.

### Modifier 99 -- Multiple Modifiers

**Description**: Used when more than four modifiers apply to a single code line. Append modifier 99 instead of listing all modifiers.

**Example**: A procedure requires modifiers 50, 59, 80, and LT. Instead of listing all four, the claim uses modifier 99, and the additional modifiers are noted in the claim note field.

---

## CMS-Specific HCPCS Modifiers

### AS -- Assistant at Surgery (Non-Physician)

**Description**: Non-physician practitioner (PA, NP, CNS) serving as an assistant at surgery.

**Use**: Appended to the surgical CPT code billed by the assistant. Payment is at 85% of the physician assistant fee schedule.

### GA -- ABN on File

**Description**: Waiver of liability statement (Advanced Beneficiary Notice) issued to the beneficiary, on file.

**Example**: Medicare likely will not cover a screening test deemed not medically necessary, but the provider has the patient sign an ABN. Bill with GA.

### GY -- Statutorily Excluded Service

**Description**: Item or service is statutorily excluded from Medicare coverage (e.g., cosmetic surgery, hearing aids, routine foot care, dental services).

**Use**: Bill with GY to notify Medicare that the service was provided but is not covered by law. This allows Medicare to apply to secondary payers.

### GZ -- Expected Denial, No ABN

**Description**: Item or service is expected to be denied as not reasonable and necessary, but the provider did **not** obtain an ABN.

**Use**: The claim is submitted for informational purposes. The provider cannot bill the patient for GZ-denied services.

### KX -- Medical Necessity Criteria Met

**Description**: Requirements specified in the applicable local/national coverage determination (LCD/NCD) have been met.

**Use**: Primarily used with DMEPOS and therapy services to attest that documentation of medical necessity is on file.

### Q0 -- Investigational Clinical Service

**Description**: Service provided in a Medicare-approved clinical research study.

### Q1 -- Routine Clinical Service in Clinical Research

**Description**: Routine care provided in a qualifying clinical trial.

### Q5 -- Reciprocal Billing Arrangement

**Description**: Service furnished by a substitute physician under a reciprocal billing arrangement.

**Example**: Two surgeons in a group cover each other's practices. Dr. A sees Dr. B's patient and bills using Dr. B's NPI with modifier Q5.

### Q6 -- Locum Tenens

**Description**: Service furnished by a locum tenens physician.

**Example**: A surgeon hires a temporary surgeon to cover their practice while on vacation. The regular surgeon bills with modifier Q6.

### QW -- CLIA-Waived Test

**Description**: Clinical Laboratory Improvement Amendments (CLIA) waived test.

**Example**: A physician office performs a rapid strep test. Append QW to the lab code (e.g., 87880QW).

---

## Ambulance Modifiers

Ambulance modifiers consist of two characters: the first character indicates the **origin**, the second character indicates the **destination**.

| Code | Meaning |
|------|---------|
| D | Physician's office, hospital outpatient, clinic, dialysis center |
| E | Residential, domiciliary, nursing home |
| G | Hospital-based ESRD facility |
| H | Hospital |
| I | Site of transfer between modes (e.g., ambulance to fixed wing) |
| J | Freestanding ESRD facility |
| N | Skilled nursing facility (SNF) |
| P | Non-hospital-based dialysis facility |
| R | Residence |
| S | Scene of accident or acute event |
| X | Intermediate stop at a physician's office in route to hospital |

**Common combinations**:
- **RH**: Residence to hospital (most common emergency transport)
- **RR**: Residence to another residence (non-emergency)
- **SH**: Scene of accident to hospital (emergency, from accident scene)
- **HN**: Hospital to SNF (transfer)
- **HH**: Hospital to hospital (interfacility transfer)
- **RG**: Residence to dialysis center
- **RD**: Residence to diagnostic/testing facility

**Example**: Ground ambulance transport from residence to hospital emergency: A0427 (ALS emergency) with modifier RH.

---

## Modifier Selection Algorithm

When deciding which modifier to use for surgical unbundling:

```
1. Different encounter?                          → XE (or 59)
2. Different structure/organ?                    → XS (or LT, RT, E1-E4, FA-F9, TA-T9)
3. Different practitioner?                       → XP
4. Different service, not overlapping?           → XU (or 59)
5. Bilateral?                                    → 50 (or LT + RT on separate lines)
6. Multiple procedures?                          → 51
7. Assistant surgeon?                            → 80, 81, 82, or AS
8. Co-surgeon?                                   → 62
9. Staged/planned?                               → 58
10. Return to OR (unplanned related)?            → 78
11. Unrelated during global period?              → 79
12. Repeat procedure?                            → 76 (same MD) or 77 (different MD)
13. Surgical care only?                          → 54
14. Post-op management only?                     → 55
15. Reduced service?                             → 52
16. Discontinued due to patient safety?          → 53
```

---

## Q&A Pairs

**Q:** What is the difference between modifier 59 and modifier XS?

**A:** Modifier 59 is the general "distinct procedural service" modifier. Modifier XS is a more specific subset indicating "separate structure" (different anatomic site or organ). CMS encourages using XS over 59 when the distinction is based on different anatomical structures. For example, if a patient has bilateral knee arthroscopies in the same session, use XS rather than 59 because the distinction is anatomical. Always use the most specific modifier.

---

**Q:** A patient undergoes a laparoscopic cholecystectomy (47562) and an intraoperative cholangiogram (47563, which is bundled). How do you unbundle?

**A:** The cholangiogram (47563) is a component of the cholecystectomy (47562) and is normally bundled by NCCI edits. However, if the cholangiogram was performed for a distinct indication (e.g., suspected common bile duct stone) and not as a routine part of the cholecystectomy, append modifier 59 to 47563. Otherwise, only 47562 should be billed.

---

**Q:** When is modifier 50 used vs. billing two lines with RT and LT?

**A:** Use modifier 50 when the CPT code's bilateral indicator shows **1 or 2** in the Medicare Physician Fee Schedule. This means the code has a standard bilateral pricing adjustment (150% for bilateral). Use two separate lines with RT and LT when the bilateral indicator is **0 or 9**. Codes with indicator 0 are not defined as bilateral -- they are reported on two lines. Codes with indicator 9 are inherently bilateral (not applicable).

---

**Q:** What is the correct use of modifier 57 vs. modifier 25?

**A:** 
- **Modifier 57**: Used when the E/M service results in the decision to perform **major surgery** (90-day global period). Medicare will not pay for the E/M during the global period without modifier 57.
- **Modifier 25**: Used when the E/M is significant and separately identifiable from a **minor procedure** (0- or 10-day global period) performed on the same day.

The key is the global period of the surgery. For 90-day global surgeries, modifier 57 applies to same-day E/M. For 0- or 10-day global procedures, modifier 25 applies.

---

**Q:** Can an E/M code be billed with modifier 24 during a post-operative global period for a chronic condition?

**A:** Yes. Modifier 24 indicates the E/M service is unrelated to the surgery. If a patient is in the post-op period for an appendectomy (90-day global) and comes in for management of diabetes, the E/M (e.g., 99214) is billed with modifier 24. The documentation must clearly show the service was for an unrelated condition.

---

**Q:** What documentation is needed to support modifier 22 (Increased Procedural Service)?

**A:** Modifier 22 requires explicit documentation of:
1. The nature of the increased complexity (e.g., extensive adhesions, morbid obesity, anatomical anomalies)
2. The extra time required (how much more than typical)
3. The specific techniques or approaches used to address the complexity
4. The outcome or result

Do not append modifier 22 simply because the case was "difficult." Submit a detailed operative note and a cover letter explaining the increased work. Many payers require prior authorization or special handling for modifier 22 claims.

---

**Q:** What is the difference between modifiers 78 and 58?

**A:** 
- **Modifier 78**: Unplanned return to the OR for a **related** procedure during the postoperative period (e.g., post-op bleeding requiring evacuation). The procedure was not planned.
- **Modifier 58**: **Planned or staged** procedure during the postoperative period (e.g., a second-stage reconstruction after mastectomy). The procedure was expected.

Correct modifier selection significantly affects payment. Modifier 78 typically pays 80% of the fee schedule. Modifier 58 pays 100% but is subject to the usual global period rules.

---

**Q:** When would you use modifier 52 vs. modifier 53?

**A:** 
- **52 (Reduced Services)**: The procedure is completed but at a reduced level. For example, an endoscopy that should have been full but was limited by anatomy (e.g., colonoscopy only to the splenic flexure due to stricture). The service was voluntarily reduced but the procedure was still complete for the clinical scenario.
- **53 (Discontinued Procedure)**: The procedure is **stopped** due to patient safety concerns. For example, the patient develops bradycardia during anesthesia and the colonoscopy is cancelled entirely. The procedure was not completed.

Use 53 when patient safety is the reason for stopping. Use 52 when the procedure simply was not performed to its intended extent but was clinically adequate.

---

**Q:** A PA assists in surgery. What modifier should be used?

**A:** Modifier AS (Assistant at Surgery, non-physician). This modifier is used for physician assistants, nurse practitioners, and clinical nurse specialists serving as surgical assistants. The claim is submitted under the PA's NPI with modifier AS. Payment is at 85% of the physician assistant fee schedule. Do not use modifier 80 (which is for physician assistant surgeons).

---

**Q:** A patient is discharged from the hospital on the same day as admission (observation status). The physician performs a history, exam, and MDM. What is the correct code and modifier combination?

**A:** Use 99234-99236 (Hospital inpatient or observation care, same date admit and discharge). These codes include both the admission and discharge in a single code. No modifier is needed for the same-day admit/discharge. If observation-to-inpatient conversion occurs across multiple days, separate codes for observation (99224-99226) and inpatient management (99231-99233) would apply.

---

**Q:** When should the -TC modifier be used vs. billing a global service?

**A:** 
- **TC (Technical Component)**: Use when the facility provides all technical aspects (equipment, supplies, technician) but does not provide interpretation. Example: Hospital performs CT scan, radiologist is from a separate group.
- **Global (no modifier)**: Use when the same provider owns the equipment AND provides the interpretation. Example: A private radiology group owns the CT machine and employs the radiologist who reads the study.

Hospitals typically bill TC; independent radiology groups typically bill global.

---

**Q:** What is the purpose of the -XE, -XS, -XP, and -XU modifiers?

**A:** These are "Medicare NCCI-associated modifiers" introduced as alternatives to modifier 59:

| Modifier | Meaning | Example |
|----------|---------|---------|
| XE | Separate encounter | Colonoscopy Monday, EGD Friday -- different days |
| XS | Separate structure | Left knee scope + right knee scope -- different joints |
| XP | Separate practitioner | Psychologist does testing, psychiatrist does med management |
| XU | Unusual non-overlapping | ECG with stress test -- the combination is not normally done together |

Using these modifiers reduces the likelihood of audits compared to modifier 59, as they provide specific reasons for unbundling.

---

**Q:** Can you use modifier 59 with add-on codes?

**A:** No. Add-on codes (identified by "+" in the CPT manual) are inherently distinct from their primary procedure and do not require modifier 59. They are always paid at 100% and are exempt from multiple procedure reduction. Never append modifier 59 to add-on codes.

---

**Q:** What is the difference between modifiers 50 and 51 when billing for bilateral and multiple procedures together?

**A:** 
- **50 (Bilateral)**: Used when the SAME procedure is performed on BOTH SIDES (e.g., bilateral knee arthroscopy = 29881-50)
- **51 (Multiple Procedures)**: Used for DIFFERENT procedures performed on the same day (e.g., knee arthroscopy and hip injection)

When both apply (e.g., bilateral procedure + additional procedure), bill the bilateral procedure with modifier 50 as the primary, and the additional procedure with modifier 51.

**Example**: Bilateral knee arthroscopy (29881-50) and right hip injection (20610-RT-51). Payment: 29881-50 at 150%, 20610-RT-51 at 50%.

---

**Q:** When should modifier 79 be used vs. modifier 24?

**A:** 
- **79 (Unrelated Procedure)**: Used when the same physician performs an **unrelated surgical procedure** during the postoperative period of a different surgery. The modifier goes on the new surgical code.
- **24 (Unrelated E/M)**: Used when the same physician performs an **unrelated E/M service** during the postoperative period. The modifier goes on the E/M code.

The key difference: 79 applies to procedures/surgeries; 24 applies to E/M services.

---

**Q:** What does it mean when a CPT code has "no modifier 50 applicable"?

**A:** Some CPT codes have a bilateral indicator of "0" in the Medicare Physician Fee Schedule, meaning modifier 50 is NOT applicable. This typically means:
- The code describes an inherently unilateral procedure that cannot be bilateral
- The code already includes bilateral services
- The code describes a midline procedure (cannot be performed bilaterally)

For these codes, if the procedure is performed on both sides, bill two separate lines with RT and LT modifiers, or consider whether an alternative code (like an unbundled code) exists.

---

**Q:** A patient receives a partial colonoscopy (only to the splenic flexure) due to poor prep. What modifiers should be used?

**A:** Append modifier 52 (Reduced Services) to the colonoscopy code (e.g., 45378-52). This indicates the procedure was initiated and completed but at a reduced level. Documentation must:
1. State the extent of the exam (e.g., "to splenic flexure")
2. Explain why the full exam could not be completed
3. Describe the poor prep quality

Some payers require specific documentation for reduced service claims. Do not append modifier 53 (Discontinued) because the procedure was not terminated for patient safety reasons.

---

**Q:** What is the role of modifier modifiers 80, 81, and 82 in surgical assisting?

**A:** 
- **80 (Assistant Surgeon)**: A qualified physician provides surgical assistance. Payment is 20% of the fee schedule.
- **81 (Minimum Assistant Surgeon)**: A physician provides minimal assistance during a procedure. Payment varies by payer.
- **82 (Assistant Surgeon - Resident Unavailable)**: Used in teaching hospitals when a qualified resident is not available to assist. Payment is 20% of the fee schedule.

The assistant surgeon bills the same CPT code as the primary surgeon with the appropriate modifier appended.

---

**Q:** Should modifier Q5 or Q6 be used when covering for another physician during vacation?

**A:** 
- **Q5**: Used when there is a **reciprocal billing arrangement** -- two or more physicians cover each other's practices on a regular basis. Example: Three surgeons in town cover each other's patients when one is on call.
- **Q6**: Used when a **locum tenens** (paid substitute) covers for an absent physician. The covering physician is not part of an ongoing reciprocal arrangement.

For a planned vacation, if you have a reciprocal arrangement (e.g., your partner covers your practice when you are away, and you cover theirs when they are away), use Q5. If you hire a temporary paid physician, use Q6.

---

**Q:** How do you bill for bilateral surgery when one side is a different procedure?

**A:** If the same procedure is performed on both sides, use modifier 50. If different procedures are performed on each side (e.g., left knee scope with meniscectomy, right knee scope with chondroplasty), bill each code with the appropriate lateral modifier (RT/LT) on separate lines. Do NOT combine them with modifier 50 since they are different CPT codes.

---

**Q:** What is the correct modifier for a physician who provides only the interpretation portion of a vascular study?

**A:** Append modifier 26 (Professional Component) to the technical code. For example, if a cardiologist interprets a carotid duplex scan performed by the hospital, bill 93880-26. The hospital bills 93880-TC (technical component). If the cardiologist's group owns the equipment and employs the sonographer, the global code (93880 without modifier) would be used.

---

**Q:** When should modifier 79 be used instead of modifier 58 for a procedure in the global period?

**A:** 
- **58 (Staged/Related)**: The procedure is planned, staged, or more extensive than the original. It is related to the original surgery but was expected.
- **79 (Unrelated)**: The procedure is completely unrelated to the original surgery and was not expected.

**Example**: Patient had a hip replacement (27130, 90-day global). Two weeks later, the SAME surgeon performs an ORIF of the patient's forearm due to a fall. This is an unrelated procedure during the post-op period. Use modifier 79 (27447-79). Do not use modifier 58 because this was not planned or staged.

---

**Q:** What is the billing implication of modifier 62 (co-surgery)?

**A:** When two surgeons co-manage a procedure, each bills the same CPT code with modifier 62. Medicare pays 62.5% of the fee schedule to each surgeon, for a total of 125%. The additional 25% accounts for the coordination and complexity of co-management. Both surgeons' documentation must explain their distinct roles in the procedure.

Documentation requirements:
- Operative note must show both surgeons participated
- Each surgeon's role must be clearly documented
- Co-surgery should be indicated before the procedure when possible
- Both surgeons must be from different specialties or bring unique skills