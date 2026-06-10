# Payment Reconciliation

## Overview

Payment reconciliation is the process of matching expected payments against actual payments received from insurance payers and patients. It is a critical function within revenue cycle management that ensures providers are paid correctly according to their contracted rates. Reconciliation identifies underpayments, overpayments, denials, and trends that require corrective action.

Effective reconciliation impacts the financial health of a practice directly: a 1% improvement in collection rates for a $10M practice equals $100,000 in additional revenue.

---

## 1. Accounts Receivable (AR) Aging

AR aging categorizes outstanding claim balances by the length of time they have remained unpaid. It is the primary metric for tracking revenue cycle health.

### AR Aging Buckets

| Bucket | Description | Industry Standard Status | Action Required |
|---|---|---|---|
| **0-30 Days** | Current — claims recently submitted | Normal | Monitor for payment |
| **31-60 Days** | Slightly aged — approaching payer timely filing | Caution | Follow up if no response |
| **61-90 Days** | Moderately aged — exceeds most timely filing limits | Warning | Call payer; review for issues |
| **91-120 Days** | Significantly aged — may require appeal | Critical | Escalate — supervisor review |
| **120+ Days** | Severely aged — high risk of non-payment | Crisis | Write-off probability assessment |

### AR Aging Report Example

| Bucket | Amount | Percentage | Target |
|---|---|---|---|
| 0-30 Days | $450,000 | 45% | >50% |
| 31-60 Days | $250,000 | 25% | <25% |
| 61-90 Days | $150,000 | 15% | <12% |
| 91-120 Days | $80,000 | 8% | <5% |
| 120+ Days | $70,000 | 7% | <3% |
| **Total AR** | **$1,000,000** | **100%** | |

### Industry Benchmarks for AR Aging

| Metric | Excellent | Good | Fair | Poor |
|---|---|---|---|---|
| **% AR Over 90 Days** | <10% | 10-15% | 15-25% | >25% |
| **% AR Over 120 Days** | <5% | 5-10% | 10-15% | >15% |
| **Days in AR** | <30 | 30-38 | 38-50 | >50 |

---

## 2. Expected Payment vs. Actual Payment

### Underpayment Identification

The core reconciliation question: "Did the payer pay what they were supposed to pay?"

**Calculation:**

```
Expected Payment = Billed Amount - Contractual Write-off
Actual Payment = Amount shown in CLP03 of 835
Underpayment = Expected Payment - Actual Payment (if positive)
```

**Example:**

| Item | Amount |
|---|---|
| Billed Charge (CLP05) | $750.00 |
| Expected Payment (per contract) | $500.00 |
| Actual Payment (CLP03) | $450.00 |
| **Underpayment** | **$50.00** |

### Underpayment Root Causes

| Cause | Description | Detection Method |
|---|---|---|
| **Wrong fee schedule** | Payer applied incorrect fee schedule (e.g., out-of-network instead of in-network) | Compare CLP03 to contracted fee |
| **Incorrect modifier application** | Multiple procedure reduction applied incorrectly | Audit SVC segments for CO:45 adjustments |
| **Bundling issue** | Payer bundled two procedures into one payment | Compare SVC lines to expected bundling rules |
| **Incorrect patient cost-sharing** | Deductible/coinsurance miscalculated | Compare CAS:PR to expected patient liability |
| **DRG miscoding** | Payer assigned wrong DRG (inpatient) | Compare MIA segment to expected DRG |
| **Site-of-service differential** | Paid at facility rate instead of office rate | Check place of service on SVC |
| **Global period issue** | Post-op procedure paid but should be included | Compare to Medicare global surgery rules |

### Automated Underpayment Detection Rules

| Rule ID | Rule Description | Alert Level |
|---|---|---|
| **UP-001** | Paid amount < 80% of expected amount | High |
| **UP-002** | Multiple procedures paid at full rate (no reduction) | Medium |
| **UP-003** | Modifier 51/59 applied incorrectly leading to reduced payment | High |
| **UP-004** | Bundling detected — payment less than sum of unbundled expected amounts | Medium |
| **UP-005** | Preventative service paid with patient cost-sharing (should be 100% covered) | High |
| **UP-006** | Payment differs from previous period for same CPT/diagnosis combination | Low |
| **UP-007** | Coinsurance calculated on incorrect allowable amount | High |

---

## 3. Contractual Adjustment Validation

Every payer contract specifies the reimbursement rate for each CPT/HCPCS code or a fee schedule percentage. The contractual adjustment is the difference between the billed charge and the contracted payment.

### Validation Process

```
Step 1: Retrieve contract terms for the payer and CPT code
Step 2: Calculate expected allowable amount
Step 3: Multiply by expected patient cost-sharing to get net expected payment
Step 4: Compare to actual CLP03
Step 5: If mismatch, flag for underpayment review
```

