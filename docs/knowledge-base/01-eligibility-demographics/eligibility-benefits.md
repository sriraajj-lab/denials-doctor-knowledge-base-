# Eligibility & Benefits Verification (270/271)

## Overview

Eligibility and benefits verification is the process of confirming a patient's health insurance coverage and determining the specific benefits available for planned services. The standard electronic transaction for this is the HIPAA-mandated 270/271 EDI transaction: the provider sends a 270 Eligibility Request and the payer responds with a 271 Eligibility Response. This document provides a comprehensive technical reference for the 270/271 transaction structure, parsing 271 responses, API-based alternatives, and real-world troubleshooting for edge cases.

---

## 1. The 270/271 EDI Transaction

### What is 270/271?

The **270 Health Care Eligibility Benefit Inquiry** and **271 Health Care Eligibility Benefit Response** are HIPAA-mandated electronic transactions (ASC X12 005010X279) used for verifying patient insurance coverage and benefits.

- **270 = Outbound Request**: Sent by the provider (or clearinghouse on behalf of the provider) to ask about a patient's eligibility and benefits.
- **271 = Inbound Response**: Returned by the payer to answer the provider's questions about coverage status, copays, deductibles, out-of-pocket maximums, and remaining benefits.

The X12 version 005010X279A1 is the current standard (adopted April 2012; 4010A1 was the previous version). Some payers still support 4010A1, but 5010 is now required for HIPAA compliance.

### Transaction Flow

```
Provider System
    |   [Creates 270 transaction with patient/payer info]
    v
Clearinghouse (optional)
    |   [Validates format, routes to correct payer]
    v
Payer System
    |   [Looks up patient in subscriber database, determines benefits]
    v
Clearinghouse (optional)
    |   [Routes response back]
    v
Provider System
    |   [Parses 271 response, displays benefits to user]
    v
User Interface
    [Shows coverage status, copay amounts, deductible, etc.]
```

### Real-Time vs Batch

| Aspect | Real-Time | Batch |
|---|---|---|
| **Speed** | 2-30 seconds | Hours to overnight |
| **Use case** | Point-of-service verification | Pre-appointment batch checks |
| **Volume** | Single patient at a time | Hundreds or thousands at once |
| **Technology** | Direct 270/271, FHIR API, portal | Batch file upload via clearinghouse |
| **Reliability** | High (immediate feedback) | Moderate (delayed response) |
| **Cost** | Per-transaction fees typical | Lower per-claim cost at volume |

---

## 2. 270 Transaction Structure (Request)

### Hierarchical Loops

The 270 transaction is organized into nested loops. Each loop represents a level in the information hierarchy:

```
ST - Transaction Set Header (beginning of 270)
    BHT - Beginning of Hierarchical Transaction (purpose code, reference ID)
    
    HL - Information Source Level (Loop 2000A) -- The Payer
        NM1 - Payer Name (Loop 2100A)
        
        HL - Information Receiver Level (Loop 2000B) -- The Provider
            NM1 - Provider Name (Loop 2100B)
            
            HL - Subscriber Level (Loop 2000C) -- The Subscriber
                NM1 - Subscriber Name/Demographics (Loop 2100C)
                
                HL - Dependent Level (Loop 2000D) -- The Dependent/Patient
                    NM1 - Dependent Name/Demographics (Loop 2100D)
                    DMG - Dependent Demographic Info (DOB, Gender)
                    DTP - Dependent Date (Service date)
                    EQ - Inquiry Service Type Codes (what service you're asking about)
                    III - Additional Information (e.g., diagnosis codes)
```

### Critical 270 Segments

**BHT (Beginning of Hierarchical Transaction)**:
- BHT02: Transaction Purpose Code (e.g., "13" = Request for information)
- BHT03: Reference Identification (transaction ID)

**HL (Hierarchical Level)**: Defines the structure
- HL01: Sequential number
- HL02: Parent HL number (for non-root levels)
- HL03: HL Code (20=Information Source/Payer, 21=Information Receiver/Provider, 22=Subscriber, 23=Dependent)
- HL04: Child indicator (0=has no children, 1=has children)

**NM1 (Individual or Organizational Name)**:
- NM101: Entity ID code
- NM102: Entity type (1=Person, 2=Non-Person)
- NM103: Name last (or organization name)
- NM104: Name first
- NM105: Name middle
- NM107: Name suffix
- NM108: ID qualifier (e.g., "MI"=Member ID, "PI"=Payer ID, "34"=SSN)
- NM109: ID (the actual ID number)

**DMG (Demographic Information)**:
- DMG01: Date Time Period Format Qualifier (D8=CCYYMMDD)
- DMG02: Date of Birth (CCYYMMDD)
- DMG03: Gender Code (M/F/U)
- DMG04: Marital Status (optional)
- DMG05: Race/Ethnicity (optional)

**DTP (Date or Time Period)**:
- DTP01: Date/Time Qualifier (e.g., "291"=Date range for plan coverage, "472"=Date of Service)
- DTP02: Date format qualifier (D8=CCYYMMDD, RD8=CCYYMMDD-CCYYMMDD)

**EQ (Eligibility or Benefit Inquiry)**:
- EQ01: Service Type Code (the most critical field -- tells the payer what benefits you need)
  - "1" = Medical Care
  - "30" = Plan Coverage/General
  - "33" = Primary Care (Office Visit)
  - "47" = Hospital (Inpatient)
  - "50" = Hospital (Outpatient)
  - "86" = Emergency Services
  - "88" = Pharmacy
  - "98" = Professional (Physician) Visit
  - "AL" = Inpatient Psychiatry
  - "MC" = Maternity
  - "MH" = Mental Health
  - "UC" = Urgent Care

### Sample 270 Transaction (Simplified)

```
ST*270*0001~
BHT*0022*13*REF001*20240610*1430~
HL*1**20*1~
NM1*PR*2*BLUE CROSS BLUE SHIELD OF ILLINOIS*****PI*48024~
HL*2*1*21*1~
NM1*1P*2*YOUR MEDICAL GROUP*****XX*1234567890~
HL*3*2*22*0~
NM1*IL*1*SMITH*JOHN*A****MI*ABC123456789~
DMG*D8*19800115~
DTP*472*D8*20240615~
EQ*30~
SE*10*0001~
```

This asks: "For patient John A. Smith (DOB 01/15/1980, member ID ABC123456789), check general plan coverage (EQ code 30) for service date 06/15/2024, with BCBS of Illinois."

### Agent Q&A

**Q:** What service type code (EQ01) should I use to check whether a patient has deductible remaining?
**A:** Use service type code "30" (Plan Coverage/General) to get general benefit information, which should include deductible and OOP max information. However, for more specific benefit details, use: "33" (Primary Care Office Visit) for PCP visit benefits, "98" (Professional Visit) for specialist visit benefits, "47" (Hospital/Inpatient) for inpatient benefits, "50" (Hospital/Outpatient) for outpatient procedure benefits, "86" (Emergency Services) for ER copay/coinsurance. Many payers return MORE specific benefit information when you use the specific service type code rather than the general code "30." If the 271 response is vague or missing information, resend the 270 with specific EQ codes for the services you are verifying. Best practice: send multiple EQ segments in one 270 to get comprehensive benefit information:

```
EQ*30~
EQ*33~
EQ*86~
EQ*50~
```

Some systems limit to one EQ per 270; check your system's capabilities.

**Q:** Why does my 270 request include a dependent loop (2000D) even when the patient IS the subscriber?
**A:** The 270 transaction structure requires loops based on the patient's relationship to the subscriber: (1) If the patient IS the subscriber (they hold the policy): HL segment with HL03="22" (Subscriber), no dependent loop needed. (2) If the patient is a dependent (spouse, child on subscriber's policy): HL with HL03="22" (Subscriber) containing subscriber info, AND HL with HL03="23" (Dependent) containing patient info. The dependent loop is not required when the patient is the subscriber. However, some clearinghouses always add a dependent loop for consistency, which is fine. Most modern 270/271 parsers handle both structures. Critical: When sending a dependent 270, the subscriber loop (2100C) must contain the subscriber's info, and the dependent loop (2100D) must contain the patient's info. Mixing these up results in a "Patient Not Found" response.

**Q:** What is the proper format for dates in the 270 transaction?
**A:** The 270/271 transaction uses the following date formats: (1) D8 = CCYYMMDD (e.g., 20240610 for June 10, 2024) -- used for a single date like date of service or DOB. (2) RD8 = CCYYMMDD-CCYYMMDD (e.g., 20240610-20240615) -- used for date ranges. (3) DTP segment for date of service uses qualifier "472" with D8 format. (4) DMG segment for DOB always uses D8 format. (5) Important: DO NOT use MM/DD/YYYY or DD/MM/YYYY format in HIPAA transactions. The X12 standard uses CCYYMMDD exclusively for D8 qualifier. If you see a 270 with dates in DD/MM/YYYY format, the transaction will be rejected by the clearinghouse.

---

## 3. 271 Transaction Structure (Response)

### Hierarchical Loops (Same as 270)

The 271 response mirrors the 270 request structure:

```
ST - Transaction Set Header
    BHT - Beginning of Hierarchical Transaction
    
    HL - Information Source Level (Loop 2000A) -- The Payer
        NM1 - Payer Name (Loop 2100A)
        
        HL - Information Receiver Level (Loop 2000B) -- The Provider
            NM1 - Provider Name (Loop 2100B)
            
            HL - Subscriber Level (Loop 2000C) -- The Subscriber
                NM1 - Subscriber Info (Loop 2100C)
                N3 - Subscriber Address
                N4 - Subscriber City/State/ZIP
                DMG - Subscriber DOB/Gender
                DTP - Subscriber Coverage Period
                
                HL - Dependent Level (Loop 2000D) -- The Patient
                    NM1 - Dependent Info (Loop 2100D)
                    N3 - Dependent Address
                    N4 - Dependent City/State/ZIP
                    DMG - Dependent DOB/Gender
                    
                    EB - Eligibility or Benefit Information (Loop 2110D) *** KEY ***
                    HSD - Health Care Services Delivery
                    REF - Prior Authorization Reference
                    DTP - Benefit Date
                    AAA - Request Validation

                            EB Loop (repeating per benefit type)
                            HSD Loop (service delivery details)
                            REF Loop (authorization numbers)
                            DTP Loop (benefit effective dates)
```

