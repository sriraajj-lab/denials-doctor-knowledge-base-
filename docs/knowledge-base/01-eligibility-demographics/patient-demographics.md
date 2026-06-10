# Patient Demographics & Information Collection

## Overview

Patient demographics is the foundational layer of the Revenue Cycle Management (RCM) process. Accurate patient identification at the point of registration prevents downstream claim denials, reduces rework, and accelerates reimbursement. Up to 15% of all claim denials stem from demographic errors -- making this the single highest-impact area for denial prevention. This document covers patient information collection standards, validation rules, insurance hierarchy determination, and coordination of benefits logic.

---

## 1. Required Patient Identifiers

### Full Legal Name

- **What to collect**: First name, middle name (or initial), last name, suffix (Jr., Sr., III, etc.)
- **Why it matters**: The name submitted on the claim must EXACTLY match the name on the patient's insurance card and the payer's records. A single-character difference can trigger a rejection.
- **Documentation rule**: Never use nicknames. "Robert" must be "Robert", not "Bob". "Elizabeth" not "Liz". The legal name on the photo ID or insurance card is authoritative.
- **Name format considerations**:
  - Hyphenated last names: "Smith-Jones" must be submitted exactly as it appears on the card
  - Prefixes: "Van Dyke", "De La Cruz" -- preserve spacing and capitalization per the card
  - Suffixes: "John Smith Jr." is not the same person as "John Smith Sr." for payer records

### Date of Birth (DOB)

- **Format**: MM/DD/YYYY (standard US healthcare format)
- **Validation**: The DOB must match the payer's records exactly. Medicare uses Month, Day, and Year -- all three must match.
- **Common issues**: Transposed month/day (03/05/1985 vs 05/03/1985) is one of the most common demographic errors. Always verify the format being used.

### Social Security Number (SSN)

- **Collection**: Full 9-digit SSN. For Medicare beneficiaries, the Medicare Beneficiary Identifier (MBI) has replaced the SSN-based HICN, but SSN is still used for identity verification with many payers.
- **Validation rules**:
  - Medicare (Original): Previously used HICN (SSN + 2-letter suffix). Now uses MBI (11-character alphanumeric). However, SSN is still used for eligibility verification through Medicare's systems.
  - Commercial plans: Many plans use SSN as the subscriber ID, but this is changing. Check the insurance card.
  - Medicaid: Varies by state. Many use the SSN, others use state-assigned ID numbers.
- **SSN format**: NNN-NN-NNNN. No alphabetic characters allowed.
- **Security**: SSN must be handled with HIPAA-compliant safeguards. Never transmit unencrypted.

### Current Address

- **Components**: Street address (or PO Box), apartment/suite number, city, state, ZIP+4 code
- **ZIP+4 requirement**: The 4-digit extension improves deliverability of Explanation of Benefits (EOB) and payment remittances. USPS reports 3-5% of mail is undeliverable without ZIP+4.
- **Address validation**: Use USPS-certified address verification. Common USPS formatting rules:
  - Street: "123 Main St" not "123 Main Street"
  - Apartment: "Apt 4B" not "#4B" or "Apartment 4-B"
  - Directionals: "N" not "North", "SE" not "Southeast"
- **Invalid addresses cause**: EOB delivery failure, claim return mail, patient notification failure, bad debt write-offs

### Phone and Email

- **Primary phone**: Used for appointment reminders, balance notifications
- **Alternate phone**: Backup contact number
- **Email**: HIPAA-compliant communication requires patient consent for email. Used for electronic statements and portal access.
- **Consent tracking**: Document patient authorization for text/email communication

### Agent Q&A

**Q:** A patient gives their name as "Mike" at registration, but the insurance card says "Michael". Should I use "Mike" or "Michael"?
**A:** Always use the name exactly as it appears on the insurance card -- "Michael". Payers match names against their subscriber database. "Mike" and "Michael" are different records from the payer's perspective, and using "Mike" will result in an eligibility not found response or a claim rejection. If no insurance card is available, ask for a government-issued photo ID and use the legal name. Document any alias names as "Also Known As" in the patient record, but never use an alias for claim submission.

**Q:** A child patient does not have an SSN. How do I handle the demographic record?
**A:** Many payers and clearinghouses accept a placeholder or omit the SSN for dependents under age 18. Some states specifically prohibit requiring an SSN for minor children. Use the value "999-99-9999" as a temporary placeholder when the SSN is not available, but note that this may cause issues with some payers. The preferred approach is to check the specific payer's requirements. Some Medicaid programs require a state-assigned ID number instead. For newborns, use "UNKNOWN" or the state-assigned temporary ID.

**Q:** What happens if I submit a claim with a misspelled patient name -- for example "Smyth" instead of "Smith"?
**A:** The claim will either reject at the clearinghouse level if the payer's eligibility system cannot match the demographic record, or it will be processed and denied with a CO 16 (Claim lacks information for adjudication) or CO 18 (Duplicate claim -- if the correct record was already processed). Even if the claim is paid, the misspelling creates issues downstream: the payment may not post correctly, the patient's EOB will have the wrong name, and subsequent services may fail. Best practice: correct the demographic record before claim submission and run pre-claim eligibility.

**Q:** A patient's address keeps getting updated every visit. Does this cause problems?
**A:** Yes. Frequent address changes create several problems: (1) EOBs and patient statements may go to the wrong address if the billing system isn't updated promptly, (2) the claim may be submitted with a different address than what the payer has on file, causing address verification mismatches, (3) collections efforts are hampered. Best practice: verify the address at every encounter, but track address history so previous addresses remain in the record. Standardize all addresses using USPS-certified address validation before submission.

**Q:** What is the correct way to handle a patient who refuses to provide their SSN at registration?
**A:** You cannot deny treatment due to refusal to provide an SSN (with the exception of Medicare, which requires an MBI). Document the refusal in the patient record. For claims that require an SSN, use the payer-assigned policy number or member ID from the insurance card. For self-pay patients, some practices assign an internal patient ID. Note that not having an SSN may affect the practice's ability to collect the balance (no credit bureau reporting for bad debt). Use the payer's member ID as the primary identifier.

---

## 2. Patient vs Guarantor vs Subscriber

### Definitions

| Role | Definition | Examples |
|---|---|---|
| **Patient** | The individual receiving healthcare services | The person who shows up for the appointment |
| **Subscriber** | The person who holds the insurance policy | The employee whose employer provides the insurance |
| **Guarantor** | The person financially responsible for the bill | The parent of a minor child, or the spouse on a family plan |
| **Dependent** | A person covered under someone else's policy | A spouse or child on the subscriber's plan |

### Key Relationships

