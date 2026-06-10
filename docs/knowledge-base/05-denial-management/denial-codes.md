# Denial Codes: CARC, RARC, and Payer-Specific Code Reference

## Overview

Denial codes are the standardized language used in electronic remittance advice (835 transactions) to explain claim adjustments, denials, and payment reductions. Understanding these codes is essential for Denials Doctor to correctly interpret denials, determine appeal strategies, and identify root causes.

This document covers Claim Adjustment Reason Codes (CARCs), Remittance Advice Remark Codes (RARCs), adjustment group classifications, how to read an 835 transaction, and how to handle payer-specific proprietary codes.

---

## 1. Claim Adjustment Reason Codes (CARCs)

CARCs are the primary codes used in 835 transactions to explain why a claim line was adjusted. Each CARC has a unique 2-3 digit numeric code, a description, and associated adjudication logic.

### CARC Adjustment Groups

Every CARC is assigned to an adjustment group that determines financial responsibility:

| Group | Name | Meaning | Patient Billing Impact |
|-------|------|---------|----------------------|
| CO | Contractual Obligation | Adjustment based on contract, fee schedule, or payer policy | Cannot bill patient (contractual write-off) |
| PR | Patient Responsibility | Amount the patient owes | Can bill patient |
| OA | Other Adjustment | Adjustment for reasons other than CO or PR | Varies by circumstance |
| PI | Payer Initiated | Reduction initiated by the payer (may be reversed) | Do not bill patient yet |
| CR | Corrections and Reversals | Correcting a previous payment or reversal | Follow CR-specific rules |

### Top 50 Most Common CARCs

#### CO (Contractual Obligation) Group

| CARC | Description | Typical Use Case | Appeal Potential |
|------|-------------|-----------------|-----------------|
| CO-4 | Procedure code inconsistent with modifier | Missing/invalid modifier, or modifier not recognized | Medium — can fix and resubmit |
| CO-5 | Procedure code inconsistent with place of service | Service not allowed in the POS billed | Medium — can fix if coding error |
| CO-11 | Diagnosis inconsistent with procedure | Medical necessity issue at the cod level | High — appeal with clinical support |
| CO-15 | Authorization exceeded | Services exceeded authorized amount | Medium — can request additional auth |
| CO-16 | Claim lacks information | Missing required data elements | High — provide missing info |
| CO-18 | Duplicate claim/service | Same claim already processed | Low — verify if resubmission needed |
| CO-22 | Payment adjusted if other insurance identified | COB pending/possible | Medium — verify primary coverage |
| CO-23 | Payment adjusted because paid by another payer | Service paid by another plan | Low — verify COB is correct |
| CO-24 | Payment adjusted because charges covered by another payer | COB issue | Low — verify COB is correct |
| CO-29 | Time limit for filing has expired | Timely filing denial | Low — only if good cause or proof of timely filing |
| CO-31 | Patient cannot be identified as insured | Eligibility/invalid ID issue | High — verify eligibility |
| CO-45 | Charge exceeds fee schedule/maximum | Standard fee schedule reduction | None — contractual |
| CO-48 | Charge outside expected range | Frequency or volume issue | Medium — appeal with support |
| CO-50 | These are not covered under this medical benefit | Medical necessity denial | High — primary appeal target |
| CO-51 | These are not covered when performed in this setting | Place of service issue | Medium — can appeal setting |
| CO-52 | Service not furnished directly by the provider | Billing provider issue | Medium — correct rendering provider |
| CO-53 | Service was denied because service was not deemed necessary | Medical necessity denial | High — appeal with clinical support |
| CO-54 | Multiple physicians/same specialty | Duplicate service by same specialty | Medium — document distinct service |
| CO-55 | Procedure/treatment deemed not effective | Experimental/investigational | High — requires clinical literature |
| CO-56 | Procedure/treatment has no proven clinical value | Experimental/investigational | High — requires clinical literature |
| CO-58 | Treatment was deemed not medically necessary | Medical necessity | High — appeal with clinical support |
| CO-59 | Processed based on multiple or bundle pricing | Bundled payment | Low — contractual |
| CO-60 | Charge for maintenance/personal care | Custodial care denial | Medium — appeal if skilled care |
| CO-61 | Denied due to failure to obtain authorization | No prior auth obtained | Medium — appeal if emergency or auth obtained |
| CO-69 | Day outlier amount | DRG payment adjustment | Low — Medicare rule |
| CO-70 | Cost outlier adjustment | DRG payment adjustment | Low — Medicare rule |
| CO-74 | The service is not covered | Non-covered service | Medium — appeal if coverage issue |
| CO-86 | Service not covered by this policy/contract | Policy exclusion | Medium — check policy for exceptions |
| CO-87 | Service not covered because it is not a benefit | Benefit exclusion | Low — policy exclusion |
| CO-88 | Service not deemed medically necessary | Clinical necessity denial | High — appeal with clinical support |
| CO-96 | Non-covered charge | Service not a covered benefit | Medium — depends on policy |
| CO-97 | Service inconsistent with patient age | Age-related edit | Medium — appeal if appropriate |
| CO-119 | Benefit maximum has been reached | Benefit limit exhausted | Medium — request exception |
| CO-149 | Lifetime benefit maximum reached | Lifetime max exhausted | Low — plan design limit |
| CO-151 | Code not allowed by payer | Payer-specific code restriction | Medium — use alternative code |
| CO-174 | Provider not in plan/network | Out-of-network provider | Medium — check continuity of care |
| CO-180 | Allowed amount reduced because procedure code invalid | Invalid/missing code | High — verify and correct code |
| CO-197 | Preauthorization/Precertification required | No prior auth | Medium — appeal with auth or necessity |
| CO-198 | Prepayment review/preauthorization | Claim selected for review | N/A — respond to records request |
| CO-204 | Services for this condition not covered | Condition-specific exclusion | Medium — appeal if coverage applies |

#### PR (Patient Responsibility) Group

| CARC | Description | Typical Use Case |
|------|-------------|-----------------|
| PR-1 | Deductible amount | Patient has not met deductible |
| PR-2 | Coinsurance amount | Patient's share of allowed amount |
| PR-3 | Copayment amount | Fixed copayment per service |
| PR-4 | Non-covered service (patient responsibility) | Service not covered — patient liable |
| PR-5 | Patient not covered on DOS | No active coverage |
| PR-6 | Prior payment amount | Previously paid amount |
| PR-7 | Payment denied after POS change | Coverage change after service |
| PR-8 | Service not covered when patient has no coverage | No coverage on DOS |
| PR-15 | Service not covered because it is not a benefit | Not a covered benefit — patient liable |
| PR-16 | Claim lacks information | Patient responsibility for missing info |
| PR-25 | Payment reduced or denied based on benefit limit | Benefit limit reached — patient liable |
| PR-27 | Expenses during non-covered benefit period | Non-covered period (e.g., waiting period) |

#### OA (Other Adjustment) Group

| CARC | Description | Typical Use Case |
|------|-------------|-----------------|
| OA-18 | Duplicate claim/service | Duplicate payment recovery |
| OA-22 | Other insurance coordination of benefits | COB-related adjustment |
| OA-23 | Denied because authorization not obtained | Prior auth denial (other adjustment) |
| OA-29 | Time limit has expired (other payer) | Timely filing — other payer |
| OA-100 | Service/equipment/drug not covered | Not covered for other reasons |
| OA-107 | Claim paid as a result of provider not accepting assignment | Assignment-related adjustment |