### The EB Segment -- Most Important Part of the 271

The **EB (Eligibility or Benefit Information)** segment is the core of the 271 response. Each EB segment describes one benefit or piece of coverage information.

**EB Segment Fields**:

| Position | Element | Description | Example Values |
|---|---|---|---|
| EB01 | Eligibility/Benefit Information Code | Benefit type | "1"=Active Coverage, "2"=Active with limits, "3"=Not active, "C"=Coverage level, "F"=Maximum benefit |
| EB02 | Coverage Level Code | Who/what is covered | "CHD"=Child, "DEP"=Dependent, "E"=Employee, "FAM"=Family, "IND"=Individual, "SPC"=Spouse |
| EB03 | Service Type Code | Type of service | "1"=Medical, "30"=Plan Coverage, "33"=Primary Care, "86"=Emergency, "98"=Physician Visit |
| EB04 | Insurance Type Code | Type of insurance | "C"=Commercial, "D"=Disability, "MA"=Medicare Part A, "MB"=Medicare Part B, "MC"=Medicaid, "HM"=HMO, "PP"=PPO |
| EB05 | Plan Coverage Description | Free text description | "COPAY: $25 OFFICE VISIT" |
| EB06 | Quantity Qualifier | Unit of measure | "99"=Months, "VS"=Visits |
| EB07 | Quantity | Number of units | "20" (visits remaining) |
| EB08 | Monetary Amount | Dollar amount | "$30.00" (copay amount) |
| EB09 | Percent | Percentage | "20" (20% coinsurance) |
| EB10 | Yes/No Code | True/false | "Y" or "N" (e.g., deductible met?) |
| EB11 | Composite Medical Procedure | Not commonly used | -- |
| EB12 | Diagnosis Code Pointer | Not commonly used | -- |
| EB13 | Information Code | Additional information | "A"=Deductible remaining, "B"=Benefit percentage, "C"=Copay info |

**Common EB01/EB13 combinations**:

| EB01 | EB13 | Meaning |
|---|---|---|
| "1" | N/A | Active coverage |
| "1" | "A" | Active coverage, copay applies |
| "1" | "B" | Active coverage, coinsurance applies |
| "1" | "C" | Active coverage, deductible applies |
| "3" | N/A | No active coverage |
| "C" | "F" | Coverage level with dollar limit |
| "F" | N/A | Maximum benefit information |
| "G" | N/A | Benefit information (general) |

### How to Parse a 271 Response

**Step 1**: Find the Subscriber or Dependent NM1 segment (2100C or 2100D). Confirm the patient/subscriber name and ID match.

**Step 2**: Check the AAA segment (Request Validation) if present. If AAA01 = "N" (No), the request was not valid -- the patient was not found, invalid subscriber ID, etc.

**Step 3**: Scan all EB segments for coverage status:
- EB01="1" or "1" with qualifiers = Active coverage
- EB01="3" = Coverage not active (patient not covered)
- EB01="G" = Benefit information (details below)

**Step 4**: For each EB segment, extract:
- Service type (EB03) -- what service the benefit is for
- Benefit details: copay amount (EB08), coinsurance % (EB09), deductible status (EB10/EB13)
- Benefit limits: visits/quantity remaining (EB06, EB07)
- Dollar maximums: EB08 with EB01="F" or "C"

**Step 5**: Check DTP segments after each EB for effective dates.

**Step 6**: Check REF segments for authorization numbers if applicable.

### Sample 271 Response (Parsed)

```
ST*271*0002~
BHT*0022*11*REF002*20240610*1445~
HL*1**20*1~
NM1*PR*2*BCBS IL*****PI*48024~
HL*2*1*21*1~
NM1*1P*2*YOUR MEDICAL GROUP*****PI*1234567890~
HL*3*2*22*0~
NM1*IL*1*SMITH*JOHN*A****MI*ABC123456789~
DMG*D8*19800115*M~
DTP*356*D8*20240101~
DTP*357*D8*20241231~

EB*1*IND*98*PP*PRIMARY CARE OFFICE~               <-- Active coverage, PCP visit
HSD*VS*1~                                           <-- Copay per visit (quantity 1)
REF*G3*COPAY: $30.00~~~                             <-- Copay is $30

EB*1*IND*33*PP*SPECIALIST OFFICE~
HSD*VS*1~                                           <-- Copay per visit
REF*G3*COPAY: $50.00~~~                             <-- Copay is $50

EB*C*FAM*30*PP*DEDUCTIBLE~
HSD***30~                                           <-- Monetary amount follows (EB08)
EB*G***DEDUCTIBLE REMAINING:$2000.00~                <-- $2,000 deductible remaining

EB*C*FAM*30*PP*OUT-OF-POCKET MAX~
EB*G***OOP REMAINING:$5000.00~                       <-- $5,000 OOP remaining

EB*1*IND*86*PP*EMERGENCY SERVICES~
HSD*VS*1~
REF*G3*COPAY: $100.00~~~                            <-- ER copay $100
EB*1*FAM*98*PP**VS*20~                               <-- 20 visits remaining

SE*18*0002~
```

**Translation**: John Smith (member ABC123456789) has ACTIVE coverage through 12/31/2024. His PCP copay is $30, specialist copay $50, ER copay $100. He has $2,000 remaining on his deductible and $5,000 remaining on his OOP max. He has 20 specialist visits remaining.

### Agent Q&A

**Q:** The 271 response shows EB01 = "3" for the subscriber (no active coverage). What does this mean?
**A:** EB01 = "3" means the subscriber has no active coverage with this plan on the date checked. Possible reasons: (1) Coverage has terminated (expired, employment ended, COBRA lapsed). (2) Coverage has not yet started (future effective date). (3) The subscriber ID is wrong (belongs to a different person or is out of date). (4) The patient's name/DOB don't match what the payer has on file. (5) The plan may be active but for a different line of business (e.g., asking about medical when only pharmacy coverage is active). Troubleshooting: (a) Check the AAA segment for error details. (b) Verify the subscriber ID against the insurance card. (c) Verify the patient's name and DOB. (d) Check the effective/termination dates in the DTP segments. (e) Try running eligibility with different service type codes. (f) Call the payer's provider services line to confirm the patient's status. (g) If coverage ended, check if the patient has other coverage (COBRA, new employer, spouse plan). (h) Do NOT assume the patient is uninsured until you've confirmed with the payer by phone.

**Q:** The 271 response shows a copay of $30 for "Primary Care Office Visit" (EQ 33), but the patient is here for a specialist visit. Is the $30 copay valid?
**A:** No. The $30 copay applies specifically to primary care office visits (EQ 33). A specialist visit (EQ 98) would have a different copay. You need to check the EB segment with EB03="98" (Physician Visit / Specialist) to see the specialist copay. If no EB segment for EQ 98 exists, it could mean: (1) The specialist copay is the same as the PCP copay (rare -- specialists typically have higher copays). (2) The specialist visit is subject to deductible (not copay-based). (3) The 271 did not return specialist visit benefits. Best practice: Always verify benefits for the SPECIFIC service type the patient needs. If the 271 does not return specialist info and you need it, resend the 270 with EQ*98~. Never assume a PCP copay applies to a specialist visit.

**Q:** The 271 response includes an AAA segment. What does it mean and how do I handle it?
**A:** The AAA segment (Request Validation) indicates that the 270 request could not be processed. Common AAA codes:

| AAA01 | AAA03 | Meaning |
|---|---|---|
| N (No) | 15 | Patient not found (subscriber ID invalid) |
| N (No) | 42 | Unable to respond at current time |
| N (No) | 57 | Invalid/Missing date of birth |
| N (No) | 60 | Invalid/Missing subscriber/payer ID |
| N (No) | 61 | Name mismatch |
| N (No) | 62 | Service type not supported |
| N (No) | 71 | Invalid diagnosis code |

When you receive an AAA segment: (1) Read the error code and take corrective action. (2) For code 15 (Patient not found): Verify the subscriber ID. (3) For code 61 (Name mismatch): Verify the patient's name. (4) For code 57 (Invalid DOB): Verify the DOB. (5) For code 42 (Unable to respond): Wait and retry. (6) Do NOT ignore the AAA -- it means the response is not reliable and should not be used for benefit verification. (7) Call the payer if you cannot identify the issue. The AAA segment is the 271's way of saying "I couldn't understand your request."

---

## 4. 271 EB Segment Deep Dive

### EB02 -- Coverage Level Codes

| Code | Meaning | Usage |
|---|---|---|
| CHD | Child only | Child-only coverage |
| DEP | Dependent | Non-subscriber dependent (spouse/child) |
| E | Employee/Subscriber | The subscriber only (individual) |
| FAM | Family | All family members covered |
| IND | Individual | Individual coverage (not family) |
| SPC | Spouse | Spouse only |
| TWO | Two party | Subscriber + one dependent (typically subscriber + spouse) |

### EB03 -- Service Type Codes (in the Response)

Common service types returned in 271 responses:

