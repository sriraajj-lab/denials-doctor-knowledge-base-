# X12 EDI: Electronic Data Interchange for Healthcare

## Overview

X12 EDI (Electronic Data Interchange) is the ANSI-accredited standard for electronic business transactions, including healthcare claims processing. In the US healthcare revenue cycle, X12 transactions are the backbone of all payer-provider electronic communication — claims, payments, eligibility checks, claim status inquiries, and prior authorizations.

Unlike FHIR (designed for clinical data exchange via RESTful APIs) and HL7 v2 (designed for intra-institutional messaging), X12 EDI is specifically designed for batch-oriented business transactions between trading partners. HIPAA mandates the use of X12 standards for all electronic healthcare transactions, making X12 understanding essential for revenue cycle management.

For Denials Doctor, X12 EDI is critical because the most actionable denial data arrives via X12 835 (payment/remittance advice) and 277 (claim status) transactions.

---

## X12 EDI Envelope Structure

X12 messages are organized in a hierarchical envelope structure with three nesting levels:

```
ISA (Interchange Control Header)        — Envelope: one interchange = one transmission
  GS (Functional Group Header)           — Group: one group = one transaction type
    ST (Transaction Set Header)          — Transaction: one transaction = one business document
      HL (Hierarchical Loops)            — Data segments organized in nested loops
      ... business data segments ...
    SE (Transaction Set Trailer)
  GE (Functional Group Trailer)
IEA (Interchange Control Trailer)
```

Each level has a header (opens) and trailer (closes) with matching control numbers for validation.

---

### ISA Segment — Interchange Control Header

The ISA segment begins every X12 transmission. It identifies the sender, receiver, and transmission metadata.

| Position | Element | Description | Example |
|---|---|---|---|
| ISA01 | I01 | Authorization Info Qualifier | `00` (no auth info), `01` (password) |
| ISA02 | I02 | Authorization Information | (blank or password) |
| ISA03 | I03 | Security Info Qualifier | `00` (no security), `01` (password) |
| ISA04 | I04 | Security Information | (blank or password) |
| ISA05 | I05 | Interchange Sender ID Qualifier | `ZZ` (mutually defined), `01` (DUNS) |
| ISA06 | I06 | Interchange Sender ID | `123456789` (typically TIN or NPI) |
| ISA07 | I05 | Interchange Receiver ID Qualifier | `ZZ` |
| ISA08 | I07 | Interchange Receiver ID | `PAYER-ID` (clearinghouse or payer ID) |
| ISA09 | I08 | Interchange Date | `250203` (YYMMDD) |
| ISA10 | I09 | Interchange Time | `1030` (HHMM) |
| ISA11 | I10 | Repetition Separator | `^` or `U` |
| ISA12 | I11 | Interchange Control Version Number | `00501` (version 5010) |
| ISA13 | I12 | Interchange Control Number | `000000001` (must match IEA02) |
| ISA14 | I13 | Acknowledgment Requested | `0` (no), `1` (interchange ACK requested) |
| ISA15 | I14 | Usage Indicator | `P` (production), `T` (test) |
| ISA16 | I15 | Component Element Separator | `:` |

### GS Segment — Functional Group Header

The GS segment opens a functional group — a collection of similar transaction sets.

| Position | Element | Description | Example |
|---|---|---|---|
| GS01 | 479 | Functional Identifier Code | `HC` (healthcare claims) |
| GS02 | 142 | Application Sender's Code | `PROVIDER-TIN` |
| GS03 | 124 | Application Receiver's Code | `PAYER-ID` |
| GS04 | 373 | Date | `20250203` (CCYYMMDD) |
| GS05 | 337 | Time | `1030` (HHMM) |
| GS06 | 28 | Group Control Number | `1` (must match GE02) |
| GS07 | 455 | Responsible Agency Code | `X` (Accredited Standards Committee X12) |
| GS08 | 480 | Version/Release/Industry ID | `005010X222` (5010, Health Care Claim) |

### ST Segment — Transaction Set Header

The ST segment opens each individual transaction:

```
ST*837*0001~    — Transaction set 837, control number 0001
```

| Position | Element | Description |
|---|---|---|
| ST01 | 143 | Transaction Set Identifier Code (e.g., 837, 835, 270) |
| ST02 | 329 | Transaction Set Control Number (must match SE02) |

### SE Segment — Transaction Set Trailer

```
SE*45*0001~    — 45 segments in this transaction (including ST and SE), control number 0001
```

---

## HIPAA-Compliant X12 Transaction Types

### 270/271 — Eligibility/Benefit Inquiry and Response

**270 (Eligibility Inquiry):** Sent by provider to ask about a patient's insurance coverage and benefits.

```
ST*270*0001~
BHT*0022*13*REF-001*20250203*1030~
HL*1**20*1~
NM1*PR*2*BLUE CROSS BLUE SHIELD*****PI*PAYER-ID~
HL*2*1*21*1~
NM1*1P*1*DOE*JANE****XX*1234567893~
HL*3*2*22*0~
TRN*1*TRACE-001~
NM1*IL*1*SMITH*JOHN****MI*MEMBER-ID~
DMG*D8*19750315*M~
DTP*291*D8*20250203~
EQ*30~
SE*11*0001~
```