#### PI (Payer Initiated) Group

| CARC | Description | Typical Use Case |
|------|-------------|-----------------|
| PI-13 | Payment amount adjusted | Payer-initiated payment change (may reverse) |
| PI-14 | Claim payment reversed | Full claim reversal |
| PI-20 | Claim payment amount adjusted due to prior payment | Retroactive adjustment |
| PI-21 | Claim adjusted for prior overpayment | Overpayment recovery |

#### CR (Corrections and Reversals) Group

| CARC | Description | Typical Use Case |
|------|-------------|-----------------|
| CR-1 | Claim reversed/adjusted | General correction |
| CR-2 | Claim reversed/adjusted because of duplicate submission | Duplicate reversal |
| CR-3 | Claim reversed/adjusted because service not provided | Service not rendered reversal |
| CR-4 | Claim reversed/adjusted because of overpayment | Overpayment recovery |
| CR-5 | Claim reversed/adjusted because of incorrect patient info | Demographic error correction |
| CR-6 | Claim reversed/adjusted because of incorrect insurance | COB correction |

---

## 2. Remittance Advice Remark Codes (RARCs)

RARCs provide additional detail about why a claim was adjusted. They accompany CARCs in the CAS segment of an 835 transaction. RARCs fall into three categories:

### N-Codes (N1-N999)

N-codes are informational remarks that explain the rationale for the adjustment.

| RARC | Description | Commonly Paired With |
|------|-------------|---------------------|
| N1 | The patient identifier is missing/invalid | CO-16, PR-16 |
| N2 | The provider identifier is missing/invalid | CO-16, CO-180 |
| N4 | Procedure code inconsistent with place of service | CO-5 |
| N5 | Procedure code inconsistent with modifier | CO-4 |
| N6 | The diagnosis code is inconsistent with the patient's age | CO-97 |
| N8 | The diagnosis code is inconsistent with the patient's sex | CO-151 |
| N9 | The diagnosis code is inconsistent with the procedure | CO-11 |
| N10 | The procedure code is not covered by this plan | CO-96, CO-86 |
| N15 | This service/diagnosis is not payable | CO-96 |
| N17 | The date of service is not within the coverage period | PR-5 |
| N20 | Procedure code not payable for this date of service | CO-5 |
| N26 | The patient is not eligible for this service | PR-5 |
| N27 | The provider is not eligible for this service | CO-174 |
| N30 | Patient payment amount exceeds charges | PR-1, PR-2, PR-3 |
| N31 | Missing/invalid patient birth date | CO-16 |
| N32 | Missing/invalid patient gender | CO-16 |
| N34 | The units of service are not covered | CO-119, MUE denial |
| N35 | Missing/invalid referring provider | CO-16 |
| N36 | Missing/invalid rendering provider | CO-16, CO-52 |
| N38 | The service was not authorized | OA-23, CO-197 |
| N39 | The authorization number is missing | CO-197 |
| N40 | The service is not allowed for this provider specialty | CO-151 |
| N42 | Missing/invalid taxonomy code | CO-16 |
| N43 | Missing/invalid service facility location | CO-16 |
| N44 | The service is not covered for this diagnosis | CO-11, CO-50 |
| N45 | The service is considered cosmetic | CO-86, CO-87 |
| N46 | The service is considered experimental/investigational | CO-55, CO-56 |
| N49 | The procedure code is not valid for this date of service | CO-180 |
| N54 | Patient signature is missing | CO-16 |
| N55 | Physician signature is missing | CO-16 |
| N57 | The procedure code is not valid for this patient | CO-97, CO-151 |
| N60 | Missing/invalid admission/discharge dates | CO-16 |
| N61 | Missing/invalid admission type | CO-16 |
| N62 | Missing/invalid admission source | CO-16 |
| N64 | Missing/invalid discharge hour | CO-16 |
| N65 | Missing/invalid admission weight (pediatric) | CO-16 |
| N66 | The authorization amount has been exceeded | CO-15, CO-197 |
| N67 | The number of days/units exceeds the authorized amount | CO-15, CO-197 |
| N68 | Service denied because authorization not obtained | OA-23 |
| N70 | This service is considered part of another service | CO-59 (bundling) |
| N71 | The service was not provided on the date of service | CO-53 |
| N72 | The service was previously paid | CO-18 (duplicate) |
| N73 | Service denied because it is a non-covered benefit | CO-96 |
| N74 | Service not covered for this patient | CO-96, PR-5 |
| N75 | The claim was filed after the filing deadline | CO-29 |
| N77 | The service is not payable because the benefit maximum has been met | CO-119 |
| N78 | The service is not payable because the lifetime benefit has been met | CO-149 |
| N80 | The service is not covered because there is no coverage at this time | PR-5, PR-8 |
| N81 | The patient was not eligible for the service on the date of service | PR-5 |
| N82 | The patient has other insurance that is primary | CO-22, CO-23 |
| N85 | The patient cannot be identified as the insured | CO-31 |
| N86 | The provider is not contracted with this plan | CO-174 |
| N87 | The provider is not participating in this network | CO-174 |
| N90 | This is a duplicate of a claim already processed | CO-18 |
| N91 | The procedure code is not valid for this modifier | CO-4 |
| N95 | This provider type/specialty may not bill this service | CO-151 |
| N98 | The service is not covered because the plan does not cover this type of service | CO-87 |
| N100 | Missing/invalid ordering provider credentials | CO-16 |
| N105 | Missing/invalid ambulance pick-up/drop-off location | CO-16 |
| N110 | This service is not payable without the primary procedure | CO-59 (add-on code issue) |
| N120 | Missing/invalid CLIA certificate number | CO-16 |
| N125 | Missing/invalid on-call provider | CO-16 |
| N130 | This service is denied because there is a higher level of review pending | CO-198 |
| N140 | The claim was processed as a corrected claim | Informational |
| N150 | The claim is being reviewed for medical necessity | CO-198 |
| N155 | Additional documentation is required | CO-198 |
| N160 | The patient's coverage terminated prior to the date of service | PR-5 |
| N165 | The patient's coverage began after the date of service | PR-5 |
| N170 | The payer reserves the right to request medical records | Informational |
| N175 | This is a post-payment review selection | Informational |
| N180 | The provider is excluded from the Medicare program | CO-174 |
| N185 | The claim is denied because it is a non-covered benefit under the patient's plan | CO-86, CO-87 |
| N190 | This decision is based on the Local Coverage Determination | CO-50 |
| N191 | This decision is based on the National Coverage Determination | CO-50 |
| N192 | This decision is based on the payer's medical policy | CO-50 |
| N193 | This decision is based on the payer's clinical criteria | CO-50 |
| N195 | The service exceeds the medical necessity frequency limit | CO-48, CO-50 |
| N200 | A peer-to-peer review is available | Informational |
| N210 | The appeal rights and process are described in the plan document | Informational |
| N220 | The service was denied based on the results of a prior audit | CO-50 |
| N230 | This service is denied as routine/preventive | CO-96 |
| N240 | The patient has reached the maximum number of visits | CO-119 |
| N250 | The service is not covered because it was performed during a global surgery period | CO-59 |
| N260 | The primary care provider referral is required | CO-197 |
| N270 | The claim was processed in accordance with your provider contract | CO-45 |
| N300 | Additional information has been requested from the provider | Informational |
| N325 | The service is denied because the documentation does not support medical necessity | CO-50 |
| N350 | The request for reconsideration was received after the filing deadline | CO-29 |
| N362 | The diagnosis code is incorrect | CO-11 |
| N375 | The procedure performed does not match the procedure billed | CO-4 |
| N380 | The level of service billed is not supported by the documentation | CO-50 |
| N386 | This decision was based on documentation provided | Informational |
| N390 | The service is not payable as billed | General |
| N395 | Only one evaluation and management service is payable per provider per day | CO-59 |
| N400 | The claim requires a patient signature on file | CO-16 |
| N425 | The provider must submit medical records for review | CO-198 |
| N450 | The service was denied per the payer's utilization management policy | CO-50 |
| N475 | This service is considered part of the global surgical package | CO-59 |
| N500 | The service was performed by an unlicensed provider | CO-151 |
| N525 | The medical record does not support medical necessity for the level of service | CO-50 |
| N550 | The patient failed to meet step therapy requirements | CO-50 |
| N575 | Prior authorization was obtained for a different service | OA-23, CO-197 |
| N600 | The service was rendered during a prior authorization gap | CO-197 |
| N625 | The claim was processed per the patient's benefit plan | Informational |
| N650 | The service is not payable because the provider did not accept assignment | CO-174 |
| N675 | The claim was processed as an out-of-network benefit | CO-174 |
| N700 | The service was denied due to a conflict of interest | CO-151 |
| N725 | The service is not payable because it is custodial care | CO-96 |
| N750 | The service is not payable because it is not reasonable and necessary | CO-50 |
| N775 | The service was denied because it is considered alternative medicine | CO-96 |
| N800 | The claim was forwarded to the patient's secondary insurance | Informational |
| N825 | The claim was forwarded to the patient as an assignment of benefits | Informational |
| N850 | The claim is denied per the contractual agreement between the payer and provider | CO variation |
| N875 | The service was denied because the patient was not enrolled at the time of service | PR-5 |
| N900 | The claim is pending review of additional information | CO-198 |
| N925 | The service was denied based on state-specific regulations | State-specific |
| N950 | The claim was processed according to federal regulation | Federal rule |