| Code | Service | Notes |
|---|---|---|
| 1 | Medical Care | General medical benefits |
| 30 | Plan Coverage / General | Overall coverage summary |
| 33 | Primary Care (Office Visit) | PCP visit benefits |
| 35 | Well Child | Developmental screening |
| 45 | Professional (Physician) Visit | Similar to 98 |
| 47 | Hospital Inpatient | Inpatient room/board |
| 50 | Hospital Outpatient | Outpatient facility |
| 52 | Inpatient Physician | Physician services for inpatients |
| 53 | Outpatient Physician | Physician services for outpatients |
| 86 | Emergency Services | ER visit |
| 88 | Pharmacy | Prescription drug |
| 89 | Drug and Alcohol | Substance abuse treatment |
| 98 | Professional (Physician) Visit | Specialist/general professional |
| A0 | Comprehensive (Wellness/Prevention) | Preventive care |
| AL | Inpatient Psychiatric | Psychiatric inpatient |
| MH | Mental Health | Mental health services |
| UC | Urgent Care | Urgent care center |
| 51 | Hospital Emergency Accident | Emergency accident |
| 98 | Professional Visit Physician | Office visits for specialist care |
| 62 | Maternity | Maternity care |

### EB06/EB07 -- Quantity and Quantity Qualifier

| EB06 (Qualifier) | EB07 (Quantity) | Meaning |
|---|---|---|
| VS | 20 | 20 visits remaining |
| VS | 0 | No visits remaining |
| VS | 999 | Unlimited visits (or use "99" qualifier for unlimited) |
| 99 (Months) | 12 | 12 months of coverage remaining |
| DY | 365 | 365 days of coverage remaining |
| (Blank) | (Blank) | No quantity limit / not applicable |

### EB08 -- Monetary Amount

Can mean different things depending on context:
- Copay: EB08 = $25 (copay amount)
- Deductible: EB08 = $1,500 (remaining deductible)
- OOP Max: EB08 = $6,000 (OOP max amount)
- Maximum benefit: EB08 = $2,000,000 (lifetime max)
- Deductible satisfied: EB08 = $0 (deductible fully met)

### EB09 -- Percent (Coinsurance)

- EB09 = "20" means 20% coinsurance (patient pays 20%)
- EB09 = "10" means 10% coinsurance
- EB09 = "0" means 0% (no coinsurance -- covered at 100%)
- (Blank): No coinsurance applies or service is copay-based

### EB10 -- Yes/No Code

- EB10 = "Y" (Yes): The condition indicated by EB13 is true
  - If EB13 = "D" (deductible applies) and EB10 = "Y": Deductible applies to this service
  - If EB13 = "A" (copay applies) and EB10 = "N": Copay does NOT apply to this service
- EB10 = "N" (No): The condition is false
- EB10 = "U" (Unknown): Status is unknown
- EB10 = (Blank): Not indicated

### Agent Q&A

**Q:** The 271 shows EB03="30" with EB13="D" and EB10="Y" and EB08="$5,000". What does this tell me?
**A:** This tells you: (1) The service type is general plan coverage (EB03="30"). (2) A deductible applies (EB13="D") and it has been met or the information is confirmed (EB10="Y"). (3) The deductible amount remaining is $5,000 (EB08=$5,000). This is confusing because EB10="Y" should mean "deductible applies to this service type" rather than "deductible is met." However, many payers use EB10 differently. In this case: the plan indicates the patient has a deductible AND the remaining deductible is shown as $5,000. If EB10="Y" and EB08=$0, the deductible is fully met. If EB10="Y" and EB08=$1,500 (or any non-zero), that is the remaining deductible. Always look at EB08 for the actual remaining amount. Some payers return separate EB segments: one with EB13="D" and EB10="Y" (deductible applies) and a different EB segment with EB13="A" and EB10="Y" (deductible remaining = $X).

**Q:** How do I determine if a service is subject to a copay OR a deductible OR both?
**A:** Parse the EB segments for the specific service type (EB03). For the matching EB segments:
1. Check for EB13="A" (Copay applies): If present, a copay exists for this service.

2. Check for EB13="D" (Deductible applies): If present, the deductible applies first.

3. Check for EB13="B" (Coinsurance applies): If present, coinsurance applies after deductible.

4. The typical order: (a) Deductible first (patient pays until deductible is met). (b) Then copay OR coinsurance (patient pays fixed amount or %). (c) Until OOP max is reached. However, some plans have "copay-only" or "deductible-only" designs. Examples:
- Copay-only plan: EB13="A" (copay), no EB13="D" -- patient only pays copay
- Deductible + coinsurance: EB13="D" and EB13="B" -- patient pays deductible first, then coinsurance
- Copay + coinsurance: Rare but possible -- patient pays copay, then also pays coinsurance on remaining

5. Look at ALL EB segments. Sometimes the deductible information is in a separate EB segment (EB03="30") while the copay is in the service-specific EB segment (EB03="33" or "98").

---

## 5. Batch Eligibility (NSF/TRN Transactions)

### What is Batch Eligibility?

Batch eligibility verification involves sending a file containing multiple 270 requests (often hundreds or thousands) to a clearinghouse or payer and receiving a batch file with 271 responses hours to a day later.

### Transaction Flow for Batch

```
                     NSF (Non-sufficient funds / Network Service File)
                    /                                                    \
Provider Batch File                                                   Clearinghouse
(Many 270 transactions)                                               Processes
                    \                                                    /
                     NSF (Processed responses)
                    /                                                    \
                    v
                Payer Processes
                Each 270
                    |
                    v
                Payer Returns
                271 Responses
                    |
                    v
                Clearinghouse Compiles
                Batch Response File
                    |
                    v
                Provider Receives
                Processed 271 Responses
```

### TRN (Trace) Segments

- **TRN02 in 270**: The provider-assigned trace number that follows each transaction through the batch process.
- **TRN02 in 271**: The same trace number returned so you can match each response to its request.

### Common Batch File Formats

- **270/271 flat files** (standard X12 005010X279A1)
- **CSV/Excel** (non-standard, used by some clearinghouses for ease of use)
- **API/JSON** (emerging standard, FHIR-based)

### Batch Eligibility Use Cases

1. **Pre-visit verification**: Run batch eligibility overnight for all patients scheduled for the next day.
2. **Population health**: Check eligibility for all patients in a disease registry.
3. **Credentialing**: Batch-verify provider participation across plans.
4. **COB monitoring**: Identify patients with multiple coverages.
5. **Coverage termination alerts**: Detect when patients lose coverage (e.g., Medicaid renewal failures).

### Agent Q&A

**Q:** What is the advantage of batch eligibility over real-time eligibility for a busy practice?
**A:** Advantages: (1) Efficiency: Check 200+ patients with a single file submission instead of 200 individual transactions. (2) Cost: Batch is often cheaper per transaction. (3) Automation: Scheduled overnight runs check all next-day patients automatically. (4) Reporting: Batch systems produce exception reports (patients not found, coverage terminated) for focused follow-up. (5) Less staff time: No need for staff to perform per-patient checks. Disadvantages: (1) Not real-time: If a patient changes coverage between the batch run and the appointment, the batch result is stale. (2) Failure rate: Some transactions in the batch may fail silently. (3) Technical complexity: Requires file generation, submission, and response parsing. Best practice: Run batch eligibility 24-48 hours before scheduled visits, THEN run real-time checks for: (a) Same-day appointments, (b) Patients flagged as "not found" in batch, (c) Patients who report recent insurance changes, (d) Procedures/services that require detailed benefit information not available in batch.

**Q:** A batch eligibility run shows "Patient Not Found" for 15% of my patients. What's the most likely cause?
**A:** A 15% not-found rate is HIGH (target is <3%). Most common causes: (1) Stale batch data: The patient information used for batch (name, member ID, DOB) is outdated. (2) Wrong payer ID: The batch file may be using an incorrect payer ID for the patient's specific plan. (3) Coverage terminated: Batch catches patients whose coverage ended (Medicaid disenrollment, employment change). (4) Data entry errors: Batch exposes errors in patient demographics (transposed DOB, misspelled names). (5) Multiple payers: Patients with multiple coverage -- perhaps the wrong payer was selected in the batch. Action steps: (a) Run a test real-time 270 for each "not found" patient. (b) If real-time also fails, check demographics against the insurance card. (c) Verify the payer ID used in the batch matches the patient's plan. (d) If real-time works but batch failed, there may be a format issue in the batch file (e.g., wrong date format, missing dependent loop). (e) Contact the clearinghouse to review the batch file format. (f) Re-run batch with corrected data.

---

## 6. API-Based Eligibility (FHIR)

### What is FHIR?

Fast Healthcare Interoperability Resources (FHIR, pronounced "fire") is a modern RESTful API standard for healthcare data exchange. For eligibility, the relevant resources are:

- **Coverage**: Represents a patient's health insurance coverage
- **EligibilityRequest**: The API request to check eligibility (similar to 270)
- **EligibilityResponse**: The API response with benefit details (similar to 271)

### FHIR Coverage Resource

```json
{
  "resourceType": "Coverage",
  "id": "9876B1",
  "status": "active",
  "subscriberId": "ABC123456789",
  "beneficiary": {
    "reference": "Patient/12345"
  },
  "relationship": {
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/subscriber-relationship",
      "code": "self"
    }]
  },
  "payor": [{
    "reference": "Organization/67890"
  }],
  "period": {
    "start": "2024-01-01",
    "end": "2024-12-31"
  }
}
```

### FHIR EligibilityRequest

```json
{
  "resourceType": "EligibilityRequest",
  "status": "active",
  "patient": {
    "reference": "Patient/12345"
  },
  "provider": {
    "reference": "Organization/54321"
  },
  "coverage": {
    "reference": "Coverage/9876B1"
  },
  "created": "2024-06-10T14:30:00Z",
  "servicedDate": "2024-06-15"
}
```

### FHIR EligibilityResponse

```json
{
  "resourceType": "EligibilityResponse",
  "status": "active",
  "patient": {
    "reference": "Patient/12345"
  },
  "disposition": "Coverage confirmed, benefits verified",
  "insurance": [{
    "coverage": {
      "reference": "Coverage/9876B1"
    },
    "benefitPeriod": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    },
    "item": [{
      "category": {
        "coding": [{
          "code": "30",
          "display": "Plan Coverage"
        }]
      },
      "financial": [{
        "type": {
          "coding": [{"code": "benefit"}]
        },
        "usedMoney": {
          "value": 1500,
          "currency": "USD"
        },
        "allowedMoney": {
          "value": 5000,
          "currency": "USD"
        }
      }]
    }]
  }]
}
```