- `EQ*30` = requesting health benefit plan coverage
- `DMG` = patient demographic data (DOB, gender)
- `DTP*291` = service date for benefits query
- `NM1*IL` = insured person information

**271 (Eligibility Response):** Payer's response with coverage and benefit details.

```
ST*271*0002~
BHT*0022*11*RESP-001*20250203*1035~
HL*1**20*1~
NM1*PR*2*BLUE CROSS BLUE SHIELD*****PI*PAYER-ID~
HL*2*1*21*1~
NM1*1P*1*DOE*JANE****XX*1234567893~
HL*3*2*22*0~
TRN*2*TRACE-001~
NM1*IL*1*SMITH*JOHN****MI*MEMBER-ID~
EB*1**30***^^^COPAY***10.00~    — $10 copay
EB*1**30***^^^COINS***20.00~    — 20% coinsurance  
EB*1**30***^^^DED***500.00~     — $500 deductible
EB*3**30~                        — Inactive coverage (if applicable)
SE*14*0002~
```

- `EB*1` = active coverage, `EB*3` = inactive, `EB*6` = no coverage
- `EB` segments specify benefit details: copay, coinsurance, deductible, out-of-pocket max
- `MSG` segments contain free-text benefit messages from the payer

---

### 276/277 — Claim Status Inquiry and Response

**276 (Claim Status Inquiry):** Provider asks payer for the current status of a submitted claim.

```
ST*276*0001~
BHT*0022*13*REF-001*20250203*1030~
HL*1**20*1~
NM1*PR*2*BLUE CROSS BLUE SHIELD*****PI*PAYER-ID~
HL*2*1*21*1~
NM1*1P*1*DOE*JANE****XX*1234567893~
HL*3*2*19*1~
DMG*D8*19750315*M~
NM1*IL*1*SMITH*JOHN****MI*MEMBER-ID~
HL*4*3*22*0~
TRN*1*TRACE-001~
REF*1K*CLAIM-12345~
AMT*F4*150.00~
DTP*472*RD8*20250201-20250201~
SE*13*0001~
```

- `REF*1K` = claim number
- `AMT*F4` = billed amount
- `DTP*472` = service date
- The 276 tracks a specific claim by its number

**277 (Claim Status Response):** Payer's response with detailed claim status.

```
ST*277*0002~
BHT*0022*11*RESP-001*20250203*1035~
HL*1**20*1~
NM1*PR*2*BLUE CROSS BLUE SHIELD*****PI*PAYER-ID~
HL*2*1*21*1~
NM1*1P*1*DOE*JANE****XX*1234567893~
HL*3*2*19*1~
DMG*D8*19750315*M~
NM1*IL*1*SMITH*JOHN****MI*MEMBER-ID~
HL*4*3*22*0~
TRN*2*TRACE-001~
STC*P4:185:ZZ*150.00**100.00*20250203*XX*CLAIM-12345~    — P4 = partially paid, $100 paid vs $150 billed
REF*1K*CLAIM-12345~
DTP*472*RD8*20250201-20250201~
SE*13*0002~
```

Status codes in STC segment:
- `P1` — Claim/line has been paid
- `P2` — Claim/line has been denied
- `P3` — Claim/line has been rejected (not in adjudication system)
- `P4` — Claim/line has been partially paid
- `P5` — Claim/line has been adjudicated but pending provider action

Claim status category codes (STC-1.1):
- `A` — Acknowledgment (received and processing)
- `P` — Payment information
- `F` — Finalized (paid, denied, or partially paid)

---

### 278 — Authorization Request and Response

**278 (Authorization Request):** Provider requests prior authorization for services.

```
ST*278*0001~
BHT*0022*13*REF-001*20250203*1030~
HL*1**20*1~
NM1*PR*2*BLUE CROSS BLUE SHIELD*****PI*PAYER-ID~
HL*2*1*21*1~
NM1*1P*1*DOE*JANE****XX*1234567893~
HL*3*2*22*0~
TRN*1*TRACE-001~
UM*HS**GD*99213***FAC*11~
UM*CCA***E11.9~
CLM1*150.00~
HL*4*3*25*0~
NM1*QC*1*SMITH*JOHN~
SE*11*0001~
```

- `UM*HS` = health services review
- `UM*CCA` = clinical diagnosis code
- `REF` segments carry authorization numbers

**278 Response:** Payer's decision.

```
ST*278*0002~
BHT*0022*11*RESP-001*20250203*1035~
HL*1**20*1~
NM1*PR*2*BLUE CROSS BLUE SHIELD*****PI*PAYER-ID~
HL*2*1*21*1~
NM1*1P*1*DOE*JANE****XX*1234567893~
HL*3*2*22*0~
TRN*2*TRACE-001~
UM*HS**GD*99213***FAC*11~
UM*CCA***E11.9~
HCR*A1*AUTH-12345~    — A1 = certified/approved, AUTH-12345 = auth number
SE*9*0002~
```

Service certification codes in HCR segment:
- `A1` — Certified (approved)
- `A3` — Not certified (denied)
- `A4` — Pending
- `A6` — Modified/revised