### M-Codes (M1-M999)

M-codes describe specific medical policy or clinical reasons for denials.

| RARC | Description |
|------|-------------|
| M1 | The service was denied based on medical necessity criteria |
| M2 | The service was denied because the diagnosis does not meet medical necessity criteria |
| M3 | The service was denied because the documentation does not support medical necessity |
| M4 | The service was denied because it is not consistent with the patient's clinical condition |
| M5 | The service was denied because it exceeds the frequency limit for this diagnosis |
| M6 | The service was denied because the patient has not exhausted alternative treatments |
| M7 | The service was denied because it is considered experimental/investigational |
| M8 | The service was denied because it is not the standard of care |
| M10 | The service was denied because it is a cosmetic procedure |
| M11 | The service was denied because it is a non-covered benefit under the medical policy |
| M15 | The service was denied because a more appropriate service is available |
| M20 | The service was denied because it was not provided in accordance with the LCD |
| M25 | The service was denied because it was not provided in accordance with the NCD |
| M30 | The service was denied because the number of services exceeds the medical policy limit |
| M35 | The service was denied because it is considered a screening service |
| M40 | The service was denied because the patient did not meet clinical criteria |
| M45 | The service was denied because the documentation was not received |
| M50 | The service was denied because the documentation was not received within the requested timeframe |
| M51 | The service was denied because the documentation was incomplete |
| M55 | The service was denied because the prior authorization was not clinically supported |
| M60 | The service was denied because it is not medically necessary for this patient |
| M65 | The service was denied because the service was not performed as authorized |
| M70 | The service was denied because the patient's condition did not warrant this level of care |
| M75 | The service was denied because the setting was not appropriate for this service |
| M80 | The service was denied because the inpatient admission was not medically necessary |
| M85 | The service was denied because the observation stay should have been an outpatient visit |
| M90 | The service was denied because the procedure was not reconstructive — deemed cosmetic |
| M95 | The service was denied because it is not payable under Medicare guidelines |
| M100 | The service was denied because it is not payable per the National Coverage Determination |

### MA-Codes (MA01-MA99)

MA-codes are informational remarks about Medicare-specific adjustments.

| RARC | Description |
|------|-------------|
| MA01 | The claim was processed as primary/secondary |
| MA02 | The allowed amount was determined by the Medicare fee schedule |
| MA03 | The payment was reduced/modified under the multiple payment reduction |
| MA04 | The payment was reduced under the surgical multiple procedure rule |
| MA05 | The payment was reduced under the diagnostic imaging multiple procedure rule |
| MA06 | The payment was reduced under the therapy multiple procedure rule |
| MA07 | The payment was reduced under the outpatient hospital multiple procedure rule |
| MA08 | The payment was reduced/denied under the medical review |
| MA09 | The payment was reduced per the outpatient code editor |
| MA10 | The payment was reduced per the consolidated billing edit |
| MA11 | The claim was processed as a non-covered service |
| MA12 | The claim was selected for medical review |
| MA13 | The claim was selected for prepayment review |
| MA14 | The claim was selected for post-payment review |
| MA15 | The claim was denied per the Medicare statute |
| MA16 | The record/documentation was not received |
| MA17 | The record/documentation was not received timely |
| MA18 | The record/documentation was received but does not support the claim |
| MA19 | Medical records are required for this type of claim |
| MA20 | The procedure code was not on the Medicare approved list for this provider specialty |
| MA21 | The procedure code was not on the Medicare approved list for this place of service |
| MA22 | The payment was reduced under the outpatient prospective payment system |
| MA23 | The payment was reduced under the inpatient prospective payment system |
| MA24 | The payment was reduced under the physician fee schedule |
| MA25 | The payment was reduced under the clinical laboratory fee schedule |
| MA26 | The payment was reduced under the durable medical equipment fee schedule |
| MA27 | The payment was reduced under the ambulance fee schedule |
| MA28 | The payment was reduced under the home health prospective payment system |
| MA29 | The payment was reduced under the skilled nursing facility prospective payment system |
| MA30 | The claim was processed as a non-Medicare claim |

---

## 3. How to Read an 835 Transaction

The 835 (Health Care Claim Payment/Remittance Advice) is the electronic transaction used by payers to explain claim payment and adjustments. Understanding the 835 structure is critical for automated denial management.

### 835 Transaction Structure

