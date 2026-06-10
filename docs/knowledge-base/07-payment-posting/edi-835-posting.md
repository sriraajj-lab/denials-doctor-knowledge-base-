# EDI 835 — Health Care Claim Payment and Remittance Advice

## Overview

The EDI 835 transaction (Health Care Claim Payment/Remittance Advice) is the HIPAA-compliant electronic standard used by payers to communicate payment information and claim adjustment details to providers. It is the core transaction for the payment posting and reconciliation function in revenue cycle management. The 835 tells the provider:

- What claims were paid, denied, or adjusted
- How much was paid per claim and per service line
- What adjustments were applied and why
- Patient responsibility amounts
- Provider-level adjustments (lump sum payments, penalties, interest)

The 835 can be received in two formats:
- **Standalone ERA (Electronic Remittance Advice)**: No actual funds transferred; the provider must reconcile with the payment received separately
- **RFP (Request for Payment) 835**: Accompanies an EFT payment

---

## 1. Complete 835 Structure

### Transaction Envelope

```
ISA~... (Interchange Control Header)
  GS~HP~... (Functional Group Header — HP = Health Care Claim Payment)
    ST~835~0001 (Transaction Set Header)
      BPR~... (Financial Information)
      TRN~... (Reassociation Trace Number)
      REF~... (Check/EFT Trace Number, when applicable)
      DTM~... (Production Date)
      N1~PR~... (Payer Identification)
      N1~PE~... (Payee Identification)
      LX~1 (Header Number — first claim group)
        CLP~... (Claim Payment Information)
        NM1~QC~... (Patient Name)
        NM1~82~... (Rendering Provider)
        REF~... (Claim IDs — Payer Claim #, Patient Account #, etc.)
        DTM~... (Date — Service Date, Claim Received Date, etc.)
        AMT~... (Claim-Level Adjustment Amounts)
        AMT~AU~... (Claim Coverage Amount)
        QTY~... (Claim Count Information)
        MIA~... (Inpatient Adjudication Information — Medicare Part A)
        MOA~... (Outpatient Adjudication Information — Medicare Part B)
        PER~... (Contact Information)
        SVC~... (Service Line)
          REF~... (Service Line Reference IDs)
          DTM~... (Service Line Date)
          CAS~... (Service Line Adjustment)
          AMT~... (Service Line Amount)
          LQ~... (Service Line Remark Codes)
        CAS~... (Claim-Level Adjustment)
        REF~... (Claim Remark Codes via LQ)
        ...
      LX~2 (next claim group)
        ...
      PLB~... (Provider Level Adjustment)
      ...
    SE~... (Transaction Set Trailer)
  GE~... (Functional Group Trailer)
IEA~... (Interchange Control Trailer)
```

---

## 2. BPR Segment — Financial Information

The BPR segment provides summary financial data about the payment or adjustment.

```
BPR*C*12345.67*D*CHK*CHK12345***CHK*1234567890**01*021000021*DRAWN_ACCOUNT~
```

| Element | Description | Values |
|---|---|---|
| **BPR01** | Transaction Handling Code | `C` = Payment, `H` = Notification Only (no funds), `I` = Remittance Only, `U` = Adjustment |
| **BPR02** | Total Payment Amount | Total dollar amount of the payment. Must equal sum of all CLP03 amounts minus PLB adjustments |
| **BPR03** | Credit/Debit Flag | `D` = Debit (money leaving payer to provider), `C` = Credit (money taken back from provider) |
| **BPR04** | Payment Method | `ACH` = Automated Clearing House, `CHK` = Check, `WIR` = Wire, `NON` = Non-Payment Data |
| **BPR05** | Payment Format Code | `CCD` = Cash Concentration and Disbursement, `CTX` = Corporate Trade Exchange |
| **BPR06** | Check/EFT Trace Number | Unique identifier assigned by the payer's financial institution. Critical for reconciliation |
| **BPR07-BPR16** | DFI/Bank Information | Routing numbers, account numbers for EFT tracking |

### BPR Scenarios

| Scenario | BPR01 | BPR02 | BPR03 | BPR04 | Notes |
|---|---|---|---|---|---|
| **Regular payment** | C | 50000.00 | D | ACH | Standard EFT payment |
| **Check payment** | C | 50000.00 | D | CHK | Physical check |
| **Zero payment ERA** | H | 0.00 | D | NON | No funds; deny/adjust only |
| **Premium recoupment** | C | -1250.00 | D | ACH | Negative amount taken back |
| **Voided payment** | U | 0.00 | D | NON | Replaces previous payment |