### Contractual Adjustment Formula

```
Allowable Amount = Contract Fee Schedule (or % of Medicare, or % of Billed)
Patient Liability = Deductible + Coinsurance + Copay
Expected Payment = Allowable Amount - Patient Liability
Contractual Adjustment = Billed Charge - Allowable Amount
```

### Contract Types and Validation Methods

| Contract Type | Example | Validation Method |
|---|---|---|
| **% of Medicare** | 150% of Medicare Fee Schedule | Look up Medicare allowable for CPT, multiply by 1.5 |
| **% of Billed** | 70% of billed charges | Multiply CLP05 by 0.70 |
| **Fixed Fee Schedule** | $50 for 99213, $75 for 99214 | Compare to fixed fee table |
| **% of MCR + carve-outs** | 125% of Medicare, E/M codes carved out | Multi-level lookup |
| **Blended** | Varies by service category | Complex multi-rule engine |
| **Case Rate** | $5,000 per inpatient admission | Compare to contract case rate |

### Validation Example

**Payer**: Blue Cross Blue Shield
**Contract**: 150% of Medicare Fee Schedule
**Service**: 99214 (Established patient, level 4)

| Item | Value |
|---|---|
| Medicare Fee Schedule for 99214 | $110.00 |
| Contract Rate (150%) | $165.00 |
| Billed Charge (CLP05) | $200.00 |
| Patient Copay (CLP04) | $25.00 |
| Expected Payment | $140.00 ($165 - $25) |
| Actual Payment (CLP03) | $140.00 |
| **Verdict** | **Correct** |

---

## 4. Underpayment Scenarios — Detailed Analysis

### Scenario 1: Wrong Fee Schedule Applied (Out-of-Network vs. In-Network)

**Symptom**: Payment is at a lower rate than contracted.
**Detection**: Compare actual allowable to contracted fee schedule for the specific CPT.
**Example**: Payer paid 120% of Medicare (OON rate) instead of 150% of Medicare (IN rate).
**Resolution**: File an appeal with a copy of the signed contract. Reference the specific contract clause with the reimbursement rate.

### Scenario 2: Incorrect Modifier Application

**Symptom**: Multiple procedure payment reduction (100%/50%/25%) applied incorrectly.
**Detection**: Review SVC segments. If two procedures have the same paid amount, the reduction may not have been applied (overpayment) or was applied incorrectly (underpayment).
**Example**: Claim billed 99214 (E/M) and 10060 (incision/drainage). Payer reduced 99214 by 50% instead of reducing the secondary procedure 10060.
**Resolution**: Appeal citing CMS multiple procedure reduction rules. E/M services should not be reduced when billed with a minor procedure.

### Scenario 3: Bundling Issue

**Symptom**: Two separately payable codes were combined into one payment.
**Detection**: CAS:CO adjustment with code 97 (Payment is Correct) or 45 (Fee Schedule) but paid amount is lower than expected.
**Example**: 93000 (EKG) and 99214 (office visit). Payer bundled EKG into visit. Contract allows separate payment for EKG with modifier 25 on E/M.
**Resolution**: Confirm modifier 25 was on claim. Appeal with NCCI unbundling reference showing the codes are separately payable with modifier 25.

### Scenario 4: Site-of-Service Differential Error

**Symptom**: Professional service paid at the facility rate instead of the non-facility rate.
**Detection**: The paid amount is significantly lower than expected (facility rate is typically 50-70% of non-facility rate).
**Example**: 99214 performed in office (POS 11). Paid at $75 (facility rate) instead of $110 (non-facility rate).
**Resolution**: Verify the place of service on the original claim. If POS 11 was correctly submitted, appeal with a copy of the claim and applicable Medicare/NCCI guidelines.

### Scenario 5: Incorrect Patient Cost-Sharing Application

**Symptom**: Patient deductible or coinsurance applied when benefit maximum was not exceeded.
**Detection**: CAS:PR adjustments exceed expected patient liability based on benefit plan design.
**Example**: Patient has $0 deductible plan but $50 deductible was applied in the 835.
**Resolution**: Verify patient's current deductible status through 270/271 eligibility. Appeal if deductible was applied in error.

### Scenario 6: DRG Miscoding

**Symptom**: Inpatient claim paid at wrong DRG rate.
**Detection**: Compare MIA04 (DRG Amount) to expected DRG amount for the ICD codes submitted.
**Example**: Claim submitted for pneumonia (DRG 193) but paid at DRG 194 (simple pneumonia with complication) with lower payment.
**Resolution**: Verify ICD-10-CM codes on the claim. Appeal if the DRG assignment does not match the clinical documentation.

---

## 5. Overpayment Handling

### Overpayment Identification

Overpayment occurs when the provider receives more than the contracted rate for a service. Causes include:

