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

### EB Segment Field-by-Field Reference

The EB (Eligibility or Benefit Information) segment is the most important data element in the 271 response. Each EB segment describes one piece of benefit information. A single 271 response may contain 5-25 EB segments covering different service types, benefit categories, and network levels.

#### EB01 -- Eligibility/Benefit Information Codes (Comprehensive)

These are the most critical codes. They tell you the type of information the EB segment is conveying. There are 40+ defined codes.

| Code | Category | Meaning | Example Usage |
|------|----------|---------|---------------|
| **1** | Active Coverage | Patient has active coverage for the specified service type | `EB*1*IND*30...` means active general coverage |
| **2** | Active - In Plan Network | Active coverage specifically for in-network providers | `EB*2*IND*30...` means in-network coverage active |
| **3** | Active - Out of Plan Network | Active coverage specifically for out-of-network providers | `EB*3*IND*30...` means OON coverage active |
| **4** | Active - Cost Sharing In Plan | Active coverage with cost sharing in-network | `EB*4*IND*98...` means office visit with cost sharing |
| **5** | Active - Cost Sharing Out of Plan | Active coverage with cost sharing out-of-network | `EB*5*IND*98...` means OON visit with cost sharing |
| **6** | Active - No Cost Sharing In Plan | Active coverage with zero patient cost sharing (e.g., preventive) | `EB*6*IND*AE...` means preventive at 100% |
| **7** | Inactive | Coverage is not active for the specified service type | `EB*7*IND*30...` means coverage terminated |
| **8** | Inactive - Pending | Coverage is pending (application in process) | `EB*8*IND*30...` means eligibility not yet determined |
| **9** | Not Used - Entity Not Eligible | The entity (patient) is not eligible for this service | `EB*9*IND*30...` means patient not found/not eligible |
| **A** | Not Used - Not Eligible (Specific) | More specific version of code 9 | Rarely used |
| **B** | Benefit - Waiting Period | Patient is in a waiting period before coverage starts | `EB*B*IND*30*27...` means waiting period applies |
| **C** | Coverage Level Information | General information about the coverage level | `EB*C*IND*30...` means coverage level info |
| **D** | Benefit - Deductible | Deductible information for this service type | `EB*D*IND*30*27*4000...` means $4,000 deductible |
| **E** | Benefit - Coinsurance | Coinsurance information | `EB*E*IND*30*27***20...` means 20% coinsurance |
| **F** | Benefit - Copayment | Copayment information | `EB*F*IND*98*27*30...` means $30 copay |
| **G** | Out of Pocket Maximum | OOP maximum information | `EB*G*IND*30*27*7000...` means $7,000 OOP max |
| **H** | Benefit - Exclusions | Services that are excluded from coverage | `EB*H*IND*AL...` means vision excluded |
| **I** | Benefit - Limit | Benefit limits (visit limits, dollar caps) | `EB*I*IND*76*27*30...` means 30 PT visits limit |
| **J** | Benefit - Benefit Description | Text description of a specific benefit | `EB*J*IND*30...` followed by MSG with description |
| **K** | Benefit - Alternative | An alternative benefit is available | Rarely used |
| **L** | Benefit - Exception | Exception information | Rarely used |
| **M** | Benefit - Prior Authorization | Prior authorization requirements | `EB*M*IND*2...` means surgery requires auth |
| **N** | Not Used | Service is not a covered benefit | `EB*N*IND*CD...` means acupuncture not covered |
| **P** | Benefit - Exclusions | Explicit exclusion from coverage | `EB*P*IND*35...` means adult dental excluded |
| **U** | Not Used - Incurred Date | Service date is outside the coverage period | `EB*U*IND*30...` means DOS outside coverage period |
| **W** | Not Used - COB | Coordination of benefits applies (another payer is primary) | `EB*W*IND*30...` means other coverage exists |
| **X** | Not Used - Pre-Existing Condition | Pre-existing condition exclusion applies | `EB*X*IND*AO...` means MH pre-existing exclusion |

#### EB02 -- Coverage Level Codes

| Code | Meaning | Usage |
|------|---------|-------|
| CHD | Child Only | Coverage applies to a child dependent only |
| DEP | Dependent | Coverage applies to a dependent (spouse/child) |
| E | Employee/Subscriber | The subscriber only (individual) |
| FAM | Family | Coverage applies to the entire family |
| IND | Individual | Individual coverage (not part of a family plan) |
| SPC | Spouse Only | Coverage for spouse only |
| TWO | Two Party | Subscriber + one dependent (subscriber + spouse typically) |

#### EB03 -- Service Type Codes (Complete Reference)

The full set of X12 service type codes used in 270/271 transactions. These are used in both the EQ segment (270 request) and the EB segment (271 response).