---

## 3. TRN Segment — Reassociation Trace Number

The TRN segment links the 835 to the funding source (EFT or check).

```
TRN*1*CHK12345*021000021~
```

- **TRN01**: Trace Type Code — `1` = Current Transaction Trace Number
- **TRN02**: Reference Number — Matches BPR06 (check/EFT trace number). Also appears in the provider's bank statement for EFT payments
- **TRN03**: Originating Company ID — Payer's routing number or EFT ID

**Importance**: The TRN is the primary key for automatically matching electronic payments to the corresponding ERA in the provider's practice management system. Every EFT transaction from a payer should have a unique TRN that appears both in the 835 and in the provider's bank statement.

---

## 4. CLP Segment — Claim Payment Information

The CLP segment is the core claim-level payment record. Each CLP represents a single claim.

```
CLP*PATIENTACCT123*1*450.00*100.00*750.00*MC*CLAIM12345678*11*2~
```

| Element | Description | Values |
|---|---|---|
| **CLP01** | Patient Account Number | The provider's patient account/control number. Used for system-to-system cross-reference |
| **CLP02** | Claim Status Code | See status table below |
| **CLP03** | Monetary Amount — Paid | Amount paid to the provider for this claim |
| **CLP04** | Monetary Amount — Patient Responsibility | Total patient responsibility (deductible + coinsurance + copay + patient deductible remaining) |
| **CLP05** | Monetary Amount — Charge Amount | Amount originally billed by the provider (total charges) |
| **CLP06** | Claim Payment Remark Code | Remark code describing payment situation (e.g., MC = Medicare Crossover) |
| **CLP07** | Payer Claim Control Number | The unique claim number assigned by the payer (critical for appeals) |
| **CLP08** | Claim Filing Indicator Code | `11` = Medicare Part A, `12` = Medicare Part B, `13` = Medicaid, `14` = CHAMPUS, `15` = TRICARE, `16` = CHAMPVA, `17` = Group Health, `18` = HMO, `19` = Dental HMO, `MB` = Medicare Part B (alternate) |
| **CLP09** | Claim Frequency Code | `1` = Original, `2` = Replacement, `3` = Void/Cancel, `7` = Replacement of Prior Replacement |
| **CLP10** | Patient Status Code | Code indicating patient status (discharge status for inpatient) |
| **CLP11** | Diagnosis-Related Group (DRG) Code | DRG code for inpatient claims |

### Claim Status Codes (CLP02)

| Code | Status | Description |
|---|---|---|
| **1** | Processed as Primary | The payer processed the claim as the primary payer. Payment reflects primary liability |
| **2** | Processed as Secondary | The payer processed as secondary payer. Payment reflects remaining liability after primary paid |
| **3** | Processed as Tertiary | The payer processed as tertiary payer |
| **4** | Denied | The claim was denied. CLP03 = 0.00. CAS segment contains denial reason |
| **5** | Processed as Primary, Forwarded to Payer | Forwarded to another payer (e.g., Medicare-to-Medicaid crossover) |
| **19** | Processed as Primary, but Captured Interest | Paid primary with interest (late payment penalties) |
| **22** | Reversal of Previous Payment | Reversing a previous payment — should cause an offset in AR |
| **25** | Payment Reversed Due to Corrected Claim | Reversal because a corrected/replacement claim was submitted |
| **27** | Information Only | No payment, informational only |

---

## 5. CAS Segment — Claim Adjustment Groups

The CAS segment is the most important segment for denial management. It contains the detailed adjustment information explaining why a claim was not paid in full.

### CAS Segment Structure

```
CAS*PR*45.00*45.00********2~
CAS*CO*45.00*45.00~
CAS*OA*10.00*10.00~
```

There are **three claim adjustment groups** that can appear:

| Group | Code | Description | Purpose |
|---|---|---|---|
| **CAS01** | `PR` | Patient Responsibility | Deductible, coinsurance, copay amounts the patient owes |
| **CAS01** | `CO` | Contractual Obligation | Amounts written off per contract (e.g., network discount, timely filing) |
| **CAS01** | `OA` | Other Adjustment | Adjustments that don't fit PR or CO (e.g., credit applied, interest) |
| **CAS01** | `PI` | Payor Initiated | Adjustments initiated by the payer (e.g., refund recovery) |
| **CAS01** | `CR` | Correction/Reversal | Correction to a previously reported adjustment |
| **CAS01** | `IH` | Information Hold | Adjustment not yet finalized |