| Cause | Example | Detection |
|---|---|---|
| **Dual payment** | Both primary and secondary paid full amount | Payment exceeds expected total |
| **Incorrect fee schedule** | Payer applied higher-than-contracted rate | Compare to contracted rate |
| **Duplicate claim** | Same claim was submitted and paid twice | Identify duplicate CLP in 835 |
| **Incorrect billing** | Wrong CPT billed — paid higher than appropriate code | Retrospective chart audit |
| **System error** | Payer system glitch causing overpayment | Trend analysis |

### Overpayment Refund Process

```
Step 1: Verify overpayment amount and cause
Step 2: Calculate exact overpaid amount
Step 3: Determine refund method:
  - Check to payer
  - Deduction from future payment (adjustment in next 835)
  - Electronic refund via payer portal
Step 4: Document refund with refund tracking number
Step 5: Adjust AR to reflect refund
Step 6: Monitor next 835 to confirm refund was accepted
Step 7: Self-report to payer if required by contract
```

### Overpayment Refund Deadlines

| Payer Type | Refund Deadline | Notes |
|---|---|---|
| **Medicare** | 60 days from identification | Failure to refund within 60 days triggers False Claims Act exposure |
| **Medicaid** | 60 days (state-specific) | Similar to Medicare rules |
| **Commercial** | Per contract (typically 60-180 days) | May vary by payer |
| **Self-Audit Discovered** | As soon as reasonably possible | Document discovery date |

### CMS-838 Form (Medicare Credit Balance Report)

The CMS-838 is a quarterly report that Medicare providers must submit if they identify credit balances (overpayments). Key points:

- Required for all Medicare Part A and Part B providers
- Filed quarterly (30 days after quarter end)
- Includes all identified Medicare credit balances
- Includes refund amounts and dates
- Penalties for late/non-filing include payment suspension

### Repayment Plan

For large overpayments where immediate full repayment is not feasible:

- Contact the payer's provider reimbursement department
- Request a repayment plan (typically 6-12 months)
- Get terms in writing
- Track each installment against the plan
- Verify each installment appears correctly in subsequent 835s

---

## 6. Credit Balance Resolution

A credit balance exists when a patient's account shows a negative balance (the provider owes the patient money).

### Common Causes of Patient Credit Balances

| Cause | Description | Resolution |
|---|---|---|
| **Duplicate payment** | Patient paid in full, then insurance paid | Refund to patient |
| **Overpayment** | Patient paid more than responsibility | Refund to patient |
| **Payment after write-off** | Patient paid practice before write-off was applied | Refund to patient |
| **Insurance refund due** | Insurance paid after patient already paid | Verify patient refund |
| **Credit from adjustment** | Adjustment created negative balance | Apply to future services or refund |

### Credit Balance Resolution Process

```
Step 1: Identify credit balance (AR aging report shows negative patient balance)
Step 2: Research root cause:
  - Review payment history
  - Check EOB/835 for patient payments
  - Verify contractual adjustments
  - Confirm insurance payments
Step 3: Determine if refund is owed to patient or insurance:
  - Patient overpaid → Refund to patient
  - Insurance overpaid → Refund to insurance
  - Both overpaid → Refund to both
Step 4: Process refund:
  - Patient: Issue check with explanation of benefits
  - Insurance: Follow refund process (Section 5 above)
Step 5: Adjust AR: Write off credit balance
Step 6: Document refund with date, check number, recipient
```

### CMS-838 Self-Audit Triggers

A credit balance report must be filed when:

- Provider has any Medicare credit balance during the quarter
- Provider receives an overpayment that has not been refunded
- Provider identifies a duplicate Medicare payment
- Provider has adjustments that create credit balances
- Provider has credit balances >$0 at quarter end

---

## 7. Secondary Claim Processing

### Auto-Crossover Process

When a primary payer processes a claim, the system should automatically create the secondary claim:

```
Step 1: Receive 835 from primary payer
Step 2: Identify CLP06 = "MC" (Medicare Crossover) or COB indicator
Step 3: Calculate remaining balance after primary payment
Step 4: Automatically forward the claim to secondary payer
Step 5: Attach primary payer EOB/835 to secondary claim
Step 6: Monitor for secondary payment
```

### Secondary Claim Submission Rules

- **Timely filing**: Secondary payer timely filing often starts from the date of primary processing (not from date of service)
- **COB fields**: The secondary claim must include the primary payer's payment amount, adjustment amounts, and EOB details
- **Crossover for Medicare**: Medicare auto-crossovers to Medicaid for dually eligible beneficiaries via the MCS (Medicare Crossover System)
- **Medigap**: Medicare auto-crossovers to Medigap supplemental plans for beneficiaries with Medigap coverage

### Secondary Claim 837 Fields