| Code | Service Type | Category | Notes |
|------|-------------|----------|-------|
| **1** | Medical Care | General Medical | Broadest category; covers most physician services |
| **2** | Surgical | Surgical | Surgical services, both inpatient and outpatient |
| **3** | Consultation | Professional | Professional consultation services |
| **4** | Diagnostic X-Ray | Diagnostics | X-ray and diagnostic imaging |
| **5** | Diagnostic Lab | Diagnostics | Clinical laboratory services |
| **6** | Radiation Therapy | Oncology | Radiation treatment |
| **7** | Obstetrical | Maternity | Obstetric and maternity care |
| **8** | Anesthesia | Surgical Support | Anesthesia services for surgery/procedures |
| **9** | Ambulance | Emergency | Emergency and non-emergency medical transport |
| **10** | Inpatient Hospital | Hospital | General inpatient care (beyond room/board) |
| **11** | Outpatient Hospital | Hospital | Hospital outpatient services |
| **12** | Durable Medical Equipment (DME) | Equipment | DME and supplies |
| **13** | Ambulatory Surgery Center | Facility | Facility fees for ASC |
| **14** | Wheelchair | DME | Wheelchair and mobility accessories |
| **18** | Benefit Exhaustion | Warning | Benefits exhausted for this service type |
| **20** | Second Surgical Opinion | Professional | Second opinion consultation |
| **22** | Chemotherapy | Oncology | Chemotherapy administration |
| **24** | Dialysis | Chronic Care | Kidney dialysis |
| **25** | Immunizations | Preventive | Vaccines and immunizations |
| **26** | EPSDT | Pediatric | Early and Periodic Screening/Diagnosis/Treatment |
| **30** | Health Benefit Plan Coverage | General | Plan-level coverage information (general inquiry) |
| **31** | Home Health Care | Home Health | Home health services (all types) |
| **33** | Chiropractic | Complementary | Chiropractic care |
| **35** | Dental Care | Dental | All dental services |
| **36** | Dental - Screening | Dental | Dental exam and screening |
| **37** | Dental - Diagnostic | Dental | Dental diagnostic services |
| **38** | Dental - Preventive | Dental | Dental preventive care (cleanings, etc.) |
| **39** | Dental - Restorative | Dental | Fillings and restorations |
| **40** | Dental - Extractions | Dental | Tooth extractions |
| **41** | Dental - Crowns | Dental | Crown and bridge |
| **42** | Dental - Prosthodontics | Dental | Dentures and prosthetics |
| **43** | Dental - Oral Surgery | Dental | Oral surgery |
| **44** | Dental - Periodontics | Dental | Gum treatment |
| **45** | Dental - Endodontics | Dental | Root canals |
| **46** | Dental - Orthodontics | Dental | Braces and alignment |
| **47** | Hospital | Hospital | General hospital services (all types) |
| **48** | Hospital - Inpatient | Hospital | Inpatient hospital services specifically |
| **49** | Hospital - Room & Board | Hospital | Daily room and board charges |
| **50** | Hospital - Outpatient | Hospital | Outpatient hospital services specifically |
| **51** | Hospital - Emergency | Hospital | Emergency department hospital services |
| **52** | Hospital - Inpatient Physician | Professional | Physician services for inpatients |
| **53** | Hospital - Outpatient Physician | Professional | Physician services for outpatients |
| **56** | Skilled Nursing Care | Facility | Skilled nursing facility care |
| **57** | Skilled Nursing - Room & Board | Facility | SNF daily room and board |
| **58** | Long Term Care | Facility | Custodial care/nursing home |
| **60** | Comprehensive Outpatient Rehab (CORF) | Rehab | CORF facility services |
| **61** | Home Health - Nursing | Home Health | Nursing home health visits |
| **62** | Home Health - PT | Home Health | Physical therapy via home health |
| **63** | Home Health - OT | Home Health | Occupational therapy via home health |
| **64** | Home Health - ST | Home Health | Speech therapy via home health |
| **65** | Home Health - Aide | Home Health | Home health aide services |
| **66** | Home Health - HHA | Home Health | Home health agency services |
| **67** | Home Health - MSW | Home Health | Medical social work via home health |
| **68** | Well Baby Care | Pediatric | Newborn and well-child visits (0-2 years) |
| **69** | Maternity Care | Maternity | Pregnancy-related care (prenatal, delivery, postpartum) |
| **75** | Speech Therapy | Rehab | Speech-language pathology services |
| **76** | Physical Therapy | Rehab | Physical therapy services |
| **77** | Occupational Therapy | Rehab | Occupational therapy services |
| **78** | Physical/Med Rehab Day Program | Rehab | Day rehabilitation program |
| **79** | Cardiac Rehabilitation | Rehab | Cardiac rehab |
| **80** | Pulmonary Rehabilitation | Rehab | Pulmonary rehab |
| **82** | Pharmacy | Pharmacy | Prescription drug coverage |
| **83** | Pharmacy - Inpatient | Pharmacy | Inpatient pharmacy |
| **84** | Compounding Pharmacy | Pharmacy | Custom-compounded medications |
| **85** | Pharmacy - Outpatient | Pharmacy | Outpatient pharmacy |
| **86** | Emergency Services | Emergency | Emergency department services (professional) |
| **87** | Emergency Services - After Hours | Emergency | After-hours emergency care |
| **88** | Network | Network | Network participation information |
| **89** | Substance Abuse | Behavioral Health | Substance use disorder treatment |
| **90** | Non-Emergency Ambulatory | Transport | Non-emergency outpatient transport |
| **91** | Brand Name Prescription Drug | Pharmacy | Brand name Rx drug |
| **92** | Generic Prescription Drug | Pharmacy | Generic Rx drug |
| **93** | Preferred Brand Name Prescription Drug | Pharmacy | Preferred brand Rx |
| **94** | Non-Preferred Brand Name Prescription Drug | Pharmacy | Non-preferred brand Rx |
| **95** | Professional Visit - Well Visit | Professional | Well/preventive professional visit |
| **96** | Professional Visit - Basic | Professional | Basic professional visit |
| **97** | Professional Visit - Specialty | Professional | Specialist visit |
| **98** | Professional Visit - Office | Professional | Office-based professional visit (most common) |
| **99** | Professional Visit - Inpatient | Professional | Inpatient professional visit |
| **A0** | Professional Visit at Office | Professional | Office visit (alternate code for 98) |
| **A1** | Professional Visit at Home | Professional | Home visit |
| **A2** | Professional Visit at Urgent Care | Professional | Urgent care visit |
| **A3** | Professional Visit at Nursing Home | Professional | Nursing home visit |
| **A4** | Professional Visit at Skilled Nursing | Professional | SNF visit |
| **A5** | Professional Visit at Independent Living | Professional | Independent living facility visit |
| **A6** | Psychotherapy | Behavioral Health | Psychotherapy services |
| **A7** | Professional Telehealth Visit | Telehealth | Telehealth professional visit |
| **A8** | Professional Telehealth at Home | Telehealth | Telehealth from patient's home |
| **A9** | Professional Telehealth at Home Originating | Telehealth | Telehealth originating site at home |
| **AA** | Diabetes Education | Education | Diabetes self-management training |
| **AB** | Diabetes Monitoring Supplies | DME | Glucose monitors, test strips, supplies |
| **AC** | Diabetes Self-Management Training | Education | Diabetes education program |
| **AD** | Nutritional Counseling | Professional | Medical nutrition therapy |
| **AE** | Preventive Care | Preventive | General preventive/wellness services |
| **AF** | Immunizations | Preventive | Immunizations (alternative to code 25) |
| **AG** | Annual Physical | Preventive | Annual wellness exam |
| **AH** | Well Child Visit | Pediatric | Well child checkup |
| **AI** | Mammogram | Screening | Breast cancer screening |
| **AJ** | Pap Smear | Screening | Cervical cancer screening |
| **AK** | Prostate Screening | Screening | Prostate cancer screening |
| **AL** | Vision Services | Vision | Eye exams and vision correction |
| **AM** | Hearing Services | Hearing | Hearing exams and aids |
| **AN** | Acupuncture | Complementary | Acupuncture therapy |
| **AO** | Mental Health Services | Behavioral Health | Mental/behavioral health services |
| **AP** | Substance Abuse Services | Behavioral Health | Substance use disorder treatment (alt code) |
| **AQ** | Inpatient Mental Health | Behavioral Health | Inpatient psychiatric care |
| **AR** | Outpatient Mental Health | Behavioral Health | Outpatient behavioral health |
| **AS** | Partial Hospitalization (Mental Health) | Behavioral Health | Day treatment mental health |
| **AT** | Residential Treatment (Mental Health) | Behavioral Health | Residential mental health treatment |
| **AV** | Home Health - Mental Health | Behavioral Health | Home-based mental health services |
| **AW** | Psychotherapy - Individual | Behavioral Health | Individual therapy session |
| **AX** | Psychotherapy - Group | Behavioral Health | Group therapy session |
| **AY** | Mental Health - Family | Behavioral Health | Family therapy session |
| **AZ** | Mental Health - Assessment | Behavioral Health | Psychiatric evaluation |
| **BA** | Mental Health - Medication Management | Behavioral Health | Psych med management |
| **BB** | Substance Abuse - Detoxification | Behavioral Health | Detox services |
| **BC** | Substance Abuse - Rehab | Behavioral Health | Rehabilitative substance abuse treatment |
| **BD** | Substance Abuse - Outpatient | Behavioral Health | Outpatient substance abuse |
| **BE** | Substance Abuse - IOP | Behavioral Health | Intensive outpatient program |
| **BF** | Substance Abuse - MAT | Behavioral Health | Medication-Assisted Treatment |
| **BG** | Dental Care - Not Covered | Exclusions | Dental services not covered |
| **BH** | Chiropractic - Not Covered | Exclusions | Chiropractic not covered |
| **BI** | Vision - Not Covered | Exclusions | Vision services not covered |
| **BJ** | Hearing - Not Covered | Exclusions | Hearing not covered |
| **BK** | Transplant | Surgical | Organ/tissue transplant |
| **BL** | Hospice | End-of-Life | Hospice care |
| **BM** | Skilled Nursing - Sub-Acute | Facility | Sub-acute SNF care |
| **BN** | Skilled Nursing - Acute | Facility | Acute SNF care |
| **BO** | Outpatient Rehabilitation | Rehab | General outpatient rehabilitation |
| **BP** | Partial Hospitalization (Non-MH) | Rehab | Day treatment (non-behavioral) |
| **BQ** | Medical/Surgical Supplies | Supplies | General medical/surgical supplies |
| **BR** | Prosthetics/Orthotics | Equipment | Prosthetic/orthotic devices |
| **BS** | DME - Respiratory | DME | Oxygen and respiratory equipment |
| **BT** | DME - Diabetic Supplies | DME | Diabetes testing supplies |
| **BU** | DME - Wheelchair | DME | Wheelchair/scooter |
| **BV** | DME - CPAP/BiPAP | DME | Sleep apnea equipment |
| **BW** | DME - Hospital Bed | DME | Hospital bed |
| **BX** | DME - Walkers/Crutches/Canes | DME | Mobility aids |
| **CA** | Podiatry | Professional | Foot care services |
| **CB** | Allergy Testing | Diagnostics | Allergy diagnostics |
| **CC** | Allergy Immunotherapy | Professional | Allergy shots/immunotherapy |
| **CD** | Acupuncture - Not Covered | Exclusions | Acupuncture excluded |
| **CE** | DME - Not Covered | Exclusions | DME excluded |
| **CF** | Chiropractic Maintenance - Not Covered | Exclusions | Maintenance chiropractic not covered |
| **CG** | Physical Therapy - Evaluation | Rehab | PT evaluation |
| **CH** | Occupational Therapy - Evaluation | Rehab | OT evaluation |
| **CI** | Speech Therapy - Evaluation | Rehab | ST evaluation |
| **CJ** | Medical Nutrition Therapy | Professional | Nutrition counseling |
| **CK** | Education/Training | Education | Patient education |
| **MH** | Mental Health (Alternate) | Behavioral Health | Behavioral health (legacy 4010 code) |
| **UC** | Urgent Care | Emergency | Urgent care services |
| **PT** | Physical Therapy (Alternate) | Rehab | Alternate PT code |
| **OT** | Occupational Therapy (Alternate) | Rehab | Alternate OT code |
| **ST** | Speech Therapy (Alternate) | Rehab | Alternate ST code |
| **DM** | Durable Medical Equipment (Alternate) | Equipment | Alternate DME code |
| **CR** | Cardiac Rehab (Alternate) | Rehab | Alternate cardiac rehab code |
| **PU** | Pulmonary Rehab (Alternate) | Rehab | Alternate pulmonary rehab code |

#### EB04 -- Insurance Coverage Information Codes

This composite field provides additional detail about what the EB segment is describing.

| Code | Meaning | Description |
|------|---------|-------------|
| **1** | Benefit Description | Free-text description of the benefit |
| **2** | In Plan Network | Benefit applies within the plan's network |
| **3** | Benefit Amount Remaining | Dollar or visit amount remaining for this benefit |
| **4** | Benefit Amount | Total benefit amount (not what is remaining) |
| **5** | Service Description | Description of the specific service |
| **6** | Time Period | The time period the service type refers to |
| **7** | Benefit Percentage | The percentage the plan pays (e.g., 80%) |
| **8** | Copayment Amount | The copayment amount for this service type |
| **9** | Deductible Amount | The deductible amount for this service type |
| **10** | Out of Pocket Maximum Amount | The out-of-pocket maximum amount |
| **11** | Benefit Limit | The specific limit for this benefit |
| **12** | Alternative Benefit | Another benefit that may apply instead |
| **13** | Accumulation Information | Running accumulations toward limits or deductibles |

#### EB05 -- Quantity/Time Period

This is a numeric value that represents remaining visits, days, or other countable benefit units.

| Value | Meaning | Example |
|-------|---------|---------|
| "30" | 30 remaining visits | 30 PT visits remaining this year |
| "20" | 20 remaining visits | 20 chiropractic visits remaining |
| "100" | 100 days remaining | 100 SNF days remaining per benefit period |
| "0" | 0 remaining | Benefit is fully exhausted |
| "999" | Unlimited | No limit on this service type |
| (Blank) | No quantity info | Benefit is not limited by count |

#### EB06 -- Time Period Qualifier

| Code | Meaning | Usage |
|------|---------|-------|
| **1** | Remaining (current period) | Visits or dollars remaining right now |
| **2** | Current Year (calendar year) | Benefit applies to the current calendar year |
| **3** | Current Month | Benefit applies to the current month |
| **4** | Current Week | Benefit applies to the current week |
| **5** | Remaining (alternate) | Same as "1" but alternate code |
| **6** | Lifetime | Benefit is for the patient's lifetime |
| **7** | Year to Date | Accumulated year to date |
| **8** | Remaining Lifetime | Remaining benefit for the patient's lifetime |
| **9** | Current Period | Generic "current period" reference |
| **10** | Day | Benefit applies to a single day |
| **11** | Remaining (specific) | Remaining for a specific period |
| **22** | Service Year | Benefit applies to the plan's service year |
| **23** | Calendar Year | Benefit applies to the calendar year |

#### EB07 -- Monetary Amount

Dollar amount related to the benefit. The meaning depends on EB01 and EB04 context:

| EB01 Context | EB07 Meaning | Example |
|--------------|--------------|---------|
| "D" or "B" (Deductible) | Remaining deductible amount | "4000" = $4,000 remaining |
| "F" (Copayment) | Copay amount | "30" = $30 copay |
| "G" (OOP Max) | OOP max amount | "7000" = $7,000 OOP max |
| "I" (Benefit Limit) | Dollar limit amount | "2000" = $2,000 annual max |
| "C" (Coverage Level) | Maximum benefit amount | "1000000" = $1M lifetime max |
| Blank/General | Depends on context | Varies by payer |

#### EB08 -- Percentage

| Value | Meaning |
|-------|---------|
| "20" | 20% coinsurance (patient pays 20%) |
| "0" | 0% coinsurance (patient pays nothing beyond deductible) |
| "50" | 50% coinsurance (often for OON) |
| "100" | 100% patient responsibility |
| (Blank) | No percentage applies |