### CAS Segment Elements (per adjustment group)

Each group can contain up to **six adjustment pairs**:

```
CAS*CO*45.00*45.00*CO*23.00*23.00*CO*12.00*12.00~
```

| Element | Description |
|---|---|
| **CAS01** | Adjustment Group Code (PR, CO, OA, PI, CR, IH) |
| **CAS02** | Claim Adjustment Reason Code (CARC) — numeric code |
| **CAS03** | Monetary Amount — dollar amount of this adjustment |
| **CAS04** | Quantity — quantity of units adjusted (optional) |
| **CAS05-CAS07** | Next adjustment pair (same structure) |
| **CAS08-CAS10** | Next adjustment pair (same structure) |

### Common CARC Codes by Group

**Patient Responsibility (PR):**

| CARC | Description |
|---|---|
| 1 | Deductible |
| 2 | Coinsurance |
| 3 | Copayment |
| 23 | Patient Charge for Out-of-Network |
| 24 | Patient Interest |
| 25 | Patient Late Payment Penalty |
| 96 | Non-Covered Charge — Patient Responsibility |
| 149 | Patient Charge Exceeds Fee Schedule |
| 152 | Other Adjustment — Patient Responsibility |

**Contractual Obligation (CO):**

| CARC | Description |
|---|---|
| 45 | Charge Exceeds Fee Schedule/Maximum Allowable |
| 50 | Timely Filing |
| 97 | Payment is Correct — No Further Payment |
| 109 | Claim Not Covered by This Payer/Contract |
| 119 | Benefit Maximum Exceeded |
| 140 | Prior Authorization Not Obtained |
| 150 | Payer Responsibility Only for Services In-Network |
| 151 | Payer Reimbursement for Out-of-Network |
| 204 | Authorization Expired |
| 205 | Authorization Not Valid for This Provider |
| 206 | Authorization Not Valid for This Service |
| 207 | Authorization Not Valid for This Date Range |

**Other Adjustment (OA):**

| CARC | Description |
|---|---|
| 18 | Duplicate Claim/Services |
| 23 | Mutual Agreement — No Payment |
| 42 | Charge Amount Exceeds Expected Amount (Manual Review) |
| 100 | Interest Payment |
| 101 | Payment Adjustment Due to Previous Payment |
| 117 | Credit Applied |
| 128 | Coverage Based on Employment Status |
| 131 | Claim Specific Negotiated Adjustment |
| 157 | Interest Payment (Claim Level) |
| 164 | Professional Provider Not in Network |
| 236 | This Procedure Code/Modifier Not Payable |
| 272 | Coverage Gap — Patient Responsibility for Premiums |
| 274 | Non-Covered Service(s) |
| A1 | Claim/Service Denied — Additional Payment Not Made |

---

## 6. SVC Segment — Service Line Payment

The SVC segment provides payment details at the individual service (procedure) level. It appears within the CLP claim group after the claim-level information.

```
SVC*HC:99213*175.00*125.00*1**2~
```

| Element | Description |
|---|---|
| **SVC01** | Composite Medical Procedure Identifier — Qualifier:code (HC:CPT, N4:NDC, AD:Revenue) |
| **SVC02** | Line Item Charge Amount — Amount originally billed for this service line |
| **SVC03** | Line Item Paid Amount — Amount paid for this service line |
| **SVC04** | Revenue Code (institutional claims) |
| **SVC05** | Units of Service Paid — Number of units paid (may differ from units billed) |
| **SVC06** | Original Units of Service — Units originally billed (if different from SVC05) |
| **SVC07** | Service Line Status — `1` = Billed, `2` = Denied/Pended, `3` = Not Billable |

### SVC-Level CAS Segments

Just like claim-level CAS segments, the SVC can have its own CAS adjustments:

```
SVC*HC:99214*150.00*100.00*1~
CAS*CO*45.00*50.00~
```

This means the 99214 service was billed at $150, paid at $100, with a $50 contractual adjustment.

### SVC-Level LQ Segment — Remark Codes

```
LQ*HE*N130~
```

- **LQ01**: Qualifier — `HE` = Claim-Level Remark Codes
- **LQ02**: Remark Code — Supplemental information about the payment decision (e.g., N130 = "Consultation code reported. Payment based on evaluation and maintenance code.")