| Loop | Segment | Element | Value |
|---|---|---|---|
| 2320 | SBR | SBR01 | P = Primary, S = Secondary, T = Tertiary |
| 2320 | AMT | AMT01 = D | Primary payment amount |
| 2320 | OI | OI03 = Y | Assignment of benefits |
| 2320 | NM1 | NM101 = IL | Primary payer name |
| 2320 | REF | REF01 = 2U | Payer claim number from primary 835 |
| 2330A | DTP | DTP03 | Date primary claim was processed |

---

## 8. Contract Management

### Tracking Payer Fee Schedules

Effective contract management requires:

1. **Centralized contract repository**: All signed payer contracts stored in a searchable system
2. **Fee schedule import**: Payer fee schedules loaded into the billing system for automatic expected payment calculation
3. **Effective date tracking**: Each contract version has effective and termination dates
4. **Reimbursement rate tables**: CPT/HCPCS code-level reimbursement rates or formulas
5. **Contract term monitoring**: Auto-renewal dates, termination notice periods

### Contract Terms to Track

| Term | Description | Impact on Reconciliation |
|---|---|---|
| **Reimbursement Rate** | % of Medicare, % of billed, or fee schedule | Directly determines expected payment |
| **Multiple Procedure Reduction** | 100/50/25 or other percentage | Affects expected payment when >1 procedure |
| **Coinsurance/Copay Policy** | Patient share percentage or flat amount | Affects expected net payment |
| **Bundling Policy** | Which codes are bundled | Affects payment for combination codes |
| **Modifier Policy** | How modifiers affect payment | Affects payment with modifiers 25, 59, etc. |
| **Incentive Programs** | Quality bonuses, P4P payments | Adjusts expected payment |
| **Hold Harmless** | No balance billing to patient | Affects write-off handling |
| **Termination Notice** | Days required to terminate | Affects contract enforcement |

### Contract Update Process

```
Step 1: Receive new contract or amendment from payer
Step 2: Verify against previous contract terms
Step 3: Identify changes in reimbursement rates or policies
Step 4: Update fee schedules in billing system
Step 5: Update expected payment calculation rules
Step 6: Test with sample claims
Step 7: Document effective date of new terms
Step 8: Train billing staff on changes
Step 9: Monitor first 30 days of claims under new contract
```

---

## 9. Key Performance Indicators (KPIs)

### Clean Claim Rate

**Definition**: Percentage of claims that pass all front-end edits and are accepted by the payer on first submission without errors.

**Calculation**:
```
Clean Claim Rate = (Claims Accepted First Submission / Total Claims Submitted) x 100
```

**Benchmarks**:
| Setting | Target | Industry Average |
|---|---|---|
| Physician Practice | >95% | 85-90% |
| Hospital | >92% | 80-88% |
| DME Supplier | >93% | 82-87% |
| Home Health | >90% | 78-85% |

### Days in Accounts Receivable (Days in A/R)

**Definition**: The average number of days between claim submission and payment receipt.

**Calculation**:
```
Days in A/R = (Total AR / Average Daily Charges) 
where Average Daily Charges = Total Charges for Period / Days in Period
```

**Alternative Calculation**:
```
Days in A/R = (Total AR / Total Charges) x Days in Period
```

**Benchmarks**:
| Metric | Target | Industry Average |
|---|---|---|
| **Overall Days in AR** | <30 days | 38-45 days |
| **Commercial Payer** | <25 days | 30-35 days |
| **Medicare** | <15 days | 12-18 days |
| **Medicaid** | <30 days | 35-50 days |
| **Self-Pay** | <45 days | 60-90 days |

### First-Pass Payment Rate

**Definition**: Percentage of claims that are paid in full on the first payment without requiring appeal or secondary submission.

**Calculation**:
```
First-Pass Payment Rate = (Claims Paid First Submission / Total Claims Finalized) x 100
```

**Benchmarks**:
| Setting | Target | Industry Average |
|---|---|---|
| Physician Practice | >70% | 60-70% |
| Hospital | >65% | 55-65% |

### Denial Rate

**Definition**: Percentage of submitted claims that are denied.

**Calculation**:
```
Denial Rate = (Denied Claims / Total Claims Submitted) x 100
```

**Benchmarks**:
| Setting | Target | Industry Average |
|---|---|---|
| Initial Denial Rate | <5% | 5-12% |
| Final Denial Rate (post-appeal) | <2% | 2-4% |
| Denial Overturn Rate | >60% | 40-55% |

### Net Collection Rate

**Definition**: The percentage of allowed amounts (contractual obligation) that the provider actually collects. This is the most important overall revenue cycle KPI.

**Calculation**:
```
Net Collection Rate = (Payments Received / (Charges - Contractual Adjustments)) x 100
```