#### EB09 -- In/Out of Network Indicator

| Code | Meaning |
|------|---------|
| **Y** | Yes, benefit applies in-network |
| **N** | No, benefit applies out-of-network |
| **U** | Unknown network status |
| (Blank) | Network status not specified or not applicable |

#### EB10-EB13 -- Additional Information Composite Fields

These composite fields contain supplementary codes that modify or qualify the benefit information in the EB segment. They are payer-specific in many cases but some standard patterns exist:

**EB10**: Yes/No Condition Indicator
- "Y" = Yes, the condition (specified in EB13) applies
- "N" = No, the condition does not apply
- "U" = Unknown

**EB13**: Information Code
- "A" = Copay applies to this service
- "B" = Coinsurance applies to this service
- "D" = Deductible applies to this service
- "F" = Benefit limit applies
- "G" = OOP max applies
- "H" = Pre-existing condition applies
- "N" = Pre-authorization/pre-certification required
- "O" = Pre-authorization/pre-certification obtained
- "P" = Benefit information (general)

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

## 8. Major Clearinghouses and Their Eligibility Interfaces

### Clearinghouse Role in Eligibility

Clearinghouses act as intermediaries between providers and payers. For eligibility, they provide:

1. **Translation**: Accept 270 inquiries from provider systems and translate into payer-specific formats if needed.
2. **Routing**: Determine which payer should receive the 270 based on the submitted payer ID.
3. **Consolidation**: Return 271 responses back to the provider system in a standardized format.
4. **Value-add**: Many clearinghouses provide a simplified eligibility interface that hides 270/271 complexity.

### Change Healthcare (formerly Emdeon/WebMD)

- **Eligibility products**: Real-Time Eligibility, Batch Eligibility, Eligibility Express
- **Coverage**: Most commercial payers, Medicare, many Medicaid plans
- **Interface**: 270/271 EDI via SFTP, real-time via HTTPS, web portal
- **Payer ID system**: Change Healthcare maintains its own payer ID list. A single payer may have multiple IDs for different lines of business (e.g., commercial vs Medicare Advantage)
- **Notable features**: "Eligibility Express" for simplified web-based checks; batch eligibility with overnight processing; automated eligibility at patient check-in for integrated PM systems
- **Pricing**: Per-transaction fee for real-time eligibility (typically $0.25-$0.50 per transaction); batch pricing varies by volume
- **Payer ID lookup**: Available through the Change Healthcare Payer List tool (searchable by payer name, state, or line of business)

### Availity

- **Eligibility products**: Availity Essentials (web portal), Real-Time Eligibility (API/EDI), Batch Eligibility
- **Coverage**: Broad commercial payer coverage, strong Medicare and Medicaid coverage
- **Interface**: Web portal, RESTful API (JSON), EDI 270/271
- **Payer ID system**: Availity uses a "Payer ID" or "Payer Name" search within their portal
- **Notable features**: "Payer Spaces" -- payer-specific portals within Availity; "Availity Link" for workflow integration; patient-friendly "Patient Eligibility Summary" display
- **Pricing**: Varies by contract; many payers subsidize Availity eligibility for their contracted providers
- **Unique capability**: "Patient Financial Responsibility" calculator that uses eligibility data to estimate patient out-of-pocket costs

### ZirMed (now FinThrive)

- **Eligibility products**: Real-Time Eligibility Manager, Batch Eligibility
- **Coverage**: Strong commercial and Medicaid coverage
- **Interface**: Web portal, integrated API, EDI 270/271
- **Notable features**: "Patient Access" module for registration-integrated eligibility; denial prevention alerts based on eligibility results
- **Pricing**: Typically bundled with claims processing services
- **Unique capability**: Automated eligibility at patient check-in -- runs a 270 automatically when a patient is checked in

### Office Ally

- **Eligibility products**: Patient 24/7 (web portal), Real-Time Eligibility, Batch Eligibility
- **Coverage**: Broad coverage including many smaller/regional payers
- **Interface**: Web portal, EDI 270/271
- **Pricing**: Free eligibility for providers using Office Ally's clearinghouse (Patient 24/7 web portal). Per-transaction pricing for integrated EDI
- **Notable features**: No-cost basic eligibility for independent practices; built-in payer ID lookup
- **Unique limitation**: The free web portal requires manual entry; integrated EDI requires a paid subscription

### Navinet (now part of Change Healthcare)

- **Eligibility products**: Navinet Eligibility (web portal)
- **Coverage**: Broad commercial payer coverage
- **Interface**: Web portal only (no direct EDI integration); integrates with some PM systems via API
- **Notable features**: Payer-specific content and alerts within the eligibility workflow
- **Pricing**: Often free to providers (payer-subsidized)
- **Unique capability**: Payer-specific "bulletin board" with updates on plan changes, authorization requirements

### Experian Health (formerly Passport Health)

- **Eligibility products**: Experian Health Eligibility
- **Coverage**: Broad commercial, Medicare, and Medicaid
- **Interface**: Web portal, API integration
- **Notable features**: Integrated patient access suite (eligibility + financial clearance + patient estimates); "Patient Access Estimate" generates cost estimates based on eligibility data; "Smart Match" for identifying patient records across different data sources
- **Pricing**: Enterprise pricing typically
- **Unique capability**: "Charity Care" screening integrated with eligibility -- automatically checks if uninsured patients may qualify for financial assistance

### Waystar (formerly Trizetto)

- **Eligibility products**: Waystar Eligibility
- **Coverage**: Broad, including Medicare and most commercial payers
- **Interface**: Web portal, integrated API/EDI
- **Notable features**: "Eligibility Automation" -- batch eligibility checks for all scheduled patients; "Patient Payment Estimation" based on eligibility data; denial prevention analytics
- **Pricing**: Typically bundled with Waystar's RCM platform
- **Unique capability**: "Payment Advisor" -- uses eligibility data plus contractual rates to provide accurate patient payment estimates at the point of service

### Payer ID Lookup Across Clearinghouses

Important facts about payer IDs:

1. **Payer IDs are NOT universal**: The payer ID for UnitedHealthcare in Change Healthcare (e.g., 87726) is different from the payer ID in Availity or Office Ally. Always use the correct payer ID for YOUR clearinghouse.

2. **Payer IDs differ by line of business**: A single payer may have different IDs for:
   - Commercial (PPO/HMO)
   - Medicare Advantage
   - Medicaid (MCO plans)
   - Self-funded (ASO) accounts

3. **Payer IDs differ by service**: Claims payer ID may differ from eligibility payer ID for the same payer.

4. **Payer IDs change**: Payers periodically update their IDs. Always check the clearinghouse's current payer ID list.

5. **Best practice**: Use the clearinghouse's Payer ID Lookup tool (search by payer name) rather than relying on saved/memorized payer IDs.

---

## 9. Payer-Specific Eligibility Quirks

### Medicare Administrative Contractors (MACs)

Each MAC processes 270/271 eligibility for their specific geographic jurisdiction. The 271 responses vary slightly between MACs:

**Noridian Healthcare Solutions (JE/JF)**:
- Covers: CA, NV, HI, US Territories (Part A/B), AK, AZ, ID, MT, ND, OR, SD, UT, WA, WY (Part B)
- Returns "Benefit Exhausted" for Medicare Part A when benefit period is exhausted or lifetime reserve days are in use
- Returns Part B deductible status as "Remaining $240" (2024) until the deductible is met
- Does NOT return Medicare Advantage benefit details (those go through the MA plan)
- Includes ESRD status in the 271 response
- Response time: Typically 3-10 seconds for real-time; 15-30 minutes for batch

**Palmetto GBA (JM/JJ)**:
- Covers: OH, KY, WV, NC, SC, VA, TN (Part A); various states (Part B)
- Returns "Medicare Secondary Payer (MSP)" information if the beneficiary has other coverage, including the effective date
- Includes "Medicare as Secondary Payer" effective dates in DTP segments
- Some Palmetto 271s include "Skilled Nursing Facility" benefits as a separate EB segment with EB03="56"

**WPS (Wisconsin Physician Services) (J5/J8)**:
- Covers: MI, IN, WI (J5 Part B); IA, MO, NE, KS, MN (J8 Part B); also Part A for various states
- Returns ESRD status in the response
- Includes lifetime reserve day information for Part A
- Returns Part B deductible with annual amount remaining

**First Coast Service Options (JN)**:
- Covers: FL, PR, VI
- Returns Part B deductible status as "Remaining $240" until deductible met
- Does NOT return Part D eligibility via 271 (Part D goes to PDP or MA-PD plan)

**NGS (National Government Services) (J6/JK)**:
- Covers: IL, MN, WI, CT, NY, MA, ME, NH, RI, VT (Part A); various (Part B)
- Returns "Medicare Entitlement" dates (Part A effective date, Part B effective date)
- Includes "Eligibility for Part B" even if the beneficiary has NOT enrolled (returns "No Coverage" if Part B not enrolled)
- Important: NGS processes Part A for NY and New England; the Part B MAC is separate for NY

**CGS Administrators (J15/JNV)**:
- Covers: KY, OH (Part A); KY, OH, TN (Part B)
- Returns detailed Part A benefit period information
- Includes inpatient hospital days used / days remaining

**Novitas Solutions (JH/JL)**:
- Covers: CO, NM, OK, TX (Part A); DE, DC, MD, NJ, PA (Part B)
- Returns "Part A Deductible Met/Not Met" status
- Provides detailed SNF benefit information

### MAC-Specific 271 Variations

| Attribute | Noridian | Palmetto | WPS | NGS | First Coast |
|-----------|----------|----------|-----|-----|-------------|
| Beneficiary name format | MBI exactly | Hyphens OK | No hyphens | No hyphens | Any format |
| Part A deductible shown | Yes | Yes | Yes | Yes | Yes |
| Part B deductible shown | $240 | $240 | $240 | $240 | $240 |
| ESRD status | Yes | Yes | Yes | Yes | Yes |
| MSP indicator | Yes | Yes | Yes | Yes | Yes |
| Part D info | No | No | No | No | No |
| Lifetime reserve days | Yes | Yes | Yes | Yes | Yes |
| SNF benefit period days | Yes | Yes | Yes | Yes | Yes |
| Response detail level | Detailed | Detailed | Standard | Detailed | Standard |

### Commercial Payer Variations