---

## 7. Revenue Code Mapping for Institutional Claims (837I / 835)

For hospital/institutional claims, the SVC segment uses revenue codes:

| Revenue Code | Description | Service Code |
|---|---|---|
| 0250 | Pharmacy - General | N4:NDCCode |
| 0300 | Lab - General | N4:NDCCode |
| 0310 | Lab - Chemistry | HC:CPT |
| 032x | Radiology | HC:CPT |
| 036x | Operating Room | HC:CPT |
| 0450 | Emergency Room | HC:CPT |
| 051x | Clinic | HC:CPT |
| 0762 | Specialty Drugs | N4:NDCCode |
| 0636 | Drugs Requiring Detailed Coding | N4:NDCCode |

---

## 8. MIA and MOA Segments — Medicare-Specific

### MIA Segment (Medicare Part A — Inpatient)

The MIA segment provides Medicare Part A-specific inpatient payment information:

```
MIA*0*12345.67*100*9999.00**5000.00~
```

| Element | Description |
|---|---|
| **MIA01** | Covered Days or Visits Count |
| **MIA02** | Total Covered Charges |
| **MIA03** | Lifetime Psychiatric Days |
| **MIA04** | DRG Amount |
| **MIA05** | Disproportionate Share Hospital (DSH) Adjustment |
| **MIA06** | Indirect Medical Education (IME) Adjustment |
| **MIA07** | Capital IME Amount |
| **MIA08** | Operating DSH Amount |
| **MIA09** | Capital DSH Amount |
| **MIA10** | Outlier Amount |
| **MIA11** | Pass-Through Amount |
| **MIA12** | Federal Specific Payment Adjustment |
| **MIA13** | Total Deductible and Coinsurance Amount |
| **MIA14** | Blood Deductible |
| **MIA15** | Non-Payable Professional Component Adjustment |

### MOA Segment (Medicare Part B — Outpatient)

The MOA segment provides Medicare Part B outpatient payment information:

```
MOA*110.00*20.00*30.00~~~
```

| Element | Description |
|---|---|
| **MOA01** | Reimbursement Rate |
| **MOA02** | HCPCS Payable Amount |
| **MOA03** | Claim Payment Remark Code |
| **MOA04** | Claim Payment Remark Code (additional) |
| **MOA05** | Claim Payment Remark Code (additional) |
| **MOA06** | Medicare Outpatient Adjudication Payment Adjustment Percentage |
| **MOA07** | Claim Payment Remark Code (additional) |
| **MOA08** | Claim Payment Remark Code (additional) |
| **MOA09** | Claim Payment Remark Code (additional) |

---

## 9. PLB Segment — Provider Level Adjustment

The PLB segment appears at the end of the 835 transaction and represents adjustments that apply at the provider level (not to individual claims). These are adjustments to the total payment amount.

```
PLB*1234567890*20250610*50*50.00*FB*50.00~*
*FB1250.00*
```

### PLB Adjustment Reason Codes

| Code | Description | Example |
|---|---|---|
| 50 | Late Filing Penalty | Penalty for claims submitted past timely filing limit |
| 51 | Interest Payment | Interest paid for late payment |
| 52 | Refund of Previous Overpayment | Payer recouping money paid in error |
| 53 | Credit Balance Refund | Refund for credit balance |
| 70 | Premium Payment | Premium payment for health insurance plan |
| 71 | Payment for Prior Period | Retroactive payment adjustment |
| 72 | Charity Adjustment | Charity care write-off |
| 73 | Risk Adjustment Payment | Risk adjustment payment for Medicare Advantage |
| 74 | Reporting Requirement Incentive | EHR or quality reporting incentive |
| 75 | Administrative Fee | Administrative fee assessed |
| 76 | Payment for Supplemental Coverage | Supplemental coverage payment |
| 77 | Settlement Payment | Settlement payment |
| 78 | Overpayment Recoupment | Recoupment of prior overpayment |
| AA | Audit Adjustment | Post-audit adjustment |
| FB | Favorable Adjustment | Lump sum or percentage increase to payment |
| L6 | Interest Owed on Claim/Service | Interest owed by payer |
| WO | Overpayment Recovery | Overpayment recovered |

### PLB Example — Interest Payment

```
PLB*1234567890*20250610*51:INTEREST*12.50~
```

This shows $12.50 interest paid for delayed payment.

### PLB Example — Overpayment Recoupment