Or more precisely:
```
Net Collection Rate = (Total Payments + Total Refunds) / (Expected Net Revenue) x 100
```

Where Expected Net Revenue = Total Charges - Expected Contractual Write-offs

**Benchmarks**:
| Metric | Target | Industry Average |
|---|---|---|
| **Net Collection Rate** | >95% | 90-95% |
| **Best Practice** | >98% | — |
| **Warning** | <90% | Significantly below industry average |

### Additional KPIs

| KPI | Calculation | Target |
|---|---|---|
| **Cost to Collect** | Total billing cost / Total collections | <3-5% |
| **Charge Lag** | Days between service date and charge entry | <3 days |
| **Claim Submission Lag** | Days between charge entry and claim submission | <2 days |
| **Payment Lag** | Days between claim submission and payment receipt | <30 days |
| **Bad Debt Rate** | Bad debt write-offs / Total charges | <2% |
| **Adjustment Rate** | Total adjustments / Total charges | Varies by contract (typically 30-50%) |
| **Accounts Receivable Turnover** | Total collections / Average AR balance | >8-12 times per year |
| **Percentage of AR Over 120 Days** | AR >120 / Total AR | <10% |

---

## 10. Reconciliation Reports

### Daily Reconciliation Report

**Purpose**: Ensure all payments received for the day are posted correctly.

| Column | Data Source | Description |
|---|---|---|
| Payment Date | BPR date or deposit date | Date payment was received |
| Payer Name | N1 segment | Insurance company name |
| Check/EFT # | TRN02 or BPR06 | Unique payment identifier |
| Total Payment | BPR02 | Total amount of payment |
| Claim Count | Count of CLP segments | Number of claims on ERA |
| Payment Amount | Sum of CLP03 | Total paid on claims |
| PLB Adjustment | Sum of PLB amounts | Provider-level adjustments |
| Balance | BPR02 - CLP total - PLB | Should be $0 |
| Posted Amount | System-generated | Actual amount posted in PMS |
| Posting Variance | Posted - Payment | Any difference requiring correction |

### Weekly AR Aging Report

**Purpose**: Track AR aging trends and identify collection problems.

| Aging Bucket | This Week | Last Week | Change | Target |
|---|---|---|---|---|
| 0-30 Days | $450,000 (45%) | $425,000 (43%) | +5.9% | >50% |
| 31-60 Days | $250,000 (25%) | $260,000 (26%) | -3.8% | <25% |
| 61-90 Days | $150,000 (15%) | $145,000 (15%) | +3.4% | <12% |
| 91-120 Days | $80,000 (8%) | $85,000 (9%) | -5.9% | <5% |
| 120+ Days | $70,000 (7%) | $65,000 (7%) | +7.7% | <3% |
| **Total AR** | **$1,000,000** | **$980,000** | **+2.0%** | — |
| **Days in AR** | **38** | **37** | **+1** | **<30** |

### Monthly Payer Comparison Report

**Purpose**: Compare payer performance and identify problematic payers.

| Payer | Claims Submitted | Clean Rate | Denial Rate | Days in AR | Net Collection Rate | Payment as % of Expected |
|---|---|---|---|---|---|---|
| Medicare | 500 | 98% | 2% | 14 | 98% | 99.5% |
| BCBS | 450 | 92% | 5% | 32 | 93% | 95.2% |
| UnitedHealthcare | 300 | 88% | 8% | 38 | 89% | 91.0% |
| Aetna | 200 | 94% | 4% | 28 | 95% | 97.1% |
| Cigna | 150 | 93% | 4% | 30 | 94% | 96.5% |
| Medicaid | 400 | 85% | 10% | 45 | 87% | 90.3% |
| **Total** | **2,000** | **92%** | **5.2%** | **30.2** | **92.8%** | **94.9%** |

### Monthly Underpayment Report

**Purpose**: Quantify losses from underpayments by payer.

| Payer | Claims with Underpayment | Total Underpayment | Recovery Rate | Amount Recovered |
|---|---|---|---|---|
| Medicare | 5 | $250 | 100% | $250 |
| BCBS | 22 | $4,500 | 45% | $2,025 |
| UnitedHealthcare | 35 | $8,750 | 30% | $2,625 |
| Aetna | 10 | $1,200 | 60% | $720 |
| Cigna | 8 | $900 | 50% | $450 |
| Medicaid | 15 | $2,250 | 50% | $1,125 |
| **Total** | **95** | **$17,850** | **38%** | **$7,195** |

### Denial Trend Report (Monthly)

**Purpose**: Identify the most common denial reasons and track resolution.