```
ISA...  (Interchange Control Header)
  GS...  (Functional Group Header)
    ST...  (Transaction Set Header)
    BPR... (Beginning Segment for Payment/Remittance)
    TRN... (Reassociation Trace Number)
    REF... (Receiver Identification)
    
    Loop 1000A - Payer Identification
      N1...  (Payer Name)
    
    Loop 1000B - Payee Identification  
      N1...  (Payee Name)
    
    Loop 2000 - Header Number
      LX...  (Header Number)
      
      Loop 2100 - Claim Payment Information
        CLP... (Claim Payment Information)
          CLP01 - Patient Control Number (Claim ID)
          CLP02 - Claim Status Code
          CLP03 - Total Claim Charge Amount
          CLP04 - Claim Payment Amount
          CLP05 - Patient Responsibility Amount
          CLP06 - Claim Filing Indicator Code
          CLP07 - Payer Claim Control Number
        
        CAS... (Claim Adjustment Segments)
          CAS01 - Claim Adjustment Group Code (CO, PR, OA, PI, CR)
          CAS02 - CARC (e.g., 45, 50, 29)
          CAS03 - Adjustment Amount
          CAS04 - Quantity (Units)
          (CAS02-CAS04 repeats up to 5 times per CAS segment)
          (Multiple CAS segments may exist per claim)
        
        NM1... (Patient Name)
        
        Loop 2110 - Service Line Information
          SVC... (Service Line)
            SVC01 - Procedure Code (CPT/HCPCS)
            SVC02 - Line Charge Amount
            SVC03 - Line Payment Amount
            SVC04 - Revenue Code
          
          CAS... (Service Adjustment Segments)
            CAS01 - Claim Adjustment Group Code
            CAS02 - CARC
            CAS03 - Adjustment Amount
            CAS04 - Quantity
        
          REF... (Remark Codes - RARCs)
            REF01 - Qualifier (usually "HE" for remark)
            REF02 - Remark Code
        
          AMT... (Remaining Patient Liability)
      
      SE...  (Transaction Set Trailer)
    GE...  (Functional Group Trailer)
  IEA...  (Interchange Control Trailer)
```

### CLP Claim Status Codes

The CLP segment contains a two-digit claim status code:

| CLP02 | Status | Meaning |
|-------|--------|---------|
| 1 | Processed as primary | Payment/adjudication as primary payer |
| 2 | Processed as secondary | Payment/adjudication as secondary payer |
| 3 | Processed as tertiary | Payment/adjudication as tertiary payer |
| 4 | Denied | Claim has been denied (no payment) |
| 5 | Processed as primary, forwarded to secondary | Primary processed, forwarded for COB |
| 6 | Processed as secondary, forwarded to tertiary | Secondary processed, forwarded for COB |
| 7 | Reversal of previous payment | A prior payment is being reversed |
| 8 | Claim not found | Claim number not found in payer system |
| 9 | Processed as primary — no payment due to COB | Primary processed but no payment (deductible, etc.) |
| 10 | Processed as primary — paid | Payment made as primary |
| 11 | Processed as secondary — paid | Payment made as secondary |
| 12 | Claim pended for review | Under review, no payment yet |
| 13 | Submitted to review | Claim has been forwarded for review |
| 14 | Claim denied - incomplete | Missing information |
| 15 | Claim denied - invalid | Invalid information on claim |
| 16 | Claim denied - duplicate | Duplicate submission |
| 17 | Claim denied - untimely | Filed after deadline |
| 18 | Claim denied - non-covered | Service not covered |
| 19 | Claim denied - authorization | No authorization |
| 20 | Claim denied - medical necessity | Not medically necessary |
| 21 | Claim denied - coding error | Incorrect coding |
| 22 | Claim denied - eligibility | Patient not eligible on DOS |
| 23 | Claim denied - benefit limit | Benefit limit exhausted |

### Reading CAS Segments: Practical Examples

**Example 1: Simple Payment with Contractual Adjustment**
```
CLP*12345*1*500*200*50*12*ABC67890~
CAS*CO*45*300~
```
- Total billed: $500
- Payment: $200
- Patient responsibility: $50
- CO-45 adjustment: $300 (contractual write-off, fee schedule reduction)
- Net: $200 payment to provider

**Example 2: Medical Necessity Denial**
```
CLP*12345*4*1000*0*0*12*DEF12345~
CAS*CO*50*1000~
```
- Total billed: $1,000
- Payment: $0
- CO-50 denial: $1,000 (not medically necessary)
- No payment — full denial

**Example 3: Multiple Adjustments**
```
CLP*12345*1*750*300*50*12*GHI67890~
CAS*PR*1*100~
CAS*CO*45*250~
CAS*OA*23*100*2~
```
- Total billed: $750
- Payment: $300
- Patient responsibility: $50 (may include PR-1 deductible)
- PR-1: $100 (deductible — patient owes)
- CO-45: $250 (fee schedule reduction — write off)
- OA-23: $100 (no authorization for 2 units at $50 each — appealable)

**Example 4: Service Line Denial with RARC**
```
CLP*12345*1*500*400*50*12*IJK12345~
NM1*QC*1*DOE*JOHN~
SVC*HC:99213*100*75~
CAS*CO*45*25~
SVC*HC:93000*400*325~
CAS*CO*50*75~
REF*HE*N386~
```
- Service line 1 (99213 office visit): billed $100, paid $75, CO-45 write-off $25
- Service line 2 (93000 EKG): billed $400, paid $325, CO-50 denial of $75
- Remark code N386: decision based on documentation provided
- Net: one service paid partially, one service denied for medical necessity

---

## 4. Payer-Specific Denial Reason Codes

In addition to standard CARCs, most payers use proprietary denial codes and reason descriptions. These are NOT standardized and vary by payer, plan, and even line of business.

### Medicare (by MAC)

| MAC | Region | Specific Denial Features |
|-----|--------|-------------------------|
| Noridian | Jurisdictions A, D, E | ABN-related code series |
| Novitas | Jurisdictions H, L, M | LCD-specific denial coding |
| Palmetto GBA | Jurisdictions J, 11 | Specific medical review codes |
| NGS | Jurisdictions 6, B, K | J6 MAC-specific adjustments |
| WPS | Jurisdictions 5, 8 | GHI-specific codes |
| CGS | Jurisdictions 15 | Home health/DME-specific |
| First Coast | Jurisdiction N | FISS system codes |
| Wisconsin Physicians Service | Jurisdiction 5, 8 | MAC-specific CARC mapping |
| CMS Shared Systems | All | FISS and VMS system reject codes |

### UnitedHealthcare (UHC/Optum)

| UHC Code | Description | Equivalent CARC |
|----------|-------------|-----------------|
| 600 | Not a covered benefit | CO-96 |
| 601 | Not medically necessary | CO-50 |
| 602 | Exceeds medical necessity | CO-50 |
| 603 | No prior authorization | CO-197 |
| 604 | Authorization exceeded | CO-15 |
| 605 | Expired authorization | CO-197 |
| 606 | Authorization for different service | OA-23 |
| 700 | Timely filing | CO-29 |
| 701 | Filing deadline exceeded | CO-29 |
| 800 | Duplicate claim | CO-18 |
| 801 | Duplicate service | CO-18 |
| 900 | Patient not eligible | PR-5 |
| 901 | Patient not active on DOS | PR-5 |
| 1000 | Provider not in network | CO-174 |
| 1001 | Non-participating provider | CO-174 |
| 1100 | Code not allowed for this provider | CO-151 |
| 1200 | Benefit limit exceeded | CO-119 |
| 1300 | Experimental/investigational | CO-55 |

### Aetna

| Aetna Code | Description | Equivalent CARC |
|------------|-------------|-----------------|
| 16000 | Clinical denial — not medically necessary | CO-50 |
| 16001 | Clinical denial — level of care | CO-50 |
| 16002 | Clinical denial — frequency | CO-48 |
| 16003 | Clinical denial — setting | CO-51 |
| 16004 | Clinical denial — experimental | CO-55 |
| 16005 | Clinical denial — cosmetic | CO-86 |
| 16100 | Administrative — no auth | CO-197 |
| 16101 | Administrative — auth not valid | CO-197 |
| 16102 | Administrative — timely filing | CO-29 |
| 16200 | Benefit limit — maximum visits | CO-119 |
| 16201 | Benefit limit — dollar maximum | CO-119 |
| 16300 | Eligibility — no coverage on DOS | PR-5 |
| 16400 | Coding — invalid code | CO-180 |
| 16401 | Coding — invalid modifier | CO-4 |
| 16402 | Coding — inconsistent with diagnosis | CO-11 |