---

### 820 — Premium Payment

Used by employers/payors to send premium payments to insurance carriers. Less directly relevant to Denials Doctor's claim processing workflow but relevant for understanding the complete RCM financial picture.

---

### 834 — Benefits Enrollment

Used by employers and insurance carriers to communicate employee/member benefits enrollment. Contains subscriber and dependent information, coverage dates, and plan selection. Relevant for Denials Doctor when reconciling patient coverage data.

---

### 835 — Payment/Remittance Advice

THE most critical X12 transaction for Denials Doctor. The 835 carries payment details and denial/adjustment information from payers to providers.

```
ST*835*0003~
BPR*C*150.00*C*CHK*************PAYER-ID**DEPOSIT-001*20250210~
TRN*1*TRACE-001*PAYER-ID~
N1*PR*BLUE CROSS BLUE SHIELD~
N3*100 Payer Blvd~
N4*Chicago*IL*60601~
LX*1~
CLP*CLAIM-12345*1*150.00*100.00*50.00*CLAIMNBR-001*11*1~
NM1*QC*1*SMITH*JOHN~    — Patient
NM1*82*1*DOE*JANE****XX*1234567893~    — Rendering provider
REF*1K*CLAIM-12345~    — Claim reference number
REF*EA*POL-12345~    — Medical record number
DTM*232*20250201~    — Service date
SVC*HC:99213*150.00*100.00~    — CPT 99213, $150 billed, $100 allowed
CAS*CO*45*50.00~    — Contractual adjustment (CO-45), $50
CAS*PR*2*50.00~    — Patient responsibility (PR-2), $50 (deductible)
DTM*233*20250203
AMT*F4*150.00~
LX*2~    — Next service line
CLP*CLAIM-12346*3*500.00*0.00*500.00*CLAIMNBR-002*11*1~
SVC*HC:99214*500.00*0.00~
CAS*CO*97*350.00~    — CO-97: Benefit not covered
CAS*CO*50*150.00~    — CO-50: Not medically necessary
PLB*20250210*WO*10987654*50.00~    — Provider level adjustment (write-off)
SE*21*0003~
```

#### 835 Key Segments for Denial Analysis

**BPR (Financial Information):**
- `BPR*C` = payment is a check/EFT; `BPR*H` = no payment (zero payment)
- Total payment amount, payment date
- Sender/receiver bank info for EFT

**CLP (Claim Payment Information):**
| Element | Description | Example |
|---|---|---|
| CLP01 | Claim Submitter's Identifier | `CLAIM-12345` |
| CLP02 | Claim Status Code | `1` (processed as primary), `2` (processed as secondary), `3` (processed as tertiary), `4` (denied), `22` (reversal) |
| CLP03 | Total Claim Charge Amount | `150.00` — amount originally billed |
| CLP04 | Claim Payment Amount | `100.00` — amount paid |
| CLP05 | Patient Responsibility Amount | `50.00` — deductible/coinsurance |
| CLP06 | Claim Filing Indicator Code | `11` (Blue Cross/Blue Shield), `12` (HMO), `13` (Medicare Part A), `14` (Medicare Part B) |
| CLP07 | Payer Claim Control Number | `CLAIMNBR-001` |

**SVC (Service Line Adjudication):**
| Element | Description | Example |
|---|---|---|
| SVC01 | Composite Medical Procedure | `HC:99213` — CPT code with qualifier |
| SVC02 | Line Item Charge Amount | `150.00` |
| SVC03 | Line Item Allowed Amount | `100.00` |
| SVC04 | Line Item Payment Amount | `70.00` |

**CAS (Claim Adjustment Group Codes and Reasons):**
```
CAS*CO*45*50.00~    — Group=CO, Reason=45, Amount=$50
CAS*PR*2*50.00~     — Group=PR, Reason=2, Amount=$50
CAS*OA*23*25.00~    — Group=OA, Reason=23, Amount=$25
```

Adjustment group codes:
| Code | Group | Description |
|---|---|---|
| `CO` | Contractual Obligations | Not payable per contract (write-offs, discounts) |
| `PR` | Patient Responsibility | Deductible, coinsurance, copay, non-covered |
| `OA` | Other Adjustments | Other payer adjustments (overpayment recovery, etc.) |
| `PI` | Payer Initiated | Payer corrections or adjustments |
| `CR` | Correction/Reversal | Reversals of prior adjustments |