**UnitedHealthcare**:
- Multiple IDs per member: Medical, pharmacy, and behavioral health may use different IDs. The 270 must use the medical subscriber ID.
- Line of business matters: UHC Commercial, UHC Medicare Advantage, UHC Community Plan (Medicaid) each have different payer IDs.
- "Patient Not Found" errors are common when using the wrong line-of-business payer ID.
- Dependents are identified by subscriber ID + their date of birth. UHC does not issue separate member IDs for dependents in most cases.
- 271 responses typically include detailed copay/coinsurance info but may not include visit limits unless queried with specific EQ codes.
- Accumulations shown are as-of-date-of-query, not date-of-service.
- For UHC Medicare Advantage: the 271 shows MA plan benefits, NOT Original Medicare benefits.

**Aetna**:
- Member ID format: 9-digit numeric (most commercial). Some newer accounts use alphanumeric IDs.
- Coverage levels: Aetna 271s frequently use EB01="C" (Coverage Level Information) for general benefit info.
- Deductible presentation: Aetna often returns separate EB segments for individual and family deductible.
- Dependent coverage: Aetna issues separate member IDs for each dependent in many plans (subscriber ID + 2-digit suffix).
- Mental health: Aetna 271s typically include service type code "AO" with cost-sharing info, but benefit limits may not appear unless specifically queried.
- OOP max: Aetna 271s include OOP max with EB01="G".
- Important: Aetna's 271 for self-funded plans may return the generic Aetna benefit template, not the employer's custom plan design.

**Cigna**:
- Member ID format: 9-digit numeric (Cigna ID). Some employer groups use custom IDs.
- Plan types: Cigna 271s explicitly state "PPO", "OAP" (Open Access Plus), "POS", or "HMO" in MSG segments.
- Copay structure: Copays are often listed as "PCP: $25, Specialist: $40" in MSG or HSD segments.
- Network status: Cigna uses EB09 to indicate INN (Y) vs OON (N) benefit levels.
- Self-funded plans: Cigna's 271 may note "Employee Welfare Benefit Plan" or "Self-Funded" in the response.
- Pharmacy carves out: Cigna often carves out pharmacy to Express Scripts (ESI). The medical 271 may return "No Coverage" for pharmacy service type codes. You must query ESI separately for pharmacy benefits.
- Behavioral health: Cigna may carve out behavioral health to Evernorth (formerly Cigna Behavioral Health). The 271 may not show behavioral health benefits.

**Blue Cross Blue Shield (All Plans)**:
- BlueCard program: When a BCBS member is outside their home plan's service area, the 271 is routed through the BlueCard system. Use the BlueCard payer ID, NOT the local BCBS plan's ID.
- BCBS 271 variations: Each BCBS plan implements 271 slightly differently. BCBS of Texas may return differently than BCBS of Illinois.
- Member ID format varies by state plan. Common: prefix + 7-9 digits (e.g., "WXY123456789"), 3-letter prefix + digits, or pure numeric.
- Group number is almost always required for BCBS eligibility queries. If omitted, the 271 may return "No Coverage."
- Federal Employee Program (FEP): BCBS FEP has its own 271 format with "FEP" or "Federal Employee Program" in the payer ID field. FEP uses a separate payer ID.
- Network codes: "BlueCard PPO" vs "BlueChoice" vs "Blue Options" can all have different benefit levels in the 271.
- Some BCBS plans (e.g., BCBS of Massachusetts, BCBS of Michigan) have separate HMO plan IDs that are different from their PPO IDs.

### Large Employer/Self-Funded Plan Variations

Self-funded (ASO) plans may have custom benefit designs that differ from the carrier's standard plan. Key differences:

- Benefit limits: The employer may have different visit limits (e.g., 30 PT visits instead of 20).
- Exclusions: Some self-funded plans exclude services the carrier's standard plan covers.
- Copay/deductible amounts may differ from standard.
- Network: May use a different network (e.g., Custom Network vs standard PPO).
- Payer ID: Some self-funded plans have their own payer ID.

When the 271 responses seem wrong for a self-funded plan, verify the employer's plan document directly. The carrier's 271 system may not have the employer's custom benefits loaded correctly.

### Payer Response Time Comparison

| Payer Type | Typical Real-Time Response | Typical Batch Response |
|------------|---------------------------|----------------------|
| Medicare MACs | 3-10 seconds | 15-30 minutes |
| Large commercial (UHC, Aetna, Cigna) | 5-20 seconds | 1-4 hours |
| Regional BCBS plans | 5-30 seconds | 2-6 hours |
| Medicaid FFS | 5-15 seconds | 4-12 hours |
| Medicaid MCOs | 5-30 seconds | 4-24 hours |
| Small/regional payers | 10-60 seconds | 12-48 hours |
| Some payers (overnight-only) | Real-time not available | 24 hours |

---

## 10. No-Fault vs Workers' Compensation Eligibility

### Why Workers' Comp and No-Fault Are Different

Workers' Compensation and No-Fault (auto insurance) do NOT use the standard 270/271 eligibility transaction in the same way as health plans. They are claim-based rather than person-based. There is no "subscriber ID" or "coverage period" in the traditional sense -- coverage is per-incident.

### Workers' Compensation Eligibility

**How eligibility works for Workers' Comp**:

Workers' Comp does not use a standard 270/271 transaction because eligibility is tied to a specific claim, not to a person/plan.

1. **The claim is the coverage**: A workers' comp claim must be established and accepted before coverage exists. The claim number is the primary identifier, not a subscriber ID.

2. **Eligibility verification process**:
   - Ask the patient: "Was this injury work-related?" and "Has a workers' comp claim been filed?"
   - Obtain the claim number from the patient or employer.
   - Contact the workers' comp adjuster for authorization (phone, email, or portal).
   - Confirm the claim is accepted and the specific service is authorized.
   - Get the claim's medical-only vs indemnity status.

3. **No standard 270/271**: Workers' comp carriers do not process 270/271 transactions for eligibility. Some support the 277 (Claim Status) transaction, but this is not widely used.

4. **Authorization is everything**: Most workers' comp claims require specific authorization for each service, different from health plan pre-authorization. The adjuster or case manager must approve each service.

5. **EDI alternative**: Some workers' comp carriers accept the 837 (claims) but eligibility is manual.

**Workers' Comp billing rules**:
- Deductibles, copays, and coinsurance do NOT apply -- the carrier pays 100% of the contracted/state fee schedule amount.
- Balance billing is prohibited -- providers must accept the workers' comp fee schedule.
- ICD-10 codes must indicate work-relatedness (e.g., contact with workplace object, exposure to occupational hazards).
- Claims are submitted using the workers' comp payer ID with the claim number included.
- The provider must determine cause of injury at registration to route the claim correctly.

**Workers' Comp eligibility checklist**:
- [ ] Ask patient: "Is this injury related to your job?"
- [ ] Obtain workers' comp carrier name
- [ ] Obtain claim number (from patient, employer, or payer)
- [ ] Verify claim is accepted (not denied or pending)
- [ ] Get adjuster name and contact information
- [ ] Obtain specific authorization for the planned service
- [ ] Document authorization number and date
- [ ] Note authorization limits (number of visits, body parts, duration)
- [ ] Re-verify authorization for each subsequent visit

### No-Fault Auto Insurance (PIP/MedPay) Eligibility

**How eligibility works for No-Fault**:

Like workers' comp, auto insurance medical benefits are claim-based. However, some states have partially automated systems.

**PIP (Personal Injury Protection) states**:
PIP states (FL, HI, KS, KY, MA, MI, MN, NJ, NY, ND, OR, PA, UT, and others) require auto insurers to provide medical benefits regardless of fault.

- **PIP coverage limits**: Vary by state (e.g., $10,000 in FL, $50,000 in NY, unlimited in MI).
- **PIP deductible**: Varies by policy ($250, $500, $1,000, $2,000).
- **PIP is primary**: For auto accident-related injuries, PIP pays before health insurance.
- **Billing process**:
  1. Obtain auto insurance company name, policy number, claim number, date of accident.
  2. Call the auto insurer's medical claims department to verify PIP benefits.
  3. Confirm PIP coverage limit and remaining amount.
  4. Confirm PIP deductible (if any).
  5. Ask about specific service restrictions or pre-authorization requirements.
  6. Submit claims to the auto insurer with the claim number.
  7. Once PIP is exhausted, submit to health insurance with the PIP EOB.

**MedPay (Medical Payments) states**:
All other states offer MedPay as optional coverage. It pays medical bills regardless of fault but has lower limits ($1,000-$10,000 typically).

- MedPay is primary for auto-related injuries.
- Eligibility is determined by verifying the policy is in force and coverage applies to the accident.
- No standard 270/271.

**Liability-based (tort) states**:
In tort states, the at-fault driver's insurance is responsible.

- Eligibility depends on establishing liability, which may take weeks or months.
- No standard 270/271 -- eligibility is manual through the adjuster.
- The provider may need to file a lien or wait for settlement.

**State-specific no-fault systems**:
| State | Key Rules |
|-------|-----------|
| New York | $50,000 minimum PIP; 15-day rule for payment; fee schedule applies |
| Florida | $10,000 PIP (reduced from $10K for non-emergency); 14-day treatment rule; fee schedule |
| Michigan | Unlimited PIP (for auto accidents); specific fee schedule; claim through Michigan Auto Insurance |
| New Jersey | $15,000/$250,000 PIP options; $250 deductible; choice of PIP limits |
| Pennsylvania | $5,000 minimum; opt-out option for limited tort; fee schedule |
| Texas | No PIP required (MedPay optional); liability-based primarily |
| California | No PIP; MedPay optional; liability-based |

### Key Differences Summary

| Aspect | Health Plan Eligibility | Workers' Comp / No-Fault |
|--------|------------------------|--------------------------|
| Identifier | Subscriber/member ID | Claim number + policy number |
| Coverage basis | Person-based (continuous) | Incident-based (per claim) |
| 270/271 support | Universal | NOT supported |
| Verification method | Automated electronic | Manual (phone/portal/adjuster) |
| Authorization | Health plan pre-auth rules | Per-incident adjuster approval |
| Effective period | Coverage period (1 year) | Duration of the claim |
| Cost sharing | Deductible/copay/coinsurance | None (100% covered if claim accepted) |
| Fee schedules | Contract rates or UCR | State-specific fee schedules |
| Balance billing | Limited (varies) | Prohibited |

### Agent Q&A