| Denial Reason | Frequency | Amount | Overturn Rate | Root Cause |
|---|---|---|---|---|
| Prior Authorization Not Obtained | 45 (22%) | $22,500 | 35% | Scheduling not checking auth status |
| Non-Covered Service | 30 (15%) | $15,000 | 20% | Beneficiary education needed |
| Timely Filing | 25 (12%) | $12,500 | 5% | Claims not submitted within 90 days |
| Medical Necessity | 20 (10%) | $10,000 | 60% | Insufficient documentation |
| Duplicate Claim | 15 (7%) | $7,500 | 10% | System duplicate detection failure |
| Other | 65 (32%) | $32,500 | 45% | Various |
| **Total** | **200** | **$100,000** | **35%** | |

---

## 11. Payer-Specific Reconciliation Quirks

### Medicare

- Consistently pays within 14 days (electronic filing)
- Payment is always at or below the Medicare Fee Schedule
- Does NOT pay more than the billed amount
- Crossover claims automatically forwarded to Medicaid/Medigap
- MAC (Medicare Administrative Contractor) specific rules apply
- Payer IDs: Noridian, Palmetto GBA, Novitas, CGS, etc.

### Medicaid

- Widely variable payment timeliness (30-90 days common)
- Fee schedules vary by state
- Some states require separate enrollment for each service type
- Retroactive eligibility creates payment reconciliation challenges
- TPL (Third Party Liability) coordination is complex

### Blue Cross Blue Shield

- Payment timeliness typically 15-30 days
- Each BCBS plan (state-specific) has its own fee schedule
- BCBS FEP (Federal Employee Program) different from commercial BCBS
- Inter-plan claims can cause delays

### UnitedHealthcare

- Payment timeliness 20-35 days
- Complex fee schedule with multiple product lines (Oxford, Golden Rule, UHC)
- Optum payment integrity reviews may recoup payments retroactively
- Claim edits may reduce payment based on internal logic

### Aetna

- Payment timeliness 15-30 days
- Clear reimbursement policy guidelines available
- Known for consistent application of multiple procedure rules

### Cigna

- Payment timeliness 20-30 days
- Known for bundling code pairs
- Payment integrity reviews common

---

## 12. Reconciliation Automation

### Automated Reconciliation Rules

| Rule | Trigger Action | Description |
|---|---|---|
| **Auto-post (no variance)** | Payment = Expected +- 2% | Post payment and adjustments automatically |
| **Manual review (small variance)** | Payment = Expected - 2-10% | Flag for review, queue for billing team |
| **Manual review (large variance)** | Payment < 80% of Expected | Flag for priority review, supervisor alert |
| **Zero payment** | CLP03 = 0 and CLP02 = 4 | Route to denial management |
| **Overpayment** | Payment > Expected | Flag for refund review |
| **PLB detected** | Any PLB segment | Flag for manual review and posting |
| **Crossover** | CLP06 = MC | Auto-crosslink to secondary submission |
| **Unmatched CLP** | Patient account not found | Place in unmatched queue for manual matching |

### Machine Learning for Reconciliation

Advanced reconciliation systems use ML to:

1. **Predict expected payments** based on historical payer behavior per CPT/diagnosis
2. **Identify recovery opportunities** by analyzing underpayment patterns
3. **Flag abnormal payment patterns** that deviate from historical norms
4. **Predict denial probability** before claim submission
5. **Auto-classify denials** into root cause categories
6. **Recommend appeal strategies** based on historical success rates

---

## 13. Q&A Pairs for Agent Training

**Q:** What is the difference between net collection rate and first-pass payment rate?
**A:** Net collection rate measures the total amount collected as a percentage of the total allowed amount (charges minus contractual adjustments). It reflects overall revenue capture effectiveness. First-pass payment rate measures the percentage of claims paid in full on the initial submission without any rework, appeals, or secondary submissions. Net collection rate addresses "did we collect what we should?" while first-pass rate addresses "how often did it go right the first time?"

**Q:** How is Days in Accounts Receivable (Days in AR) calculated and what is the target?
**A:** Days in AR = (Total Accounts Receivable / Average Daily Charges). Average daily charges = total charges for the period divided by the number of days in the period. For example, if total AR is $1,000,000 and average daily charges are $25,000, then Days in AR = 40. The target is under 30 days. The industry average is approximately 38-45 days. Higher numbers indicate slow payment or collection issues.

**Q:** What should a provider do when a payer underpays a claim?
**A:** (1) Identify the specific underpayment amount by comparing actual payment (CLP03) to the contractually expected amount. (2) Review the CAS adjustments to understand why the payer paid less. (3) If it is a contractual error (wrong fee schedule, wrong modifier application), gather documentation including the contract, the claim, and the 835. (4) File a formal appeal with the payer, referencing the contract. (5) Track the appeal and escalate if no response within 30 days. (6) If unresolved, consider filing a complaint with the state insurance commissioner.