**CAS adjustment reason codes (CARC — Claim Adjustment Reason Codes):**
| Code | Description | Denials Doctor Category |
|---|---|---|
| 1 | Deductible | Patient Responsibility |
| 2 | Coinsurance | Patient Responsibility |
| 3 | Copayment | Patient Responsibility |
| 4 | Procedure code/taxonomy inconsistency | Coding Error |
| 5 | Not medically necessary | Medical Necessity |
| 6 | Pre-existing condition | Coverage Issue |
| 11 | Service not covered | Coverage Issue |
| 16 | Missing/incomplete/invalid claim information | Missing Info |
| 18 | Duplicate claim/service | Duplicate |
| 20 | Requested information not provided | Missing Info |
| 22 | This care may be covered by another plan | Coordination |
| 23 | Service not authorized | Prior Authorization |
| 24 | Charges exceed fee schedule | Fee Schedule |
| 26 | Expenses incurred prior to coverage | Coverage Issue |
| 27 | Expenses incurred after coverage stopped | Coverage Issue |
| 29 | Time limit for filing expired | Timely Filing |
| 31 | Patient cannot be identified | Patient Matching |
| 45 | Charge exceeds fee schedule/maximum allowable | Fee Schedule |
| 49 | This is a non-covered service | Coverage Issue |
| 50 | Service not medically necessary | Medical Necessity |
| 51 | Denial based on exclusionary rider | Coverage Issue |
| 52 | Services not approved by authorized entity | Authorization |
| 96 | Non-covered charge(s) | Coverage Issue |
| 97 | The benefit for this service is included in the payment/allowance for another service | Bundling |
| 107 | Requested information was not provided timely | Timely Filing |
| 108 | Rent-purchase not allowed | Policy |
| 109 | Claim not covered by this plan/contract | Coverage Issue |
| 119 | Benefit maximum for this service has been reached | Benefit Limit |
| 120 | Patient is not covered | Coverage Issue |
| 125 | Submission/billing error(s) | Billing Error |
| 151 | No referral on file for this claim | Authorization |
| 153 | Service not before nor after benefit period | Coverage Issue |
| 167 | Mutual agreement | Contractual |
| 204 | This service/equipment is considered to be not medically necessary | Medical Necessity |
| 214 | Claim/service denied by prior approval requirement | Authorization |
| 224 | Patient has not met required waiting period | Coverage |
| 235 | Timely filing exceeded | Timely Filing |
| 236 | No matching provider record | Provider Issue |
| 237 | Provider not eligible for payment | Provider Issue |
| 239 | Claim spans multiple claim payment periods | Billing Error |
| 240 | Payer responsibility for processing error | Payer Error |
| 242 | Services not provided by a network provider | Network |
| 243 | Services not provided in network level of care | Network |
| 250 | Payment reduced based on medical bill review | Medical Necessity |
| 252 | Service not authorized/in-network services on out-of-network basis | Authorization |
| A1 | Claim/Service denied due to missing/incomplete/invalid medical records | Missing Info |
| B1 | Non-covered care provided in non-covered setting | Coverage Issue |
| B7 | Coordination of benefits | Coordination |

**PLB (Provider Level Balance):**
Used for adjustments not tied to a specific claim (retroactive adjustments, interest, lump-sum write-offs):
```
PLB*20250210*WO*10987654*50.00~    — Write-off $50
PLB*20250210*50*20250101*25.00~    — Late filing charge
```

**DTM (Date/Time Reference):**
Multiple DTM qualifiers provide date context:
- `232` — Service date
- `233` — Claim received date
- `050` — Claim processed date
- `036` — Payment EFT date

---

### 837 — Health Care Claim

The 837 is the claim submission transaction. Three versions exist:
- **837P** (Professional): Claims from individual providers (doctors, therapists)
- **837I** (Institutional): Claims from facilities (hospitals, nursing homes)
- **837D** (Dental): Dental claims

#### 837P Structure (Professional Claim)

```
ST*837*0001~
BHT*0019*00*SUBMIT-001*20250203*1030*CH~
NM1*41*2*PROVIDER CLINIC*****46*TIN-12345~    — Submitter name
PER*IC*JOHN DOE*TE*555-123-4567~    — Submitter contact
NM1*40*2*BLUE CROSS BLUE SHIELD*****46*PAYER-ID~    — Receiver
HL*1**20*1~
NM1*85*1*DOE*JANE****XX*1234567893~    — Billing provider
N3*500 Medical Dr~
N4*Anytown*CA*90210~
REF*EI*12-3456789~    — TIN
HL*2*1*22*0~
SBR*P*18*******CI~    — Subscriber info: P=primary, 18=employment group
NM1*IL*1*SMITH*JOHN****MI*MEMBER-ID~    — Insured/subscriber
DMG*D8*19750315*M~
NM1*PR*2*BLUE CROSS BLUE SHIELD*****PI*PAYER-ID~    — Payer
HL*3*2*23*0~
PAT*19~    — Patient info: 19=patient is same as subscriber
NM1*QC*1*SMITH*JOHN****MI*MEMBER-ID~    — Patient
CLM*CLAIM-12345*150.00***11::1*Y*A*Y*Y~    — Claim info
DTP*434*RD8*20250201-20250201~    — Service date range
PWK*OZ*AC**EL*20250201~    — Attachment (if needed)
CN1*07*REFERRAL-001~    — Referral information
HI*ABK:E119~    — Diagnosis: ICD-10-CM E11.9
NM1*82*1*DOE*JANE****XX*1234567893~    — Rendering provider
LX*1~
SV1*HC:99213*150.00*UN*1*11***25~    — Service line
DTP*472*D8*20250201~    — Service date for this line
LX*2~
SV1*HC:80048*75.00*UN*1*11***25~
DTP*472*D8*20250201~
SE*28*0001~
```