**Q:** A patient says their auto insurance has "PIP coverage" after a car accident. How do I verify eligibility for PIP benefits?
**A:** PIP is not verified through the standard 270/271 transaction. Process: (1) Collect auto insurance company name, policy number, claim number (if established), and date of accident. (2) Call the auto insurance company's medical claims department or use their provider portal. (3) Confirm the PIP coverage limit (e.g., $10,000, $50,000) and remaining benefits. (4) Confirm the deductible (e.g., $250, $500, $1,000). (5) Ask about service restrictions or pre-authorization requirements. (6) Document all communication with the adjuster and the claim number. (7) PIP is primary for auto-related injuries. Health insurance is secondary. After PIP is exhausted, submit to health insurance with the PIP EOB. Some health plans have "auto exclusion" clauses and will not pay ANY auto-related claims regardless of PIP exhaustion. Verify the patient's health plan covers auto-related injuries as secondary.

**Q:** A workers' comp claim was denied by the carrier. The patient still wants treatment. Can I bill their health insurance instead?
**A:** Yes, but ONLY if: (1) The workers' comp denial is final (not provisional/pending appeal). (2) You have written documentation of the denial (denial notice or EOB from the workers' comp carrier). (3) The ICD-10 code reflects the condition as non-work-related (the health insurance payer will check). If the workers' comp denial is under appeal and later reversed, the health insurance may seek reimbursement (subrogation). Process: (a) Obtain the workers' comp denial in writing. (b) Submit the claim to health insurance with the denial documentation. (c) Use a non-work-related ICD-10 code if clinically appropriate. (d) Inform the patient that if workers' comp is later approved, the health insurance may recoup payment. (e) Track the workers' comp appeal status. Critical: Do NOT submit a claim to BOTH workers' comp AND health insurance simultaneously -- this is double billing and constitutes fraud.

**Q:** A patient is injured at work and also has personal health insurance. Which insurance do I bill first?
**A:** Workers' Compensation is primary for work-related injuries. The health insurance claim will deny if the diagnosis code indicates the injury is work-related (most payers check ICD-10 codes for work-relatedness). The claim flow: (1) Verify the workers' comp claim is approved. (2) Submit all work-related charges to the workers' comp carrier with the claim number and adjuster contact. (3) If workers' comp denies the claim (injury determined not work-related), submit to health insurance with the workers' comp denial EOB. (4) If workers' comp pays partially or reaches a limit, submit the balance to health insurance as secondary. (5) Coordinate with the patient's employer and workers' comp adjuster. Critical: Never submit an auto-generated claim to health insurance for a known work-related injury -- this constitutes fraud. The provider MUST determine the cause of injury at registration and route the claim appropriately.

---

## 11. Real-World Edge Cases (Part 1)

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

## 12. 271 Response Translation Examples

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

## 13. 271 Response Codes Reference

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

## 14. Additional Real-World Edge Case Scenarios

### Newborn Coverage

**Situation**: A mother gave birth 2 weeks ago. The newborn needs a follow-up visit. The 270 for the newborn returns:

```
EB*9*IND*30*******Y~
MSG*PATIENT NOT FOUND. SUBSCRIBER NOT ON FILE. NO DEPENDENT COVERAGE.~
```

**Analysis**: EB01 = "9" means "Not Used -- Entity Not Eligible." The newborn is not yet on the insurance.