**Q:** How does the AR aging report help identify revenue cycle problems?
**A:** The AR aging report categorizes unpaid claims by age buckets (0-30, 31-60, 61-90, 91-120, 120+ days). It helps identify: (1) Payer performance issues — if a specific payer has a disproportionate amount in older buckets. (2) Claims processing bottlenecks — if many claims are stuck at the same age. (3) Denial patterns — if denied claims are inflating older buckets. (4) Cash flow projections — older AR is less likely to be collected. (5) Staff workload priorities — which buckets need focused collection efforts.

**Q:** What is the 60-day overpayment refund rule for Medicare?
**A:** Under the Affordable Care Act, a provider who receives a Medicare overpayment must notify CMS and refund the overpayment within 60 days of identifying it. "Identification" means the date the provider has, or should have through reasonable diligence, determined the overpayment exists. Failure to refund within 60 days creates liability under the False Claims Act, including treble damages and penalties. This applies to all Medicare Part A and Part B providers.

**Q:** What is a clean claim rate and why is it important?
**A:** The clean claim rate is the percentage of claims that pass front-end edits and are accepted by the payer on first submission without errors. It is important because: (1) It directly impacts cash flow — clean claims pay faster. (2) It reflects the effectiveness of front-end RCM processes. (3) A low clean claim rate increases administrative costs from rework. (4) It is tracked by payers and regulators; Medicare Advantage plans report clean claim rates. The target is >95% for physician practices.

**Q:** How should a provider handle a credit balance on a patient's account?
**A:** (1) Research the cause — was it a duplicate payment, overpayment, or adjustment? (2) If the patient overpaid, issue a refund check with an explanation of the refund. (3) If insurance overpaid and created a patient credit, determine if the refund should go to the patient or the insurance plan. (4) Document the refund with the check number, date, and amount. (5) Adjust the patient account AR to zero. (6) For Medicare credit balances, file the CMS-838 quarterly report. (7) State laws may have escheatment requirements for unclaimed credits.

**Q:** What is the CMS-838 form and who needs to file it?
**A:** The CMS-838 (Hospital/Supplier Medicare Credit Balance Report) is a quarterly report that Medicare providers must file to report any identified credit balances (overpayments). It is required for all Medicare Part A and Part B providers, including hospitals, skilled nursing facilities, home health agencies, and physicians. The report is due 30 days after the end of each calendar quarter. Failure to file can result in payment suspension. The report includes the amount of each credit balance, the cause, and the refund date.

**Q:** How does secondary claim processing work after a primary payer has paid?
**A:** After receiving the primary 835, the system calculates the remaining balance (primary allowed amount minus primary payment minus patient responsibility). The secondary claim is automatically submitted with: (1) SBR segment indicating secondary processing. (2) AMT segment reporting primary payment amount. (3) OL segment or OI segment showing primary payment information. (4) The primary payer's claim number. The secondary payer pays up to their allowed amount minus what the primary already paid and what the patient owes. Medicare automatically crossovers to Medicaid and Medigap through the MCS system.

**Q:** What are the key differences between contractual adjustments (CO) and patient responsibility adjustments (PR)?
**A:** Contractual adjustments (CO) are amounts the provider writes off per the payer contract. They are never billed to the patient. Examples include network discounts, fee schedule differences, and non-covered services per contract. Patient responsibility adjustments (PR) are amounts the patient owes. Examples include deductibles, coinsurance, and copays. These amounts are moved from insurance AR to patient AR and the patient is billed. The critical distinction: CO adjustments reduce revenue permanently; PR adjustments represent collectible patient revenue.

**Q:** What is first-pass payment rate and what is a good target?
**A:** First-pass payment rate is the percentage of claims that are paid in full on the first submission without requiring any appeals, corrected claims, or secondary submissions. A good target is >70% for physician practices and >65% for hospitals. The industry average is 60-70% for practices and 55-65% for hospitals. Low first-pass payment rates indicate problems in front-end processes such as eligibility verification, prior authorization, coding accuracy, and claim submission.

**Q:** How can a provider identify underpayments from commercial payers?
**A:** Underpayments are identified through a multi-step process: (1) Build and maintain an accurate fee schedule for each payer contract. (2) For each received payment, calculate the expected payment: Expected = (Contracted Rate - Patient Responsibility). (3) Compare the expected payment to the actual CLP03 amount. (4) If actual < expected, flag as underpayment. (5) Review the CAS adjustments to understand why the payer paid less. (6) Aggregate underpayments by payer, CPT code, and reason. (7) File batch appeals for systematic underpayments. (8) Track recovery rates.

**Q:** What is the impact of charge lag on AR aging?
**A:** Charge lag is the time between when a service is provided and when it is entered into the billing system. Each day of charge lag delays the entire revenue cycle. For example, if charge lag is 5 days and the payer takes 30 days to pay, the effective Days in AR is 35 for those claims. Reducing charge lag from 5 days to 1 day improves Days in AR by 4 days. Best practice is charge entry within 24-48 hours of service. Each day of delay reduces net collection by approximately 0.5-1%.