Key 837 segments for Denials Doctor:
| Segment | Description | Denials Doctor Usage |
|---|---|---|
| `CLM` | Claim information | Claim number, charge amount, POS, provider signature indicator, assignment of benefits |
| `HI` | Health diagnosis codes | ICD-10 codes — used for medical necessity review |
| `SV1` | Service line | CPT/HCPCS code, charge amount, unit count, modifiers — the core service data |
| `PWK` | Report/attachment | Indicates supporting documentation attached to the claim |
| `SBR` | Subscriber info | Payer responsibility (P=primary, S=secondary, T=tertiary) |
| `CN1` | Contract information | Referral number, contract type |
| `REF*EA` | Medical record number | Patient matching across systems |
| `DTP*434` | Service date range | Date span of services |
| `AMT` | Claim level monetary amounts | Discounts, adjustments |

#### 837I vs 837P Key Differences

| Feature | 837P (Professional) | 837I (Institutional) |
|---|---|---|
| Provider type | Individual/Small group | Facility/Hospital |
| Service line | `SV1` (CPT/HCPCS) | `SV2` (Revenue Code + CPT) |
| Patient status | `CLM` segment | `CL1` (Institutional) — admission type, source |
| Diagnosis | `HI` with qualifiers | `HI` with diagnosis type indicators |
| Value codes | Not used | `HI` for value codes (blood pints, implant costs) |
| Occurrence dates | Not used | `HI` for occurrence dates (admit, discharge, onset) |
| Condition codes | Not used | `HI` for condition codes (readmission, weekend) |

---

### 999 — Implementation Acknowledgment

The 999 replaces the older 997 and provides detailed validation feedback at the transaction level.

```
ST*999*0001~
AK1*HC*1*005010X222~
AK2*837*0001~
AK3*CLM*5*12*1~    — Error at segment 5, CLM segment, position 12
AK4*1**16*101*1~    — Error at element 1, missing required data
AK9*R*1*1*1~       — Transaction rejected
SE*8*0001~
```

- `AK1` = functional group acknowledgment
- `AK2` = transaction set acknowledgment
- `AK3` = segment error details
- `AK4` = data element error details
- `AK5` = transaction set response code (`A` accepted, `E` accepted with errors, `R` rejected)
- `AK9` = functional group response

---

## TA1 — Interchange Acknowledgment

The TA1 is a segment-level acknowledgment for the entire interchange (ISA segment level). It validates the ISA envelope itself — correct sender, receiver, and control numbers.

```
TA1*123456789*250203*1030*A*000~
```

- `A` = interchange accepted
- `R` = interchange rejected
  - `000` — No errors
  - `001` — Interchange control number mismatch
  - `002` — Invalid sender ID
  - `003` — Invalid receiver ID
  - `004` — Invalid date
  - `005` — Invalid standard identifier
  - `006` — Invalid control structure
  - `007` — Unauthorized interchange

---

## 997 — Functional Acknowledgment

The 997 (now largely replaced by 999) provides acknowledgment at the functional group level:

```
ST*997*0001~
AK1*HC*1*005010X222~
AK2*837*0001~
AK5*A~    — A=Accepted
AK9*A*1*1*1~
SE*6*0001~
```

---

## 277CA — Claim Acknowledgment

The 277CA (Claim Acknowledgment) provides the submission-level response from the clearinghouse or payer:

```
ST*277*CA*0002~
HL*1**20*1~
NM1*PR*2*BLUE CROSS BLUE SHIELD*****PI*PAYER-ID~
HL*2*1*21*1~
NM1*1P*1*DOE*JANE****XX*1234567893~
HL*3*2*19*1~
DMG*D8*19750315*M~
NM1*IL*1*SMITH*JOHN****MI*MEMBER-ID~
HL*4*3*22*0~
TRN*1*TRACE-001~
STC*A1:0:ZZ*150.00**0.00*20250203****CLAIM-12345~    — A1 = accepted
REF*1K*CLAIM-12345~
SE*11*0002~
```

Claim status category codes in 277CA:
- `A1` — Claim received (accepted into adjudication system)
- `A2` — Claim rejected — not in adjudication system
- `A3` — Claim returned to provider for correction
- `A4` — Claim incomplete — additional information required
- `A5` — Claim forwarded to another payer
- `A6` — Claim reversed from prior payment
- `A7` — Claim adjusted from prior payment

---

## Data Element Requirements

### Version 5010

X12 5010 is the current HIPAA-mandated version (effective January 1, 2012). Key requirements:
- All healthcare transactions must use version 5010
- 5010 uses the 999 acknowledgment (not 997)
- Improved patient identification with multiple identifiers
- Enhanced ICD-10 support (required for ICD-10 transactions)
- More specific service line adjudication in the 835
- Provider taxonomy codes required on professional claims (837P)
- National Provider Identifier (NPI) required on all claims

### Version 4010 (Legacy)

- Pre-2012, no longer HIPAA compliant
- Limited to ICD-9 (no ICD-10 support)
- Simpler structure, fewer data requirements per segment
- 997 acknowledgment (not 999)
- Some trading partners may still accept 4010 for specific transactions

---

## Trading Partner Agreements

### ISA Sender/Receiver IDs