### API vs EDI: Pros and Cons

| Aspect | EDI 270/271 | FHIR API |
|---|---|---|
| **Standard** | X12 005010X279 | HL7 FHIR (R4) |
| **Format** | Text-based | JSON/XML |
| **Speed** | Real-time (2-30s) | Real-time (sub-second) |
| **Complexity** | Complex parsing required | Simple parsing |
| **Adoption** | Universal (all payers) | Growing (larger/commercial payers) |
| **Data richness** | Structured (loops/segments) | Structured (resources/elements) |
| **Error handling** | AAA segments | HTTP status codes + OperationOutcome |
| **Authentication** | Clearinghouse connection | OAuth 2.0 / API key |
| **Batch** | Supported natively | Requires custom implementation |

### Agent Q&A

**Q:** Is FHIR replacing 270/271 entirely?
**A:** No, not in the near to medium term. While FHIR is growing rapidly for patient-facing apps and interoperability, 270/271 EDI remains the universal standard for provider-to-payer eligibility verification. Several factors slow the transition: (1) EDI is deeply embedded in clearinghouse and practice management systems. (2) Every payer supports EDI 270/271. Not all support FHIR. (3) Small payers and regional plans may never implement FHIR. (4) Clearinghouse infrastructure is built around EDI translation and routing. (5) Batch eligibility (bulk patient checks) works better in EDI than FHIR currently. (6) Federal regulations (HIPAA) mandate EDI 5010 standards. That said: FHIR is increasingly used for: (a) Patient-facing eligibility checks (patient portals, mobile apps). (b) Provider direct-to-payer API integration (bypassing clearinghouses). (c) Real-time benefit verification at the point of care. (d) Prior authorization data integration. The future will likely see both standards coexisting -- EDI for clearinghouse-based batch and FHIR for real-time point-of-service verification.

**Q:** An FHIR EligibilityResponse returns "active" status but no financial details (copays, deductible). Why?
**A:** Several possible reasons: (1) The API request did not include service type codes -- without specifying what services you're checking, the system may return only a generic "active/inactive" status. (2) The payer's FHIR implementation may not support financial detail -- some payers implement minimal FHIR APIs that only return coverage status. (3) The patient may have a plan with no cost sharing beyond the deductible -- some plans have no copay information to return. (4) The API may require an OAuth token with specific scopes to access financial details. (5) The API consumer may not have the "benefit" financial scope approved. Troubleshooting: (a) Check if the API supports the `EligibilityRequest` with specific service types. (b) Check if the API supports the `benefit` financial type. (c) Review the API documentation for required OAuth scopes. (d) Fall back to EDI 270/271 for full benefit details. (e) Contact the payer's developer support.

---

## 7. Clearinghouse & Payer Routing

### How Clearinghouses Work

A clearinghouse is an intermediary that:
1. Accepts 270 requests from multiple providers
2. Translates formats (if needed -- e.g., from proprietary to X12 5010)
3. Routes requests to the correct payer based on the payer ID
4. Receives 271 responses from payers
5. Translates responses back to the provider's system format
6. Returns responses to the provider

### Payer IDs in the Clearinghouse

- Each clearinghouse maintains a database of payer IDs (electronic payer IDs) that map to payer electronic connections.
- The same payer may have different IDs across different clearinghouses.
- The payer ID in the 270 HL/2000A/NM1 loop (NM109 with NM108="PI") tells the clearinghouse where to route the request.

### Common Clearinghouses

| Clearinghouse | Key Features |
|---|---|
| Change Healthcare (formerly Emdeon/WebMD) | Largest, supports most payers |
| Availity | Popular for BCBS and major payers |
| ZirMed (now FinThrive) | Strong middle-market presence |
| Office Ally | Popular with small practices (free tier available) |
| Trizetto Provider Solutions (Waystar) | Large enterprise presence |
| SSI / SimpleAdmit | Real-time eligibility focus |

### How Routing Works

```
Provider sends 270 with payer ID "48024"
    |
    v
Clearinghouse looks up payer ID 48024
    |
    v
Payer ID maps to "Blue Cross Blue Shield of Illinois"
    |
    v
Clearinghouse determines which payer connection to use
    |
    v
270 is sent to BCBS IL's EDI system
    |
    v
BCBS IL returns processed 271
    |
    v
Clearinghouse translates and returns to provider
```

### Agent Q&A

**Q:** Why does my claim with BCBS of Illinois using payer ID 48024 work, but eligibility with the same payer ID fails?
**A:** This is a common issue. Possible reasons: (1) Different payer IDs for different lines of business: Claims may use payer ID "48024" for BCBS IL claims, but eligibility requires a different payer ID (e.g., "48025"). (2) Different payer connections: Claims and eligibility often use different EDI connections (even on the same payer ID). (3) Eligibility is for a different BCBS plan: The patient's BCBS of Illinois plan may be a specific employer plan that has a different eligibility connection. (4) Payer ID mismatch: The payer ID for claims may route to BCBS IL's claims system, while eligibility requires a different ID that routes to the eligibility system. (5) Clearinghouse routing: The clearinghouse may have separate routing tables for claims vs eligibility. Solutions: (a) Check the clearinghouse's payer ID lookup tool and look for the "Eligibility" payer ID (it's often different from the "Claims" payer ID). (b) Search for BCBS IL in the eligibility lookup specifically. (c) Call the clearinghouse support. (d) Try using the generic "BlueCard" eligibility ID if the patient has a BCBS plan from another state.

**Q:** I send a 270 transaction but never receive a 271 response. What happened?
**A:** Several possible causes: (1) Clearinghouse communication failure: The clearinghouse may not have received your 270, or you may not have received the 271 back. (2) Payer did not respond: Some payers do not respond to 270 transactions at certain times (batch processing windows, system downtime). (3) Authentication failure: The clearinghouse rejected the transaction due to authentication issues. (4) File format error: The 270 is malformed and cannot be processed. (5) Network timeout: The transaction timed out. (6) Clearinghouse filtering: The clearinghouse may have filtered the transaction (e.g., due to a missing/invalid required field). Troubleshooting: (a) Check the clearinghouse's transaction log for the status of your 270. (b) Verify your connection to the clearinghouse is active. (c) Check your system's 270 generation for format errors. (d) Try a single test 270 for a known-good patient. (e) Contact the clearinghouse support. (f) If the clearinghouse shows "submitted to payer" with no response, the payer may have a system issue or the 270 may have been rejected by the payer without an acknowledgment. (g) Try calling the payer directly for a manual eligibility check.

---

## 8. Real-World Edge Cases

### Edge Case 1: Patient Not Found

**Symptom**: The 271 response includes AAA segment with AAA03="15" (Patient not found) or EB01="3" (No active coverage).