**Q:** How does a provider reconcile a payment that includes both current claims and adjustments from prior periods?
**A:** (1) Separate the 835 into current-period claims and adjustment entries. (2) For current-period claims, post payments and adjustments normally. (3) For adjustments (CAS segments on previously paid claims), create offsetting entries — do not post as new claims. (4) Apply PLB adjustments to the provider-level payment account. (5) Ensure the total BPR02 equals all current claim payments plus all adjustments plus PLB. (6) Create a reconciliation report showing the breakdown between current and prior-period activity.

**Q:** What are the main payer performance metrics to track?
**A:** Key payer performance metrics include: (1) Clean claim rate per payer — which payers cause the most rework. (2) Days in AR per payer — which payers are slowest to pay. (3) Denial rate per payer — which payers deny the most claims. (4) Net collection rate per payer — which payers pay the lowest percentage of allowed amounts. (5) Underpayment total per payer — which payers systematically underpay. (6) Appeal overturn rate per payer — which payers respond to appeals. (7) Average payment lag per payer — days from claim submission to payment.

**Q:** What are the most common denial reasons that payment reconciliation identifies?
**A:** Based on industry data, the most common denial reasons identified through reconciliation are: (1) Prior authorization not obtained or expired (15-25% of denials). (2) Non-covered services or medical necessity (10-20%). (3) Timely filing — claim submitted after filing deadline (8-15%). (4) Duplicate claim submission (5-10%). (5) Coding errors (5-10%). (6) Missing or invalid claim data (5-8%). (7) Benefit plan exclusions (3-7%). (8) Coordination of benefits issues (3-5%).

**Q:** How does the reconciliation system handle the "expected payment" calculation when a claim includes multiple procedure code payment reductions?
**A:** For multiple procedure reductions (typically 100% for primary, 50% for second, 25% for subsequent), the expected payment calculation must: (1) Identify which procedure is primary (usually highest RVU or highest allowed amount). (2) Calculate expected payment for each procedure: Primary = 100% of fee schedule, Secondary = 50% of fee schedule, Tertiary+ = 25% of fee schedule. (3) Sum the individual expected payments. (4) Compare to the actual total payment. (5) If the payer applied a different reduction methodology (e.g., 100/50/25 vs. 100/50/50), flag for review.

**Q:** What is a "prompt pay" penalty and how is it tracked in reconciliation?
**A:** Many state laws and payer contracts require payers to pay "clean claims" within a specified timeframe (e.g., 15 days for electronic, 30 days for paper). If the payer exceeds this timeframe, they must pay interest or a penalty on the late payment. The penalty appears in the 835 as a PLB segment with reason code 51 (Interest Payment). Reconciliation should track: (1) Payment receipt date vs. submission date. (2) Days to pay. (3) Interest/penalty due vs. interest/penalty paid. (4) If penalty not paid, file a prompt-pay complaint.

**Q:** How should a provider handle a negative PLB (recoupment) in the 835?
**A:** A negative PLB (e.g., PLB*52*500.00~) means the payer is taking money back from the current payment. The system should: (1) Identify the PLB reason code (52 = Overpayment Recoupment, 50 = Late Filing Penalty, etc.). (2) Verify the recoupment is valid — was there actually a prior overpayment? (3) Adjust AR by reducing the current payment. (4) Do NOT adjust individual claim postings unless the recoupment is claim-specific. (5) Create a separate tracking record for the recoupment. (6) If the recoupment appears invalid, contact the payer for a corrected 835.

**Q:** What is the relationship between timely filing and denial management?
**A:** Timely filing is a contractual requirement that claims must be submitted within a specified period (typically 90-365 days from date of service, depending on payer). If a claim is denied for timely filing (CARC 50), the provider has almost no chance of overturning it — the time has passed. Therefore, timely filing denials should be a rare occurrence that triggers process review. Reconciliation systems should flag claims approaching their timely filing deadline and prioritize collection follow-up. Prevention is the only effective strategy: submit claims within 24-48 hours of service.

**Q:** How do reconciliation reports help in payer contract negotiations?
**A:** Reconciliation data provides evidence for contract negotiations by showing: (1) Which payers have the lowest net collection rates. (2) Which payers have the highest underpayment totals. (3) Which payers have the most denials. (4) Which payers pay the slowest (highest Days in AR). (5) Which payer contracts result in reimbursement below industry benchmarks for specific CPT codes. (6) Quantified financial impact of payer performance — e.g., "UnitedHealthcare underpaid $105,000 in the last year across 420 claims." This data transforms negotiations from subjective impressions to objective financial analysis.