### Cigna

| Cigna Code | Description | Equivalent CARC |
|------------|-------------|-----------------|
| D0 | Not medically necessary | CO-50 |
| D1 | Experimental/investigational | CO-55 |
| D2 | Non-covered service | CO-96 |
| D3 | Benefit limit exhausted | CO-119 |
| D4 | No prior authorization | CO-197 |
| D5 | Cosmetic procedure | CO-86 |
| D6 | Not a covered benefit | CO-87 |
| D7 | Service not indicated | CO-50 |
| D8 | Frequency exceeds guideline | CO-48 |
| D9 | Exceeds medical policy limit | CO-119 |
| A0 | Timely filing | CO-29 |
| A1 | Duplicate claim | CO-18 |
| A2 | Patient not eligible | PR-5 |
| A3 | No contract with provider | CO-174 |
| A4 | Invalid/incomplete claim | CO-16 |

### Blue Cross Blue Shield (Varies by State)

| BCBS Code | Description | Notes |
|-----------|-------------|-------|
| BCBS Standard 1-99 | Administrative denials | Varies by plan |
| BCBS Standard 100-199 | Clinical/medical necessity denials | Varies by plan |
| BCBS Standard 200-299 | Coding denials | Varies by plan |
| BCBS Standard 300-399 | Authorization denials | Varies by plan |
| BCBS Standard 400-499 | Eligibility denials | Varies by plan |
| BCBS Standard 500-599 | Benefit limit denials | Varies by plan |

Note: BCBS is a federation of 34 independent companies. Each BCBS plan uses proprietary coding systems. There is NO national standard for BCBS denial codes.

### Humana

| Humana Code | Description | Equivalent CARC |
|-------------|-------------|-----------------|
| HUM-01 | Not medically necessary | CO-50 |
| HUM-02 | No prior authorization | CO-197 |
| HUM-03 | Non-covered service | CO-96 |
| HUM-04 | Benefit limit exceeded | CO-119 |
| HUM-05 | Coding error | Various |
| HUM-06 | Timely filing | CO-29 |
| HUM-07 | Duplicate | CO-18 |
| HUM-08 | Patient ineligible | PR-5 |
| HUM-09 | Out-of-network | CO-174 |

### Tricare

| Tricare Code | Description | Equivalent CARC |
|--------------|-------------|-----------------|
| TR-01 | Not medically necessary | CO-50 |
| TR-02 | Non-covered service | CO-96 |
| TR-03 | No authorization | CO-197 |
| TR-04 | Timely filing | CO-29 |
| TR-05 | Benefit limit | CO-119 |
| TR-06 | Out-of-network | CO-174 |
| TR-07 | Coding error | Various |
| TR-08 | Duplicate | CO-18 |
| TR-09 | COB issue | CO-22 |
| TR-10 | Ineligible dependent | PR-5 |

---

## 5. NCPDP (Pharmacy) Denial Codes

Pharmacy denials use NCPDP (National Council for Prescription Drug Programs) standard codes, which differ from medical CARCs.

### NCPDP Reject Codes (Common)

| Reject Code | Description | Equivalent Medical CARC |
|-------------|-------------|------------------------|
| 1 | Missing/Invalid BIN | CO-16 |
| 2 | Missing/Invalid PCN | CO-16 |
| 3 | Missing/Invalid Group ID | CO-16 |
| 4 | Missing/Invalid Cardholder ID | CO-16 |
| 5 | Missing/Invalid Person Code | CO-16 |
| 6 | Missing/Invalid Date of Birth | CO-16 |
| 7 | Missing/Invalid Patient Gender | CO-16 |
| 8 | Patient not covered | PR-5 |
| 9 | Coverage expired | PR-5 |
| 10 | Prior authorization required | CO-197 |
| 11 | Refill too soon | CO-48 |
| 12 | Quantity exceeds limit | CO-119 |
| 13 | Days supply exceeds limit | CO-48 |
| 14 | Duplicate claim/service | CO-18 |
| 15 | Non-covered drug | CO-96 |
| 16 | Drug not in formulary | CO-96 |
| 17 | Brand-name drug dispensed, generic required | CO-45 |
| 18 | Drug not covered for this diagnosis | CO-11 |
| 19 | Age restriction | CO-97 |
| 20 | Gender restriction | CO-151 |
| 21 | Drug-disease interaction | CO-50 |
| 22 | Drug-drug interaction | CO-50 |
| 23 | MME (Morphine Equivalent) exceeded | CO-50 |
| 24 | Step therapy required | CO-197 |
| 25 | Medication therapy management required | CO-50 |
| 50 | Maximum daily dose exceeded | CO-48 |
| 51 | Maximum lifetime dose exceeded | CO-119 |
| 60 | Patient age exceeds plan maximum | CO-97 |
| 61 | Patient age below plan minimum | CO-97 |
| 70 | Product not covered — medical benefit | CO-96 |
| 79 | Refill exceeds maximum | CO-119 |
| 80 | Claim too old (timely filing) | CO-29 |
| 85 | Claim submitted beyond timely filing limit | CO-29 |
| 88 | Drug not covered for patient age | CO-97 |
| 99 | Other error (see description) | Varies |

---

## 6. How to Map Proprietary Payer Codes to Standard CARCs

Mapping proprietary codes to CARCs is essential for standardized denial analysis and reporting. The Denials Doctor system should normalize all payer codes to standard CARCs where possible.

### Mapping Process

1. **Collect denial data**: Gather denial details from remittance advice, payer portals, and clearinghouse reports
2. **Identify the proprietary code**: Note the payer-specific denial code and description
3. **Determine the adjustment group**: Is the adjustment contractual (CO), patient (PR), or other (OA)?
4. **Map to standard CARC**: Find the closest matching CARC based on the denial description and financial outcome
5. **Preserve the proprietary code**: Store the original payer code alongside the mapped CARC for reference
6. **Track mapping accuracy**: Periodically verify that mappings remain accurate as payers update their systems

### Common Mapping Scenarios

| Proprietary Description | Likely Payer | Mapped CARC | Strategy |
|------------------------|-------------|-------------|----------|
| "Not medically necessary for this diagnosis" | Any | CO-50 | Clinical appeal |
| "Service does not meet medical necessity criteria" | Any | CO-50 | Clinical appeal |
| "Prior approval not obtained" | UHC, Aetna, Cigna | CO-197 | Auth or medical appeal |
| "Benefit maximum for this service has been reached" | Any | CO-119 | Request exception |
| "Claim received after timely filing limit" | Any | CO-29 | Good cause or proof of timely filing |
| "Service not covered by your plan" | Any | CO-96 | Check policy |
| "Invalid CPT/HCPCS code" | Any | CO-180 | Verify and correct code |
| "Non-participating provider" | Any | CO-174 | Network verification |
| "Duplicate of previously processed claim" | Any | CO-18 | Check prior claim |
| "Incomplete or missing information" | Any | CO-16 | Submit missing info |
| "Patient is not eligible" | Any | PR-5 | Verify eligibility |
| "Diagnosis does not support procedure" | Any | CO-11 | Clinical/coding fix |
| "Provider is not eligible to perform this service" | Any | CO-151 | Provider credentialing |
| "Procedure inconsistent with patient age" | Any | CO-97 | Verify age on claim |
| "Incorrect modifier used" | Any | CO-4 | Fix modifier |