Trading partner agreements define the sender and receiver IDs used in the ISA envelope:
- **ISA05/ISA06 (Sender):** Provider's clearinghouse-assigned ID, TIN, or NPI
- **ISA07/ISA08 (Receiver):** Payer's clearinghouse-assigned ID or payer ID

### Envelope Requirements

The agreement specifies:
- **Delimiters:** Allowed values for segment terminator (~), element separator (*), sub-element separator (:)
- **Interchange size:** Maximum number of functional groups per interchange (typically 1-5)
- **Functional group size:** Maximum number of transactions per group (typically 100-500)
- **Transmission schedule:** Daily, real-time, batch windows
- **Acknowledgment requirements:** Whether TA1 or 999 are required

### Test vs Production

- **ISA15 = T:** Test transmission — data is not processed as real claims
- **ISA15 = P:** Production transmission — data enters the live adjudication system

### Common Trading Partner Fields

| Field | Provider Sets | Payer Provides |
|---|---|---|
| Submitter Name | Provider name | — |
| Receiver ID | — | Payer/clearinghouse ID |
| Interchange Size | 50 claims/batch | Maximum per agreement |
| Filing Indicator | Provider's taxonomy | Required codes |
| Payer ID | From clearinghouse | Payer-specific ID |
| Test Indicator | T or P | Must match |

---

## EDI Translation

### Translation Software

| Software | Vendor | Type | Notes |
|---|---|---|---|
| **Edifecs** | Edifecs | Commercial | Enterprise-grade, HIPAA compliance validation, extensive payer support |
| **Cleo** | Cleo | Commercial | AS2/AS3/AS4, integrated trading partner management |
| **B2BGateway** | B2BGateway | Cloud service | Managed EDI, healthcare-specific modules |
| **bTrade** | bTrade | Commercial | MFT (Managed File Transfer) with EDI |
| **DiCentral** | DiCentral | Cloud/PaaS | EDI translation as a service |
| **In-House (custom)** | Custom integration | Custom | Using X12 parsers/libraries (EDI.NET, Edifact) |

### Translation Process

1. **Parse:** Read the raw X12 data, validate envelope structure (ISA/GS/ST), extract transactions
2. **Validate:** Check against 5010 implementation guides, trading partner rules, HIPAA requirements
3. **Map:** Transform X12 data to internal format (JSON, database records, application objects)
4. **Enrich:** Add provider data, reference data, cross-walk codes where needed
5. **Route:** Send to appropriate downstream system (claims to billing, 835 to payment posting, 277 to claim status tracking)

---

## X12 vs FHIR

| Aspect | X12 EDI | FHIR R4 |
|---|---|---|
| Paradigm | Batch-oriented, file-based | RESTful API, resource-oriented |
| Format | Delimited text (ISA/GS/ST/SE) | JSON, XML |
| Protocol | AS2, SFTP, HTTPS (file upload) | HTTPS (REST) |
| Authentication | Digital certificates, AS2 IDs | OAuth2 (SMART on FHIR) |
| Transaction type | Business/administrative | Clinical and administrative |
| Claim processing | Native — designed for claims (837/835) | Clinical data focus, Claim/EOB resources |
| Real-time | Limited (batch processing) | Yes (RESTful, subscriptions) |
| Data granularity | Transaction-level (entire claim) | Resource-level (individual data objects) |
| Implementation cost | High (translation software, trading partner setup) | Lower (standard web APIs) |
| HIPAA compliant | Yes (mandated by HIPAA) | Yes, but not HIPAA-mandated format |
| Adoption for claims | Universal (all payers) | Growing (primarily Medicare/Medicaid) |
| Denial data | Rich (CARC codes, claim status, payment) | Moderate (EOB adjudication) |
| Learning curve | Steep (segment codes, nested loops) | Moderate (standard REST, JSON) |
| Integration complexity | High (multiple trading partners, each with custom rules) | Lower (standard API patterns) |

For Denials Doctor, X12 and FHIR are complementary:
- **X12** handles the core claims workflow: submission (837), status inquiry (276/277), payment/denial (835), authorization (278), and eligibility (270/271)
- **FHIR** provides clinical context for denials (patient, encounter, condition, procedure, observation) and enables real-time data access

---

## Agent Training: Q&A Pairs

**Q:** What is the difference between an 837P and an 837I claim transaction?
**A:** 837P (Professional) is used by individual providers and physician groups for billing professional services. It uses the SV1 segment for service lines (CPT/HCPCS codes). 837I (Institutional) is used by facilities and hospitals for billing facility services. It uses the SV2 segment with revenue codes, condition codes, occurrence codes, and value codes. The 837I also includes additional institutional-specific segments like CL1 (admission type/source) and HI segments for value codes. In revenue cycle management, the 837P type applies to physician billing while 837I applies to hospital/facility billing.

**Q:** How does the 835 transaction encode denial information?
**A:** The 835 encodes denials primarily through three mechanisms: (1) CAS (Claim Adjustment) segments with group codes (CO=contractual/denied, PR=patient responsibility, OA=other adjustment, PI=payer-initiated, CR=correction/reversal) and CARC codes (the specific denial reason); (2) CLP02 (Claim Status Code) which indicates the overall claim status — 1=primary processed, 4=denied; (3) PLB (Provider Level Balance) for adjustments not tied to a specific claim. For Denials Doctor, the CAS segments are the most important because they provide the adjudication detail per service line, including the specific CARC codes that categorize denial reasons.