```
PLB*1234567890*20250610*52:OVERPYMT*250.00~
```

This shows $250.00 being recouped from the current payment for a previous overpayment.

---

## 10. Mapping 835 to Accounts Receivable

### Standard AR Posting Logic

| 835 Element | AR Impact | Description |
|---|---|---|
| **CLP05** (Charge Amount) | Original Charge | The amount the provider originally billed. Used to verify charge matches what was billed |
| **CLP03** (Paid Amount) | Payment | Applied to the claim balance. Reduces AR |
| **CLP04** (Patient Responsibility) | Patient Balance | Amount moved from insurance to patient responsibility |
| **CAS:PR** | Patient Adjustment | Patient deductible, coinsurance, copay — moves to patient balance |
| **CAS:CO** | Contractual Adjustment | Written off. Reduces total AR but not patient AR |
| **CAS:OA** | Other Adjustment | Various — may write off or transfer |
| **SVC03** (Line Paid) | Service Line Payment | Payment allocated to specific line item |
| **PLB** | Provider Adjustment | Adjusts total payment, not claim-specific |

### Posting Algorithm

```
Step 1: Parse CLP segment
  - Identify claim: match CLP01 (patient account #) to AR record
  - Apply CLP05 as charge verification (flag if different from billed charge)

Step 2: Parse CAS segments (claim-level)
  - For each CAS group (PR, CO, OA):
    - Extract adjustment reason codes and amounts
    - Post PR amounts to patient responsibility
    - Post CO amounts to contractual write-off
    - Post OA amounts to other adjustment

Step 3: Apply CLP03 as payment
  - Post payment amount to the claim
  - Balance = CLP05 - CLP03 - sum(CAS amounts)

Step 4: Parse SVC segments
  - Post line-level payments to individual service lines
  - Apply line-level CAS adjustments

Step 5: Post PLB adjustments
  - Adjust total payment or create separate adjustment records

Step 6: Reconcile
  - Verify: BPR02 = sum(all CLP03) + sum(all PLB amounts)
  - Verify: For each CLP, CLP05 = CLP03 + CLP04 + sum(CO) + sum(OA)
```

---

## 11. Coordination of Benefits (COB) in 835

When multiple insurance plans are involved, the 835 provides COB information.

### Primary vs. Secondary Processing

**Primary Payer (CLP02 = 1):**
```
CLP*ACCT001*1*500.00*50.00*750.00~
CAS*PR*1*100.00*100.00~
CAS*PR*2*50.00*50.00~
CAS*CO*45*100.00*100.00~
```
- Primary paid $500 after applying $100 deductible, $50 coinsurance, and $100 contractual adjustment

**Secondary Payer (CLP02 = 2):**
```
CLP*ACCT001*2*40.00*10.00*750.00~
CAS*OA*23*50.00*50.00~
CAS*PR*2*10.00*10.00~
```
- Secondary paid $40. The OA group with code 23 indicates the claim was adjusted based on primary payment. Patient owes remaining $10 coinsurance.

### Crossover Claims (Medicare to Medicaid)

- **CLP06** = "MC" (Medicare Crossover) indicates the claim was auto-forwarded from Medicare to a secondary payer
- Medicare is always primary for beneficiaries who also have Medicaid
- The 835 for crossover claims may show **CLP02 = 19** (Processed as Primary, Captured Interest)
- The secondary payer (Medicaid) often sends a separate 835 with CLP02 = 2

### COB Processing Logic

```
When CLP02 = 1: This is the primary payment. Post payment and adjustments.
                 Create expected secondary information for the next submission.

When CLP02 = 2: This is secondary payment. Only post additional payment.
                 Do NOT re-apply adjustments from primary — they are already applied.
                 Secondary should only pay what primary left unpaid (up to secondary max).

When CLP02 = 3: Tertiary payment. Rare. Typically covers remaining after primary and secondary.

When CLP06 = MC: Medicare crossover. Automatically forward to Medicaid/Medigap.
```

---

## 12. Medicare 835 Quirks

### Medicare Part A (Inpatient) Adjustments

The MIA segment contains Medicare Part A-specific adjustments that affect payment calculation:

- **MIA04**: DRG Amount — the base payment rate for the DRG
- **MIA05**: DSH Adjustment — additional payment for disproportionate share hospitals
- **MIA06**: IME Adjustment — additional payment for teaching hospitals
- **MIA10**: Outlier Amount — extra payment for high-cost cases exceeding the outlier threshold
- **MIA13**: Total Deductible and Coinsurance Amount — patient responsibility portion