- **Patient = Subscriber**: The patient holds their own insurance policy. Billing responsibility is with the patient.
- **Patient = Dependent, Subscriber = Parent**: The child is covered under the parent's plan. The parent is the subscriber AND the guarantor (financially responsible).
- **Patient = Spouse, Subscriber = Other Spouse**: One spouse covers the other. The subscriber is not the patient but holds the policy. The patient may or may not be the guarantor.
- **Patient = Dependent on ex-spouse's policy**: Common in divorce scenarios with court-ordered coverage. The subscriber is the ex-spouse. The patient is the dependent. The custodial parent may be the guarantor.

### Why the Distinction Matters for Billing

1. **Claim submission**: The 837 claim requires the subscriber's information (name, DOB, ID) in Loop 2010BA (Subscriber), while the patient's info is in Loop 2010CA (Patient/Payer). Getting these swapped causes rejections.
2. **EOB delivery**: EOBs are sent to the subscriber, not the patient, unless otherwise specified.
3. **Payment responsibility**: The guarantor receives statements. If the guarantor is not the same as the patient, statements must go to the guarantor.
4. **Balance collection**: If a parent (subscriber) is divorced, the guarantor may be the custodial parent, even though the subscriber carries the insurance.

### Agent Q&A

**Q:** A 17-year-old comes in for a checkup. The mother (subscriber) is not present. Who is the guarantor?
**A:** The mother is both the subscriber (she holds the insurance) and the guarantor (financially responsible for a minor child). Even though the mother is not present, she is the guarantor. The clinic should have the mother's consent on file (HIPAA authorization and financial agreement). For billing: (1) Subscriber info = mother's name, DOB, policy ID. (2) Patient info = child's name, DOB. (3) Guarantor = mother's name and address. If the mother is not present, the minor cannot sign financial agreements. Collect the mother's signature via e-consent or at a prior visit. In emergency situations, treat the minor and obtain consent retroactively.

**Q:** A patient is married and covered under their spouse's insurance. The patient is the one receiving services. Who is the subscriber on the claim?
**A:** The spouse is the subscriber (they hold the insurance policy through their employer). The patient is a dependent/spouse on the plan. On the 837 claim: Loop 2010BA (Subscriber) = the spouse's name, DOB, and subscriber ID. Loop 2010CA (Patient) = the patient's name, DOB, and relationship to the subscriber (usually "Spouse"). The guarantor can be the patient themselves if they are responsible for payment, or the subscriber spouse. This is a common point of confusion -- staff often mistakenly put the patient as the subscriber. Always look at the insurance card: the subscriber's name is listed as the primary policyholder.

**Q:** Can a patient be their own guarantor if they are an adult dependent on a parent's plan (e.g., a 22-year-old college student)?
**A:** Yes, an adult dependent (age 18+) can be their own guarantor even if they are a dependent on the parent's insurance policy. The parent is the subscriber (insurance holder), but the adult patient can sign the financial agreement as the guarantor. In practice: (1) Subscriber = parent (the person who holds the policy through their employer). (2) Patient = adult child. (3) Guarantor = adult child (if they sign the financial agreement). However, if the parent agrees to be financially responsible, the parent is the guarantor. Collect the financial agreement at registration. This distinction matters for collections -- you can pursue the guarantor for unpaid balances, not the subscriber (unless the subscriber is also the guarantor).

**Q:** What if the subscriber is deceased? Who is the guarantor for services provided to a dependent?
**A:** When the subscriber is deceased, the insurance policy typically continues for dependents under COBRA or through the surviving spouse's employer. The guarantor becomes the surviving parent or legal guardian. For Medicare: if a Medicare beneficiary dies, their spouse may be eligible for survivor benefits. For the claim: (1) The subscriber ID remains active during the COBRA/continuation period. (2) The subscriber/patient relationship codes still apply (the deceased is still the subscriber in the payer's system). (3) The guarantor must be updated to the surviving responsible party. This is a complex situation -- consult the payer's bereavement policy for claims processing.

---

## 3. Coordination of Benefits (COB)

### What is COB?

Coordination of Benefits (COB) determines which insurance plan pays first (primary) and which pays second (secondary) when a patient has coverage under more than one health plan. The secondary payer processes the claim after the primary has paid, applying its benefits to any remaining patient responsibility.

### Primary vs Secondary Determination Rules

#### Rule 1: The Birthday Rule (for Dependent Children)

When a child is covered by both parents' employer plans, the plan of the parent whose birthday (month and day, NOT year) falls earlier in the calendar year is primary.

**Example**:
- Mother's birthday: June 15, 1985
- Father's birthday: April 10, 1983
- The father's plan is primary because April (4) comes before June (6).
- If both parents have the same birthday (month and day), the plan that has covered the parent longer is primary.

#### Rule 2: Medicare is Primary When Eligible (Employer with <20 Employees)

If a patient is 65+ and covered by Medicare AND an employer group health plan:
- Employer with **20+ employees**: Group health plan is primary. Medicare is secondary.
- Employer with **fewer than 20 employees**: Medicare is primary. Group health plan is secondary.

#### Rule 3: The Subscriber Rule

The plan that covers a person as an employee/subscriber (or member/insured) is primary over a plan that covers them as a dependent.

**Example**: John has insurance through his employer (primary for John). John's wife Susan has insurance through her employer (primary for Susan). If Susan is on John's plan as a dependent, John's plan is primary for John. Susan's plan is primary for Susan. John's plan is secondary for Susan.

#### Rule 4: COBRA vs Active Coverage