### Payer Code Mapping Example

```
Original Denial:
  Payer: UnitedHealthcare
  Proprietary Code: 601
  Description: Not medically necessary
  Adjustment Amount: $500.00
  Claim Type: Professional

Mapped to Standard:
  CARC: CO-50
  Group: Contractual Obligation
  Category: Medical Necessity
  Appeal Strategy: Clinical Documentation Appeal
  Priority: High
  Success Estimate: 50-60% at Level 1
```

---

## 7. Denial Code Analysis for Root Cause Identification

### Coding Denial Pattern Analysis

| CARC Pattern | Likely Root Cause | Prevention Strategy |
|-------------|-------------------|---------------------|
| CO-4 repeatedly | Modifier issues | Modifier verification in claim scrubber |
| CO-11 repeatedly | Diagnosis-Procedure mismatch | Pre-submission medical necessity checker |
| CO-16 repeatedly | Missing data | Completeness checks at claim generation |
| CO-29 repeatedly | Filing delays | Automated filing deadline tracking |
| CO-31 repeatedly | Eligibility verification gaps | Pre-visit eligibility checks |
| CO-45 repeatedly | Fee schedule issues | Contractual (not appealable) |
| CO-48 repeatedly | Frequency/volume issues | Utilization management review |
| CO-50 repeatedly | Clinical documentation gaps | Physician documentation training |
| CO-97 repeatedly | Age-related edits | Age verification in claim system |
| CO-119 repeatedly | Benefit limit tracking | Real-time benefit utilization tracking |
| CO-151 repeatedly | Payer-code mapping | Payer-specific code validation |
| CO-174 repeatedly | Network participation | Provider credentialing verification |
| CO-180 repeatedly | Code validity issues | Code validation in claim system |
| CO-197 repeatedly | Authorization gaps | Pre-service authorization workflow |
| PR-5 repeatedly | Eligibility verification issues | Automated eligibility checks |

---

## 8. Denial Code Lookup Quick Reference

### Appeal by CARC Priority

**High Appeal Success Potential** (50%+ at Level 1):
- CO-11: Diagnosis inconsistent with procedure
- CO-16: Claim lacks information
- CO-31: Patient cannot be identified as insured
- CO-50: Not medically necessary
- CO-53: Service not deemed necessary
- CO-88: Not deemed medically necessary
- CO-180: Procedure code invalid
- PR-5: Patient not covered on DOS (if coverage was active)

**Medium Appeal Success Potential** (25-50%):
- CO-4: Procedure inconsistent with modifier
- CO-5: Inconsistent with place of service
- CO-15: Authorization exceeded
- CO-48: Charge outside expected range
- CO-51: Not covered when performed in this setting
- CO-74: Service not covered
- CO-86: Service not covered by policy
- CO-97: Inconsistent with age
- CO-119: Benefit maximum reached
- CO-151: Code not allowed by payer
- CO-174: Provider not in network
- CO-197: No prior authorization
- CO-204: Condition not covered

**Low Appeal Success Potential** (typically contractual or policy):
- CO-18: Duplicate claim (if truly duplicate)
- CO-22/23/24: COB adjustments
- CO-29: Timely filing (unless good cause)
- CO-45: Fee schedule reduction (never appealable)
- CO-87: Service not a benefit
- CO-96: Non-covered charge
- CO-149: Lifetime benefit maximum
- PR-1/2/3: Deductible/coinsurance/copay (patient responsibility)

---

## Agent Q&A Pairs for Training

**Q: What is the difference between CO-45 and CO-50?**
**A:** CO-45 means "Charge exceeds fee schedule/maximum allowable or contracted/legislated fee arrangement" — this is a contractual payment reduction, not a denial. The payer is reducing the payment because the billed charge exceeds their allowed amount based on your contract or their fee schedule. This is NOT appealable — it is a standard contractual write-off. CO-50 means "These are not covered under this medical benefit/part/maximum" — this IS a denial. The payer is denying the entire service as not medically necessary or not covered. CO-50 denials are appealable with clinical documentation. A CO-45 is routine and expected for virtually every paid claim. A CO-50 requires an investigation and appeal strategy.

**Q: What does the CAS segment in an 835 represent?**
**A:** The CAS (Claim Adjustment Segment) in an 835 transaction contains the actual adjustment/denial details. Each CAS segment has: CAS01 (group code: CO, PR, OA, PI, CR), CAS02 (the CARC, e.g., 45, 50, 29), CAS03 (the adjustment amount in dollars), and CAS04 (the quantity/units adjusted). A single claim can have multiple CAS segments (one per group code) and within each CAS segment, up to 6 adjustment pairs (CARC + amount + quantity). For example, a claim could have CAS*CO*45*200~ (contractual write-off $200) and CAS*PR*1*100~ (patient deductible $100). Reading the CAS segments correctly is how you determine the exact reason for every adjustment.

**Q: What is a RARC and how does it relate to a CARC?**
**A:** A RARC (Remittance Advice Remark Code) provides additional context to a CARC. The CARC tells you WHAT type of adjustment was made (e.g., CO-50 = not medically necessary), while the RARC tells you WHY at a more granular level (e.g., N386 = this decision was based on documentation provided; N190 = this decision is based on the Local Coverage Determination). A single CARC can be accompanied by multiple RARCs. The combination of CARC + RARC gives you the complete picture of the denial reason. In an 835, RARCs appear in REF segments following the CAS segment. When analyzing denials, always look at both the CARC and RARC together.

**Q: What does CLP02 4 mean and what should I do?**
**A:** CLP02 4 means "Claim Denied" — the entire claim has been denied with no payment. This is indicated by a payment amount of $0 in the CLP segment. When you see CLP02 4, you must examine the CAS segments to understand the specific denial reasons. The CAS segments will show the CARCs (e.g., CO-50 for medical necessity) and the amounts denied. Do not close the case after seeing "Claim Denied" — check each service line's CAS segment to determine which specific services were denied and for what reason, then develop an appeal strategy for each appealable denial.

**Q: How do I determine if a denial is appealable based on the CARC?**
**A:** Use this framework: (1) CO-denials are appealable unless they are fee schedule adjustments (CO-45), benefit exclusions (CO-87), or non-covered charges (CO-96) — most CO denials should be investigated, (2) PR-denials are patient responsibility but may still be worth appealing if the patient is unable to pay or if the eligibility/benefit determination was incorrect, (3) OA-denials should be investigated — OA-23 (no auth) is a common appeal target, (4) PI-denials are payer-initiated adjustments — wait to see if they reverse before appealing, (5) CR-denials are corrections/reversals — investigate why the correction was made. High-priority appeal targets: CO-50 (medical necessity), CO-11 (diagnosis inconsistency), CO-197 (no auth), OA-23 (no auth), PR-5 (patient not covered — if coverage was active), CO-31 (patient not identified).