### Medicare Part B (Outpatient) Adjustments

The MOA segment contains Medicare Part B-specific adjustments:

- **MOA01**: Reimbursement Rate — the APC or fee schedule rate
- **MOA02**: HCPCS Payable Amount — the amount Medicare paid for this HCPCS code
- **MOA06**: Medicare Outpatient Adjudication Payment Adjustment Percentage — for outlier or pass-through adjustments

### Medicare Unique CAS Codes

| CARC | Medicare-Specific Meaning |
|---|---|
| 1 | Medicare Part A Deductible (per benefit period) |
| 2 | Medicare Part B Coinsurance (typically 20%) |
| A1 | Claim/Service Denied — Additional Payment Not Made |
| 45 | Charge Exceeds Medicare Fee Schedule |
| 97 | Payment is Correct — Explanation Only |
| 119 | Benefit Maximum Exceeded (e.g., PT cap, inpatient days) |
| 204 | Authorization Not Obtained for Medicare Advantage |
| 205 | Not Covered — Medicare Statutory Exclusion |

---

## 13. 835 Payment Reconciliation Process

### Daily Reconciliation Steps

1. **Receive 835**: From clearinghouse or direct from payer
2. **Validate BPR**: Confirm total matches deposit/check amount
3. **Parse each CLP**: Match each CLP to patient account in PMS
4. **Post payments**: Apply CLP03 to each claim
5. **Post adjustments**: Apply CAS adjustments by type
6. **Post patient balance**: Move PR amounts to patient statement
7. **Flag denials**: Identify CLP02 = 4 claims for denial management
8. **Reconcile totals**: BPR02 = sum(CLP03) +/- PLB
9. **Post PLB adjustments**: Apply provider-level adjustments
10. **Confirm end-of-day totals**: Match to deposit/check amount

### Common Posting Errors

| Error | Cause | Resolution |
|---|---|---|
| **Unmatched CLP** | Patient account in 835 doesn't match PMS | Search by payer claim number or SSN; manual crosswalk |
| **Misapplied CAS** | PR adjustments posted as CO or vice versa | Reversing journal entry; re-post with correct group |
| **Duplicate posting** | Same 835 processed twice | Reverse the duplicate; verify 835 is only processed once |
| **PLB not posted** | Provider-level adjustment missed | Manual journal entry; verify all PLB segments are captured |
| **Crossover missed** | Secondary payer 835 not processed | Verify COB setup; ensure secondary claim is submitted |
| **CLP05 charge mismatch** | Billed amount differs from PMS | Investigate: was claim amended/resubmitted? |

---

## 14. 835 Integration with RCM Systems

### Required Data Flow

```
Payer
  |
  v
Clearinghouse (e.g., Change Healthcare, Availity, Waystar)
  |
  v
Revenue Cycle Management System
  |
  +---> Payment Posting Module
  |       - Parse 835
  |       - Match CLP to AR records
  |       - Post payments, adjustments, patient balances
  |       - Generate daily reconciliation report
  |
  +---> Denial Management Module
  |       - Flag CLP02=4 claims
  |       - Extract CAS reason codes
  |       - Route to appropriate work queue
  |
  +---> Reporting Module
          - Payment comparisons (expected vs actual)
          - Payer performance metrics
          - AR aging updates
```

### System Validation Rules

| Rule | Description | Action if Violated |
|---|---|---|
| **Balance check** | CLP03 + PR + CO + OA = CLP05 | Flag for manual review |
| **Total check** | BPR02 = sum(CLP03) + PLB | Generate reconciliation exception |
| **CARC validation** | All CARC codes are valid, up-to-date codes | Map unknown codes; update code table |
| **NPI validation** | Provider NPI in 835 matches PMS | Investigate payer setup |
| **Date validation** | Payment date is reasonable | Check for stale/late payments |

---

## 15. Q&A Pairs for Agent Training

**Q:** What does CLP02 = 4 mean and how should the system handle it?
**A:** CLP02 = 4 means the claim was denied. CLP03 (paid amount) will be 0.00. The CAS segment will contain the denial reason codes. The system should: (1) Flag the claim as denied in AR. (2) Extract the CARC codes from the CAS segment. (3) Route the claim to the denial management work queue. (4) Generate an appeal letter template based on the CARC codes. (5) Do NOT post as a patient balance unless PR adjustments are present indicating patient responsibility.