**Q:** What does CLP02 = 4 mean in a 835 transaction?
**A:** CLP02 = 4 means the claim has been denied — the payer processed the claim but paid $0 because all service lines were denied. This is different from CLP02 = 1 (processed as primary with payment), 2 (processed as secondary with payment), or 3 (processed as tertiary with payment). When CLP02 = 4, the CLP04 (Claim Payment Amount) will be $0.00, and the CAS segments will contain the denial reason codes for each denied service line.

**Q:** What is the purpose of the 999 Implementation Acknowledgment?
**A:** The 999 Implementation Acknowledgment replaces the older 997 and provides detailed validation feedback for X12 5010 transactions. It validates that the transaction conforms to the implementation guide (IG) syntax — correct segment order, required fields present, data types valid, code sets valid. The 999 uses AK segments (AK1-AK9) to report errors at the functional group, transaction set, segment, and element level. It does NOT validate business logic or clinical appropriateness — it only validates that the X12 data structure is correct according to the IG.

**Q:** What are the main adjustment group codes in the 835 CAS segment and how does Denials Doctor use them?
**A:** The CAS segment supports five group codes: CO (Contractual Obligations) — contractual write-offs and denials per the payer contract; PR (Patient Responsibility) — deductible, coinsurance, copay amounts; OA (Other Adjustments) — overpayment recovery, credit balances; PI (Payer Initiated) — payer corrections and adjustments; CR (Correction/Reversal) — reversals of prior adjustments. Denials Doctor analyzes CAS segments by group code to categorize denial reasons: CO codes indicate payer denials (medical necessity, coding errors, authorization issues), PR codes indicate patient financial responsibility should be billed to the patient, and PI codes indicate payer processing errors.

**Q:** How does a 277 Claim Status Response differ from a 277 Claim Acknowledgment (277CA)?
**A:** The 277 is a general claim status response that responds to a 276 claim status inquiry. It provides real-time status updates (paid, denied, pending) for claims already submitted. The 277CA is specifically the claim acknowledgment generated upon claim submission — it tells the provider whether the claim was accepted into the adjudication system, rejected, or requires additional information. The 277CA uses different status codes: A1=accepted, A2=rejected, A3=returned for correction, A4=incomplete. The 277 uses payer-specific status codes indicating the current point in the adjudication lifecycle.

**Q:** What does the X12 TA1 acknowledgment indicate and when is it used?
**A:** The TA1 (Interchange Acknowledgment) validates the ISA envelope structure — it checks that the interchange is syntactically valid and addressed to the correct receiver. It is sent before any business-level processing. Common TA1 rejection reasons: 001 (interchange control number mismatch — ISA13 doesn't match IEA02), 002 (invalid sender ID — ISA06 not recognized), 003 (invalid receiver ID — ISA08 doesn't match the receiver). The TA1 is typically sent automatically by the EDI infrastructure before the 999 or business acknowledgment.

**Q:** What is the role of the ISA15 element (Usage Indicator) in X12 production workflows?
**A:** ISA15 indicates whether the transmission is production (P) or test (T). Production data goes through the live adjudication pipeline and generates real payments, denials, and patient financial responsibility. Test data is processed in a test environment and does not generate real claims activity. If a test file (ISA15=T) is accidentally sent to a production trading partner, it will typically be rejected at the envelope level or routed to a test queue. Denials Doctor must ensure ISA15 is correctly set to P for all production claim submissions.

**Q:** What is the X12 835 payment adjustment reason code CO-45?
**A:** CO-45 (Contractual Obligation, reason code 45) means the charge exceeds the fee schedule/maximum allowable amount established by the contract between the provider and payer. This is a contractual write-off — the provider agreed to accept the payer's allowed amount as payment in full, and the difference between the billed charge and the allowed amount is written off. CO-45 adjustments are not denials in the traditional sense; they are expected contractual adjustments. Denials Doctor should distinguish CO-45 write-offs from true denials (like CO-50 for medical necessity or CO-97 for benefit not covered).

**Q:** What is the 837 SV1 segment and what data does it carry for each service line?
**A:** The SV1 (Professional Service) segment carries the service line details in an 837P: SV101 — Composite Medical Procedure Identifier (CPT/HCPCS code with qualifier HC); SV102 — Line Item Charge Amount (billed amount); SV103 — Unit or Basis for Measurement (typically UN for units); SV104 — Quantity (number of units); SV105 — Facility Code (place of service); SV106 — Service Type Code; SV107 — Composite Diagnosis Code Pointer (links to diagnosis codes); SV108 — Monetary Amount (if different from SV102); SV109 — Modifiers (CPT modifiers like 25, 59). Each SV1 segment represents one billed service line.