**Q: What is CO-204 and what type of denial is it?**
**A:** CO-204 means "Services/charges related to the treatment of this condition are not covered." This is a non-covered condition denial. It occurs when the payer's policy specifically excludes coverage for the diagnosed condition. Common conditions that trigger CO-204: obesity/weight loss, infertility, cosmetic procedures, routine foot care, routine dental, routine vision, hearing services, and certain behavioral health conditions. To appeal: (1) Get the specific policy language explaining the exclusion, (2) Determine if the exclusion truly applies or if the diagnosis code is incorrect, (3) If the service is reconstructive (not cosmetic), provide documentation proving reconstructive nature, (4) Check for exceptions or riders that cover the excluded condition, (5) If the exclusion is valid and no appeal path exists, the patient is financially responsible with a valid waiver.

**Q: What is the difference between CO-86, CO-87, and CO-88?**
**A:** All three are non-coverage codes but with different nuances: CO-86 means "Service not covered by this policy/contract" — the service may be medically necessary but the policy does not cover it (e.g., IVF is not covered by the specific contract). CO-87 means "Service not covered because it is not a benefit of the policy" — the service is not a benefit under the plan design (e.g., cosmetic surgery is explicitly excluded from benefits). CO-88 means "Service not deemed medically necessary" — this is a medical necessity denial, not a benefit exclusion. CO-88 is the most appealable of the three because you can appeal with clinical documentation showing the service WAS medically necessary. CO-86 and CO-87 are harder to appeal because they relate to the policy contract, not clinical judgment.

**Q: What does PR-25 mean?**
**A:** PR-25 means "Payment reduced or denied based on benefit limit" — this is a benefit limit denial that has been classified as patient responsibility. The payer is saying the patient has exceeded their benefit limit for this service, and the patient is financially responsible for the charges. Common examples: physical therapy visits exhausted, chiropractic visits exceeded, dollar maximum reached. Important considerations: (1) Check whether the benefit limit calculation is correct — payer systems can show incorrect remaining benefits, (2) If the limit is correct and was disclosed to the patient, the patient owes the amount, (3) If the limit was not disclosed or the service was pre-authorized without mentioning benefit limits, you may have a basis to appeal, (4) Some states have laws protecting patients from surprise benefit limit liability, (5) Mental health parity laws may apply — mental health benefit limits cannot be more restrictive than medical/surgical benefit limits.

**Q: How do I find the RARC on an 835?**
**A:** RARCs appear in REF segments within the service line (Loop 2110) or claim level (Loop 2100) of an 835 transaction. The REF segment qualifier is typically "HE" (Health Care Remark Code) or occasionally "F4" (Version Identifier). The format is:
```
SVC*HC:99213*100*75~
CAS*CO*50*25~
REF*HE*N386~
```
Here, RARC N386 ("This decision was based on documentation provided") accompanies CARC CO-50 (not medically necessary). In paper remittance advices, RARCs appear in the "Remark Codes" column or section. Some payers include RARCs in the provider remarks section of the paper RA. When analyzing a denial, always identify the RARC to understand the specific clinical or administrative reason for the denial.

**Q: My claim was denied with CO-31. What does this mean?**
**A:** CO-31 means "Patient cannot be identified as our insured." This is an eligibility/identification issue — the payer's system cannot find the patient in their membership records with the information provided. Common causes: (1) Incorrect patient ID/member number on the claim, (2) Incorrect patient name (different spelling than what the payer has), (3) Incorrect date of birth, (4) Patient ID changed (new member ID card), (5) Patient was added to policy but payer system not updated, (6) Insurance is under a different subscriber (e.g., spouse's ID instead of patient's own). Resolution: (1) Verify the correct member ID from the patient's insurance card, (2) Verify patient demographics (name, DOB exactly as the payer has them), (3) Verify eligibility through a 270/271 transaction, (4) Correct the claim with the verified information and resubmit, (5) If the payer's system still cannot find the patient, call the payer to reconcile the records.

**Q: What do MA-codes mean on a Medicare remittance?**
**A:** MA-codes (MA01-MA99) are Medicare-specific informational remark codes that explain how a Medicare claim was processed. They are NOT denial codes but rather explanatory notes about the Medicare payment methodology. For example: MA01 indicates how the claim was processed (primary/secondary), MA04 indicates a surgical multiple procedure reduction was applied, MA06 indicates a therapy multiple procedure reduction, MA22 indicates reduction under OPPS, MA23 indicates reduction under IPPS, MA24 indicates reduction under the physician fee schedule. MA-codes are used primarily for Medicare Part A and B claims. They help providers understand why a payment amount is different from the billed charge, but they are not appealable denials.

**Q: How do I tell if a denial is appealable based on the group code?**
**A:** Group codes are critical: CO (Contractual Obligation) — Most CO adjustments are appealable EXCEPT CO-45 (fee schedule), CO-87 (benefit exclusion), and CO-96 (non-covered charge). CO-50 (medical necessity), CO-197 (no auth), CO-11 (diagnosis inconsistency), and CO-4 (modifier issue) are all appealable. PR (Patient Responsibility) — These are the patient's financial responsibility (deductible, coinsurance, copay). You can appeal PR denials if the benefit determination is wrong or the patient cannot pay. OA (Other Adjustment) — These are often appealable because they are for reasons other than contractual or patient responsibility. OA-23 (no auth) is a prime appeal target. PI (Payer Initiated) — Adjustments the payer made on their own. Do not appeal immediately — wait 30 days to see if the payer reverses. CR (Corrections and Reversals) — The payer corrected a prior payment. Investigate why the correction was made before appealing.