**Causes**:
1. Invalid subscriber ID (wrong ID, transposed digits, missing prefix)
2. Name mismatch (name on card doesn't match payer database)
3. DOB mismatch
4. Coverage terminated
5. Coverage is for a different line of business (e.g., checking medical when only pharmacy is active)
6. The patient is a dependent, and the subscriber loop contains the dependent's info instead of the subscriber's

**Resolution steps**:
1. Verify patient identity and subscriber ID against the insurance card
2. Re-run the 270 with corrected information
3. If still failing, check if the patient's name or DOB has recently changed (marriage, typo)
4. Call the payer's provider services line
5. If payer confirms coverage is active but 270 fails, ask for the correct format for the subscriber ID
6. Check if the patient's coverage is brand new (some systems have a 24-72 hour delay before coverage appears)

### Edge Case 2: Invalid Subscriber ID

**Symptom**: AAA03="15" or "60" (Invalid subscriber ID).

**Causes**:
- Leading zeros omitted or included incorrectly
- Hyphens/spaces included when they should not be (or vice versa)
- The patient is using a pharmacy ID for a medical eligibility check
- The patient has a new member ID due to plan change
- Subscriber ID from an old insurance card (patient changed plans)

**Resolution**:
1. Ask to see the insurance card directly
2. Enter the ID exactly as shown on the card
3. Try the ID without spaces/hyphens, then with them
4. Check if the patient's member ID changed (new plan year, new employer, plan update)
5. Verify through the payer's website or customer service

### Edge Case 3: COB Not Working

**Symptom**: 271 shows only one active coverage, but patient says they have two.

**Causes**:
- The second coverage is not linked in the payer's COB system
- The 270 was sent to the wrong payer (the one that doesn't have primary)
- The secondary coverage requires a separate 270 to a different payer
- The patient's COB information has not been entered by the primary payer

**Resolution**:
1. Send a separate 270 to each insurance company
2. Ask the patient for the other insurance card
3. Check the primary payer's COB records manually by calling
4. The 271 from a single payer will NOT show other coverage unless COB is active in their system
5. To check COB: look for EB01="3" with remarks about other coverage, or check the AAA segment

### Edge Case 4: Medicare Part B Only

**Symptom**: 271 shows Medicare Part B active but Part A not found.

**Meaning**: Patient only enrolled in Part B (outpatient/physician), not Part A (inpatient hospital).

**Implications**:
- Outpatient services: Part B covers (80% after deductible)
- Inpatient services: NOT covered (patient needs Part A or other coverage)
- DME: Part B covers (80% after deductible)
- Hospital observation: Part B covers (outpatient status)
- Skilled nursing: Requires Part A coverage (not covered under Part B)

### Edge Case 5: Payer Says "Coverage Verified" but Benefits Are Vague

**Symptom**: 271 returns "Active Coverage" but no copay, deductible, or coinsurance information.

**Causes**:
- The 270 used a generic EQ03 code (e.g., "30") instead of service-specific codes
- The payer's system does not return detailed benefits via EDI (rare but happens)
- The plan has a customized benefit design that cannot be determined by EDI
- The plan is self-funded and benefit details are employer-specific

**Resolution**:
1. Re-run with specific EQ codes (e.g., "33" for PCP, "86" for ER, "98" for specialist)
2. Call the payer to confirm detailed benefits (ask for copay, deductible, OOP max)
3. Check the payer's provider portal for detailed benefit information
4. If the patient has a complex benefit design, ask for a copy of the Summary of Benefits and Coverage (SBC)

### Agent Q&A

**Q:** A patient has an HMO plan and needs to see a specialist. I run eligibility and it says "Active" but I cannot see any copay information. What should I do?
**A:** For HMO plans, the eligibility system may not return copay information because the benefit details depend on: (1) Whether the patient has a valid PCP referral. (2) Whether the referral has been authorized. (3) Whether the specialist is in-network. (4) The specific service being performed. The 270 with generic EQ03 code may not return copay info for HMO specialist visits because the system needs the authorization to calculate benefits. Solutions: (a) Check if the referral/authorization has been obtained and is active. (b) Run the 270 with EQ03="98" (Physician Visit) after the authorization is in place. (c) Call the HMO's provider services line and ask: "What is the specialist copay for this patient?" (d) Check the provider portal for the specific patient's benefit details. (e) If all else fails, the contract rate may determine the copay -- check your contract for standard copay amounts. (f) Document that benefit details were unavailable through EDI and manual verification was performed.

**Q:** A previously covered patient's 271 response now shows "Coverage Terminated" even though the patient says they still have insurance. What could have happened?
**A:** Several possibilities: (1) The patient lost coverage without realizing it (employer stopped paying premiums, COBRA expired). (2) The patient changed plans (new employer, new plan year) but has a new member ID. (3) Data mismatch: The patient's name/DOB/ID in your system don't match their CURRENT coverage (which may have a different ID). (4) Timely filing: The old member ID may have been deactivated at the end of the plan year. (5) Medicaid redetermination: The patient may have failed to respond to their Medicaid renewal notice. (6) The patient's coverage was terminated by the employer for non-payment (common with union plans). First step: Contact the patient and say "Our records show your coverage may have changed. Do you have a new insurance card?" If the patient confirms coverage is active, ask for the new card. If the patient is unsure, call the payer with the patient present (on speakerphone) to investigate.

**Q:** Can a 271 response tell me if a service requires prior authorization?
**A:** Yes, sometimes. The 271 can include prior authorization information in: (1) The REF segment after the EB segment, with REF01="G1" (Prior Authorization Number) if an authorization exists. If no authorization number is returned, it may mean: no auth is required, or auth is required but not obtained yet. (2) Some payers return EB segments with EB01="G" (Benefit information) and a text description like "Prior auth required" in EB05 (Plan Coverage Description) or in the REF segment. (3) Look for EB13="P" or specific text notes indicating authorization requirements. However: Not all payers return prior auth requirements in the 271. The 271 is an eligibility/benefits transaction, NOT a utilization management transaction. For many plans, prior auth requirements are determined separately. Best practice: Always check the payer's specific prior authorization requirements through their provider portal, provider manual, or phone line. Do not rely solely on the 271 to determine whether prior auth is needed.

---

## 9. 271 Response Translation Examples

### Example 1: Comprehensive Benefits for a PPO Visit

**Raw 271 Data** (for EQ03="98" Professional Visit):
```
EB*1*IND*98*PP*OFFICE VISIT~
HSD*VS*1~
REF*G3*COPAY: $30.00~~~
EB*G**DEDUCTIBLE REMAINING:$500.00~
EB*C*FAM*30**OUT-OF-POCKET MAX:$3000.00~
```

**Translation**:
- Active coverage for professional visits
- Copay: $30 per visit
- Deductible remaining: $500
- Out-of-pocket max: $3,000

**Patient's total cost before services** : $30 copay
**Note**: The $30 copay applies. The deductible is $500 remaining (for services not covered by copay).

### Example 2: Deductible-Only Plan (HDHP)

**Raw 271 Data**:
```
EB*1*IND*30*PP*HDHP~
HSD***1000~
EB*G**DEDUCTIBLE REMAINING:$2000.00~
EB*1**98**OFFICE VISIT~
HSD***250~
EB*G**PATIENT PAYS 100% UNTIL DEDUCTIBLE MET~
```

**Translation**:
- HDHP active
- Deductible remaining: $2,000
- Office visit cost: 100% patient responsibility until deductible is met ($250 per visit allowed amount, patient pays $250)
- After deductible: 80/20 (if shown in another EB)

### Example 3: Medicare Secondary Payer

**Raw 271 Data**:
```
EB*1*IND*30*MB*MEDICARE PART B~
EB*G**DEDUCTIBLE:$240.00~
EB*G**COINSURANCE:20%~
EB*1*IND*30*C*GROUP HEALTH SECONDARY~
```

**Translation**:
- Medicare Part B active
- Deductible: $240 (annual)
- Coinsurance: 20%
- Secondary coverage: Group health plan (active)

### Example 4: Visit Limit Exceeded

**Raw 271 Data**:
```
EB*1*IND*33**PRIMARY CARE~
HSD*VS*20~
EB*G**COPAY: $25.00~
EB*1**35**WELL CHILD~
HSD*VS*0~
EB*G**NO VISITS REMAINING~
```

**Translation**:
- Primary care: 20 visits remaining, $25 copay
- Well child visits: 0 visits remaining (benefit limit exceeded)

### Agent Q&A

**Q:** I have a 271 that shows "Deductible: $1,000" AND "Copay: $25 office visit." Does the patient pay both a copay AND the deductible?
**A:** It depends on the plan design. There are two main scenarios: (1) **Copay-only plans**: Some plans (especially PPOs with copay-first designs) have services that are copay-only -- the copay applies and the deductible does not. (2) **Deductible-first then copay**: Some plans apply the deductible to ALL services first, then after the deductible is met, the patient pays a copay. (3) **Deductible-then-coinsurance**: More common than copay-after-deductible. After deductible, patient pays 20% coinsurance. Here's how to tell from the 271: (a) Look at the EB13 indicator for each EB segment. If EB13="A" (Copay) AND EB13 does not contain "D" (Deductible), the service may be copay-only. (b) If the EB segment for the same service type mentions "D" (Deductible), the deductible applies first. (c) Check the EB13 sequence: typically EB13="D" before EB13="A" means deductible first. (d) When in doubt, call the payer and ask: "For a standard office visit, does the copay apply first, or does the deductible apply first?" (e) The HSD segment can also indicate -- if it shows a monetary amount (HSD03=M3), that's a copay. If it shows a percentage, that's coinsurance (applies after deductible).

**Q:** The 271 shows "Visit limit: 0 remaining" for physical therapy. The patient says they haven't used any PT this year. Who is right?
**A:** The payer's system is likely correct. Possible explanations: (1) The benefit limit for PT is a lifetime limit, not annual. If the patient has used all 20 visits over multiple years, there are no visits remaining. (2) The patient may have PT under a different condition (e.g., auto accident) using a different benefit. (3) The visit limit may have been applied across all therapies (PT + OT + speech combined), and the patient used OT visits. (4) There may be a gap between when visits are used and when the system updates (unlikely -- most are real-time). (5) The service type code in the 271 may not match what is actually used. Steps: (a) Call the payer to confirm the benefit remaining and ask for the specific dates of prior PT visits. (b) Check if the limit is annual, per-condition, or lifetime. (c) Ask the patient about prior PT visits (they may have forgotten). (d) If the patient's other provider's visits are being counted, that is correct -- the limit applies across all providers. (e) Appeal with documentation if the system is wrong (rare). (f) If the limit is truly exceeded, discuss self-pay or alternative treatment options.

---

## 10. 271 Response Codes Reference

### EB01 -- Eligibility/Benefit Information

| Code | Description | Meaning |
|---|---|---|
| 1 | Active Coverage | Patient has active coverage |
| 2 | Active Coverage with Limits | Coverage is active but has limits or restrictions |
| 3 | No Active Coverage | Patient is not covered on this date |
| 4 | Coverage is Inactive | Coverage exists but is inactive (e.g., terminated) |
| A | Co-Insurance | Patient has coinsurance benefit |
| B | Co-Payment | Patient has copay benefit |
| C | Deductible | Plan has a deductible |
| D | Benefit Description | Detailed benefit description |
| E | Exclusions | Service is excluded from coverage |
| F | Maximum Benefit | Benefit maximum applies (visit limit or dollar cap) |
| G | Benefit Information | General benefit information |
| H | Non-Covered | Service is not covered |
| L | In-Network Coverage | Benefit is for in-network providers |
| M | Out-of-Network Coverage | Benefit is for out-of-network providers |
| P | Benefit Disclaimer | Contains disclaimer or cautionary info |
| R | Other or Additional Payor | Other coverage exists (COB) |
| S | Prior Authorization Required | Authorization needed for service |

### EB13 -- Information Codes

| Code | Description |
|---|---|
| A | Copay applies |
| B | Coinsurance applies |
| C | Service not covered |
| D | Deductible applies |
| E | Exclusions apply |
| F | Limits apply |
| G | Out-of-pocket maximum applies |
| H | Pre-existing condition applies |
| I | Risk pool adjustment |
| J | Secondary payer information |
| K | Third-party liability |
| L | Workers' compensation |
| M | Other insurance information |
| N | Pre-authorization/pre-certification required |
| O | Pre-authorization/pre-certification obtained |
| P | Benefit information |

### AAA03 -- Reject Reason Codes

| Code | Description |
|---|---|
| 15 | Patient/Insured not found |
| 26 | Subscriber/Insured not found |
| 42 | Unable to respond at current time |
| 57 | Invalid/Missing date of birth |
| 58 | Invalid/Missing insured name |
| 59 | Invalid/Missing subscriber/insurer name |
| 60 | Invalid/Missing subscriber/insurer ID |
| 61 | Name mismatch (subscriber name does not match ID) |
| 62 | Service type not supported by payer |
| 63 | Dependent not found |
| 64 | Invalid subscriber/insured relationship |
| 65 | Invalid gender code |
| 66 | Invalid/missing provider name |
| 67 | Invalid/missing provider ID |
| 68 | Provider not eligible for inquiry |
| 69 | Invalid/missing diagnosis code |
| 70 | Invalid/missing procedure code |
| 71 | Diagnosis code inconsistent with patient age |
| 72 | Invalid/missing charge amount |
| 73 | Invalid/missing date of service |
| 74 | Invalid/missing provider type/specialty |
| 75 | Provider type/specialty not applicable to inquiry |

### Agent Q&A

**Q:** The 271 returns EB01="E" (Exclusions) for a service I'm trying to verify. What does this mean for the patient?
**A:** EB01="E" means the service you asked about is specifically excluded from the patient's plan. This could be because: (1) The service is a standard exclusion in the plan (e.g., cosmetic surgery, weight loss surgery). (2) The service requires additional criteria to be covered (e.g., medical necessity, step therapy, prior authorization). (3) The patient's specific plan (employer-specific) excludes this service even though other plans from the same payer cover it. (4) The exclusion applies only for certain diagnosis codes. Impact on the patient: the service will not be paid by insurance. The patient can: (a) Pay out-of-pocket (if the provider allows private pay for excluded services). (b) Appeal if they believe the service should not be excluded. (c) Check if the exclusion can be waived (some plans have an "exclusion waiver" process for medical necessity). (d) Use a different insurance if they have secondary coverage. (e) Seek the service from a provider or facility that bills under a different benefit. If EB01="E" and the provider performs the service anyway, the provider should have the patient sign an Advanced Beneficiary Notice or waiver acknowledging that the service will not be covered.

**Q:** The 271 shows EB01="S" (Prior Authorization Required). What does this mean for workflow?
**A:** EB01="S" means the payer is indicating that prior authorization is REQUIRED for the service you're checking. This triggers a specific workflow: (1) Do NOT proceed with the service until prior authorization is obtained (unless it's an emergency). (2) Check the payer's prior authorization requirements -- the 271 does not tell you HOW to obtain the auth (phone, portal, fax, EDI). (3) Some payers provide the authorization requirements in the REF segment after the EB segment (REF01="G1" for auth info). (4) Check if the patient already has an auth (some may be obtained by the referring provider). (5) Initiate the prior authorization request through your system or the payer's portal. (6) Ensure the auth is in hand before the service date. (7) If the patient schedules the service without a necessary auth and the claim later denies, the provider CANNOT bill the patient for the denied charges (unless the patient signed a waiver). (8) EB01="S" is the 271's way of saving you from a preventable denial -- treat it seriously. (9) Some payers have "soft" auth requirements where the 271 shows "S" but the auth is automatically obtained or not actually required -- call to confirm if unclear.

**Q:** What does EB01="R" (Other or Additional Payor) mean?
**A:** EB01="R" is important -- it means the payer is indicating that the patient has OTHER coverage. This is the payer's way of doing COB notification through the 271. What it tells you: (1) The payer has records of other active insurance. (2) The other coverage may be through a spouse, Medicare, Medicaid, or another group plan. (3) The coverage order (primary vs secondary) may need investigation. (4) IF you submitted a claim to this payer and they are not primary, the claim will deny as CO 22 (COB). Action steps: (a) Ask the patient: "Do you have any other insurance coverage?" (b) Confirm the other coverage details. (c) Determine which plan is primary. (d) Submit the claim to the correct primary payer first. (e) If the patient denies having other coverage, call the payer to investigate -- the payer may have erroneous COB data. (f) Do NOT ignore EB01="R" -- submitting a claim to the wrong payer wastes time and causes rework.

---

## 11. Workflow Integration & Best Practices

### Recommended Workflow

```
Patient Check-In
    |
    v
Verify Patient Identity (Name/DOB)
    |
    v
Collect Insurance Card (Front/Back)
    |
    v
Select Payer ID in System
    |
    v
Enter Subscriber ID, Patient Demographics
    |
    v
Send 270 with Service-Type EQ Codes
    |
    v
Receive 271 Response
    |
    v
Parse and Display Benefits to User
    |
    v
Check: Coverage Active? --------- No --> Alert: Coverage Issue
    |                                       |
    Yes                                     v
    |                                  Contact Payer / Patient
    v
Check: Plan Type / Network
    |
    v
Check: Pre-Auth Required? --------- Yes --> Initiate Auth
    |                                       |
    No                                      v
    v                                  Wait for Auth Obtained
Check: Benefit Limits (Visits,       |
Deductible, Copay, OOP Max) ----------+
    |
    v
Check: COB (Other Insurance?) ------ Yes --> Note Secondary Coverage
    |                                       |
    No                                      v
    v                                  Determine Order
All Clear                                      |
    |                                          v
    v                                     Note for Claim
Proceed with Service
```

### Best Practices Checklist

- [ ] Always verify eligibility BEFORE rendering services (pre-service)
- [ ] Use service-specific EQ codes (not just "30")
- [ ] Document the 271 response (print or save)
- [ ] Re-verify for same-day changes (if the patient reports a change)
- [ ] For scheduled procedures: verify at scheduling AND day-of-service
- [ ] Batch-verify all patients for the next day (overnight batch)
- [ ] Alert on "Not Found" or "Coverage Terminated" responses
- [ ] Check for COB indicators (EB01="R")
- [ ] Verify network participation separately (does not come from 271)
- [ ] Run 270 1-2 weeks before the service for large deductibles / high-cost procedures

### Integration with Other RCM Systems

| RCM Function | How Eligibility Data Integrates |
|---|---|
| Patient Scheduling | Insurance verified at time of scheduling |
| Patient Registration | Demographic data linked to eligibility response |
| Claim Generation | Subscriber ID, group number, payer ID from eligibility |
| Payment Posting | Copay/coinsurance amounts from eligibility help with payment estimation |
| Denial Management | 271 data helps identify COB issues before claim submission |
| Patient Statements | Patient responsibility amounts from eligibility used for estimates |

### Agent Q&A

**Q:** How do you verify network participation if the 271 doesn't tell you if the provider is in-network?
**A:** The 271 eligibility response does NOT tell you if a specific provider is in-network. You must check network participation through separate methods: (1) Payer's provider directory website (most common). (2) Payer's provider portal (look up your NPI to see if you are listed as in-network). (3) Payer's provider services phone line (ask "Is NPI 1234567890 in-network for this patient's specific plan?"). (4) The insurance card's network name (e.g., "BlueCard PPO" -- you would need to be in the BlueCard network). (5) Clearinghouse network verification tools (some clearinghouses offer network lookups). (6) Contract documentation (your signed contract with the payer lists which networks you participate in). Important: Being in-network for one plan from a payer does NOT mean you are in-network for ALL plans from that payer. A provider may be in-network for a PPO plan but out-of-network for an HMO plan from the same insurance company. Always check network participation specifically for the patient's plan.

**Q:** What is the best strategy for high-deductible patients -- should I collect the expected patient responsibility before service?
**A:** Yes, for high-deductible plans, best practice is to collect expected patient responsibility at the time of service (before service for scheduled procedures, at check-in for office visits). Strategy: (1) Use the 271 response to determine: deductible remaining, coinsurance %, OOP max, and whether the service is subject to deductible. (2) Estimate the patient's cost: for a deductible-applied service, use the payer's contracted rate (or usual charge) to estimate patient responsibility. (3) Provide a good faith estimate (as required by the No Surprises Act for uninsured/self-pay patients). (4) Collect at least the expected deductible amount before service. (5) For established patients, consider payment plans or sliding scale. (6) Document the estimate and provide to the patient in writing. (7) After the claim processes, reconcile the collected amount with the actual EOB and adjust (refund if over-collected, bill if under-collected). This approach improves cash flow and reduces bad debt.

---

## 12. Common Denials Related to Eligibility

### Denial Codes and Their Eligibility Root Causes

| Denial Code | Description | Root Cause in Eligibility |
|---|---|---|
| CO 16 | Claim lacks information | Eligibility not verified -- missing subscriber ID |
| CO 22 | COB issue | Other coverage existed but was not identified |
| CO 29 | Timely filing | Eligibility was verified too late |
| CO 31 | Patient cannot be identified | Subscriber ID mismatch (270 would have shown "patient not found") |
| CO 32 | Not pre-authorized | 271 showed EB01="S" but auth was not obtained |
| CO 35 | Benefit limit exceeded | 271 showed visit limit or dollar limit exhausted |
| CO 50 | Service not covered | 271 showed EB01="E" (exclusion) or EB01="H" (non-covered) |
| CO 97 | Benefit included in another | 271 showed the wrong service type was used |
| CO 119 | Benefit maximum reached | 271 showed "0 visits remaining" or "$0 maximum remaining" |
| CO 141 | Patient has no coverage | 271 showed EB01="3" or "4" |
| CO 167 | Diagnosis not covered | 271 showed service/diagnosis mismatch |
| CO B14 | Place of service inconsistency | May have verified for wrong place of service type |
| PR 34 | Missing authorization | EB01="S" was ignored |

### How Eligibility Verification Prevents Each Denial

| Denial | Prevention via Eligibility |
|---|---|
| CO 16 | 270 verifies patient/subscriber identity before claim submission |
| CO 22 | 270 with COB check identifies multiple coverages |
| CO 29 | 270 confirms coverage is active within timely filing window |
| CO 31 | 270 confirms patient ID matches payer records |
| CO 32 | 271's EB01="S" triggers prior auth workflow |
| CO 35 | 271's EB06/EB07 shows remaining visit limits |
| CO 50 | 271's EB01="E" or "H" shows excluded/non-covered services |
| CO 119 | 271's HSD/EB shows benefit maximum remaining |
| CO 141 | 271's EB01="1" confirms active coverage |
| PR 34 | 271's prior auth indicator triggers auth before rendering service |

### Agent Q&A

**Q:** A claim denied with CO 35 (Benefit limit exceeded) for physical therapy. The 271 showed 20 visits remaining. What went wrong?
**A:** The 271 data may have been stale or incorrect. Possible issues: (1) **Time lag**: The 271 was run 2 weeks before the service. Between then and the service, other providers may have submitted PT claims that used up the visits. Eligibility data is a "snapshot" at the time of the 270, not a reservation of benefits. (2) **Wrong service type**: The 271 showed 20 visits for "Physical Therapy" (EQ 47 or similar), but the claim was processed against a DIFFERENT benefit pool (e.g., "Rehabilitation" which includes PT+OT+speech). (3) **Plan change**: The patient's plan renewed on Jan 1, and the benefit limit reset -- or did not reset. (4) **Data synchronization**: The payer's 271 system and claims system may not be in sync. (5) **Other providers**: Another provider submitted claims that reduced the benefit count. Prevention: (a) Run eligibility 24 hours before scheduled services, not 2 weeks before. (b) Track benefit usage in your system (cumulative visits). (c) Call the payer to confirm remaining benefits before high-utilization procedures. (d) For benefit-limited services (PT, chiro, mental health), verify benefits monthly and track usage.

**Q:** A claim was denied because the patient's coverage had lapsed (CO 141). The 271 showed active coverage just 3 days before the service. How could this happen?
**A:** Several scenarios: (1) The patient lost coverage between the 270 and the service date (employment termination, premium non-payment, employer plan termination). (2) The 270 was run with a future service date but the coverage ended before the actual service date. (3) The patient had a "grace period" for premium payment -- coverage appeared active on the 271 but actually lapsed retroactively when the premium was not paid. (4) The patient's coverage was terminated retroactively (e.g., due to fraud investigation or retroactive Medicaid disenrollment). (5) For Medicaid: patients can lose coverage retroactively to the beginning of the month if they fail redetermination. Actions: (a) Contact the patient to confirm coverage status. (b) Contact the payer to determine the exact termination date. (c) If coverage ended retroactively, the patient is responsible for the full charge. (d) If coverage was active on the date of service, appeal with the 271 printout as evidence. (e) If the coverage ended on the date of service (same day), the claim may still process if submitted (some payers honor same-day termination). (f) For Medicaid: if the patient has been disenrolled retroactively, check if they can re-enroll and get retroactive coverage reinstated.

**Q:** The 271 response shows "Deductible remaining: $0" but the claim processes with a deductible applied? What happened?
**A:** Possible explanations: (1) **Service-type mismatch**: The 271 was for a service type that is exempt from deductible (e.g., preventive care), but the actual claim was for a service type that is subject to deductible (e.g., problem-oriented visit). (2) **Family vs individual deductible**: The patient's individual deductible shows as met, but the service was applied to the family deductible (which has a different remaining balance). (3) **Embedded vs aggregate**: The 271 showed the embedded deductible (individual), but the family deductible (aggregate) still has a balance. (4) **Time lag**: Accumulations between the 270 and the claim reduced the deductible to $0, then a new charge triggered a new deductible period. (5) **Plan year reset**: The 271 was run in the old plan year when the deductible was met, but the service fell in the NEW plan year (deductible reset). Prevention: (a) Run eligibility on the DATE OF SERVICE, not before. (b) Use the correct EQ code for the specific planned service (not general "30"). (c) Verify deductible at the INDIVIDUAL AND FAMILY levels. (d) Check the plan year dates (DTP segments). (e) For high-dollar services, re-verify coverage and accumulations immediately before the service.

---

## 13. Training Q&A Bank

### Core Knowledge Q&A

**Q:** What is the difference between a 270 and a 271 transaction?
**A:** The 270 is the "Eligibility Benefit Inquiry" -- the request sent by the provider asking about a patient's coverage and benefits. The 271 is the "Eligibility Benefit Response" -- the payer's answer to the 270. The 270 goes OUT from the provider (hence the "0" -- outbound), and the 271 comes IN (the "1" -- inbound). The 270 must contain patient identification (name, DOB, subscriber ID) and service date information. The 271 returns coverage status, copays, deductibles, coinsurance, and other benefit information.

**Q:** How long does a real-time 270/271 transaction typically take?
**A:** Most real-time 270/271 transactions complete in 2-30 seconds. Factors affecting speed: (1) Clearinghouse processing time (usually <1 second). (2) Payer system response time (2-15 seconds typical; can be slower for complex queries). (3) Network latency. (4) Payer system load (peak hours can slow response). (5) Batch-mode transactions take hours (overnight processing). If a real-time 270 takes longer than 30 seconds, the payer system is likely slow or the connection has timed out. Most clearinghouses implement a 30-60 second timeout.

**Q:** What is the difference between "Eligibility" and "Benefits" in the context of 270/271?
**A:** "Eligibility" refers to whether the patient is enrolled in the plan and their coverage is active as of a specific date. "Benefits" refers to the specific covered services, cost sharing amounts (copays, deductible, coinsurance), benefit limits (visit counts, dollar caps), and other plan details. The 270 asks about both. The 271 returns separate information: Eligibility status (EB01="1" or "3") and Benefit information (EB segments with copay, deductible, limit details). In practice, the terms are used interchangeably ("eligibility verification"), but technically: eligibility = "is the patient covered?" benefits = "what is covered and at what cost?"

**Q:** What information do I need to send a valid 270 transaction?
**A:** Minimum required data: (1) Payer ID (to route the request). (2) Provider NPI (to identify the requesting provider). (3) Subscriber ID (member ID from the insurance card). (4) Subscriber name (first, last). (5) Subscriber date of birth. (6) Service date (or date range). (7) Service type code (or general "30"). Optional but helpful: (8) Patient name/DOB (if different from subscriber). (9) Patient relationship to subscriber. (10) Gender. (11) Diagnosis code (some payers use it for benefit determination). Missing any of the first six items will likely result in an AAA reject code (invalid request).

### Scenario Q&A

**Q:** A patient is scheduled for an MRI next week. What 270 EQ codes should I use to verify benefits?
**A:** For an MRI (a high-cost diagnostic imaging service), use these EQ codes: (1) EQ*30~ (General coverage) -- to confirm the patient is covered. (2) EQ*50~ (Outpatient hospital) -- if the MRI will be done at a hospital outpatient department. (3) EQ*47~ (Inpatient hospital) -- if the MRI requires admission. (4) EQ*98~ (Professional visit / physician service) -- for the radiologist's interpretation fee. (5) EQ*1~ (Medical care) -- for general medical/surgical benefits. (6) You may also want: EQ*86~ (Emergency) -- if the MRI could be performed emergently, though for a scheduled MRI this is unlikely. Important: MRIs are often subject to prior authorization. Even if the 271 shows "Active coverage" and "Deductible: $X remaining," it doesn't guarantee the MRI will be paid. You MUST also verify: (a) Prior authorization requirements. (b) Medical necessity criteria. (c) Whether the MRI requires a specific diagnosis code. (d) Whether the facility is in-network. The 271 only tells you about benefits, not about authorization or medical necessity.

**Q:** A new patient calls to schedule an appointment. They provide their insurance info over the phone. Should I run eligibility before scheduling?
**A:** Yes. Best practice is to verify eligibility at the time of scheduling for new patients. This helps: (1) Confirm the patient has active coverage. (2) Identify any COB issues early. (3) Determine if the plan type (HMO, PPO) requires a PCP referral. (4) Check if prior authorization is needed for initial visits (rare for office visits, common for procedures). (5) Estimate patient copays/deductibles so you can communicate cost expectations. (6) Avoid scheduling a patient who no longer has coverage or whose plan you don't participate with. Exceptions: (a) Some practices wait until the day before if the scheduling window is very long (>30 days out). (b) If you run eligibility at scheduling, ALWAYS re-run on the day of service (coverage can change). (c) For same-day/urgent scheduling, run eligibility at check-in.

**Q:** A patient has an HMO plan and needs a referral to a specialist. I verified eligibility and the patient's coverage is active. Can the patient see the specialist now?
**A:** Not yet. HMO plans require a PCP referral before the specialist visit. Even though eligibility is active: (1) The patient must have a valid PCP on file with the HMO. (2) The PCP must issue a referral for the specific specialist and specific service. (3) The referral must be authorized by the HMO (this generates a referral number or authorization number). (4) The specialist visit must be within the effective dates of the referral. (5) Some HMOs also require the specialist to be pre-authorized in their system. Best practice: (a) Confirm the patient has a PCP on file. (b) Request the referral from the PCP (the specialist's office may need to do this). (c) Verify the referral authorization number before the appointment. (d) On the date of service: re-confirm the referral is active. (e) File the claim with the authorization number. (f) If the patient sees the specialist without a referral, the claim will deny (CO 32 -- not pre-authorized). The 271 alone does NOT confirm referral or authorization status for most plans.

**Q:** A patient's Medicaid eligibility shows as "Active" but with the remark "Pending Renewal." What does this mean?
**A:** "Pending Renewal" means the patient's Medicaid redetermination is in process. This occurs when: (1) The patient's annual renewal date has passed or is approaching. (2) The state sent a renewal form but has not received the patient's response. (3) The state processed the renewal but the results are pending. The patient's coverage is still active during this period. If the patient does not complete the renewal, coverage will be terminated. For claims processing: (1) The coverage is active -- claims will process. (2) However, if the renewal fails and the patient is disenrolled retroactively, the claims from this period will be DENIED. (3) The provider may be left with uncollectible charges. Action steps: (a) Advise the patient to complete their Medicaid renewal immediately. (b) Provide contact information for the state Medicaid agency. (c) If the renewal is already in process, ask for the confirmation/receipt number. (d) For high-cost services, consider whether to proceed or wait for the renewal to be finalized. (e) If the patient loses coverage retroactively, the provider may need to write off the charges (depending on state law and provider policy for retroactive disenrollment).

---

## 14. 270/271 Testing and Troubleshooting

### Testing Your 270/271 Connection

1. **Clearinghouse certification**: Most clearinghouses provide a certification process to validate your 270 generation software.
2. **Test patients**: Use the payer's test patients (provided during onboarding) to validate the transaction.
3. **Common test data**:
   - Subscriber ID: Usually a known test value provided by the payer
   - Payer ID: Test payer ID (varies by clearinghouse)
   - Service date: Future date within 365 days

4. **Expected successful response**: 271 with EB01="1" (Active coverage)
5. **Expected failure response**: AAA segment with a reject code

### Common Transaction Errors

| Error | Symptom | Fix |
|---|---|---|
| Invalid Payer ID | 270 not accepted by clearinghouse | Verify payer ID in clearinghouse database |
| Invalid Subscriber ID | AAA15 (Patient not found) | Verify ID from card |
| Missing Required Field | 270 rejected at clearinghouse | Check required segments are populated |
| Date Format Error | 270 rejected at clearinghouse | Use CCYYMMDD format |
| Loop Structure Error | 270 rejected at clearinghouse | Check correct HL hierarchy (2000A > 2000B > 2000C > 2000D) |
| Provider Not Authorized | 270 rejected at clearinghouse | Verify provider is credentialed with payer |
| Service Type Not Supported | 270 accepted by clearinghouse but rejected by payer | Use a different service type code |
| Payer Connection Down | 270 accepted but no response | Wait and retry |

### Agent Q&A

**Q:** My clearinghouse says "Connection to Payer is Down" when I send a 270 to a specific payer. What should I do?
**A:** This is a payer system outage, not a problem with your 270. Actions: (1) Wait 10-15 minutes and retry. (2) Check the clearinghouse's status page for known outages. (3) Call the payer's EDI support line to confirm the status. (4) If the outage is expected to be short (< 1 hour), wait and retry. (5) If the outage is expected to be longer: (a) Use the payer's provider portal for manual eligibility checks. (b) Call the payer's provider services line. (c) Document: "Eligibility could not be verified due to payer system outage on [date/time]." (d) For scheduled patients, note the issue and plan to re-verify before services. (e) For same-day patients, proceed with services but collect a deposit (especially for self-pay/high-deductible). (f) Re-run eligibility once the system is back up. (g) If the claim processes with a denial due to the outage-related verification failure, appeal with documentation of the system outage.

**Q:** How do I troubleshoot a 270 transaction that returns an unexpected AAA code?
**A:** Follow this systematic troubleshooting: (1) Read the AAA03 code. (2) Check for field-specific validation: AAA03="57" (Invalid/Missing DOB) -> verify DOB format is 8-digit CCYYMMDD (not DD/MM/YYYY or MM/DD/YYYY) AND matches the payer's records. AAA03="60" (Invalid/Missing ID) -> verify the subscriber ID is exactly as on the card. AAA03="61" (Name mismatch) -> verify the subscriber name is spelled exactly as on the card. AAA03="64" (Invalid relationship) -> verify the relationship code is correct (Self, Spouse, Child). (3) If the code is nonspecific (15=Patient not found): (a) Verify ALL patient/subscriber data. (b) Try removing or adding hyphens/spaces in the ID. (c) Try the name with or without middle initial. (d) Check the date of service -- is it within the coverage period? (e) Check the payer ID -- is it the right one for this plan? (4) Call the payer for help: "I'm getting an AAA code [X]. Can you help me identify what needs to be corrected?" (5) Document the troubleshooting for future reference.

---

## 15. Compliance and Regulatory Notes

### HIPAA Requirements

- 270/271 transactions must comply with HIPAA Transaction and Code Set Rule (45 CFR 162)
- The current standard is ASC X12 005010X279A1
- All covered entities (providers, clearinghouses, health plans) must use HIPAA-compliant transactions
- Violations can result in HIPAA penalties

### No Surprises Act (2022)

- Requires providers to give uninsured/self-pay patients a good faith estimate of charges
- "Good faith estimate" is based on eligibility benefit information
- The 271 response is used to calculate patient cost estimates
- Insurance-based good faith estimates: Providers must estimate and share expected charges with patients who request them (for scheduled services)

### Medicare Requirements

- Medicare eligibility can be verified through the Medicare Beneficiary Lookup Tool
- Medicare 271 responses follow the same 5010 standard but Medicare-specific rules
- Advanced Beneficiary Notice (ABN) required for Medicare patients when services may not be covered
- Medicare Advantage plans have different eligibility verification requirements

### Agent Q&A

**Q:** Can I be penalized for submitting incorrect 270 transactions?
**A:** Directly: No, the 270 is an inquiry, not a claim. Incorrect 270 data will simply result in an AAA reject or incorrect benefits returned. However: (1) If you systematically submit incorrect data to the clearinghouse (e.g., wrong NPIs, wrong provider credentials), the clearinghouse may restrict your access. (2) If you use the 271 response to collect patient payments (estimated amounts) and the estimate is consistently wrong due to improper 270 use, you could face patient complaints or Payer/State Consumer Protection scrutiny. (3) HIPAA compliance: You must use standard transactions (5010), but errors in the data content do not carry civil penalties. (4) False Claims Act: Not applicable to eligibility inquiries. The 270/271 is for inquiry only -- it is not a financial transaction and does not involve government funds. Best practice: Ensure your 270 data is accurate to get accurate 271 responses, which in turn reduces billing errors and patient complaints.

**Q:** Do I need a patient's consent to run a 270 eligibility check?
**A:** Generally, no -- eligibility verification is a standard part of healthcare operations and is permitted by HIPAA for treatment, payment, and healthcare operations purposes. The HIPAA Privacy Rule allows covered entities to disclose protected health information (PHI) for payment and healthcare operations without patient authorization. Eligibility verification falls under both: (1) Payment: Determining whether insurance will pay for services. (2) Healthcare operations: Conducting quality assessment and improvement activities, business planning, and development. However: (a) Some states have additional privacy protections (e.g., for mental health, reproductive health). (b) If the patient has requested restrictions on how their information is used, you must honor those restrictions. (c) For sensitive services (substance abuse, mental health), additional consent may be required. (d) Best practice: include authorization for eligibility verification in the general consent-to-treat form that patients sign.

---

## 16. Glossary

| Term | Definition |
|---|---|
| **270** | Health Care Eligibility Benefit Inquiry (outbound request) |
| **271** | Health Care Eligibility Benefit Response (inbound response) |
| **5010** | Current HIPAA standard version for 270/271 (ASC X12 005010X279A1) |
| **AAA** | Request Validation segment in 271 -- indicates a problem with the 270 |
| **BHT** | Beginning of Hierarchical Transaction -- identifies the transaction type |
| **COB** | Coordination of Benefits -- determining which plan pays first |
| **DTP** | Date or Time Period segment |
| **DMG** | Demographic Information segment (DOB, gender) |
| **EB** | Eligibility or Benefit Information segment (core of the 271) |
| **EQ** | Eligibility or Benefit Inquiry segment (core of the 270 -- service type codes) |
| **FHIR** | Fast Healthcare Interoperability Resources (modern API standard) |
| **HL** | Hierarchical Level segment (defines the loop structure) |
| **HSD** | Health Care Services Delivery segment (copay per visit, deductible amounts) |
| **MAC** | Medicare Administrative Contractor |
| **NPI** | National Provider Identifier (10-digit unique provider ID) |
| **NSF** | Network Service File (batch eligibility file format) |
| **NM1** | Individual or Organizational Name segment |
| **OOP Max** | Out-of-Pocket Maximum |
| **REF** | Reference Identification segment (authorization numbers, additional info) |
| **ST/SE** | Transaction Set Header/Trailer (beginning/end of transaction) |
| **TRN** | Trace segment (used for batch tracking) |
| **X12** | The standards body that defines EDI transaction formats (ASC X12) |
| **Clearinghouse** | Intermediary that translates and routes EDI transactions between providers and payers |
| **Real-time** | 270/271 completed in seconds (versus batch which takes hours) |
| **Service Type Code** | EQ03/EB03 -- identifies the specific healthcare service being inquired about |
| **Payer ID** | Identifier used to route transactions to the correct payer via the clearinghouse |

---

## 17. Summary: Key Takeaways for LLM Agent

When processing eligibility and benefits verification:

1. **270 is the request, 271 is the response** -- always send the right EQ codes for the services you are verifying.
2. **The EB segment is the heart of the 271** -- parse EB01 (coverage status), EB08 (monetary amounts), EB09 (percentages), EB06/EB07 (visit limits), and EB13 (benefit type indicators).
3. **AAA segment means the 270 was rejected** -- check AAA03 for the specific reason.
4. **Real-time is seconds; batch is hours** -- choose based on the use case.
5. **Pre-service verification prevents denials** -- 15% of denials are demographic/eligibility-related and preventable.
6. **The 271 does not tell you everything** -- it does not confirm network participation, prior authorization status, or the patient's financial ability to pay.
7. **Stale eligibility data causes denials** -- always verify close to the date of service.
8. **COB issues are common with eligibility** -- look for EB01="R" or EB01="C" to identify secondary coverage.
9. **Medicare verification is different** -- check for Medicare Part A and Part B separately; use the MBI, not the HICN.
10. **API (FHIR) is growing but EDI 270/271 remains the standard** -- be familiar with both.

---

*End of Eligibility & Benefits Verification Knowledge Base Document*