**Q:** What is the difference between the CAS:PR, CAS:CO, and CAS:OA adjustment groups?
**A:** CAS:PR = Patient Responsibility adjustments (deductible, coinsurance, copay). These amounts are moved to the patient's balance. CAS:CO = Contractual Obligation adjustments (network discounts, timely filing, authorization issues). These are written off as contractual adjustments and never billed to the patient. CAS:OA = Other Adjustments (credits, interest, mutual agreement amounts). These fall outside standard patient or contractual categories and may require special handling.

**Q:** How does the 835 handle coordination of benefits (COB)?
**A:** The 835 handles COB through CLP02 status codes: CLP02=1 means processed as primary, CLP02=2 means processed as secondary, CLP02=3 means processed as tertiary. CAS:OA with adjustment code 23 (Mutual Agreement/No Payment) is commonly used by secondary payers to indicate the adjustment was due to primary payment. The CLP06 element can show "MC" for Medicare crossover claims. The 835 does NOT include the primary EOB detail — it only shows how the current payer processed the claim.

**Q:** What does a zero-payment 835 look like and how should it be processed?
**A:** A zero-payment 835 has BPR01 = "H" (Notification Only) and BPR02 = 0.00. All CLP02 codes will show status 4 (Denied) with corresponding CAS adjustment amounts. The 835 is still important because it contains the denial reasons. The system should process all CLP and CAS segments to update AR status and denial tracking, even though no payment was received.

**Q:** What is the PLB segment and how is it different from claim-level adjustments?
**A:** The PLB (Provider Level Adjustment) segment applies at the provider level, not to individual claims. It appears after all CLP segments and adjusts the total payment amount. Examples include interest payments (code 51), overpayment recoupments (code 52), late filing penalties (code 50), and risk adjustment payments (code 73). Unlike CAS adjustments which affect specific claims, PLB adjustments affect the provider's total payment. The system must verify: BPR02 = Sum(CLP03) + Sum(PLB amounts).

**Q:** How should a system reconcile the BPR02 total with the sum of CLP03 payments?
**A:** The system must calculate: BPR02 should equal sum of all CLP03 paid amounts, minus any PLB deduction amounts (e.g., recoupments), plus any PLB addition amounts (e.g., interest). This is the fundamental 835 integrity check. If the values do not match, the ERA should be flagged for manual review. Common causes of mismatches include: PLB adjustment not properly parsed, claims in the 835 that were already posted from a previous ERA, or the ERA covers multiple payments.

**Q:** What is the purpose of the TRN segment and how is it used for EFT reconciliation?
**A:** The TRN (Reassociation Trace Number) segment links the 835 to the EFT payment. TRN02 contains a trace number that appears both in the 835 and in the provider's bank statement for the corresponding EFT transaction. The practice management system should match the TRN from the 835 against the bank feed to automatically reconcile payments. This enables straight-through processing where payments post automatically without manual intervention.

**Q:** How does the 835 handle Medicare Part A inpatient payments differently from Part B outpatient?
**A:** Medicare Part A 835s include the MIA segment with DRG payment information, DSH adjustments, IME adjustments, and outlier amounts. The SVC segment in Part A 835s uses revenue codes (e.g., 0360 for OR) rather than CPT codes. Medicare Part B 835s include the MOA segment with APC rates and HCPCS payable amounts. Part B SVC segments use CPT/HCPCS codes. The MIA and MOA segments provide the specific Medicare calculation logic needed to validate that the payment is correct.

**Q:** What CARC codes indicate an authorization-related denial?
**A:** Key authorization-related CARCs: 140 (Prior Authorization Not Obtained), 204 (Authorization Expired), 205 (Authorization Not Valid for This Provider), 206 (Authorization Not Valid for This Service), 207 (Authorization Not Valid for This Date Range). These appear in the CAS:CO group and represent contractual obligation adjustments — the amount is written off, not billed to the patient (unless the patient signed an ABN).

**Q:** What is the relationship between the CLP and SVC segments in an 835?
**A:** The CLP segment provides claim-level payment information (total paid, total adjustments, patient responsibility). The SVC segments within the CLP group provide line-item detail for each service billed on the claim. The sum of all SVC paid amounts within a claim should equal CLP03 (the claim-level paid amount). If SVC segments are present, they provide the detail needed for service-level payment posting. If no SVC segments exist, the provider has only claim-level payment data.