**Q: My claim shows CARC CO-45 but I think the fee schedule amount is wrong. What can I do?**
**A:** CO-45 means "Charge exceeds fee schedule/maximum allowable or contracted/legislated fee arrangement." This is a standard contractual adjustment based on the payer's fee schedule. While CO-45 is generally not appealable through the standard denial appeal process, you have options: (1) Review your signed provider contract to confirm the fee schedule percentage or rates, (2) Request a copy of the payer's fee schedule from your provider relations representative, (3) If the fee schedule amount does not match your contract, file a contract dispute (not an appeal), (4) For Medicare CO-45 adjustments, verify the Medicare fee schedule amount through the CMS website, (5) If the payer applied the wrong fee schedule (e.g., Medicare when you're a commercial payer), contact the payer for correction, (6) If you believe the fee schedule is incorrectly configured in the payer's system, request a system review. CO-45 adjustments should be tracked for accuracy but are NOT denial appeals.

**Q: What is the difference between a 997 and a 277CA?**
**A:** The 997 Functional Acknowledgment confirms that an electronic claim file (X12 837 transaction) was received at the technical level — it confirms the format was valid and the file was accepted by the clearinghouse or payer. If you get a 997 with an "R" (Rejected) status, the entire file was rejected and must be resubmitted. The 277CA (Health Care Claim Acknowledgment) is a more detailed, claim-level acknowledgment. It tells you the status of EACH INDIVIDUAL CLAIM in the batch — accepted (A), rejected (R), or pending (P). The 277CA also includes specific error codes at the claim level. For timely filing proof, the 277CA is stronger evidence because it shows the specific claim was received. Both acknowledgments should be saved as proof of timely filing, but the 277CA provides claim-level proof.

**Q: How do I handle a denial with OA-100?**
**A:** OA-100 means "The service/equipment/drug is not covered" — classified as an Other Adjustment (OA). This code is used when a service is not covered for reasons that are not purely contractual (which would be CO) or patient-related (which would be PR). Common reasons: (1) The drug/device does not have a valid HCPCS code, (2) The service is not a benefit under the patient's specific plan, (3) The FDA-approved indication does not match the condition, (4) A specific code does not exist for the service. Resolution steps: (1) Read any accompanying RARC to understand the specific reason, (2) If a valid code exists, correct the code and resubmit, (3) If the service is truly covered but coded incorrectly, submit with the correct coding, (4) If the service is not covered, determine if an exception or appeal path exists, (5) If using an NOC (not otherwise classified) code, provide supporting documentation and a detailed description.

**Q: Why do my paper remittance advices show codes I cannot find in the CARC list?**
**A:** Paper remittance advices (RAs) from some payers use PROPRIETARY denial codes, not standard CARCs. This is especially common with: (1) Smaller regional payers, (2) Medicaid plans (each state has unique codes), (3) Blue Cross Blue Shield plans (each of the 34 independent BCBS plans uses different code systems), (4) Worker's Compensation payers, (5) Dental payers (use ADA codes, not CARCs). These proprietary codes must be mapped to standard CARCs for analysis. Steps: (1) Look up the payer's code manual (often available on their provider portal), (2) Create a mapping table from their proprietary codes to CARCs, (3) Note that some proprietary codes may not have a direct CARC equivalent, (4) For electronic 835s, proprietary codes are typically mapped to standard CARCs by the clearinghouse. If you receive both electronic and paper RAs, the paper version sometimes shows the proprietary code while the electronic version shows the standard code.

**Q: What does N386 RARC mean?**
**A:** N386 means "This decision was based on documentation provided." This is one of the most common RARCs and it accompanies medical necessity denials (typically CO-50). When you see N386, it means the payer reviewed the documentation you submitted (or that was available) and determined, based on that documentation, that the service was not medically necessary. This does NOT mean the payer rejected your documentation — it simply states that their decision was based on what was in the record. To appeal: (1) Review what documentation was available to the payer, (2) Identify gaps in the documentation — what clinical information was missing or insufficient, (3) Gather additional clinical notes, test results, and physician statements that address the specific medical necessity criteria, (4) Resubmit with a comprehensive appeal that directly maps clinical findings to the payer's medical necessity criteria, (5) If the documentation was not submitted before, include a cover letter explaining it was previously unavailable.

**Q: How can I tell if a denial is a contractual write-off or a true denial?**
**A:** Look at the group code and the CARC combination: Contractual write-offs (not appealable, do not bill patient): CO-45 (fee schedule reduction), CO-59 (bundling/packaging), CO-69/70 (outlier adjustments), MA-series codes (Medicare payment methodology). True denials (appealable): CO-50 (medical necessity), CO-11 (diagnosis inconsistency), CO-197 (no auth), CO-4 (modifier issue), OA-23 (no auth), CO-16 (lacks info), CO-180 (invalid code). Also check the CLP02 claim status: if CLP02 is 1, 2, or 3 (processed), with CO-45, this is a payment reduction, not a denial. If CLP02 is 4 (denied), the entire claim was denied and every adjustment is a true denial. For service line denials (within a partially paid claim), look at the CAS segment — if the group code is CO and the amount equals the full charge for that line, it is a denial. If the amount is less than the charge and the CARC is 45, it is a contractual reduction.

**Q: What is CR-1 and why would I see it on a remittance?**
**A:** CR-1 means "Claim reversed/adjusted" — it is a Correction/Reversal code. When you see CR-1 on a remittance, it means the payer is reversing a PREVIOUSLY ISSUED PAYMENT. This can happen when: (1) The payer identified a duplicate payment, (2) The payer identified an overpayment, (3) A post-payment review found that the claim should not have been paid, (4) The claim was paid incorrectly based on incorrect data, (5) A retroactive coverage change occurred (patient lost coverage retroactively), (6) Coordination of benefits was identified after payment. When you see CR-1: (1) Do not spend the payment if you have not yet — the money will be recouped, (2) If the money was already deposited, prepare for an offset on future payments, (3) Determine why the reversal occurred before appealing, (4) If the reversal was in error, file an immediate appeal with supporting documentation showing the original payment was correct. CR-1 adjustments come with a corresponding negative dollar amount in the CAS segment.

**Q: What is the proper way to appeal a PI-20 adjustment?**
**A:** PI-20 means "Claim payment amount adjusted due to prior payment" — it is a Payer-Initiated adjustment. This occurs when the payer makes a retroactive adjustment to claim payment due to a prior payment being incorrect. Common scenarios: (1) The payer identified a prior overpayment and is recouping it, (2) A COB change after initial payment, (3) A retroactive coverage change, (4) A payment policy change applied retroactively. The best approach: (1) First, wait 60 days before appealing — PI adjustments sometimes reverse automatically, (2) Determine the reason for the PI adjustment by reviewing the RARCs and contacting the payer, (3) If the adjustment was made due to a valid reason (COB, retroactive eligibility loss), the appeal is unlikely to succeed, (4) If the adjustment was made due to a payer error (wrong code applied, wrong patient, wrong dates), submit a written appeal with supporting documentation, (5) PI adjustments typically cannot be appealed through the standard appeal process — you may need to go through the payer's provider dispute or claims correction process.

**Q: How do I interpret the "Quantity" field in a CAS segment?**
**A:** The CAS04 field (Quantity) represents the number of units affected by the adjustment. This is most relevant for denials based on number of units or visits. Examples: (1) CAS*CO*119*200*5 means an adjustment of $200 for 5 units where the benefit maximum was reached, (2) CAS*OA*23*150*3 means 3 units denied for no authorization at $50 per unit, (3) CAS*CO*48*100*2 means 2 units denied as exceeding expected frequency. When a service line has multiple units and some are denied, the quantity field tells you exactly which units were affected. If the quantity is blank or 1, only 1 unit was adjusted. This is critical for partial denials where the same CPT code has multiple units but only some are denied.

**Q: My 835 shows CAS*CO*50*0. What does a zero adjustment mean?**
**A:** A zero adjustment amount (CAS*CO*50*0) can indicate several things: (1) The denial was already applied at the claim level and the service line adjustment is informational, (2) The service line is informational and the actual financial adjustment is at the claim level CAS segment, (3) The payer is indicating a denial reason for the record even though the financial impact is zero (this can happen with overlapping adjustments), (4) A processing error in the 835. Zero adjustments should not be ignored — check the claim-level CAS segment for the financial adjustment. If the claim-level CAS also shows zero, contact the payer to clarify the 835. In most cases, the service line CAS with a zero adjustment means the financial impact was captured at another level.

**Q: How do I match RARCs to specific CARCs when there are multiple adjustments on a service line?**
**A:** In an 835, RARCs appear in REF segments that follow the CAS segment for a service line. The general rule: RARCs that appear AFTER a specific CAS segment apply to that CAS segment. However, in practice, the RARC may apply to the service line overall. If a service line shows:
```
SVC*HC:99213*100*75~
CAS*CO*45*25~
CAS*CO*50*30~
REF*HE*N386~
```
RARC N386 applies to the entire service line adjustment, explaining both the CO-45 and CO-50 adjustments. If you need specific mapping: (1) Some payer systems assign RARCs to specific CAS segments through the order they appear, (2) Multiple CAS segments may share the same RARC, (3) Each CAS segment can have its own RARC through additional REF segments, (4) In paper RAs, the remark code column generally applies to all adjustments on the line. For denials analysis, it is safest to associate all RARCs on a service line with all CARCs on that service line unless specific mapping is provided by the payer.