**Key rules for newborn coverage**:
- **ACA-compliant plans**: Newborns are covered for the first 30 days from birth under the mother's plan, even if not yet added as a dependent. This is retroactive to the date of birth once the newborn is added.
- **Medicaid**: Newborns are automatically covered under the mother's Medicaid for the first year of life in most states.
- **Employer plans**: Most have a 30-day window to add a newborn with retroactive coverage to the birth date.
- **Medicare**: Not applicable -- Medicare does not cover newborns (mother's coverage covers the newborn).

**How to handle billing**:
1. Ask the mother: "Have you added the baby to your insurance plan yet?"
2. If yes (within 30 days): Bill with the newborn as a dependent on the mother's policy. Use the newborn's name and DOB in the 2000D dependent loop.
3. If no (within 30 days): Ask the mother to add the newborn immediately. Coverage will be retroactive.
4. If more than 30 days: The newborn may not be covered. Check the specific plan's late enrollment rules.
5. Even if the 271 shows "Patient Not Found," submit the claim. Most payers process the claim once the newborn is added. If denied, add the newborn to the plan, then resubmit with a note that coverage is retroactive.

### Pre-Existing Condition Exclusion

**Situation**: A patient is enrolled in a grandfathered individual plan. The 271 includes:

```
EB*X*IND*AO*27*****Y~
MSG*PRE-EXISTING CONDITION EXCLUSION APPLIES. EXCLUSION PERIOD: 12 MONTHS.
MSG*EXCLUDED CONDITIONS: PREVIOUSLY TREATED MENTAL HEALTH CONDITIONS.
```

**Analysis**: EB01 = "X" means "Not Used -- Pre-Existing Condition." Pre-existing condition exclusions are:
- **Prohibited** for ACA-compliant plans (all plans issued after March 23, 2010).
- **Still allowed** on grandfathered individual plans in some cases.
- **Limited to 12 months** for most grandfathered plans.
- **Reduced by creditable coverage** (previous continuous health coverage without a 63+ day break).

**What to do**:
1. Determine if the plan is grandfathered (check plan documents).
2. If the plan is ACA-compliant, the pre-existing exclusion may be a system error -- escalate to the payer.
3. If grandfathered, check the creditable coverage period. If the patient had prior continuous coverage, the exclusion period should be reduced or eliminated.
4. Request a "Creditable Coverage" letter from the patient's prior insurer.
5. If the exclusion is valid, the denied service is not covered. Options: self-pay, appeal with proof of prior coverage.
6. File an appeal with documentation of prior creditable coverage to have the exclusion period reduced or waived.

### Benefit Limits Exhausted

**Situation**: A physical therapy patient has used 30 PT visits this year. The 271 shows:

```
EB*I*IND*76*27*0***01*Y~
MSG*PHYSICAL THERAPY: BENEFIT EXHAUSTED. VISITS REMAINING: 0.~
```

**Analysis**: EB01 = "I" (Benefit Limit). EB05 = "0" (zero remaining visits). EB06 = "1" (remaining this period). The patient has exhausted their PT benefit.

**What this means**: The plan will not pay for additional PT visits in the current benefit period. Benefits reset at the next plan year (usually January 1, or the employer's plan year).

**Options**:
1. **Appeal**: Some plans allow additional visits with medical necessity documentation (clinical notes, treatment plans, letter of medical necessity).
2. **Self-pay**: Some plans allow the patient to pay out-of-pocket. Check the plan's policy.
3. **Alternative benefit**: Check if a different benefit pool (e.g., OT) has remaining visits.
4. **Wait for reset**: If the benefit resets at the next plan year, the patient may need to wait.
5. **Secondary insurance**: Check if secondary coverage has a separate PT benefit limit.
6. **Medicare exception**: No visit limit for Medicare Part B PT, but there is a "medical necessity" threshold.

### Waiting Period

**Situation**: A patient enrolled in a new employer plan 14 days ago. The 271 shows:

```
EB*B*IND*30*27*****Y~
MSG*WAITING PERIOD IN EFFECT. ELIGIBLE FOR COVERAGE ON: 20240201.~
```

**Analysis**: EB01 = "B" means "Benefit -- Waiting Period." The patient is enrolled but coverage has not yet started.

**Key facts about waiting periods**:
- Common for new enrollments: 30/60/90 day waiting periods for new employees.
- Medicare: No waiting period for premium-free Part A. Part B General Enrollment Period has a waiting period.
- Marketplace plans: No waiting period.
- COBRA: No waiting period (continuous coverage).
- Medicaid: No waiting period (coverage begins on date of application).

**What to do**:
1. Confirm the coverage effective date from the 271 or patient.
2. If the service date is BEFORE the effective date, the patient is uninsured.
3. If the service date is AFTER the effective date, re-run eligibility after the effective date.
4. If uninsured, bill as self-pay or discuss charity care.
5. Provide a good faith estimate of charges before service.

### Dependent Not Found

**Situation**: A mother brings in a 10-year-old child. The subscriber (mother) is found in the 271 but the child returns:

```
EB*7*IND*30*******Y~
MSG*SUBSCRIBER: ACTIVE COVERAGE. NO DEPENDENT COVERAGE FOUND.~
```

**Analysis**: The subscriber has active coverage but the dependent child is not on the plan.

**Root causes**:
1. **Child never added**: The subscriber never added the child (common after birth or adoption when the 30-day window was missed).
2. **Child aged out**: The child may have turned 26 (or younger for non-student dependents).
3. **Child removed**: The subscriber removed the child during open enrollment.
4. **Wrong subscriber**: The child may be on the other parent's plan (most common in divorced families).
5. **Wrong DOB**: The child's date of birth in the 270 does not match the payer's records.

**Troubleshooting steps**:
1. Ask the parent: "Is [child's name] listed on your insurance policy?"
2. If yes, ask the parent to call the insurance company to verify the child's coverage and correct DOB.
3. If no, ask: "Is the child covered under the other parent's insurance?"
4. If recently added, check the effective date -- it may not have taken effect yet.
5. If the child was recently born, ask if the subscriber added the child within the 30-day window.
6. If added but 271 still shows no dependent, allow 48-72 hours for system update.

### Agent Q&A

**Q:** A patient's 271 shows "Subscriber: Active" but "Dependent: Not Found." The patient says their spouse and children are covered. What is the most likely cause?
**A:** The most common cause is that the dependents have NOT been added to the subscriber's plan. Simply being married or having children does not automatically make them dependents on the employer plan. The employee (subscriber) must specifically add each dependent during open enrollment or a special enrollment period. Other causes: (1) The dependent was covered under the subscriber's old plan but not the new plan. (2) The dependent turned 26 and aged out, but the subscriber did not remove them from the prior plan records -- the 271 is showing current accurate data. (3) The dependent age/DOB in the 270 does not match payer records -- transposed digits are common. (4) The relationship code is wrong ("Child" vs "Spouse" vs "Other"). (5) The 2000D loop structure is wrong in the 270 -- the subscriber info must be in the subscriber loop (2000C) and the dependent info in the dependent loop (2000D). Fix: Ask the subscriber to verify their dependents with the insurance company directly, then re-run eligibility with corrected data.

**Q:** A newborn is 25 days old. The parent has not yet added the newborn to the insurance plan. The 271 shows "Patient Not Found." Can the newborn's visit be billed?
**A:** Yes, in most cases. Under the ACA and most employer-sponsored plans, newborns are covered for the first 30 days from birth under the mother's plan, even if not yet added as a dependent. This is "retroactive coverage" -- once the newborn is added to the plan, coverage is effective back to the date of birth. Process: (1) Provide the service and document it. (2) Ask the parent to add the newborn to the plan immediately. (3) Once the newborn is added (within the 30-day window), submit the claim. (4) Use the newborn's name and DOB as the dependent, with the mother as the subscriber. (5) Include a note that the newborn is within the 30-day retroactive coverage period. (6) If the claim is denied for "Patient Not Found," resubmit after the newborn is added to the plan. (7) If more than 30 days have passed, check the plan's late enrollment rules (some allow 60 days for certain life events).

**Q:** A grandfathered plan returns EB01="X" for a service. The patient had prior coverage with no gap. Can the exclusion be overridden?
**A:** Yes, if the patient has creditable coverage from a prior plan without a break of 63+ days. Process: (1) Obtain a "Certificate of Creditable Coverage" from the patient's prior insurance company. (2) Submit the certificate to the current plan with an appeal requesting reduction or elimination of the pre-existing exclusion period. (3) The plan must credit the patient's prior continuous coverage against the 12-month exclusion period. (4) If the patient had 6 months of prior coverage, the exclusion period is reduced to 6 months. (5) If the patient had 12+ months of prior continuous coverage, the exclusion is eliminated entirely. (6) The Health Insurance Portability and Accountability Act (HIPAA) gives patients the right to creditable coverage credit. (7) If the plan refuses to honor creditable coverage, file a complaint with the state insurance department or the Department of Labor (for ERISA plans). (8) Note: The HIPAA creditable coverage rules apply to group health plans and grandfathered individual plans. ACA-compliant plans cannot impose pre-existing condition exclusions at all.

**Q:** A patient's 271 shows "Visits Remaining: 0" for physical therapy. The benefit limit is 20 per year. The patient used 18 visits in one week because they were in an intensive rehab program. Is this correct?
**A:** Yes, this is correct. Visit limits count each visit (defined as each date of service or each session) regardless of how close together they occur. An intensive rehab program with daily visits for 2.5 weeks would consume 18 visits. The patient does not get more visits because they used them quickly. However: (1) Check if the plan has a "rehab" or "intensive therapy" exception for higher limits. (2) Check if the visits are counted as individual visits or as "treatment days" or "episodes of care." (3) Some plans have separate limits for acute therapy (post-surgery) vs maintenance therapy. (4) Appeal for additional visits with medical necessity documentation if the therapy is still needed. (5) If the patient has both PT and OT benefits, check if OT still has remaining visits that could be used (if clinically appropriate). (6) Some plans allow "benefit extension" requests for catastrophic or intensive therapy needs.

---

## 15. Workflow Integration & Best Practices

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

## 16. Common Denials Related to Eligibility

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

## 17. Training Q&A Bank

This expanded Q&A bank covers all major eligibility and benefits topics for agent training. Questions are organized by category.

### Core Knowledge Q&A (Part 1)

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

### Core Knowledge Q&A (Part 2)

**Q:** What does the "D8" date format mean in a 270/271 transaction?
**A:** "D8" is the X12 date format qualifier for "CCYYMMDD" -- a specific 8-digit format representing Century, Year, Month, and Day. For example, June 10, 2024 is represented as "20240610." This is the ONLY format allowed in HIPAA-compliant X12 transactions for dates with the D8 qualifier. Do not use slashes, hyphens, or spaces. Do not use MM/DD/YYYY or DD/MM/YYYY. Other date qualifiers include: "RD8" (date range, e.g., 20240101-20241231), "DTP" (date/time period format), and "TM" (time format, e.g., 1430 for 2:30 PM).

**Q:** What is the purpose of the HL (Hierarchical Level) segment in a 270 transaction?
**A:** The HL segment defines the nested loop structure of the 270 transaction. Each HL segment represents one "level" in the hierarchy: HL03="20" (Information Source = Payer), HL03="21" (Information Receiver = Provider), HL03="22" (Subscriber), HL03="23" (Dependent). HL02 points to the parent HL by its HL01 number. HL04 indicates whether the level has child levels (0 = no, 1 = yes). The hierarchy must be properly nested. An incorrect HL structure (e.g., putting the dependent loop inside the subscriber loop incorrectly) will cause the 270 to be rejected by the clearinghouse.

**Q:** What is the difference between the "EQ*30" inquiry and an inquiry with a specific service type code?
**A:** EQ*30 (Health Benefit Plan Coverage) is a general inquiry asking the payer "tell me about the patient's overall coverage." The response typically includes: coverage status, plan name, coverage dates, network type, deductible, OOP max, and general cost-sharing info. A specific service type inquiry (e.g., EQ*76 for Physical Therapy) asks the payer "tell me about the patient's PT-specific benefits." The response includes PT-specific visit limits, PT coinsurance/copay, PT pre-authorization requirements, and PT-specific exclusions. General inquiry is a good starting point but may NOT return service-specific details like visit limits or therapy-specific cost-sharing. For comprehensive verification, send the general EQ*30 PLUS specific EQ codes for the services the patient is scheduled to receive.

**Q:** A 271 response shows EB01="C" for coverage level information. What EB01 code would indicate "copay" vs "coinsurance" vs "deductible"?
**A:** (1) EB01 = "F" means copay (the patient pays a fixed dollar amount per service). (2) EB01 = "E" means coinsurance (the patient pays a percentage). (3) EB01 = "D" means deductible (the patient pays 100% of allowed amount for covered services up to the deductible limit). (4) EB01 = "G" means out-of-pocket maximum (the total amount the patient will pay per year). Each of these codes appears in a separate EB segment. For example, a plan with a $30 copay for office visits would have `EB*F*IND*98*27*30**01*Y~`, and a plan with 20% coinsurance would have `EB*E*IND*1*27***20*01*Y~`. Look for these specific codes when parsing benefits, not just EB01="C" (which is generic coverage level info).

**Q:** What is the correct way to format a patient's middle name in a 270 transaction?
**A:** The 270 NM1 segment contains: NM103 (Last Name), NM104 (First Name), and NM105 (Middle Name/Initial). Use the middle INITIAL (one character) in NM105 if the insurance card shows a middle initial. Use the FULL middle name (spelled out) in NM105 only if the insurance company's database has the full middle name. When in doubt: (1) Use the name exactly as shown on the insurance card. (2) If the card shows "JOHN A SMITH," use NM103="SMITH", NM104="JOHN", NM105="A". (3) If the card shows "JOHN SMITH" with no middle name, leave NM105 blank. (4) Do NOT include the middle initial in the subscriber ID (NM109). (5) The name matching rules vary by payer -- some do a strict "exact match" on all three name fields, others only match last name + first initial.

### Scenario Q&A (Part 2)

**Q:** A self-pay patient arrives and says they have insurance but forgot their card. Can I run eligibility with just their SSN?
**A:** Some clearinghouses offer an "SSN-based eligibility" service that can look up coverage using the patient's Social Security Number and DOB. However: (1) This is NOT the standard 270/271 transaction -- it is a value-added service from the clearinghouse. (2) Not all clearinghouses offer this. (3) The SSN lookup success rate varies (50-80% depending on the clearinghouse/payer coverage). (4) You must have the patient's consent to use their SSN for eligibility lookup (HIPAA allows this for payment/healthcare operations but best practice is to document the patient's consent). (5) If the SSN lookup fails, you can try other methods: call the payer's provider services line, ask the patient to call their insurance for their member ID, or check if the payer has a patient portal the patient can access. (6) If all methods fail, treat as self-pay and follow up when the patient provides their insurance information. (7) Under the No Surprises Act, you must provide a good faith estimate before service.

**Q:** A patient has Medicare Part A and Part B plus a Medigap (Medicare Supplement) plan. How does eligibility work for these two coverages?
**A:** Medicare and Medigap are verified separately: (1) Run a 270 to the Medicare MAC (e.g., Noridian, WPS) using the patient's MBI. The 271 returns: Part A coverage status, Part B coverage status, Part A deductible (per benefit period), Part B deductible ($240/year), Part B coinsurance (20%), and any MSP (Medicare Secondary Payer) information. (2) Medigap plans do NOT have a standard 270/271 eligibility check. Medigap eligibility is part of the Medicare "crossover" process -- when a claim is submitted to Medicare, Medicare automatically forwards the claim to the Medigap plan. (3) You do NOT need to separately verify Medigap eligibility for most services. (4) The Medigap plan's coverage is determined by plan type (Plan F, G, N, etc.) and is standard -- no visit limits or pre-auth requirements for most services. (5) Exception: Medigap Plan N requires copays ($20 office visit, $50 ER) that are NOT covered by Medicare. You must bill the patient for these copays. (6) For Medigap verification: ask the patient "Do you have a Medicare supplement plan?" and note the plan type. Submit claims to Medicare; the crossover handles the rest.

**Q:** A patient has a 271 response showing "Copay: $25 PCP Visit, $50 Specialist Visit." The patient saw the PCP for a routine physical and also complained of knee pain. What is the correct patient collection?
**A:** This is a common scenario where the preventive component (routine physical) and the problem-oriented component (knee pain) are billed separately. For the preventive component (CPT 99397 or G0439): ACA-compliant plans cover this at 100% with no cost sharing -- the $25 copay does NOT apply. For the problem-oriented component (CPT 99213 with knee pain diagnosis): The $25 copay applies. Some practices collect the $25 copay at check-in and then write off the preventive portion after the insurance processes. Others collect nothing upfront and bill the patient after the EOB confirms the copay. Best practice: Collect the $25 copay at check-in for the problem-oriented portion, document that the preventive portion should be $0, and adjust after adjudication. Some payers apply the full visit to the preventive code and do not separately process the problem-oriented component -- this can result in no copay being due. Always review the EOB before writing off or billing additional amounts.

### Denial Prevention Q&A

**Q:** What is the most common eligibility-related denial and how do I prevent it?
**A:** The most common eligibility-related denial is CO 22 (Coordination of Benefits) -- "This care may be covered by another payer per coordination of benefits." This occurs when: (1) A claim is submitted to the wrong payer. (2) The patient has multiple coverages and the payer's COB records indicate the claim should go to another plan first. (3) The patient has Medicare but the provider billed a commercial plan as primary incorrectly. (4) The patient has COBRA coverage that should be secondary to a new employer plan. Prevention: (a) At every registration, ask the patient specifically: "Do you have any other health insurance coverage, including through a spouse, employer, Medicare, Medicaid, COBRA, or VA?" (b) Run eligibility to check for COB indicators (EB01="R" or "W" in the 271). (c) Determine correct billing order using COB rules. (d) Submit to the correct primary payer first. (e) If CO 22 appears after submission, verify COB order with both payers before resubmitting.

**Q:** A claim was denied with CO 16 (Claim lacks information for adjudication). The 270 showed the patient as eligible. How are these related?
**A:** CO 16 means the claim is missing required information for the payer to process it (e.g., missing subscriber ID, missing referring provider, missing authorization number). While the eligibility check confirmed the patient's coverage was active, it does not validate that the CLAIM contains all required data. The 270 confirms "is the patient covered?" but the claim needs additional data like: correct CPT/HCPCS codes, correct ICD-10 codes, place of service, referring provider NPI (if applicable), authorization number (if required), and rendering provider NPI. Prevention: Use the eligibility data (subscriber ID, payer ID) to populate the claim correctly. Run claim validation/scrubbing before submission (most clearinghouses offer this). Verify that the claim matches what the eligibility check showed (same subscriber ID, same patient, same coverage dates).

**Q:** A patient's 271 shows "Active Coverage" with a $30 copay. The claim processes with a $500 patient responsibility because the deductible was not yet met. Why didn't the 271 show the deductible?
**A:** Several possibilities: (1) The 271 showed the copay for a specific service type (e.g., EB03="98" for office visit with copay) but did not show the deductible information because the deductible was in a different EB segment (EB03="30" for general coverage with EB01="D" for deductible). The 271 parsing may have missed the deductible segment. (2) The service type queried (e.g., EQ*33 for PCP visit) may be a "copay-only" service under some plan designs, but the patient actually received a service that falls under a different category (e.g., injection, procedure) that is subject to the deductible. (3) The 271 was run without specific EQ codes and returned only general information, which included the copay but not the deductible application rules. (4) The payer's 271 does not clearly indicate which services are subject to deductible vs copay-only. Best practice: Always check for deductible information in ALL EB segments, not just the service-type-specific ones. Look for EB01="D" or EB01="B" (with EB13="D") across ALL EB segments. If the deductible is present but the copay is also present, call the payer to ask: "Does the copay apply before or after the deductible is met?" Document the answer.

**Q:** An 835 ERA (remittance advice) shows a denial as patient responsibility (PR) for a service that was pre-verified with a 271. Can the provider bill the patient?
**A:** It depends on WHY the service was denied: (1) If the denial is for a non-covered service (e.g., experimental, excluded): Yes, the provider can bill the patient IF they were informed in advance and signed an Advanced Beneficiary Notice or waiver. (2) If the denial is for a benefit limit exceeded (e.g., "visits exhausted"): Depends on state law and the provider's contract. Some plans contractually prohibit balance billing for services beyond the benefit limit. Most providers must write off benefit-exhausted services. (3) If the denial is for lack of prior authorization: The provider CANNOT bill the patient unless the patient was informed and signed a waiver. The provider is responsible for obtaining auth. (4) If the denial is due to a data error (wrong ID, wrong payer): Correct and resubmit. (5) If the denial is for timely filing: The provider cannot bill the patient unless the patient caused the delay. In all cases: The 271 provides benefit ESTIMATES, not guarantees. The claim's adjudication determines the actual patient responsibility. If the 271 and the claim adjudication differ, the claim adjudication controls. The provider should not bill the patient for amounts they were not expecting without careful review.

### Medicare-Specific Q&A

**Q:** How does Medicare Part A deductible work in the context of 271 eligibility?
**A:** Medicare Part A has a per-benefit-period deductible (not annual). A "benefit period" starts when the patient is admitted as an inpatient and ends after 60 consecutive days out of the hospital or SNF. In 2024, the Part A deductible is $1,632 per benefit period. The 271 from the MAC returns: (1) DTP*356 (Coverage Effective Date) showing Part A entitlement start date. (2) EB segment with EB01="D" (Deductible) showing the Part A deductible amount as remaining or met. (3) The 271 may show days remaining in the current benefit period. (4) Lifetime reserve days (60 per lifetime) may be shown if the patient is in a long hospital stay. Important: The 271 does NOT tell you how many benefit periods the patient has used this year, nor does it show the current benefit period status (whether the patient is currently in a benefit period). You must get this information from the patient's Medicare Summary Notice (MSN) or by calling 1-800-MEDICARE.

**Q:** A Medicare patient's 271 shows "Part A: Active" and "Part B: Active." A claim for a home health visit is denied. Why?
**A:** Home health services are covered under BOTH Part A and Part B depending on the circumstances: (1) Part A covers home health after a qualifying inpatient stay of 3+ days (the patient must be "homebound" and need skilled nursing or therapy). (2) Part B covers home health WITHOUT a prior inpatient stay. However: The 271's "Active" status for Part A and Part B does not tell you if the patient meets the CLINICAL criteria for home health coverage (homebound status, need for skilled services, care plan established by physician). The denial is likely for one of these reasons: (1) The patient is not "homebound" as defined by Medicare. (2) The services do not meet the "skilled care" threshold. (3) The plan of care was not established or certified by a physician. (4) The provider is not a certified Medicare home health agency. (5) The claim was submitted incorrectly (wrong place of service, wrong provider type). The 271 cannot predict clinical criteria denials -- only claim-level data can confirm coverage.

**Q:** A Medicare Advantage (Part C) patient's 271 shows "Active Coverage" but the claim denies. The MA plan says "service is not covered under Medicare." What happened?
**A:** Medicare Advantage plans must cover all Medicare Part A and Part B services (the "Medicare benefit package"). However, MA plans can apply "medical necessity" criteria that may be more restrictive than Original Medicare. When an MA plan denies a service: (1) The plan must follow Medicare coverage rules (NCDs and some LCDs). (2) The plan can have its own prior authorization requirements. (3) The plan can have its own network restrictions. (4) If the service is denied as "not covered under Medicare," the patient can appeal through the MA plan's internal appeals process, then to an Independent Review Entity (IRE). (5) The provider should check: "Was the service pre-authorized?" and "Is the provider in-network?" and "Does the plan cover this service under their specific benefit package?" (6) If the MA plan denies a service that Original Medicare would cover, the patient has appeal rights. (7) Some MA plans market additional benefits (dental, vision, hearing) that Original Medicare does NOT cover -- these are plan-specific and may have their own coverage rules, limits, and exclusions.

### Batch Processing Q&A

**Q:** My batch eligibility file is scheduled to run at midnight. A patient checks in at 8 AM before the batch results are back. Can I treat the patient?
**A:** Yes, but you need to use real-time (not batch) eligibility for this patient. The batch results for this patient may not be available until later in the day (or the next batch cycle). Best practice: (1) Run a real-time 270 for same-day patients at check-in, regardless of batch schedules. (2) Use batch eligibility for FUTURE appointments (next day or next week). (3) For same-day patients: check in, run real-time eligibility, review results, proceed with service. (4) For patients who were in a batch that completed: if the batch results show active coverage, the eligibility is valid as of last night -- verify no changes since then by asking the patient "Has your insurance changed since your last visit?" (5) For patients whose batch results show "Not Found" or "Terminated": run a real-time verification to confirm the batch result (batch may have had data issues). (6) Never rely solely on batch results for same-day patients. Real-time always takes precedence.

**Q:** A batch eligibility response shows "Not Found" for 50% of my patients. The clearinghouse says the batch was processed successfully. What could be wrong?
**A:** A 50% not-found rate is extremely high. Likely causes: (1) Wrong payer ID used for the entire batch. If you used the commercial payer ID for all patients but some have Medicare or Medicaid, those will return "Not Found." (2) Batch file format error causing all 270s to be rejected even though the clearinghouse says "processed." Check the 999/997 functional acknowledgment -- there may be AK5 rejection codes. (3) Wrong trading partner agreement: The batch file's ISA06 (Sender ID) may not match your clearinghouse configuration, causing all transactions to be invalidated. (4) Data mapping error: Your system may have populated the batch file with the wrong field (e.g., patient DOB in the subscriber ID field). (5) Test mode: The batch may have been sent to the testing environment instead of production. Solutions: (a) Run real-time 270 tests for a sample of the "Not Found" patients. (b) If real-time works, the batch format is wrong. (c) Check the 997/999 acknowledgment for error details. (d) Send a small test batch (5-10 patients) with known-good patient data to isolate the issue. (e) Contact the clearinghouse's EDI support team with your batch file and the acknowledgment for analysis.

### Clearinghouse Q&A

**Q:** Can I switch clearinghouses without disrupting my eligibility verification workflow?
**A:** Yes, but with careful planning: (1) Payer IDs are clearinghouse-specific. When you switch, you must update ALL payer IDs in your system to the new clearinghouse's IDs. (2) The 270/271 transaction format is the same (X12 5010), but the connectivity method may differ (SFTP vs HTTPS, authentication method). (3) Test the new clearinghouse with a subset of payers before switching all practice management system configurations. (4) Run both clearinghouses in parallel for 2-4 weeks to verify the new clearinghouse's response accuracy matches the old one. (5) Update your patient registration/check-in workflows to use the new clearinghouse's interface. (6) Verify batch eligibility with the new clearinghouse for a test batch before switching production. (7) Notify your PMS vendor of the clearinghouse change (they may need to update EDI connection settings). (8) Allow 30-60 days for the full transition. (9) Keep the old clearinghouse active for claims processing during the transition to avoid disruptions. (10) Monitor denial rates closely for 90 days after the switch -- clearinghouse routing changes can cause unexpected denials.

**Q:** Why does the same patient's 271 response look different when queried through Change Healthcare vs Availity?
**A:** The 271 response format should be the same (both use X12 5010 271), but the PAYER ID and ROUTING may differ: (1) If you use the wrong payer ID in each clearinghouse, the 270 may be routed to different payer systems (e.g., Change Healthcare routes to UHC's commercial system while Availity routes to UHC's self-funded system). (2) Different payer systems may have different levels of detail in their 271 responses. (3) The clearinghouse may add, modify, or remove segments in the 271 during translation (value-added services). For example, Change Healthcare may strip out certain payer-specific segments while Availity passes them through. (4) The time of day matters -- 271 responses during peak hours may be truncated or abbreviated. (5) The EQ codes sent may differ between the two systems (one system may send EQ*30 while the other sends multiple specific EQ codes). Best practice: When comparing 271 responses between clearinghouses, use the SAME 270 inquiry (same patient, same EQ codes, same service date, same time) for both. If the responses differ, the clearinghouse or payer routing is the cause.

### Special Situations Q&A

**Q:** A patient is incarcerated. How does eligibility verification work?
**A:** For incarcerated patients: (1) Medicare: Medicare does NOT pay for services provided during incarceration (except for inpatient care in specific circumstances like 3+ day inpatient stays in a hospital). The Medicare 271 will show active coverage but claims will deny. (2) Medicaid: Medicaid is SUSPENDED (not terminated) during incarceration. The 271 will show "No Active Coverage" or "Suspended." Claims for services during incarceration will deny. The state must provide medically necessary care at the correctional facility's expense. (3) Commercial plans: Most commercial plans terminate or suspend coverage during incarceration. Check the plan's specific policy. (4) The correctional facility is financially responsible for all medical care during incarceration. Bill the correctional facility, not the insurance. (5) If the patient is released, eligibility resumes (Medicaid reinstatement may take time). (6) For care provided after release but billed during incarceration: the coverage may be active if the service date is after the release date. (7) The 271 cannot tell you about incarceration status -- you must ask the patient or the facility. (8) Some correctional facilities require a specific authorization or PO (purchase order) number before treatment.

**Q:** A patient requests eligibility verification for a service they plan to receive out-of-state. How do I handle this?
**A:** Out-of-state eligibility depends on the plan type: (1) **PPO/EPO**: Most PPO plans have out-of-area coverage through their national network (e.g., BlueCard for BCBS). The patient can use a PPO plan out-of-state with in-network or reduced benefits. (2) **HMO**: HMO plans generally do NOT cover out-of-network non-emergency care. The patient would need a referral from their PCP to see an out-of-state specialist (rare). (3) **Medicare**: Original Medicare covers care in any state from Medicare-enrolled providers. Medicare Advantage plans may only cover emergencies out-of-state. (4) **Medicaid**: Medicaid does NOT cross state lines except for emergencies. The patient needs coverage in the state where services are performed. For out-of-state checks: (a) Use the BlueCard eligibility ID (for BCBS plans) if the patient is a BCBS member out-of-state. (b) For other plans, call the payer and ask: "What are the out-of-area benefits for this patient?" (c) The 271 returned from a local (in-state) payer may not show out-of-state benefits accurately. (d) For Medicare patients: all states are covered as long as the provider accepts Medicare assignment. Run 271 using the Medicare MAC for the patient's HOME state, not the service state.

**Q:** A patient is deceased. How do I handle eligibility and billing?
**A:** When a patient dies: (1) Coverage generally ends on the date of death (some plans continue coverage to the end of the month). (2) The 271 may show "Active Coverage" for a brief period after death (system lag). (3) Claims for services rendered BEFORE death should be processed normally. (4) Claims for services rendered AFTER death will deny as "Patient Deceased." (5) For services before death: bill the estate. The estate (executor/administrator) is financially responsible. (6) For Medicare: the MBI becomes invalid after death. Claims submitted with the deceased MBI will reject. (7) For the estate: coordinate with the executor/administrator for payment. (8) Some states have streamlined probate processes for small medical estates. (9) The provider can write off the balance as a bad debt if the estate cannot pay (with proper documentation). (10) Do NOT bill the surviving spouse for the deceased patient's debt unless the spouse co-signed as guarantor or state law (community property) makes the spouse responsible.

### Advanced 271 Parsing Q&A

**Q:** A 271 response has multiple EB segments with EB03="98" (Professional Visit). One shows a $30 copay and another shows 20% coinsurance. Which one applies?
**A:** When a 271 has multiple EB segments for the same service type, they represent DIFFERENT conditions. Look at EB09 (in/out of network): one EB segment may show in-network benefits (EB09="Y" = $30 copay) while another shows out-of-network benefits (EB09="N" = 20% coinsurance). Also check EB02 (coverage level): one may show IND (individual) and another FAM (family) benefits. Also check EB01: "F" (copay) vs "E" (coinsurance). In many PPO plans, the in-network benefit is a copay (e.g., $30 for office visits) while the out-of-network benefit is coinsurance (e.g., 40% after a separate OON deductible). The patient's cost depends on whether the provider is in-network. If both benefits show the same EB09 (both "Y" for in-network), call the payer to clarify -- it may be that the copay applies only to certain visit types (e.g., preventive has no copay, problem-oriented has copay) or the 271 is showing both possible benefits (new plan design with both copay and coinsurance).

**Q:** How do I determine if a benefit limit is annual or lifetime from the 271?
**A:** Check EB06 (Time Period Qualifier) in the EB segment with EB01="I" (Benefit Limit). The qualifier tells you the period: "1" = Remaining (current period) -- typically annual, "2" = Current Year (calendar year) -- annual, "3" = Current Month, "6" = Lifetime, "7" = Year to Date, "8" = Remaining Lifetime -- lifetime limit is remaining, "22" = Service Year -- annual by plan year, "23" = Calendar Year -- annual. If EB06 = "6" or "8", the limit is a LIFETIME limit -- it will NOT reset. If EB06 = "1", "2", "22", or "23", the limit is an ANNUAL limit -- it resets at the next plan year. Example: `EB*I*IND*33*27*12***06*Y~` means "Chiropractic: 12 visits, LIFETIME limit." `EB*I*IND*33*27*12***01*Y~` means "Chiropractic: 12 visits remaining, ANNUAL limit (resets next year)." This distinction is critical for long-term treatment planning.

**Q:** A 271 response shows "Deductible remaining: $4,000" AND "OOP Max: $7,000." The patient owes $500 for a service. Is this $500 applied to the deductible or the OOP max?
**A:** In a standard plan design: (1) The $500 is first applied to the DEDUCTIBLE. (2) Once the deductible is met ($4,000 total), remaining charges are billed at the coinsurance rate. (3) The coinsurance amount + deductible paid count toward the OOP max. (4) In this example: The patient has $3,500 remaining on the deductible AFTER this $500. (5) If the patient had already met their deductible, the $500 would be billed at the coinsurance rate (e.g., 20% = $100 patient responsibility, $400 plan pays). (6) The 271 does NOT explicitly tell you this ordering -- you need to know the plan design. (7) In general: deductible first, then coinsurance, until OOP max is reached. Copays may apply before or after deductible depending on the plan. (8) The 271 shows the REMAINING amounts for deductible AND OOP max. After a $500 service (with deductible not yet met), the deductible remaining should decrease by $500, while the OOP max remaining decreases by $500 (if the deductible applies to OOP max, which it always does in standard plans).

**Q:** A 271 response includes an MSG segment that says "COVERAGE INFORMATION" with no additional detail. Is there more data available?
**A:** A generic MSG like "COVERAGE INFORMATION" means the payer's 271 implementation is minimal. This is common with: (1) Small/regional payers with limited EDI capabilities. (2) Medicaid plans with basic 271 implementations. (3) Self-funded plans where the employer's benefit data is not fully integrated into the payer's 271 system. (4) Payers whose 271 focus is eligibility (active/inactive) but not detailed benefits. When the 271 is vague: (a) Check all EB segments carefully -- the structured data (EB01, EB08, EB09) often contains more detail than the MSG. (b) Resend the 270 with specific EQ codes (EQ*33, EQ*98, EQ*86, EQ*50) to try to get more detailed responses. (c) Use the payer's provider portal (web-based) for manual benefit lookup. (d) Call the payer's provider services line. (e) For self-funded plans, ask for the employer's Summary Plan Description (SPD) or Summary of Benefits and Coverage (SBC). (f) Document: "271 response from [payer] returned only basic eligibility information. Manual verification performed via [method]."

### End-to-End Workflow Q&A

**Q:** Walk me through the complete eligibility verification workflow for a new patient scheduled for an MRI next week.
**A:** Complete workflow: (1) At scheduling (1-2 weeks out): Collect insurance card, subscriber ID, DOB, group number. Run a 270 with EQ*30 (general coverage) and EQ*50 (outpatient hospital) and EQ*48 (inpatient hospital) if applicable. (2) Review 271: Confirm active coverage (EB01="1"). Check deductible remaining (EB01="D" or "B", EB08). Check OOP max (EB01="G", EB08). Check coinsurance/copay for the service. Check if prior authorization is required (EB01="M" or "S"). (3) If prior auth is indicated: Initiate the prior authorization request. Provide clinical documentation (diagnosis, reason for MRI, relevant history). Most insurers require auth for advanced imaging (MRI, CT, PET). (4) Day before service: Run another 270 (batch or real-time) to confirm coverage hasn't changed. Verify prior auth status (check the REF segment for authorization number). (5) Day of service: Run real-time 270 at check-in. Confirm coverage is still active. Verify the correct copay/coinsurance. Collect estimated patient responsibility. (6) After service: Submit claim with the correct diagnosis and procedure codes. Include authorization number if required. (7) Post-service: Monitor claim status. If denied, appeal with the eligibility verification results (show the 271 confirming coverage). Track patient payments and EOB. This workflow prevents the most common MRI-related denials: not covered (if eligibility failed), no auth (if not obtained), and patient not found (if data was stale).

**Q:** A provider office does not have integrated eligibility verification software. They do all eligibility checks by phone. What is the minimum data they should document?
**A:** For manual (phone) eligibility verification, document: (1) Date and time of call. (2) Payer name and representative name/ID (if provided). (3) Patient name and subscriber ID verified. (4) Coverage status (Active/Inactive/Terminated/Pending). (5) Coverage effective date and termination date. (6) Copay amount for planned service (PCP visit, specialist, etc.). (7) Deductible remaining (individual and family). (8) Coinsurance percentage (in-network and out-of-network). (9) Out-of-pocket maximum remaining. (10) Visit limits remaining (if applicable, e.g., PT, chiropractic). (11) Prior authorization requirements. (12) Network participation confirmed (in-network or out-of-network). (13) COB information (any other coverage on file). (14) Any exclusions or special notes. Example documentation: "Called BCBS IL on 06/10/2024 at 10:30 AM. Rep: Sarah (ID 54321). Subscriber John Smith (ID ABC123456789) has active coverage through 12/31/2024. Office visit copay: $30 PCP, $50 Specialist. Deductible: $1,500 remaining. Coinsurance: 20% after deductible. OOP max: $6,000. No auth required for office visits. In-network confirmed." This documentation protects the provider in case of a dispute and supports appeals if eligibility was verified but the claim later denies.

## 18. 270/271 Testing and Troubleshooting

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

## 19. Compliance and Regulatory Notes

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

## 20. Glossary

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

## 21. Summary: Key Takeaways for LLM Agent

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