COBRA continuation coverage is secondary to:
- Any other group health plan (excluding a plan that covers the person as a dependent under a divorced spouse's coverage)
- Medicare (if Medicare entitlement began before COBRA election or after 18+ months of COBRA)

#### Rule 5: Automobile / Liability Insurance

Auto insurance medical payments or Personal Injury Protection (PIP) is primary to health insurance for auto accident-related injuries. Health insurance pays after auto coverage is exhausted.

### COB Claim Submission Flow

1. **Primary claim**: Submit with the primary payer ID, include the patient's COB information (secondary payer ID and policy number) in the claim.
2. **Primary pays**: Receive the EOB/ERA from the primary payer.
3. **Secondary claim**: Submit to the secondary payer with:
   - Primary payer's paid amount
   - Primary payer's allowed amount
   - Primary payer's patient responsibility
   - Claim adjustment reason codes (CARCs) and Remittance Advice Remark Codes (RARCs)
4. **Secondary pays**: The secondary applies its benefits to the remaining patient balance.

### Common COB Errors

| Error | Description | Impact |
|---|---|---|
| Wrong order | Primary and secondary are reversed | Denial: CO 22 (This care may be covered by another payer) |
| Missing COB data | No secondary info on claim | Claim paid by primary, secondary never informed |
| Birthday rule misapplied | Using birth year instead of month/day | Incorrect primary determination |
| Medicare status unknown | Patient is 65+, employer size not checked | Wrong payer billed |
| Outdated subscriber info | Divorced parents, custody changes | Wrong subscriber billed |

### Agent Q&A

**Q:** A patient has Medicare Part A and Part B, plus a retiree plan from their former employer. Which is primary?
**A:** Medicare is primary. The retiree plan is secondary. The rule: When an individual is age 65+ and covered by Medicare AND a retiree health plan (not an active employer plan), Medicare is always primary. The retiree plan pays secondary. If the retiree plan has a Medicare carve-out (doesn't cover services that Medicare covers), then the retiree plan may only pay for services not covered by Medicare (e.g., Part D prescription drugs). The claim flow: Submit to Medicare first. After Medicare pays, submit the Medicare EOB to the retiree plan for secondary processing.

**Q:** A child is covered by both parents' plans. Mother's birthday is 02/14/1987, Father's birthday is 02/14/1985. Same month and day, different years. Which plan is primary?
**A:** When both parents have the same birthday (month and day), the birthday rule dictates that the plan that has covered the parent the longest is primary. The year of birth is NOT used -- only the month and day. If both parents have been covered for the same length of time, the plan that covered the parent longer is primary. If the tie cannot be broken, the plan of the parent whose last name comes first alphabetically is used as the tiebreaker. In practice, this scenario is rare; most payers will accept either determination and will notify the provider if the order is wrong.

**Q:** A patient covered under their parent's insurance turns 26 and loses dependent coverage. They are also covered by their own employer's plan. Is there still a COB issue?
**A:** Once the dependent loses coverage due to age, there is only one active plan (the patient's own employer plan). No COB issue exists. However, if the dependent coverage is still active (e.g., some states extend coverage beyond age 26, or the patient is disabled), then the subscriber rule applies: the plan covering the patient as an employee/subscriber (their own employer plan) is primary. The plan covering them as a dependent (parent's plan) is secondary.

**Q:** My claim received a CO 22 denial -- "This care may be covered by another payer per coordination of benefits." The patient says they only have one insurance. What should I do?
**A:** The CO 22 denial means the payer's records show another active coverage. This does not necessarily mean the patient is wrong -- there are several possibilities: (1) The patient may have forgotten about other coverage (spouse's plan, COBRA, Medicare). (2) The payer may have outdated COB information (e.g., an old policy that wasn't terminated). (3) The patient may have recently added/changed coverage and the COB record hasn't updated. Action steps: (a) Ask the patient specifically: "Do you have any other insurance including through a spouse, employer, Medicare, Medicaid, VA, or auto insurance?" (b) Check the COB data in your system. (c) If the patient confirms only one policy, ask the payer to investigate and update their COB records. (d) Submit a corrected claim after the COB issue is resolved. Do NOT resubmit without resolution -- it will deny again.

**Q:** A patient is injured in a car accident and has health insurance plus auto insurance with medical payments coverage. How does COB work?
**A:** Auto insurance medical payments coverage (MedPay) or Personal Injury Protection (PIP) is primary for injuries related to the auto accident. Health insurance is secondary. The claim flow: (1) Submit the auto-related charges to the auto insurance carrier first. (2) After auto benefits are exhausted or denied, submit to health insurance with the auto insurance EOB showing what was paid/denied. Important: (a) You MUST indicate on the health insurance claim that the condition is auto accident-related (use occurrence code "AA" in the 837). (b) Some health plans have exclusions for auto-related injuries unless auto benefits are exhausted. (c) Check state laws -- some states require PIP coverage, others do not. (d) Workers Compensation also takes precedence if the accident occurred during employment.

---

## 4. Medicare-Specific Demographics

### Medicare Beneficiary Identifier (MBI)

- **Format**: 11-character alphanumeric: 4 letters + 5 numbers + 2 letters/digits (pattern: C1CC1N2N3N4N5C6C7)
- **Example**: 1EG4-TE5-MK73
- The MBI replaced the SSN-based Health Insurance Claim Number (HICN) in 2018.
- The MBI is unique to each beneficiary and does not change when the beneficiary moves or changes address.
- An MBI can be reused after a beneficiary dies -- but this is extremely rare.

### Medicare Beneficiary Categories

| Category | Description | Parts Covered |
|---|---|---|
| Aged | Age 65+ | Part A, Part B |  
| Disabled | Under 65, on Social Security Disability (24+ months) | Part A, Part B |
| ESRD | End-Stage Renal Disease | Part A, Part B |
| Dual Eligible | Medicare + Medicaid | Full Medicare + state Medicaid | |
| Medicare Advantage | Medicare Part C (private plan) | All Medicare benefits through private insurer |

### Medicare Entitlement Dates

- **Part A**: Starts the first day of the month you turn 65 (or the first day of the 25th month of disability)
- **Part B**: Starts when enrolled, but effective dates vary by initial enrollment period
- **Late enrollment penalty**: 10% per 12-month period for Part B, higher for Part D

### Agent Q&A

**Q:** A patient presents a Medicare card that shows the old HICN format (SSN + letter). Is this still valid?
**A:** The CMS MBI (Medicare Beneficiary Identifier) replaced the SSN-based HICN in 2018, and as of January 1, 2020, all Medicare claims must use the MBI. A patient presenting an old card with a HICN format likely has an MBI that they don't know. You can: (1) Ask the patient to look up their MBI on mymedicare.gov. (2) Use the Medicare Beneficiary Lookup tool in your system. (3) Call the Medicare IVR (1-800-MEDICARE) to obtain the MBI. However, CMS operates a MBI Lookup Tool for healthcare providers. Do NOT use the HICN on claims -- it will reject (claim status code 331: Missing/incomplete/invalid HIC number). If the patient has an old Medicare card with "1-800-MEDICARE" on it, they need the new card.

**Q:** A patient is 65 and still working for an employer with 200 employees. They declined Medicare Part B. Is this okay?
**A:** Yes. If the employer has 20+ employees, the patient can defer Medicare Part B without penalty because the group health plan provides "creditable coverage." They can enroll in Part B later (during a Special Enrollment Period) without paying the late enrollment penalty. IMPORTANT: The employer must certify that they have 20+ employees. If the employer has fewer than 20, the patient MUST enroll in Medicare Part B or face a lifetime late enrollment penalty (10% per 12-month period the patient was eligible but did not enroll). The employer size determination is based on the number of employees, NOT the number of covered lives.

**Q:** A Medicare patient is also covered by Medicare Advantage (Part C) through UnitedHealthcare. Which is primary?
**A:** Medicare Advantage (Part C) IS Medicare for claims processing purposes. The patient has elected to receive their Medicare benefits through a private insurer (UnitedHealthcare) instead of Original Medicare. There is NO "primary vs secondary" between Original Medicare and Medicare Advantage -- they are the same benefit. The patient's coverage is through the Medicare Advantage plan. You submit claims to the Medicare Advantage plan (UnitedHealthcare), not to Original Medicare. However, if the patient also has other coverage (e.g., employer retiree plan), then the Medicare Advantage plan is primary and the retiree plan is secondary.

---

## 5. Address Validation Standards

### USPS Address Standards (Publication 28)

The United States Postal Service maintains standardized address formats in Publication 28. Key rules:

| Incorrect | Correct | Rule |
|---|---|---|
| 123 Main Street | 123 Main St | Street suffix abbreviated |
| 456 Elm Avenue, Apt 7 | 456 Elm Ave Apt 7 | Comma removed, apartment abbreviated |
| 789 North West Boulevard | 789 NW Blvd | Directional prefix standardized |
| P.O. Box 123 | PO Box 123 | Periods removed |
| Building 5, 100 Industrial Pkwy | 100 Industrial Pkwy Bldg 5 | Secondary designator after street |

### Why Address Validation Matters in RCM

1. **EOB Delivery**: If the address is wrong, the Explanation of Benefits (EOB) goes to the wrong place. The patient doesn't know what the insurance paid or what they owe.
2. **Patient Statements**: Statements mailed to the wrong address create bad debt. Healthcare providers write off millions annually in uncollectible patient balances due to bad addresses.
3. **COB Notices**: Coordination of benefit correspondence goes to the wrong person.
4. **Refund Checks**: Refunds from overpayments go to the wrong address.
5. **Claim rejections**: Some payers validate the patient's address on file. A mismatch can trigger a claim rejection.

### ZIP+4 Codes

- The ZIP+4 code (9-digit ZIP) identifies a specific delivery route, building, or PO Box.
- USPS reports that **over 96% of ZIP+4 coded mail is deliverable**, versus approximately 85% for 5-digit ZIP.
- Many practice management systems and clearinghouses offer USPS address verification as an integrated feature.

### Agent Q&A

**Q:** A patient gives their address as "123 Main Street, Apt #4, Springfield, IL 62701." How should this be formatted for claim submission?
**A:** The USPS-standardized format is: "123 Main St Apt 4", City: "Springfield", State: "IL", ZIP: "62701-1234" (if the ZIP+4 extension is known). Specific changes: (1) "Street" becomes "St". (2) "#" is removed -- use "Apt" as the secondary address designator. (3) The comma before "Apt" is removed. (4) The ZIP code should include the 4-digit extension if available. (5) The state must be the official 2-letter USPS abbreviation (not "Illinois" or "Ill"). An invalid address format may cause the claim to be rejected by the clearinghouse or payer.

**Q:** Can I use a PO Box as the patient's primary address for claim submission?
**A:** Yes, a PO Box is a valid mailing address for claim submission. However, consider: (1) Some payers require a physical address for the "patient residence" field. (2) Check whether your billing software distinguishes between "mailing address" and "physical address." (3) If the patient lives in a rural area without street delivery, PO Box is the standard. (4) For emergency services, having a physical address is important. Best practice: collect both a physical address and a mailing address if they differ. Use the mailing address for statements and the physical address for demographic reporting.

**Q:** A claim is denied because the patient's address doesn't match what the payer has on file. How do I fix this?
**A:** First, verify the patient's current address with the patient directly. If the patient moved and didn't update their insurance, you need to: (1) Update the address in your system. (2) Have the patient contact their insurance to update their address on file. (3) Wait for the payer to confirm the address change. (4) Resubmit the corrected claim. Most payers have a 24-48 hour lag between when the address is updated and when the eligibility system reflects the change. Do NOT simply change the address in your system without the patient updating it on the insurance side -- the mismatch will continue to cause problems.

---

## 6. Demographic Data Quality

### Common Errors and Prevention

| Error | Frequency | Prevention Strategy |
|---|---|---|
| Transposed SSN digits | High | Double-entry validation, scan the insurance card |
| Misspelled patient name | Medium | Verify against insurance card, ask patient to spell it |
| Wrong date of birth | Medium | Verify DOB verbally with patient: "Can you confirm your date of birth?" |
| Invalid address | High | USPS address validation at registration |
| Wrong subscriber selected | Medium | Have patient present insurance card, verify group number |
| Missing secondary insurance | High | Ask specifically: "Do you have any other insurance coverage?" |
| Incorrect relationship code | Low | Verify: Self, Spouse, Child, Other |

### Data Quality Metrics

Leading RCM organizations track these demographic quality metrics:
- **Demographic accuracy rate**: % of registrations with all demographic fields verified (target: >98%)
- **Address validation rate**: % of addresses passed through USPS validation (target: 100%)
- **Eligibility verification rate**: % of encounters with eligibility verified before service (target: >95%)
- **Clean claim rate**: % of claims paid on first submission (target: >95%, impacted by demographics)
- **Denial rate due to demographics**: % of denials caused by demographic errors (target: <3%)

### Agent Q&A

**Q:** What is the single most important demographic field to get right for Medicare claims?
**A:** The Medicare Beneficiary Identifier (MBI) is the single most important field. If the MBI is wrong, the claim will reject as a beneficiary mismatch. The second most important is the beneficiary's name -- Medicare uses an exact name match against the Social Security Administration records. A misspelled name or a name that doesn't match SSA records will result in an MBI mismatch reject. For all payers: the policy/member ID is the key identifier. Getting the ID wrong means the payer can't identify the patient at all.

**Q:** How often should patient demographics be reverified?
**A:** Best practice: verify demographics at EVERY encounter (every visit). This is called "registration verification" or "patient check-in verification." For established patients: confirm name, DOB, address, phone, email, and insurance coverage. For new patients: collect all demographics from scratch. The Joint Commission requires that patient identification be verified before each encounter. Most leading RCM practices have the front desk staff ask "Can you please confirm your name and date of birth?" at check-in. For insurance specifically, reverify at every visit -- insurance can change monthly.

**Q:** A patient's insurance card shows the subscriber name as "JOHN A SMITH" but the patient says their name is "Johnathan Andrew Smith." Which name should I use?
**A:** Use the name exactly as it appears on the insurance card: "John A Smith." The insurance company's database has the patient under that exact name. Using "Johnathan Andrew Smith" will cause an eligibility verification failure or claim rejection. You can note the patient's full legal name in the internal demographic record, but the claim must match the insurance card. If the patient wants their card updated, they need to contact their insurance company. This is a common issue -- insurance cards often use abbreviated or shortened names, and the provider MUST match the card.

---

## 7. Registration Checklist

### Minimum Data Collection for Every Patient

- [ ] Full legal name (as it appears on insurance card/photo ID)
- [ ] Date of birth (verified with patient verbatim)
- [ ] Gender (M, F, or X per state requirements)
- [ ] Current address (verified through USPS if possible)
- [ ] Primary phone number
- [ ] Insurance subscriber ID (from card)
- [ ] Insurance group number (from card)
- [ ] Payer name
- [ ] Patient's relationship to subscriber
- [ ] Guarantor name and contact info
- [ ] SSN or Tax ID (if available/payer requires)
- [ ] Email address (with communication consent)
- [ ] Emergency contact name and phone

### Additional for Medicare Patients

- [ ] Medicare Beneficiary Identifier (MBI)
- [ ] Medicare Part A effective date
- [ ] Medicare Part B effective date
- [ ] Secondary/Supplemental insurance info (Medigap, employer retiree, Medicaid)
- [ ] Medicare Advantage plan information (if applicable)
- [ ] ESRD status (if applicable)
- [ ] Disability status (if applicable)

### Additional for Minors / Dependents

- [ ] Subscriber (parent) demographic information
- [ ] Relationship to subscriber (child, stepchild, foster child, etc.)
- [ ] Custodial parent information (if parents are divorced)
- [ ] Court order for medical coverage (if applicable)
- [ ] Minor's SSN (if available) or state-assigned ID

### Agent Q&A

**Q:** How should I handle registration for a patient who is non-verbal or has a cognitive impairment?
**A:** If the patient cannot provide their own demographic information: (1) Attempt to obtain demographics from a family member, legal guardian, or caretaker who is present. (2) Verify the patient's identity using whatever means possible -- hospital bracelet, previous medical records, photo ID. (3) If the patient has a guardian, collect the guardian's information (guardianship paperwork may be needed for financial consent). (4) If the patient is incapacitated and no representative is present, treat under the Emergency Medical Treatment and Labor Act (EMTALA) if applicable, and collect demographics later. Document: "Patient unable to provide demographics due to [condition]. Information obtained from [source name/relationship]."

**Q:** A new patient arrives and says they "don't have their insurance card with them." How do I proceed?
**A:** Step 1: Ask if they know the insurance company name and whether they can look up their member ID online through their insurance portal or a digital ID card on their phone. Step 2: If they have no access to the information, collect their demographics (name, DOB, address, SSN) and register them as self-pay initially. Step 3: Use the clearinghouse's eligibility lookup service to find insurance coverage by SSN (if available). Step 4: If insurance cannot be verified, treat the patient with a self-pay deposit and a signed agreement that they will provide insurance information later. Step 5: Follow up within 48 hours to obtain insurance details. Step 6: If insurance information is obtained after the visit, submit the claim within the payer's timely filing window (often 90-365 days from date of service). Do NOT refuse care because the patient doesn't have their card.

**Q:** A divorced couple shares custody of a child. The mother carries the insurance. The father brings the child for the appointment. Who is the guarantor?
**A:** The mother is the subscriber (she holds the insurance). The father is the responsible party at the time of service. However, the guarantor depends on the divorce decree: (1) If the decree says the mother is responsible for medical expenses: the mother is the guarantor. (2) If the decree says the father is responsible: the father is the guarantor. (3) If the decree splits expenses: both are guarantors for their respective share. At registration: collect the subscriber's info (mother) for insurance billing. Collect the father's info as the point-of-service contact. For the financial agreement: get the financially responsible parent's signature. If the father does not have legal authority to consent, consider whether state law allows a stepparent or caretaker to consent for treatment. HIPAA: both parents generally have access to the child's medical records unless restricted by court order.

---

## 8. Special Considerations

### Homeless Patients

- Use the clinic's address or a shelter address for mailing purposes
- Document "homeless" or "no fixed address" in the demographic record
- Many states allow Medicaid enrollment with a shelter or clinic address
- For SSN: use placeholder if unavailable (999-99-9999)
- Coordinate with case management for follow-up

### Incarcerated Patients

- Medicaid is suspended (not terminated) during incarceration -- claims for services during incarceration are generally not covered by Medicaid
- Medicare coverage continues but claims are not paid for services provided during incarceration (except for inpatient care in specific circumstances)
- Use the inmate identification number when available
- Coordinate with the correctional facility for payment responsibility

### Foreign Nationals / Non-Residents

- Passport number may be used in lieu of SSN
- Visa type and expiration date
- Country of residence
- Guarantor must be identified
- Some payers have specific requirements for non-resident aliens
- Embassies and consulates may have payment agreements for their citizens

### Agent Q&A

**Q:** How do I handle demographics for a patient who is homeless and has no ID, no insurance card, and no SSN?
**A:** This is a high-risk registration scenario. Proceed as follows: (1) Collect whatever identifying information the patient can provide (name, approximate DOB). (2) Assign an internal patient ID. (3) Offer to connect with a social worker or case manager who can help the patient obtain identification and enroll in benefits (Medicaid, SNAP, etc.). (4) For the visit: treat and register as self-pay/charity care. (5) If the patient is eligible for Medicaid, many states allow retroactive coverage (up to 90 days prior) for qualifying individuals. (6) Document the registration carefully -- note that no ID was available and that the patient could not provide standard identifiers. (7) Bill as self-pay initially; if the patient obtains Medicaid retroactively, rebill with the Medicaid ID. (8) A homelessness flag in the demographic record helps the organization track and serve this population appropriately.

**Q:** A patient comes in after living abroad for 5 years and has lost all documentation. They are a US citizen. How do I register them?
**A:** This patient can still be registered: (1) Use whatever identifying information is available -- name, estimated DOB, last known US address. (2) If they have a passport, use that for identity verification. (3) If they have no SSN, use a placeholder. (4) If they have no current US insurance, register as self-pay. (5) If they are 65+ or disabled, they may need to re-enroll in Medicare through Social Security (this can take time). (6) For the EOB/statement address, use a family member's address or a mailing address they can access. (7) Contact Social Security Administration to verify the patient's SSN/identity if needed. (8) This is a complex registration -- coordinate with the registration supervisor.

---

## 9. Insurance Card Identification

### What to Look For on the Insurance Card

| Field | Description | Example |
|---|---|---|
| Payer Name | Insurance company name | Blue Cross Blue Shield of Illinois |
| Member/Subscriber ID | Unique identifier for the policyholder | ABC123456789 |
| Group Number | Employer group identifier | GRP-98765 |
| Plan Type | HMO, PPO, POS, EPO, HDHP | PPO |
| Effective Date | Coverage start date | 01/01/2024 |
| Copay Amounts | Office visit copay | $25 PCP / $50 Specialist |
| Deductible | Amount patient must pay before insurance pays | $1,500 Individual |
| Out-of-Pocket Max | Maximum patient pays per year | $6,000 Individual |
| Network Information | Which network to use | BlueCard PPO |
| Pharmacy Benefits (Rx) | Prescription drug coverage | $10/$30/$50 tiers |
| Mental Health Coverage | Behavioral health benefits | Same as medical |
| Emergency Coverage | Emergency room copay/coinsurance | $100 copay, then 20% |
| Claims Address | Where to send claims (or payer ID#) | PO Box 12345, Chicago IL |
| Customer Service | Phone for eligibility verification | 1-800-XXX-XXXX |
| Provider Services | Phone for provider inquiries | 1-800-XXX-XXXX |

### Agent Q&A

**Q:** How do I distinguish between an HMO and PPO card?
**A:** Look for these clues: (1) HMO cards often say "HMO", "Health Net", "Kaiser", "Select", or "Network" explicitly. (2) HMO cards typically have a "PCP" field or "Primary Care Physician" listed. (3) PPO cards often say "PPO", "Choice", "Open Access", "National", or "BlueCard". (4) PPO cards rarely list a specific PCP on the card. (5) HMO cards usually have a single claims address and a specific network name. (6) PPO cards may have different benefits/copays for in-network vs out-of-network. If in doubt, call the customer service number on the card and ask: "Is this an HMO plan or a PPO plan?" Confirm the network affiliation before rendering services.

**Q:** A patient hands you an insurance card that has no group number. Is this a problem?
**A:** Not necessarily. Many individual (non-employer) plans and some Medicare Advantage plans do not have group numbers. The subscriber/member ID is sufficient for eligibility verification and claim submission. However, if your billing system requires a group number, use a standard placeholder (often "000" or leave blank). For employer-based plans that truly don't have a group number on the card, call the payer to confirm. Some small employers have group numbers that are not printed on the card. For no-group-number scenarios: (1) Submit with the member ID only. (2) The claim will pend for manual review or process normally depending on the payer. (3) If it pendes, the payer will request the group number. (4) Obtain the group number from the patient's HR department or from the payer's provider portal.

---

## 10. Technology & Workflow Integration

### How Demographics Flow Through RCM

```
Patient Registration
       |
       v
Demographic Validation (USPS, SSN format check, name/DOB validation)
       |
       v
Eligibility Verification (270/271 transaction)
       |
       v
Pre-Authorization Check (if required)
       |
       v
Service Rendered
       |
       v
Charge Capture (CPT/HCPCS + ICD-10 codes)
       |
       v
Claim Generation (837 transaction)
       |
       v
Claim Submission (electronic or paper)
       |
       v
Payment Posting (835 ERA)
```

### System Integration Points

- **Practice Management System (PMS) / EHR**: Stores the demographic record, generates claims
- **Clearinghouse**: Validates demographics, translates formats, routes claims to payers
- **Eligibility Verification System**: Runs 270/271 transaction or API-based checks
- **Patient Portal**: Allows patients to update their own demographics
- **Credit Card on File**: For guarantor payment collection
- **Address Validation Service**: Real-time USPS address standardization

### Agent Q&A

**Q:** Why does my system sometimes reject a claim with "Invalid Payer ID" even though the payer name is correct?
**A:** "Invalid Payer ID" means the electronic payer ID (the ID used to route the claim) does not match the payer's name or the patient's insurance. This happens when: (1) You selected the wrong payer from the clearinghouse list (e.g., "Blue Cross Blue Shield of Illinois" vs "Blue Cross Blue Shield of Texas"). (2) The payer ID entered manually has a typo. (3) The payer has changed their electronic payer ID (this happens periodically). (4) You're using an outdated payer ID from an old claim. Action: look up the correct payer ID for the patient's specific plan. Many payers have multiple different payer IDs depending on the line of business (PPO vs HMO vs Medicare Advantage vs Medicaid). Use the clearinghouse's payer ID lookup tool or call the payer for the correct electronic payer ID.

**Q:** Can I use demographic data from a patient's previous visit to generate a new claim, even if the patient hasn't registered for the new visit yet?
**A:** Yes, but ONLY if you have verified that the demographic data has not changed. Most systems copy forward the last known demographics. However, you should always reverify at the point of service. Copying stale demographic data is a common source of errors: (1) The patient may have changed insurance. (2) The patient may have moved. (3) The patient's subscriber ID may have changed. (4) The patient may have gotten married (name change). Best practice: Always run eligibility verification before the next visit, even if the patient's demographics were previously validated. Many clearinghouses offer batch eligibility checks that can run overnight for scheduled patients.

---

## 11. Denial Prevention Through Demographics

### Top 10 Demographic Denials and How to Prevent Them

1. **CO 31 - Patient cannot be identified**: Missing or invalid patient ID. Prevent: Verify complete patient identification at every visit.

2. **CO 16 - Claim lacks information**: Missing demographic data. Prevent: Use structured registration forms and mandatory fields.

3. **CO 203 - Patient identifier mismatch**: Name/ID doesn't match payer records. Prevent: Verify eligibility 48 hours before service.

4. **CO 22 - COB issue**: Wrong payer billed. Prevent: Ask about other coverage at every visit.

5. **CO B14 - Procedure alters service date but procedure or revenue code is inconsistent with place of service**: Often caused by incorrect patient type (inpatient/outpatient) in demographics. Prevent: Verify patient status at registration.

6. **CO 4 - Procedure inconsistent with patient age**: Wrong DOB. Prevent: Verify DOB at every check-in.

7. **CO 58 - Treatment was considered experimental/investational**: Rarely demographic-related but can happen if patient's clinical trial status is missing. Prevent: Collect clinical trial participation info.

8. **CO 97 - The benefit for this service is included in the payment/allowance for another service/procedure**: Can happen if demographics link to wrong benefit category. Prevent: Verify plan type (HMO/PPO/Medicare).

9. **CO 103 - Patient status inconsistent with age**: Wrong patient age in demographics. Prevent: Age verification.

10. **CO 167 - This (these) diagnosis(es) is (are) not covered**: Can be prevented by verifying patient's condition and coverage type.

### Agent Q&A

**Q:** What percentage of claim denials are caused by demographic errors, and where should I focus prevention efforts?
**A:** Industry estimates suggest 10-15% of all claim denials are caused by demographic or registration errors. The most impactful prevention strategies ranked by ROI: (1) Real-time eligibility verification at the point of registration (reduces demog denials by 40-60%). (2) USPS address validation (reduces address-related EOB failures by 90%). (3) Insurance card scanning with automated data extraction (reduces manual entry errors by 70%). (4) Training staff on COB rules (reduces wrong-payer denials by 50%). (5) Patient portal with demographic self-service (reduces stale demographics). The cost of preventing a demographic error at registration is approximately $1-2. The cost of reworking a denied claim due to a demographic error is $25-50. Every dollar spent on demographic accuracy saves $12-25 in rework.

**Q:** How do I handle a claim that was denied because the insurance company has the patient's name wrong (their own database error)?
**A:** Even though the error originated with the payer, you cannot submit a claim with a name that doesn't match. Solution: (1) Contact the payer's provider services line. (2) Explain that the patient's name in the payer's system needs to be corrected. (3) Provide documentation (copy of insurance card, photo ID) to support the correct name. (4) Ask the payer to update their system. (5) Wait for confirmation that the name has been updated (typically 24-48 hours). (6) Run a test eligibility check to confirm the correction. (7) Resubmit the claim. Do NOT change the name on your claim to match the wrong name in the payer's database -- this creates long-term problems. Escalate to a supervisor if the payer refuses to correct their data.

**Q:** A newly enrolled Medicare patient receives their MBI, but it doesn't match any records in Medicare's eligibility system. What's going on?
**A:** There's a lag between when a person enrolls in Medicare and when the MBI is activated in Medicare's Front-End System. This can take 2-4 weeks after enrollment. During this period: (1) The patient has an MBI card, but Medicare's eligibility system may not recognize it yet. (2) The 270/271 eligibility check will return "Patient Not Found." (3) Claims submitted during this period will reject. Solutions: (a) If the patient has a welcome letter from Medicare, use the effective date on the letter. (b) Wait 2-4 weeks and re-verify. (c) If the patient needs services immediately, bill as a conditional claim. (d) If urgent, call 1-800-MEDICARE to confirm the MBI activation date. (e) Check if the patient was previously covered under a different MBI (e.g., they were a spouse on someone else's Medicare).

---

## 12. State-Specific Considerations

### Community Property States vs Non-Community Property States

- **Community property states** (AZ, CA, ID, LA, NV, NM, TX, WA, WI): Both spouses may be equally responsible for medical debts regardless of who signed the financial agreement.
- **Non-community property states**: Only the person who signs is responsible.

### Consent and Minor Treatment Laws

- Age of majority varies by state (generally 18, but some states allow 14+ to consent for specific services)
- Emancipated minors can consent for themselves
- Parental consent requirements vary for reproductive health, mental health, substance abuse

### Agent Q&A

**Q:** A 16-year-old patient in California comes in for mental health counseling. The parent is not present. Can the minor consent to treatment?
**A:** In California, minors 12+ can consent to outpatient mental health treatment without parental consent if: (1) The minor is mature enough to participate in treatment, AND (2) The minor would present a danger to self or others without treatment, OR (3) The minor is a victim of incest or child abuse. For billing: (a) The parent is still the subscriber if the minor is on the parent's insurance. (b) The claim will show the parent as the subscriber and the minor as the patient. (c) HIPAA: the parent may still have access to the minor's treatment records unless the minor objects or the provider determines disclosure would be harmful. (d) For EOBs: the parent (subscriber) receives the EOB, which will reveal the services provided. This is called "the confidentiality gap" -- the EOB discloses to the parent what the minor may have sought confidentially. In California, there are specific protections for minors 12+ regarding sensitive services. Check state law carefully.

**Q:** A patient is a covered veteran with VA benefits and also has private insurance. Is the VA primary?
**A:** VA coverage is NOT a health insurance plan in the traditional sense for COB purposes. The VA (Veterans Administration) provides healthcare through VA facilities and does NOT function as a standard health plan for private providers. If the patient receives care at a VA facility, VA is the payer. If the patient receives care at a non-VA private provider, the private insurance is primary. The VA only pays for non-VA services in very specific circumstances: (1) Authorized by the VA through a Community Care program. (2) Emergency care at a non-VA facility. (3) Services related to a service-connected disability. For private practice: submit to the private insurance first. Do NOT submit to VA unless you have a specific VA authorization number. The patient may also be responsible for copays under their private plan. VA coverage is secondary to all other third-party payers for non-VA care.

---

## 13. Glossary of Key Terms

| Term | Definition |
|---|---|
| **Subscriber** | The person who holds the insurance policy through employment or individual purchase |
| **Dependent** | A person (spouse, child) covered under the subscriber's policy |
| **Guarantor** | The person financially responsible for the healthcare bill |
| **COB** | Coordination of Benefits -- rules determining which insurance pays first |
| **Primary Payer** | The insurance plan that pays benefits first |
| **Secondary Payer** | The insurance plan that pays benefits after the primary has processed |
| **Birthday Rule** | Method for determining primary coverage for dependent children of married parents |
| **MBI** | Medicare Beneficiary Identifier -- 11-character alphanumeric ID replacing SSN-based HICN |
| **HICN** | Health Insurance Claim Number -- old SSN-based Medicare identifier (phased out) |
| **EOB** | Explanation of Benefits -- statement showing what the insurance paid and patient responsibility |
| **HIPAA** | Health Insurance Portability and Accountability Act -- privacy and security standards |
| **PCP** | Primary Care Physician -- required for HMO plans to manage care |
| **USPS** | United States Postal Service -- maintains address standardization standards |
| **ZIP+4** | 9-digit ZIP code that identifies a specific delivery route |
| **SSN** | Social Security Number -- used for identity verification by many payers |
| **ERA** | Electronic Remittance Advice -- electronic version of an EOB (835 transaction) |
| **EMTALA** | Emergency Medical Treatment and Labor Act -- mandates emergency care regardless of ability to pay |

---

## 14. Summary: Key Takeaways for LLM Agent

When processing patient demographics:
1. **Name + DOB + ID must match the insurance card exactly** -- no exceptions, no nicknames
2. **SSN/MBI is the most critical identifier** for payer identity matching
3. **Address validation via USPS** prevents EOB delivery failures and some claim rejections
4. **Subscriber vs patient vs guarantor** is the most commonly confused distinction
5. **COB rules are deterministic** -- birthday rule, subscriber rule, Medicare primary rule
6. **Always ask about other insurance** -- missing secondary coverage is the top COB error
7. **Verify at every encounter** -- demographics and insurance can change between visits
8. **Document everything** -- especially special situations (homeless, incarcerated, foreign national)

### Agent Q&A (Final Set)

**Q:** What should I do if a payer's 271 response says "Patient Not Found"? List troubleshooting steps.
**A:** Step-by-step process: (1) Check the subscriber ID -- is it exactly what's on the card? (2) Check the patient's name -- does it match the card exactly? (3) Check the patient's DOB -- is it correct? (4) Check the relationship code -- is "Self" used when the patient is the subscriber? (5) Check the payer ID -- is it the correct payer for this plan? (6) Call the payer's provider services line and ask them to check eligibility. (7) If the payer finds the patient, ask why the 270 failed and correct the data. (8) If the payer cannot find the patient, the subscriber ID may be wrong or the coverage may have terminated. (9) Ask the patient to confirm their insurance info directly with the payer. (10) If all else fails, register as self-pay and follow up with the patient's insurance documentation. Do NOT assume the patient is uninsured -- there is usually a correctable data issue.

**Q:** What is the difference between "guarantor" and "responsible party"?
**A:** In healthcare billing, these terms are often used interchangeably but there is a subtle difference: (1) Guarantor: Specifically refers to the person who signed the financial agreement/consent for treatment agreeing to be financially responsible. (2) Responsible Party: A broader term that refers to whoever is ultimately expected to pay the bill. In most cases, they are the same person. The distinction matters when: (a) A parent signs for a minor (the parent is the guarantor). (b) The parent later dies or becomes incapacitated -- the responsible party may change. (c) A court orders the non-custodial parent to pay medical expenses (that parent is a responsible party but may not have signed as guarantor). (d) For Medicaid patients, the state is the payer but the patient may still have a small co-pay -- the patient is responsible for the co-pay. In your system: link claims to the guarantor for statements and collections, but track the responsible party(s) for legal purposes.

**Q:** A patient with Medicare Part A only comes for an office visit. Will Medicare pay for the visit?
**A:** No. Medicare Part A covers inpatient hospital care, skilled nursing facility care, hospice, and some home health care. Medicare Part B covers outpatient services, physician services, and preventive care. A standard office visit is a Part B service. If the patient has only Part A, Medicare will NOT pay for the office visit. What the patient needs: (1) Medicare Part B enrollment (there is a late enrollment penalty if they delay). (2) Or a Medicare Advantage (Part C) plan that covers both Part A and Part B benefits through a private insurer. (3) Or alternative coverage (employer group health plan, Medigap, etc.). For this visit: (a) Check if the patient has any other coverage. (b) If they have only Part A, the visit is patient responsibility (self-pay). (c) Notify the patient that they should consider enrolling in Part B during the next General Enrollment Period (January 1 - March 31 each year). (d) Provide a good faith estimate of charges before service.

**Q:** How do I handle a same-sex married couple with a dependent child for COB purposes?
**A:** The same COB rules apply regardless of the parents' genders: (1) The birthday rule applies to determine which parent's plan is primary for the dependent child. (2) The parent whose month and day of birth (not year) falls first in the calendar year has the primary plan for the child. (3) If both parents have the same birthday, the plan that has covered the parent longest is primary. (4) The subscriber rule still applies: each parent's own employer plan is primary for them individually. (5) For the child, apply the birthday rule to determine which parent's plan is primary. (6) If the parents are not married, the court order or custody agreement determines medical coverage responsibility. (7) Same-sex marriage is legally recognized for all federal purposes (including Medicare and COB) under the Supreme Court's Obergefell decision (2015). Treat same-sex married couples identically to opposite-sex married couples for COB purposes.

**Q:** What is the fastest way to identify that a patient's demographic data entered into the system is likely incorrect?
**A:** Multiple red flags: (1) Eligibility check returns "Patient Not Found" or "No Coverage Found." (2) Claim rejects with CO 31 (Patient cannot be identified). (3) The insurance card photo shows a different name than what was entered. (4) The system-generated "name match" score is low (e.g., 65% match for a returning patient). (5) The patient says "That's not my date of birth" when you read it back. (6) The demographic record has a placeholder SSN (999-99-9999) but the patient's insurance card shows a member ID that resembles an SSN. (7) The patient's address in your system is flagged by USPS as "undeliverable" or "invalid." The most reliable single indicator: the 270 eligibility response returning "No match found" is 99% indicative of a demographic data entry error or a coverage termination.

**Q:** When should I use the relationship code "Other" for a patient-to-subscriber relationship?
**A:** Relationship code "Other" (code 34 in the 270/271, or code "18" sometimes) should be used when: (1) The patient is a foster child covered under the state's policy. (2) The patient is a ward of the court. (3) The patient is a legal dependent who is not a spouse or child (e.g., an elderly parent living with the subscriber). (4) The patient is covered under a domestic partner benefit where "spouse" is not applicable. (5) The patient is a grandchild living with the grandparent subscriber. Use "Other" sparingly -- if the patient's relationship clearly fits "Self" (18/19), "Spouse" (01), or "Child" (19), use those codes. Incorrect relationship code can cause the 270 to return "No coverage" or cause a claim denial. When in doubt, start with the payer's relationship code options.

**Q:** Can a single patient have multiple subscriber IDs (e.g., one for medical, one for pharmacy)?
**A:** Yes, this is common. A patient may have: (1) Different member IDs for medical vs pharmacy benefits (common with carve-out pharmacy plans). (2) Different IDs for different lines of business (e.g., one ID for commercial, a different ID for Medicare Advantage). (3) Different IDs for different family members (some plans issue distinct member IDs for each enrolled family member). However, many plans use a single subscriber ID for all members, with different suffixes or no suffix at all. Best practice: always use the ID exactly as it appears on the specific card for the benefit being verified. If the patient has separate medical and pharmacy cards, use the member ID from the medical card for medical eligibility and the pharmacy card for pharmacy eligibility.

---

## Training Summary

This document covers the complete lifecycle of patient demographics in RCM, from collection through validation through ongoing management. Key proficiency areas for the LLM agent:

1. **Identifier validation** -- SSN, MBI, DOB, name matching rules
2. **Role distinction** -- patient vs subscriber vs guarantor vs dependent
3. **COB determination** -- birthday rule, subscriber rule, employer size rule
4. **Address standards** -- USPS formatting, ZIP+4, deliverability
5. **Medicare specifics** -- MBI format, entitlement, Part A/B/C/D
6. **Special populations** -- minors, homeless, incarcerated, foreign nationals, veterans
7. **State-specific laws** -- age of consent, community property, minor treatment
8. **Denial prevention** -- top demographic denials and prevention strategies
9. **Registration workflow** -- minimum data collection, reverification frequency
10. **Technology integration** -- how demographics flow through the RCM system

The LLM agent should use this document to answer patient demographic questions, identify demographic data quality issues, troubleshoot demographic-related denials, and guide registration staff on correct data collection procedures for any patient scenario.