**Q:** How should a system handle a 835 with a CLP02 = 22 (Reversal of Previous Payment)?
**A:** CLP02 = 22 indicates the payer is reversing a previously submitted payment. The system should: (1) Locate the original payment posting for this claim. (2) Create a reversal entry that exactly offsets the original payment. (3) Reset the claim's AR status to unpaid. (4) Flag the claim for investigation — reversals can be due to corrected claims, audits, or recoupments. (5) The next 835 may include the corrected payment as a regular CLP.

**Q:** What is the difference between a claim-level CAS and a service-line CAS?
**A:** A claim-level CAS appears after the CLP segment but before any SVC segments and applies adjustments to the claim as a whole. A service-line CAS appears within an SVC segment and applies adjustments to that specific line item. Both can exist in the same 835 — for example, a deductible (PR:1) applied at the claim level, and a contractual adjustment (CO:45) applied at the service line level because only certain CPT codes exceeded the fee schedule.

**Q:** How does the 835 handle patient copay, deductible, and coinsurance?
**A:** These appear in the CAS:PR (Patient Responsibility) group: CARC 1 = Deductible, CARC 2 = Coinsurance, CARC 3 = Copayment. The dollar amounts in these adjustments represent the patient's financial responsibility. The system should: (1) Post the PR amounts to the patient's account as a transfer from insurance to patient. (2) Generate a patient statement reflecting these amounts. (3) Track deductible accumulation for the patient's plan year. (4) The CLP04 element provides the total patient responsibility, which should equal the sum of all PR adjustments.

**Q:** What is the 835 transaction set identifier and functional group identifier?
**A:** The 835 transaction set identifier is "835" in the ST segment (ST*835*...). The functional group identifier in the GS segment is "HP" (GS*HP*...), which stands for Health Care Claim Payment. The transaction set name is "Health Care Claim Payment/Remittance Advice." The 835 is defined by the X12N implementation guide 005010X221 (for version 5010).

**Q:** What should a provider do when the 835 payment total (BPR02) does not match the sum of claim payments?
**A:** First, verify the 835 integrity: are PLB adjustments included? If PLB exists, recalculate: BPR02 = sum(CLP03) + sum(positive PLB) - sum(negative PLB). If still mismatched, check for: (1) Claims in the 835 that were previously posted (partial ERA). (2) Multiple checks/payments covered in one 835. (3) Voided or reversed claims. If the mismatch persists, contact the payer's provider service line for a corrected 835. Do not post until the discrepancy is resolved.

**Q:** How are multiple procedure payment reductions reflected in the 835?
**A:** Multiple procedure payment reductions (e.g., 50% reduction for second surgical procedure) appear as CAS:CO adjustments with appropriate CARC codes. Common codes include: CO:45 (Charge Exceeds Fee Schedule — payer reduces the fee for second procedure), CO:131 (Claim Specific Negotiated Adjustment — multiple surgery reduction), or CO:97 (Payment is Correct — explanation of reduction). The SVC segment for the reduced procedure will show a lower paid amount than the primary procedure even if the billed amounts are the same.

**Q:** What is the "RA" (Remittance Advice) remark code and where does it appear?
**A:** Remark codes appear in the LQ (Healthcare Remark Codes) segment following the CAS segment or SVC segment. LQ01 = "HE" for Claim-Level Remark Codes. Remark codes are alpha-numeric (e.g., N130, M2, MA01, N5). They provide additional explanation for the adjustment — for example, N130 = "Consultation code reported. Payment based on evaluation and maintenance code." They are informational and do not affect posting amounts.

**Q:** How does an 835 handle a claim that was submitted with multiple lines but paid for only some?
**A:** Each SVC segment within the CLP group represents a service line. Paid SVC lines will have positive SVC03 amounts. Denied service lines will have SVC03 = 0 and may include CAS adjustments showing the denial reason. The system should post payments only for SVC lines with positive SVC03 and apply CAS adjustments to the appropriate lines. The sum of all SVC03 amounts should equal CLP03.

**Q:** What is the "balance forward" or "negative plb" situation in 835?
**A:** A negative PLB (e.g., PLB*52*250.00~) appears when the payer is recouping money from a previous payment. This means the total check amount (BPR02) will be less than the sum of all CLP03 amounts. The system must subtract the negative PLB from the payment total during reconciliation. If the negative PLB exceeds the total payment, BPR02 could be negative, meaning the provider owes the payer money. This triggers a refund scenario.