**Q:** How does coordination of benefits (COB) appear in X12 transactions?
**A:** COB appears in multiple X12 transactions: (1) In the 837 — the SBR segment indicates P (primary), S (secondary), or T (tertiary) for each claim instance; (2) In the 835 — CLP02 indicates the processing level (1=primary, 2=secondary, 3=tertiary, 4=denied); (3) In the 835 — CAS OA-23 indicates "services not paid by this plan as they were covered by another plan"; (4) In the 271 — EB segments indicate coordination status. When submitting secondary claims, the 837 must include the primary payer's payment information and any applicable adjustments.

**Q:** What is the 278 HCR segment and what do its certification codes mean?
**A:** The HCR segment in a 278 response contains the authorization decision. HCR01 is the action code: A1=Certified/Approved (services authorized as requested), A2=Not Certified (services denied), A3=Not Certified (specific alternative recommendations), A4=Pending (additional review required), A6=Modified/Revised (approved but with changes). For Denials Doctor, A3 and A6 responses are particularly important as they indicate conditional approvals, while A2 responses indicate denied prior authorizations that may lead to claim denials.

**Q:** What EDI transmission protocols are commonly used for healthcare X12?
**A:** Common transmission protocols: (1) AS2 (Applicability Statement 2) — most common for direct payer connections; uses HTTPS with digital certificates for secure transport; (2) SFTP (SSH File Transfer Protocol) — common for clearinghouse connections; (3) FTP with TLS (FTPS) — used for some legacy connections; (4) OFTP (Odette File Transfer Protocol) — used with some large payers; (5) HTTPS — increasingly used for direct API-based submission, especially with clearinghouses like Change Healthcare and Availity.

**Q:** How does the 837 HI segment handle ICD-10 diagnosis codes?
**A:** The HI (Health Diagnosis Code) segment in 837P uses qualifiers to identify the diagnosis type: ABK=principal diagnosis; ABF=admitting diagnosis; ABJ=patient reason for visit; ABG=referral reason; ABR=other diagnosis. Each diagnosis is coded as a composite: `ABK:E119` means principal diagnosis is ICD-10 E11.9. Multiple HI segments carry multiple diagnoses. In 837I, HI includes additional qualifiers for admitting diagnosis, external cause of injury, and POA (present on admission) indicators.

**Q:** What is the 835 PLB segment and what adjustments does it carry?
**A:** The PLB (Provider Level Balance) segment carries adjustments that apply at the provider/receiver level rather than to a specific claim. Common PLB adjustment reason codes: WO=provider write-off, 50=late filing charge, 51=interest penalty (paid to provider), AH=withholding, CS=adjustment. PLB adjustments are typically applied to the total payment amount at the provider level and are not tied to individual claims or service lines. Denials Doctor must track PLB adjustments separately from claim-level adjustments in the 835.

**Q:** What is the 835 TRN segment and what is its purpose?
**A:** The TRN (Trace) segment provides a trace/reference number for the transaction. In the 835, it appears at the beginning of the file with TRN*1 (payer trace number) and must be unique per 835 file. The TRN number is used when submitting corrections, adjustments, or inquiries about a specific remittance. If a provider needs to dispute a payment or request a corrected 835, they reference the TRN number to identify the specific remittance file in question.

**Q:** What happens when a 997 or 999 indicates a transaction was rejected?
**A:** When a 997 or 999 returns R (rejected) for a transaction: (1) the claim was NOT accepted into the payer's adjudication system — it was rejected before processing; (2) the provider must correct the errors identified in the AK3/AK4 error segments and resubmit; (3) common rejection reasons: invalid ZIP code, missing NPI, invalid procedure code, diagnosis-to-procedure code mismatch, missing required field; (4) the 277CA acknowledgment also indicates whether the claim was accepted (A1) or rejected (A2); (5) rejected claims do NOT generate a 835 remittance — they must be resubmitted.

**Q:** What trading partner information does Denials Doctor need for 837 claim submission?
**A:** Denials Doctor needs: (1) Payer ID — the receiver identifier (ISA08) for the clearinghouse or direct payer connection; (2) Sender ID — the provider's ISA06 identifier; (3) Submitter Name (NM1*41) — the entity submitting claims; (4) Filing Indicator — the receiver's plan-specific code; (5) ISA qualifiers — ISA05/ISA07 values (typically ZZ); (6) Test/Production flag — ISA15 set appropriately; (7) File naming conventions — expected by trading partner; (8) Transmission schedule — when claims are expected to be sent and acknowledged.

---

## Summary

X12 EDI is the foundation of healthcare claims processing and denial management in the US. The eight critical transaction types are: 270/271 (eligibility), 276/277 (claim status), 278 (authorization), 820 (premium payment), 834 (enrollment), 835 (payment/remittance), 837 (claims), and 999 (implementation acknowledgment).

The 835 transaction is the most important for Denials Doctor — it carries payment details, denial codes (CARC in CAS segments), and adjustments. Understanding the envelope structure (ISA/GS/ST/SE), CAS denial codes, and the relationship between 837 (submission) and 835 (response) is essential for denial analysis and revenue cycle optimization.

X12 5010 is the current HIPAA-mandated version. While FHIR is growing for clinical data exchange, X12 remains the universal standard for payer-provider financial transactions and will continue as such for the foreseeable future.