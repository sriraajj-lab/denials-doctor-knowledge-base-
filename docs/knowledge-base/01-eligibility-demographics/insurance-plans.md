# Insurance Plans

## Overview

Health insurance plans define the financial and access framework for healthcare services. Understanding plan structures, how to read insurance ID cards, and the nuances of each plan type is essential for accurate claim submission, eligibility verification, and denial prevention. This document covers all major commercial and government plan types, payer identification, claim routing, and plan benefit limitations.

---

## 1. Insurance Plan Types

### Health Maintenance Organization (HMO)

**How it works**: HMO plans require members to select a Primary Care Physician (PCP) who manages all healthcare services. The PCP provides referrals to specialists within the HMO network.

**Key characteristics**:
- **PCP required**: Yes. The patient must have a designated PCP.
- **Referral required**: Yes. Specialist visits require a PCP referral.
- **In-network only**: No coverage for out-of-network care except for true emergencies.
- **Out-of-network coverage**: Emergency services only (under the prudent layperson standard).
- **Premium**: Typically lower than PPO.
- **Deductible**: Often $0 (copay-only model) or low deductible.
- **Copay model**: Common structure -- $25 PCP visit, $50 specialist visit.
- **Network**: Strictly defined. If the provider is not in the HMO network, there is no coverage.
- **Authorization**: Pre-authorization required for many services.

**Claims processing for HMO**:
- Claims are submitted to the HMO plan's claims address or electronic payer ID.
- If a service is rendered without a referral, the claim will deny.
- If the provider is out-of-network, the claim will deny as non-covered.
- Some HMOs capitate the PCP -- the PCP receives a fixed monthly payment per member, and the specialist claims are processed separately.

### Preferred Provider Organization (PPO)

**How it works**: PPO plans offer more flexibility by allowing members to see any provider, with better benefits for in-network care.

**Key characteristics**:
- **PCP required**: No.
- **Referral required**: No. Patients can self-refer to specialists.
- **In-network vs out-of-network**: Separate benefit levels.
  - In-network: Lower copay/coinsurance, lower deductible, out-of-pocket max applies
  - Out-of-network: Higher copay/coinsurance, separate (often higher) deductible, separate OOP max (or no OOP max)
- **Premium**: Generally higher than HMO.
- **Deductible**: Varies widely -- $500 to $5,000+.
- **Coinsurance**: Typically 80/20 in-network (plan pays 80%), 50-60% out-of-network.
- **Authorization**: Still required for certain services (MRI, surgery, etc.) even in-network.

**Claims processing for PPO**:
- Claims may include a "non-covered" or "reduction" for out-of-network providers.
- Out-of-network claims may use "usual, customary, and reasonable" (UCR) fee schedules rather than contracted rates.
- Balance billing is allowed by out-of-network providers unless prohibited by state law or plan terms.
- PPO benefit levels are indicated by a "Benefit Level" or "Network" indicator on the insurance card.

### Point of Service (POS)

**How it works**: A hybrid plan combining HMO and PPO features. Members choose a PCP and need referrals for in-network specialist care, but can also see out-of-network providers at a higher cost.

**Key characteristics**:
- **PCP required**: Yes.
- **Referral required**: Yes, for in-network specialist care.
- **In-network**: Lower cost sharing, managed care model.
- **Out-of-network**: Higher cost sharing, no referral needed.
- **Premium**: Mid-range between HMO and PPO.
- **Deductible**: Often separate in-network and out-of-network deductibles.
- **The "Point of Service" name**: The member decides at the time of service (point of service) whether to stay in-network or go out-of-network.

**Claims processing for POS**:
- If a patient has a POS plan and sees an out-of-network provider without a referral, the claim processes at the OON benefit level.
- If they see an in-network provider with a valid referral, it processes at the in-network level.
- The claims address is the same for both, but the benefit adjudication differs.

### High Deductible Health Plan (HDHP)

**How it works**: An HDHP has a higher deductible than a traditional insurance plan but lower monthly premiums. HDHPs are designed to work with Health Savings Accounts (HSAs).

**Key characteristics**:
- **2024 Minimum Deductibles** (IRS-defined):
  - Individual: $1,600
  - Family: $3,200
- **2024 Maximum Out-of-Pocket** (IRS-defined):
  - Individual: $8,050
  - Family: $16,100
- **HSA eligibility**: Only HDHPs qualify for HSA contributions.
- **Preventive care**: Covered at 100% before the deductible is met (by law).
- No copay model -- nearly everything goes to the deductible first.
- Premiums are lower.

**Important distinctions**:
- Some plans call themselves "high deductible" but do not meet IRS HDHP requirements -- these are NOT HSA-eligible.
- The deductible is cumulative for the family. Once the family deductible is met, all family members have met their deductible.
- HSA contributions are tax-deductible, grow tax-free, and are tax-free for qualified medical expenses.

**Claims processing for HDHP**:
- Most services are applied to the deductible.
- Preventive care is covered at 100% pre-deductible (ACA requirement).
- The claim adjudication will show amounts applied to deductible.
- If the patient has an HSA, payments from the HSA are patient responsibility.

### Exclusive Provider Organization (EPO)

**How it works**: EPO plans combine features of HMO and PPO. Like HMOs, there is no out-of-network coverage (except emergencies). Like PPOs, no PCP or referral is required.

**Key characteristics**:
- **PCP required**: No.
- **Referral required**: No.
- **Out-of-network coverage**: None (except emergencies).
- **Premium/Cost**: Typically lower than PPO, higher than HMO.
- **Network**: Must use plan's provider network exclusively.
- **Authorization**: Pre-authorization still required for many services.

**Claims processing for EPO**:
- Out-of-network claims (non-emergency) deny as non-covered.
- EPOs are popular on the ACA marketplace (healthcare.gov).
- Members should verify provider network participation before care.
- Balance billing protection: Some states protect EPO members from balance billing for out-of-network care.

### Agent Q&A

**Q:** A patient has an HMO plan and sees a specialist without a PCP referral. The specialist is in-network. Will the claim be paid?
**A:** No. HMO plans require a PCP referral for specialist visits. Even if the specialist is in-network, the claim will deny because the service was not authorized through the PCP. The denial reason will typically be CO 32 (Our records indicate that this service was not pre-authorized/pre-certified) or PR 34 (Claim lacks required pre-certification/authorization). The patient may appeal, but the provider cannot bill the patient for a non-covered service if the denial is due to lack of authorization (per most managed care contracts). If the provider is out-of-network, the claim denies as non-covered AND unauthorized -- double denial. Always obtain authorization before treating HMO patients outside the PCP's scope.

**Q:** A patient has a PPO plan with an out-of-network deductible. They see an out-of-network provider. Are they responsible for the full billed amount?
**A:** Not necessarily. PPO plans calculate benefits based on the "Usual, Customary, and Reasonable" (UCR) amount or the plan's "allowed amount" for out-of-network care. The plan pays a percentage (e.g., 60%) of the allowed amount, not of the billed amount. The patient is responsible for: (1) The difference between the billed amount and the allowed amount (balance billing), (2) The coinsurance on the allowed amount, (3) Any amount applied to the out-of-network deductible. This can result in the patient owing significantly more than with an in-network provider. Some states limit balance billing for out-of-network services. The provider should provide a good faith estimate and discuss the patient's out-of-network benefits before service.

**Q:** Can a patient have an HSA with a non-HDHP plan?
**A:** No. Health Savings Accounts (HSAs) are only available to individuals enrolled in a qualified High Deductible Health Plan (HDHP) as defined by the IRS. Additionally, the individual must: (1) Not have any other health coverage (there are exceptions for specific coverage types like dental, vision, accident, disability). (2) Not be enrolled in Medicare. (3) Not be claimed as a dependent on someone else's tax return. If a patient contributes to an HSA but has a non-qualifying plan, they face tax penalties. Best practice: verify the plan is HSA-eligible (look for "HSA-Compatible" or "HDHP" on the card) before helping a patient with HSA-related billing.

**Q:** What is the difference between an EPO and an HMO?
**A:** The key differences are: (1) **PCP requirement**: HMO requires a primary care physician. EPO does not. (2) **Referral requirement**: HMO requires PCP referrals for specialists. EPO does not. (3) **Self-referral**: EPO allows patients to self-refer to any in-network specialist. HMO does not. (4) **Out-of-network**: Both have no out-of-network coverage (except emergencies). (5) **Cost**: EPO premiums are typically between HMO and PPO. From a claim processing perspective: EPO claims that are out-of-network will deny as non-covered (same as HMO). But EPO claims from in-network specialists will be paid without needing a referral number. Make sure you know which network the EPO uses -- it may be the same as a PPO network or a distinct EPO-only network.

---

## 2. Medicare

### Original Medicare (Fee-for-Service)

**Part A -- Hospital Insurance**:
- Covers: Inpatient hospital stays, skilled nursing facility (SNF) care, hospice, some home health care
- Premium: Generally premium-free if the beneficiary or spouse paid Medicare taxes for 40+ quarters
- Deductible (2024): $1,632 per benefit period (not per year; one benefit period starts when admitted to hospital and ends after 60 consecutive days without hospital or SNF care)
- Coinsurance: Days 1-60: $0 after deductible. Days 61-90: $408/day. Days 91-150: $816/day (60 lifetime reserve days)

**Part B -- Medical Insurance**:
- Covers: Doctor visits, outpatient services, preventive care, durable medical equipment (DME), some home health
- Premium (2024): $174.70/month standard (higher for higher-income beneficiaries)
- Deductible (2024): $240/year
- Coinsurance: 20% of Medicare-approved amount for most services (patient pays)

**Part D -- Prescription Drug Coverage**:
- Stand-alone Prescription Drug Plans (PDPs) or included in Medicare Advantage
- Premium, deductible, and formulary vary by plan
- Coverage gap ("donut hole"): After initial coverage limit, the patient enters the coverage gap. In 2024, the coverage gap has been eliminated by the Inflation Reduction Act -- once the patient reaches the catastrophic threshold, they have no additional cost sharing.

### Medicare Part C -- Medicare Advantage (MA)

**How it works**: Private insurance plans (HMO, PPO, PFFS) that contract with Medicare to provide Part A, Part B, and usually Part D benefits.

**Key characteristics**:
- Must cover all Original Medicare services (cannot cherry-pick).
- Often includes extra benefits: dental, vision, hearing, fitness programs.
- Can have $0 premium (plan premium, not Part B premium).
- Network restrictions: Most MA plans are HMO or PPO.
- Annual enrollment: Open Enrollment (Oct 15 - Dec 7), MA Open Enrollment (Jan 1 - Mar 31).
- Must use plan's provider network for non-emergency care.

**Claims processing for MA**:
- Claims go to the private insurer (e.g., UnitedHealthcare, Aetna), not to Medicare.
- The same pre-authorization and referral rules as commercial plans apply.
- Medicare Advantage plans have different timeliness and appeal rules than Original Medicare.
- Some MA plans use "Medicare as secondary" rules for beneficiaries who are still working.

### Medicare Supplements (Medigap)

**How it works**: Private insurance that fills "gaps" in Original Medicare (copays, coinsurance, deductibles).

**Key characteristics**:
- Standardized plans: A, B, C, D, F, G, K, L, M, N (varies by state; Plans C and F no longer available to new enrollees after Jan 1, 2020).
- Plan F: Covers all Medicare gaps (most comprehensive; grandfathered only).
- Plan G: Covers everything except Part B deductible.
- Plan N: Lower premium, requires copays for some services.
- Medigap does NOT cover prescription drugs (need Part D separately).

**Claims processing for Medigap**:
- Medicare automatically forwards claims to Medigap plans (crossover).
- No separate claim submission needed for most providers.
- The Medigap plan pays the provider directly for the Medicare coinsurance/deductible.
- If the provider accepts Medicare assignment, they must accept the Medicare + Medigap payment as payment in full.

### Medicare Part A vs Part B Coverage

| Service Type | Part A | Part B | Notes |
|---|---|---|---|
| Inpatient hospital | Yes | No | Applies to Part A deductible/benefit period |
| Outpatient hospital | No | Yes | Part B covers |
| Physician services | No | Yes | Part B covers |
| Skilled nursing facility | Yes (up to 100 days) | No | Requires prior hospital stay of 3+ days |
| Home health | Limited | Yes | Most covered under Part B |
| Hospice | Yes | No | Part A covers |
| Durable medical equipment | No | Yes | Part B covers |
| Preventive care | No | Yes | Part B covers at 100% |
| Prescription drugs | No | No | Part D or MA plan |
| Ambulance | No | Yes | Part B covers |
| ER services | No | Yes | Part B covers outpatient ER |
| Lab services | No | Yes | Part B covers at 100% |

### Agent Q&A

**Q:** A patient has Original Medicare Part A and Part B. What is their financial responsibility for a standard office visit?
**A:** Under Original Medicare, the patient pays: (1) The Part B deductible of $240/year (2024) -- applies once per calendar year. After the deductible is met: (2) 20% of the Medicare-approved amount for the visit. Example: If Medicare's approved amount is $150 for the visit, Medicare pays $120 (80%) and the patient owes $30 (20%). If the patient has a Medigap plan (e.g., Plan G), the Medigap plan would pay the $30. If the patient does not have Medigap, the provider collects the $30 from the patient. Important: The provider must accept Medicare assignment -- meaning they agree to accept the Medicare-approved amount as payment in full and cannot balance bill beyond the 20% coinsurance and deductible.

**Q:** A patient is on Medicare Advantage (HMO) and comes to our out-of-network clinic. Can we bill the patient for the full amount?
**A:** Generally no, for emergency services. For non-emergency services: The Medicare Advantage HMO plan likely has no out-of-network coverage (except emergencies). The provider CAN bill the patient directly for non-covered services IF: (1) The patient was informed in advance that the service would not be covered. (2) The patient signed a waiver (Advance Beneficiary Notice or ABN for Medicare patients). (3) State law allows it. Without an ABN: The provider may be liable for the charges if Medicare determines the patient could not have reasonably known the service was not covered. For emergencies: The plan must cover emergency out-of-network care at in-network cost sharing. Best practice: verify network participation and obtain a signed waiver before providing non-emergency out-of-network services to a Medicare Advantage patient.

**Q:** What is a Medicare "benefit period" and how is it different from a calendar year?
**A:** A Medicare benefit period (also called a "spell of illness") is a unique feature of Medicare Part A. It begins when the patient is admitted to a hospital or SNF and ends after the patient has been out of the hospital or SNF for 60 consecutive days. There is no limit to the number of benefit periods a patient can have. Key differences from a calendar year: (1) The Part A deductible applies per benefit period, not per year. A patient could have multiple hospital admissions in a single year and pay the Part A deductible each time. (2) The benefit period structure means a patient could have 3 separate admissions in January-March -- each a new benefit period with its own deductible. (3) The 60-day "clean period" resets after 60 days out of the hospital/SNF. (4) Calendar year is used for Part B (annual deductible, annual OOP max). (5) Skilled nursing facility benefits are also tied to the benefit period -- the 100-day SNF benefit is per benefit period, not per year.

---

## 3. Medicaid

### State-Specific Programs

Medicaid is a joint federal-state program. Each state administers its own program within federal guidelines.

**Federal requirements**:
- Must cover: Inpatient/outpatient hospital, physician services, lab/x-ray, nursing facility, home health, EPSDT (children), family planning
- Income eligibility: States set their own thresholds (ACA expansion states: 138% FPL)
- Must offer Early and Periodic Screening, Diagnostic and Treatment (EPSDT) for children under 21

**State variations**:
- Program name: Medicaid, Medical Assistance, Medi-Cal (CA), MassHealth (MA), BadgerCare (WI), SoonerCare (OK), Apple Health (WA)
- Managed care vs fee-for-service: Most states use MCOs for most populations
- Dental: Optional for adults, mandatory for children
- Transportation: Some states cover non-emergency medical transportation (NEMT)
- Premiums: Most states have no premiums, but some charge "premiums" for certain populations
- Prescription drug formularies: State-specific

### Managed Care Organizations (MCOs)

Most Medicaid beneficiaries are enrolled in managed care plans:

| State | Major MCOs |
|---|---|
| California | Anthem Blue Cross, Health Net, Kaiser, L.A. Care |
| Texas | Superior Health, UnitedHealthcare, Molina, Cook Children's |
| New York | Healthfirst, Empire (BCBS), Fidelis, MetroPlus |
| Florida | Simply Healthcare, Sunshine Health, UnitedHealthcare |
| Illinois | CountyCare, Meridian, Molina, Blue Cross Community |

### Dual Eligible (Medicare + Medicaid)

Patients who qualify for both Medicare and Medicaid are "dual eligibles."

- **Full dual**: Entitled to full Medicare Part A and Part B + full Medicaid benefits. Medicaid pays the Part B premium, Part A premium (if any), and provides wrap-around coverage (covers deductibles, coinsurance).
- **Partial dual (SLMB, QMB, QI)**: Medicare Savings Programs that pay Medicare premiums/coinsurance but do not provide full Medicaid coverage.
  - **QMB (Qualified Medicare Beneficiary)**: Pays Part A/B premiums, deductibles, and coinsurance. The QMB patient cannot be balance billed.
  - **SLMB (Specified Low-Income Medicare Beneficiary)**: Pays Part B premium only.
  - **QI (Qualifying Individual)**: Pays Part B premium only (similar to SLMB, funded differently).

**Billing for dual eligibles**:
1. Submit to Medicare first (primary).
2. After Medicare processes, crossover to Medicaid automatically (or submit manually).
3. Medicaid pays the Medicare deductible/coinsurance up to the Medicaid allowed amount.
4. Provider must accept Medicare + Medicaid as payment in full.
5. **Important**: QMB patients CANNOT be billed for Medicare deductibles or coinsurance. Federal law prohibits balance billing QMB beneficiaries.

### Agent Q&A

**Q:** A patient has both Medicare and Medicaid (dual eligible). Do I need to submit claims to both, or will they automatically crossover?
**A:** If the provider accepts Medicare assignment and participates in Medicaid, Medicare claims should automatically "crossover" to the state's Medicaid program. This works differently by state: (1) Some states have automatic crossover via the Medicare Common Working File (CWF). (2) Others require the provider's clearinghouse to submit a separate claim to Medicaid. (3) Some use the 837 crossover transaction with the primary payer's paid amounts. Best practice: (a) Verify crossover is working by checking your ERA (835) -- if you see both Medicare and Medicaid payments coming through, crossover is active. (b) If you do not see Medicaid payments within 30 days of Medicare payment, submit a separate claim to Medicaid. (c) For QMB patients, you CANNOT bill the patient at all. For other dual eligibles, you can bill the patient only for services not covered by either Medicare or Medicaid. For the claim: submit to Medicare with the patient's Medicare ID (MBI). Include the patient's Medicaid ID in the claim (Loop 2320/2330 in the 837 for COB) so Medicare can forward the claim to Medicaid.

**Q:** A patient presents a Medicaid card from a different state than where our practice is located. Can we treat them?
**A:** This is a complex situation: (1) Standard Medicaid coverage does NOT cross state lines (except for emergency services and specific out-of-state arrangements). (2) For non-emergency services: the patient must be covered in the state where services are rendered, either by that state's Medicaid program or by a reciprocal agreement. (3) For emergency services: Medicaid must cover emergency care provided in any state (under the Supremacy Clause / federal Medicaid requirements). (4) The patient should contact their state Medicaid office to arrange coverage if they are temporarily in your state. (5) Some states have limited reciprocity agreements with bordering states. (6) Best practice: treat the patient, collect their out-of-state Medicaid info, and check with your state's Medicaid office for specific billing instructions. For non-emergency care: verify coverage before service and have a self-pay/charity care plan if the coverage doesn't cross state lines.

**Q:** What is the difference between fee-for-service (FFS) Medicaid and managed care Medicaid for claims processing?
**A:** **Fee-for-service (FFS) Medicaid**: (1) The state Medicaid agency or its fiscal agent processes claims directly. (2) No network restrictions (any Medicaid-enrolled provider can bill). (3) Claims are submitted to the state's Medicaid claims address/payer ID. (4) Reimbursement is at the state's fee schedule. (5) No prior authorization needed for most services (or state-specific requirements). **Managed care Medicaid (MCO)**: (1) The patient is enrolled in a private managed care plan (e.g., Molina, UnitedHealthcare Community Plan). (2) The MCO processes claims like a commercial insurance plan. (3) Network restrictions apply -- must be in the MCO's network. (4) Prior authorization and referral requirements follow MCO rules (similar to commercial HMO/PPO). (5) Claims are submitted to the MCO's payer ID, not the state Medicaid payer ID. (6) Reimbursement is per the MCO's contract. Critical: Billing FFS when the patient is in managed care will result in denial and vice versa. Always verify the patient's enrollment status before submitting.

---

## 4. Other Payer Types

### Workers' Compensation

- **Coverage**: Medical treatment for work-related injuries or illnesses.
- **Primary payer**: Workers' Comp is primary for work-related conditions. Health insurance is secondary.
- **Claim-specific**: Each workers' comp claim has a claim number and adjuster.
- **No cost sharing**: Deductibles, copays, and coinsurance do not apply.
- **No balance billing**: Providers must accept the workers' comp fee schedule.
- **State-specific**: Each state has its own workers' comp laws, fee schedules, and claims processes.
- **Authorization**: Often requires specific authorization from the workers' comp carrier.
- **Billing**: Claims are submitted using the workers' comp payer ID, with the claim number included. ICD-10 codes must indicate work-relatedness (contact with workplace injury).

### Auto Insurance

- **Medical Payments Coverage (MedPay)**: Pays medical bills regardless of fault. Primary for auto accident-related injuries.
- **Personal Injury Protection (PIP)**: Similar to MedPay but broader. May include lost wages, funeral costs.
- **Liability coverage**: The at-fault driver's insurance may pay medical bills.
- **Health insurance**: Pays after auto insurance medical benefits are exhausted.
- **State variations**: No-fault states (PIP required), tort states (liability-based), choice states.
- **Billing**: Requires the auto insurance company name, policy number, claim number, and accident date. Use occurrence codes on the claim.

### Tricare / CHAMPVA

- **Tricare**: Health insurance for active duty and retired military.
  - Tricare Prime (HMO-like), Tricare Select (PPO-like), Tricare for Life (Medicare wraparound for 65+)
  - Tricare is primary for active duty, secondary for retirees with other coverage
- **CHAMPVA**: Health insurance for dependents of veterans with permanent/total service-connected disabilities
- **Tricare for Life**: For Tricare beneficiaries age 65+ who have Medicare Parts A and B. Medicare is primary, Tricare for Life is secondary/payer of last resort.

### Federal Employees Health Benefits (FEHB)

- Health insurance for federal employees.
- Administered by OPM (Office of Personnel Management).
- Plans include: Blue Cross Blue Shield (most popular), GEHA, Mail Handlers, various PPOs and HMOs.
- No state-specific versions -- same plan nationwide.
- FEHB enrollees can also have Medicare (age 65+) -- Medicare is primary.

### Agent Q&A

**Q:** A patient is injured at work but also has personal health insurance. Which insurance should I bill first?
**A:** Workers' Compensation is primary for work-related injuries. The health insurance claim will deny if the diagnosis code indicates the injury is work-related (most payers check ICD-10 codes for work-relatedness). The claim flow: (1) Verify the workers' comp claim is approved. (2) Submit all work-related charges to the workers' comp carrier with the claim number and adjuster contact. (3) If workers' comp denies the claim (e.g., the injury is determined not work-related), submit to health insurance with the workers' comp denial EOB. (4) If workers' comp pays partially or reaches a limit, submit the balance to health insurance as secondary. (5) Coordinate with the patient's employer and workers' comp adjuster. Critical: Never submit an auto-generated claim to health insurance for a known work-related injury -- this constitutes fraud. The provider MUST determine the cause of injury at registration and route the claim appropriately.

**Q:** A patient is involved in a car accident and has auto insurance with PIP and health insurance. What is the billing order?
**A:** (1) Auto insurance PIP (Personal Injury Protection) is primary for medical bills related to the accident. (2) Health insurance is secondary after PIP benefits are exhausted. (3) If the patient has MedPay instead of PIP, MedPay is also primary but may have lower limits. (4) The health insurance claim will typically require: the auto insurance EOB showing what was paid/denied, an accident description, and the date of the accident. (5) Some states have "no-fault" laws requiring PIP to be used first. (6) Some health insurance plans have "automobile exclusion" clauses -- they will not pay ANY auto-related claims. The patient should be informed at registration that auto-related billing may involve multiple payers and that they should contact their auto insurance agent. The claim must include occurrence code "AA" (auto accident) on the 837 transaction.

**Q:** A Tricare for Life patient has Medicare Part A and B and Tricare. What is the billing process?
**A:** For Tricare for Life (TFL) beneficiaries age 65+ with Medicare Parts A and B: (1) Medicare is primary. Submit the claim to Medicare. (2) After Medicare processes, the claim "crosses over" to Tricare automatically. (3) Tricare for Life acts as secondary coverage -- it pays the Medicare deductible and coinsurance (the 20% Part B coinsurance, the Part A deductible, etc.). (4) Tricare for Life is essentially a Medigap-like plan that fills the gaps in Medicare coverage. (5) The provider should NEVER bill the Tricare for Life patient directly for the Medicare coinsurance -- Tricare will pay it. (6) If the claim does not auto-crossover, submit a claim to Tricare with the Medicare EOB. (7) TFL also covers services that Medicare does not (e.g., some overseas care, experimental treatments) -- those are billed to Tricare directly.

---

## 5. Reading Insurance ID Cards

### Card Layout and Key Fields

Insurance cards vary dramatically by payer, but most contain these fields in standard locations:

```
[PAYER LOGO]          Blue Cross Blue Shield of Illinois
____________________________________________________
Member ID:            ABC1234567890
Group Number:         GRP-98765                      Rx Group: RX-GRP-54321
Member Name:          JOHN A. SMITH                  Rx Bin: 123456
Effective Date:       01/01/2024                     Rx PCN: ABCD
Plan:                 PPO Choice
Network:              BlueCard PPO
____________________________________________________
| Copays:             | Deductible: $1,500/Indiv    |
| PCP Visit: $25      | OOP Max: $6,000/Indiv       |
| Specialist: $50     | Rx: $10/$30/$50 tiers       |
| ER: $100            |                             |
| UC: $50             |                             |
____________________________________________________
Claims Address:       PO Box 12345, Chicago, IL 60601
Customer Service:     1-800-XXX-XXXX
Provider Services:    1-800-XXX-XXXX
```

### How to Extract Key Information

**Member ID**: The most critical field. Used for the 270/271 eligibility transaction and on all claims. Rules:
- Use it EXACTLY as shown -- including leading zeros, letters, hyphens, spaces
- Do not add or remove characters
- Case sensitivity: Some payers are case-sensitive, most are not
- If the ID has a hyphen or space, some clearinghouses want it WITH the hyphen, others WITHOUT

**Group Number**: Identifies the employer or group. Used for some eligibility checks. Some plans (individual, Medicare) do not have group numbers. If missing, use a placeholder or omit.

**Rx (Pharmacy) Fields**:
- **Rx Bin**: Identifies the pharmacy processor. Six-digit number.
- **Rx PCN**: Processor Control Number. Alphanumeric.
- **Rx Group**: Pharmacy group number.
- These are used for pharmacy claims (NCPDP format), NOT medical claims (837 format).

**Claims Address**: Where to send paper claims. Electronic claims use the payer ID instead.

**Customer Service Number**: For patient inquiries. Provider services number is for provider inquiries.

### Payer Identification Numbers

**National Plan ID (NPID)**: Standard identifier for health plans under HIPAA. Not widely used.

**Electronic Payer ID**: The ID used to route electronic claims through a clearinghouse. Each clearinghouse may have different IDs for the same payer.

**Payer Taxonomy**: Many payers have multiple "lines of business" with different payer IDs:
- Commercial PPO: ID 12345
- Commercial HMO: ID 12346
- Medicare Advantage: ID 12347
- Medicaid MCO: ID 12348

### Agent Q&A

**Q:** A patient's insurance card has a member ID of "ABC 123 456 789" (with spaces). Do I include the spaces in the claim?
**A:** It depends on the payer and the clearinghouse. Some rules of thumb: (1) Most commercial payers expect the ID without spaces (ABC123456789). (2) Medicare MBIs should be entered with hyphens (1EG4-TE5-MK73) or without -- the system handles both. (3) Some Medicaid states require spaces. (4) If your clearinghouse has a "payer ID lookup" tool, it will often indicate the correct formatting. Best practice: (a) Enter the ID exactly as printed, including spaces/hyphens. (b) The clearinghouse will format it correctly for the payer. (c) If you get "Invalid Member ID" rejections, try removing spaces/hyphens. (d) When in doubt, call the payer's provider services line and ask: "What format do you expect the subscriber ID in?"

**Q:** What is the Rx Bin number on an insurance card, and do I need it for medical claims?
**A:** The Rx Bin number identifies the pharmacy claims processor. It is used for NCPDP (pharmacy) claims, NOT for medical claims (837). You do NOT need the Rx Bin number for medical claims processing. However: (1) Some billing systems ask for Rx fields when setting up a payer configuration even for medical claims. (2) If a practice dispenses medications (e.g., a physician's office that gives samples), you may need the Rx Bin. (3) If you are verifying pharmacy benefits, you need the Rx Bin. For medical claims: ignore the Rx fields entirely. For pharmacy claims: Use the Rx Bin + Rx PCN + Rx Group + member ID for the NCPDP transaction. Many payers have different member IDs for medical vs pharmacy.

**Q:** The insurance card shows a "PCP" name. Does this mean the plan is an HMO?
**A:** Not necessarily, but it strongly suggests the plan is either HMO or POS (which also requires a PCP). PPO and EPO plans do not typically have a PCP field on the card. However: (1) Some PPO plans list a default PCP even though no PCP is required -- this is rare. (2) Some insurance cards list a PCP for "administrative" purposes. (3) Medicare Advantage HMO plans prominently list the PCP. (4) Some employer plans assign a PCP for care coordination even though the plan is technically a PPO. When in doubt: (a) Call the customer service number and ask "Does this plan require a PCP referral for specialist visits?" (b) If yes, it is an HMO or POS. (c) If no (PCP is listed but referral not needed), the plan is a PPO with a notional PCP. (d) Check the plan type on the card -- most cards explicitly state "HMO", "PPO", "EPO", or "POS."

---

## 6. Electronic Payer IDs for Major Payers

### Medicare Administrative Contractors (MACs)

MACs process Medicare Part A and Part B claims for specific geographic jurisdictions.

| MAC | Jurisdiction | States Covered | Electronic Payer ID |
|---|---|---|---|
| Noridian Healthcare Solutions | JE, JF | Part A: CA, NV, HI, US Territories. Part B: CA, NV, HI, US Territories, AK, AZ, ID, MT, ND, OR, SD, UT, WA, WY | 04101 (JE A), 04201 (JF B) |
| Palmetto GBA | JM, JJ | Part A: OH, KY, WV, NC, SC, VA, TN. Part B: (various) | 15101 (JM A), 15201 (JJ B) |
| NGS (National Government Services) | J6, JK | Part A: IL, MN, WI, CT, NY, MA, ME, NH, RI, VT. Part B: (various) | 13101 (J6 A), 13201 (JK B) |
| WPS (Wisconsin Physician Services) | J5, J8 | Part A: KS, NE, IA, MO, IN, MI. Part B: MI, IN, WI, IA, MO, NE, KS, MN | 05101 (J5 A), 05201 (J8 B) |
| First Coast Service Options | JN | Part A: FL, PR, VI. Part B: FL, PR, VI | 09101 (JN A), 09201 (JN B) |
| CGS Administrators | J15, JNV | Part A: KY, OH. Part B: KY, OH, TN | 16101 (J15 A), 16201 (JNV) |
| Novitas Solutions | JH, JL | Part A: CO, NM, OK, TX. Part B: DE, DC, MD, NJ, PA | 12101 (JH A), 12201 (JL B) |

### Commercial Payer Electronic IDs

| Payer | Notes | Common Electronic Payer ID |
|---|---|---|
| UnitedHealthcare | Most lines of business | 87726 |
| Aetna | Commercial, Medicare, Medicaid | 60054 |
| Cigna | Most lines of business | 62308 |
| Humana | Commercial and Medicare | 61265 |
| Blue Cross Blue Shield | Varies by state -- each state BCBS has its own ID | See state-specific |
| Coventry | UnitedHealthcare subsidiary | 80695 |
| MultiPlan | Secondary/reprice network | 77251 |

**State-specific BCBS plan IDs**: Examples:
- BCBS of Alabama: 46021
- BCBS of California (Anthem): 38927
- BCBS of Florida: 54023
- BCBS of Illinois (HCSC): 48024
- BCBS of Massachusetts (Blue Cross Blue Shield of MA): 58277
- BCBS of Michigan (Blue Care Network): 42025
- BCBS of New York (Empire): 56029
- BCBS of Texas: 58028

**Important caveat**: Payer IDs change and vary by clearinghouse. Always verify the correct payer ID for your specific clearinghouse (Change Healthcare, Availity, ZirMed, Office Ally, etc.).

### Agent Q&A

**Q:** What payer ID should I use for a Medicare Part B claim for a patient in California?
**A:** For Medicare Part B claims in California, the MAC is Noridian Healthcare Solutions, Jurisdiction JF (Part B). The electronic payer ID is typically 04201. However: (1) This ID may vary by clearinghouse. (2) Noridian processes Part B for CA, NV, HI, US Territories, AK, AZ, ID, MT, ND, OR, SD, UT, WA, WY. (3) Part A claims in CA go to Noridian JE (payer ID 04101). Important: Do NOT use the MAC payer ID for Medicare Advantage claims. Medicare Advantage plans are processed by the private insurer (e.g., UnitedHealthcare, Aetna), not by the MAC. Use the plan's commercial payer ID instead. Check your clearinghouse's payer ID list for the most current MAC payer IDs.

**Q:** Why does my claim reject with "Invalid Payer ID" when I use the same payer ID I used last month?
**A:** Payer IDs can change for many reasons: (1) The payer may have updated their claims processing system. (2) The clearinghouse may have updated their routing tables. (3) The patient's line of business may have changed (e.g., from commercial to Medicare Advantage under the same payer name). (4) The payer may have changed TPAs (third-party administrators). (5) The payer may have been acquired by another company (e.g., Aetna acquiring Coventry). Troubleshooting: (a) Check your clearinghouse's payer ID lookup tool. (b) Search for the payer by name, not by old ID. (c) Verify you are using the correct payer ID for the correct line of business (commercial vs Medicare vs Medicaid). (d) Check if the payer requires a different clearinghouse. (e) Call the payer to confirm their electronic payer ID. (f) If all else fails, use the payer's "default" payer ID or central claims address.

**Q:** What if a payer doesn't have an electronic payer ID in my clearinghouse?
**A:** This typically means: (1) The payer may not accept electronic claims -- you must submit paper claims. (2) The clearinghouse may not have a direct connection to the payer -- use a "clearinghouse" payer ID that routes through a network. (3) The payer may have recently changed names or been acquired. (4) The payer may only accept electronic claims through a specific portal (direct data entry/ DDE). Solutions: (a) Look for the payer under a different name or parent company. (b) Call the payer and ask: "What electronic payer ID do you use?" (c) Check if the payer is part of a larger network (e.g., MultiPlan, PHCS, Galaxy Health). (d) Use a paper claim template for the rare payer that truly does not accept electronic claims. (e) Some very small or regional payers may require direct enrollment in their provider portal.

---

## 7. Plan Benefit Limits

### Visit Limits

Many plans limit the number of visits for specific services per year:

| Service Type | Typical Limit | Notes |
|---|---|---|
| Chiropractic visits | 12-24 visits/year | Medicare: no limit (if medically necessary). Many commercial plans: 20-30 visits. |
| Physical therapy | 20-30 visits/year | Medicare: no hard limit but medical review after 10 visits. |
| Occupational therapy | 20-30 visits/year | Often combined with PT for limit. |
| Speech therapy | 20-30 visits/year | Often separately limited from PT/OT. |
| Acupuncture | 12-20 visits/year | ACA: covered for chronic low back pain. |
| Mental health therapy | 20-60 visits/year | ACA: MH/SUD parity applies -- same limits as medical/surgical. |
| Cardiac rehabilitation | 36 sessions (Medicare) | Per cardiac event. Often once per lifetime. |
| Pulmonary rehabilitation | 36 sessions (Medicare) | Per qualifying condition. |

### Dollar Maximums and Lifetime Caps

- **Annual maximum**: Some plans have a maximum dollar amount they will pay per year (e.g., $1,000 dental, $2,000 PT). Once the max is reached, no further payment.
- **Lifetime maximum**: $2 million lifetime cap (rare on ACA-compliant plans -- ACA prohibits lifetime dollar limits on essential health benefits). Still common on:
  - Grandfathered plans
  - Some self-funded (ERISA) plans
  - Dental plans
  - Vision plans
- **Per-condition maximum**: Some plans limit coverage for specific conditions (e.g., $25,000 lifetime for infertility treatment).

### Out-of-Pocket Maximums

- **ACA requirement**: All non-grandfathered plans must have an annual out-of-pocket maximum. 2024 limits: $9,450 individual, $18,900 family.
- **Family OOP max**: Once the family OOP max is met, all family members are considered to have met their individual OOP max.
- **Embedded vs aggregate deductible**: 
  - Embedded: Each family member has their own deductible within the family deductible. Once one member meets their individual deductible, cost sharing kicks in for them.
  - Aggregate: The entire family must meet the family deductible before cost sharing kicks in for anyone.
- **OON OOP max**: Some PPO plans have separate out-of-pocket max for in-network and out-of-network. OON OOP max may be higher or non-existent.

### Agent Q&A

**Q:** A patient's physical therapy claim is denied with "Benefit limit exceeded" (CO 119). The patient has 40 PT visits this year. Their plan covers 20 PT visits per year. What happens now?
**A:** Once a plan's benefit limit is reached, no further payment will be made for that service. The options: (1) The patient can appeal for additional visits if medically necessary (some plans allow "extra benefit" requests). (2) The patient can pay out-of-pocket (check if the plan allows this -- some plans do not allow balance billing after the benefit limit is reached). (3) The provider can write off the charges if the patient cannot pay. (4) The patient may have alternate coverage (e.g., a separate plan for auto accident or workers comp) that has a separate PT limit. (5) The patient can wait for the next plan year when benefits reset. (6) For Medicare: there is no visit limit on PT, but there is a "medical necessity" threshold. If Medicare denied the PT benefit, it means they determined the PT was not medically necessary. Best practice: Verify benefit limits before treatment. Use the 271 response -- look for EB segment with EB03 = "30" (Visits) for the specific service type.

**Q:** How do I determine if a patient's out-of-pocket maximum has been met for the year?
**A:** The 271 eligibility response provides this information. Look for: (1) EB segment with EB01 = "C" (Coverage level information) and EB09 = "F" indicating out-of-pocket maximum. (2) The MSG or NTE segments may show "Deductible met" or "OOP max met." (3) Some 271 responses show remaining deductible and remaining OOP in the same segment. (4) If the 271 shows $0 remaining OOP max, the patient should have no additional patient responsibility (except for non-covered services). (5) However, the 271 is snap-shot data -- actual accumulations may differ on the processed claim. (6) If the 271 shows "Not available" for OOP accumulations, the information is not available through eligibility. Call the payer or check the provider portal. (7) Important: The OOP max only applies to the same plan/family. If the patient has multiple plans, each plan has its own OOP max.

**Q:** A patient has an ACA-compliant plan with a $5,000 deductible and $8,000 OOP max. When does the plan start paying?
**A:** (1) The patient pays the first $5,000 of covered services (the deductible). (2) After the deductible is met, cost sharing begins -- typically 80/20 plans meaning the patient pays 20% until they reach $8,000 total. (3) Once the patient's total out-of-pocket (deductible + coinsurance/copays) reaches $8,000, the plan pays 100% of covered services. The $8,000 includes the $5,000 deductible. So the patient's maximum additional cost sharing after the deductible is $3,000 (20% of $15,000 = $3,000, bringing them to $8,000). However, if the plan is 80/20, the patient pays 20% on services until OOP max is reached. The timing depends on the total allowed amount of services received. Preventive services are covered at 100% before the deductible. Non-covered services do not count toward the OOP max.

---

## 8. Plan ID Card Formats by Payer

### UnitedHealthcare

- **Commercial**: Card shows the "UHG" logo with a "UHC" watermark. Member ID: 9-digit or 10-digit alphanumeric (no spaces). Plan name (e.g., "Choice Plus", "Navigate", "Core").
- **Medicare Advantage**: Card shows "UnitedHealthcare Medicare Advantage" or "AARP Medicare Advantage" (UHC administers AARP plans). Member ID: 11-character alphanumeric. 
- **Medicaid**: "UnitedHealthcare Community Plan." Member ID: varies by state.
- **Key features**: "Claims" address line usually at bottom. "Customer Service" number for patients. "Provider Services" for providers. "Medical ID" vs "Rx ID" may differ.

### Aetna

- **Commercial**: Aetna logo at top. Member ID: 9-digit numeric or alphanumeric. "Plan: Open Access PPO", "Aetna Choice POS", etc.
- **Medicare Advantage**: "Aetna Medicare" logo. Member ID: varies. Group number may reference the plan name.
- **Medicaid**: "Aetna Better Health" for most states.
- **Key features**: "Member ID" is the primary identifier. Copay/benefit grid prominently displayed. "Prescription Drug Coverage" section at bottom.

### Cigna

- **Commercial**: Cigna logo. Member ID: 9-digit numeric (Cigna ID) or alphanumeric (for some accounts). "Plan: Cigna PPO" / "OAP" (Open Access Plus).
- **Medicare Advantage**: "Cigna Medicare" logo. Member ID: varies.
- **Key features**: Member ID format -- look for "Cigna ID" or "Subscriber ID." "Administered by Cigna" vs "Insured by Cigna" -- this indicates self-funded vs fully insured.

### Blue Cross Blue Shield

- **Each state plan issues its own card**: BCBS of Illinois card looks different from BCBS of Texas.
- **Logo**: The blue cross and blue shield logo. The state plan name is below it.
- **Member ID**: Format varies by plan. Often 9-digit or 10-digit numeric (e.g., "WXY123456789"). Some plans use letters + numbers.
- **Group Number**: Almost always present for employer plans.
- **Network**: "BlueCard PPO", "Blue Options", "BlueChoice", etc.
- **Routing**: Out-of-area claims route through the BlueCard program (use the BlueCard payer ID).

### Agent Q&A

**Q:** A patient presents a Blue Cross card from Texas but lives in Illinois. Where do I submit the claim?
**A:** This is handled through the BlueCard program. The claim routing depends on the patient's plan: (1) If the patient is covered by BCBS of Texas but receives care in Illinois, the claim routes through "BlueCard" to BCBS of Texas. (2) The electronic payer ID is typically the BlueCard ID (e.g., 54022 for BlueCard national). (3) The provider does NOT send the claim directly to BCBS of Texas -- it goes through the BlueCard central clearinghouse. (4) BCBS of Texas adjudicates the claim based on their contract with the patient. (5) The in-network benefits depend on whether you (the Illinois provider) are in the BlueCard PPO network. (6) BCBS PPO plans participate in BlueCard -- HMO plans generally do NOT. (7) For HMO: The patient would need to be in their home state or have a referral from their PCP. Best practice: for non-local BCBS cards, verify eligibility through the BlueCard system (use the "BlueCard Eligibility" payer ID) and confirm network participation before service.

**Q:** What does "Self-Funded" or "ASO" mean on an insurance card?
**A:** "ASO" stands for Administrative Services Only (self-funded). The employer bears the financial risk of the health plan, and the insurance company (e.g., Cigna, Aetna) only provides administrative services (claims processing, network access, customer service). This means: (1) The employer determines the benefit plan (not the insurance company). (2) The employer's plan document controls benefits -- state insurance mandates may not apply. (3) ERISA (federal law) governs the plan, not state insurance law. (4) Appeals go to the employer's plan administrator, not the insurance company. (5) The claim still gets submitted to the payer on the card (Cigna, Aetna, etc.) -- the claims address is the same. (6) Self-funded plans may have different benefits, exclusions, and limitations than standard commercial plans. (7) ERISA preemption: State laws like independent external review may not apply. When you see "Self-Funded" or "ASO" on a card, know that the benefit details are governed by the employer's plan document and may differ from the "standard" plan benefits of that insurance company.

---

## 9. Plan Exclusions and Limitations

### Common Plan Exclusions

| Service | Typically Excluded | Notes |
|---|---|---|
| Cosmetic surgery | Yes | Unless reconstructive (medically necessary) |
| Dental | Yes (adult) | Pediatric dental covered under ACA |
| Vision | Yes (adult) | Routine eye exams and glasses |
| Hearing aids | Yes | Some plans offer hearing benefits |
| Weight loss surgery | Often excluded | Medical necessity documentation needed |
| Fertility treatment | Often excluded | Or limited to specific covered services |
| Experimental / Investigational | Yes | Defined by the plan |
| Custodial care | Yes | Custodial care is not skilled care |
| Acupuncture | Often excluded | ACA covers for chronic low back pain |
| Chiropractic care | Limited | Visit limits apply |
| Out-of-network | Excluded on HMO/EPO | Emergency exceptions |

### Timely Filing Limits

Each payer has a specific window for claim submission (from date of service):

| Payer | Filing Limit | Notes |
|---|---|---|
| Medicare | 12 months (full), 36 months (conditional) | Must submit within 12 months of DOS |
| Medicaid | Varies by state (90-365 days) | Check state-specific rules |
| BCBS | 90-365 days (varies by plan) | Typically 180 days |
| UnitedHealthcare | 90-365 days (varies by plan) | Typically 180-365 days |
| Aetna | 180-365 days (varies by plan) | Some plans 90 days |
| Cigna | 180-365 days (varies by plan) | Typically 180 days |
| Tricare | 365 days (12 months) | From date of service |
| Workers Comp | Varies by state | Typically 90 days to 2 years |
| Auto insurance | Varies by state | Typically 2-5 years |

**Critical note**: Timely filing denials (CO 29) are preventable. Track the filing deadline from the date of service and ensure claims are submitted well within the window. Secondary claims (after primary has paid) have a separate timely filing window -- check the secondary payer's rules.

### Agent Q&A

**Q:** A claim is denied for timely filing (CO 29). The primary reason was that the claim was submitted 187 days after the date of service. The plan has a 180-day timely filing limit. What can be done?
**A:** A timely filing denial (CO 29) means the claim was submitted after the payer's deadline. Options: (1) Check if the payer has a timely filing waiver process -- some payers waive the limit for "good cause" (e.g., medical records, appeals). (2) Check if the claim was initially submitted within the window but rejected for another reason and the corrected claim missed the window -- some payers honor the original submission date. (3) Some states have "prompt pay" laws that override the payer's timely filing limit. (4) If the payer has an online appeals tool, file a timely filing appeal with documentation of the original submission. (5) If nothing works, the provider must write off the charges (cannot bill the patient for a timely filing denial unless the patient caused the delay). (6) Secondary claims have their own filing limit from the date of the primary EOB -- not from the date of service. Best practice: Set up automated timely filing tracking. Claims should be submitted within 30 days of service to provide a buffer for corrections.

**Q:** A patient's chiropractic benefits are limited to 20 visits per year. They have already had 20 visits but the chiropractor says they need more treatment. Can the patient pay out-of-pocket?
**A:** This depends on the plan: (1) Some plans allow the patient to pay out-of-pocket for services beyond the benefit limit. (2) Many HMO/EPO plans do NOT allow balance billing after a benefit limit is exceeded -- the provider must write off the charges or obtain a waiver. (3) Some plans have a "benefit limit exception" process where additional visits can be authorized with medical necessity documentation. (4) For Medicare: no visit limit on chiropractic, but the service must meet medical necessity criteria. (5) The patient should also check if their secondary insurance covers chiropractic with a separate limit. Action steps: (a) Verify the plan's policy on benefit limit exceedance via the provider manual. (b) Have the patient sign a waiver (Advanced Beneficiary Notice for Medicare, or a private pay waiver) if permitted. (c) File an appeal for additional visits with supporting medical records. (d) If the patient is willing to pay, confirm with the plan that private payment is allowed before collecting.

**Q:** A patient has a plan that excludes "experimental/investigational" treatments. How is "experimental" defined?
**A:** Plans typically define experimental/investigational based on: (1) FDA approval status (off-label use may be experimental). (2) Published peer-reviewed studies (lack of evidence). (3) National guidelines (not recommended by NIH, NCCN, etc.). (4) Coverage in major formularies (not covered by Medicare, not in standard compendia). (5) Technology assessment (e.g., Blue Cross Blue Shield TEC assessment). The plan's "Medical Policy" or "Coverage Policy" explicitly lists what is considered experimental. If the plan denies a service as experimental: (1) Ask the plan which specific policy/guideline they used. (2) Check the policy for exceptions or clinical trial coverage. (3) Provide medical literature supporting the treatment. (4) Some states have "external review" processes that allow independent determination. (5) Some plans cover experimental treatments under clinical trial participation. Best practice: always verify coverage before performing potentially experimental treatments.

---

## 10. Claim Submission by Plan Type

### How Plan Type Affects Where and How to Submit

| Plan Type | Submission Method | Payer ID | Authorization Required |
|---|---|---|---|
| HMO (Commercial) | Electronic via clearinghouse | Plan-specific commercial ID | Yes (referral + auth) |
| PPO (Commercial) | Electronic via clearinghouse | Plan-specific commercial ID | Yes (certain services) |
| POS (Commercial) | Electronic via clearinghouse | Plan-specific commercial ID | Yes (if using in-network with referral) |
| EPO (Commercial) | Electronic via clearinghouse | Plan-specific commercial ID | Auth required for some services |
| HDHP (Commercial) | Electronic via clearinghouse | Plan-specific commercial ID | Same as plan type |
| Medicare Part A/B | Electronic via MAC | MAC payer ID (e.g., 04201) | Medicare-specific NCD/LCD |
| Medicare Advantage | Electronic via plan | MA plan payer ID (not MAC ID) | MA plan's authorization rules |
| Medicaid FFS | Electronic via state | State Medicaid payer ID | State-specific |
| Medicaid MCO | Electronic via MCO | MCO payer ID | MCO-specific |
| Tricare | Electronic via clearinghouse or DDE | 73083 (WPS) or regional | Tricare policy |
| Workers Comp | Electronic or paper | Comp carrier ID | State-specific, case-specific |
| Auto | Paper or electronic | Auto insurer payer ID | Claim-specific |

### Agent Q&A

**Q:** A patient has a PPO plan. The claim was denied as "not covered" (CO 50). What are the possible reasons?
**A:** CO 50 denial (services not covered by this plan) for a PPO could mean: (1) The service is specifically excluded from the plan's benefit package (e.g., cosmetic surgery, infertility treatment). (2) The provider is in the network but the specific service is not a covered benefit. (3) The service was rendered at a place of service that is not covered (e.g., services in a non-participating facility). (4) The service frequency exceeds the plan's limit (visit limit exceeded). (5) The service was pre-authorized but the authorization was for a different service. (6) The patient's benefits have terminated (coverage ended). (7) A specific rider/exclusion applies to this patient's plan. Troubleshooting: (a) Look at the claim remarks (RARCs) for more detail. (b) Call the payer and ask for the specific reason: "CO 50 shows, but what is the explanation?" (c) Review the patient's Summary of Benefits and Coverage (SBC). (d) Check if the plan requires pre-authorization that was not obtained. (e) File an appeal with supporting documentation. (f) For PPOs, the service must be a covered benefit in the plan document -- check the employer's specific plan document.

**Q:** How do I find the correct claims address for a paper claim submission?
**A:** Several sources: (1) The patient's insurance card: Many cards list the claims address at the bottom. (2) The payer's website: Most payers have a "Claims" or "Submit a Claim" page. (3) The payer's provider manual (if you are a contracted provider). (4) The 271 eligibility response: Some 271s include the claims address in the response. (5) The Medicare MAC website for Medicare claims. (6) The state Medicaid website for Medicaid claims. (7) Clearinghouse databases: Many clearinghouses have payer address databases. (8) Call the payer's provider services number. When in doubt, call and confirm: "What is the correct mailing address for submitting a paper claim?" Important: Paper claims are increasingly rare (electronic is the standard). Most payers charge a penalty for paper claims or reject them. Use electronic submission whenever possible.

---

## 11. Marketplace (ACA) Plans

### Plan Metal Tiers

| Tier | Actuarial Value | Plan Pays | Patient Pays | Premium Level |
|---|---|---|---|---|
| Bronze | 60% | 60% | 40% | Lowest |
| Silver | 70% | 70% | 30% | Medium |
| Gold | 80% | 80% | 20% | High |
| Platinum | 90% | 90% | 10% | Highest |
| Catastrophic | Below 60% | Almost nothing until OOP max | Almost everything | Lowest (under 30 only) |

### Cost-Sharing Reductions (CSR)

- Silver plans only: Income-based reductions in deductible, copays, OOP max
- Available to individuals with income between 100-250% FPL
- Not visible on the insurance card -- claim processing reflects CSR automatically
- Providers are often not told about CSR -- but it reduces patient responsibility

### Key Marketplace Plan Features

- **Essential Health Benefits (EHBs)**: All marketplace plans cover 10 categories (ambulatory, emergency, hospitalization, maternity, mental health, prescription drugs, rehabilitative, lab, preventive, pediatric/dental)
- **No pre-existing condition exclusions**: Cannot deny coverage for pre-existing conditions
- **No lifetime or annual dollar limits**: On essential health benefits (non-EHB may have limits)
- **Pediatric dental and vision**: Included in all marketplace plans
- **Preventive care at 100%**: No cost sharing for USPSTF A/B recommended preventive services

### Agent Q&A

**Q:** A patient has a Bronze marketplace plan with a $6,000 deductible. They come in for a preventive care visit. Is the visit covered before the deductible?
**A:** Yes. Under the ACA, all non-grandfathered marketplace plans must cover preventive care services (USPSTF A/B recommendations) with no cost sharing, regardless of whether the deductible has been met. This includes: wellness visits, immunizations, cancer screenings (mammograms, colonoscopies), blood pressure screening, cholesterol screening, depression screening, diabetes screening, and other USPSTF-recommended services. IMPORTANT: If the provider performs additional services during the same visit (e.g., treats a sinus infection during a wellness visit), those additional services ARE subject to the deductible. The visit itself (preventive) is covered at 100%, but the problem-oriented component is not. Use the correct ICD-10 code (Z00.00 for general adult wellness) and CPT code. The claim split may result in some charges being covered and others applied to the deductible. Providers should clearly communicate: "Your wellness visit is covered, but any additional treatment will apply to your deductible."

**Q:** A patient has a Silver marketplace plan with cost-sharing reductions. How does this affect billing?
**A:** Cost-Sharing Reductions (CSR) are only available on Silver plans for individuals with income 100-250% of the Federal Poverty Level. CSR reduces the patient's deductible, copays, and out-of-pocket maximum. For billing: (1) The plan's claims processing system automatically applies CSR -- you do NOT need to do anything special. (2) The patient's co-pays and deductibles will be lower than the standard Silver plan. (3) The provider cannot charge the patient more than the reduced cost sharing. (4) CSR is invisible on the insurance card -- there is no special indicator. (5) You can detect CSR eligibility by comparing the patient's cost sharing to the standard Silver plan amounts -- if deductible or copays are lower than expected, CSR may be in effect. (6) The provider's reimbursement is the same whether or not CSR is in effect -- CSR reduces patient cost sharing, not provider reimbursement. (7) Providers should check the 271 response for CSR-related benefit information.

---

## 12. Benefit Verification Best Practices

### Pre-Service Verification Checklist

- [ ] Verify patient identity (name, DOB)
- [ ] Obtain insurance card (front and back)
- [ ] Identify plan type (HMO, PPO, POS, EPO, HDHP)
- [ ] Verify network participation
- [ ] Run 270/271 eligibility check
- [ ] Review 271 response: coverage dates, deductible, copay, coinsurance, OOP max
- [ ] Check benefit limits (visits, dollar caps)
- [ ] Verify pre-authorization requirements
- [ ] Check COB (ask about other insurance)
- [ ] Document all verification in the patient record
- [ ] Print eligibility response summary

### Common Pitfalls

1. **Assuming eligibility = coverage**: Eligibility means the patient is enrolled. It does not guarantee the service is covered.
2. **Ignoring benefit limits**: Plan may have visit limits, dollar caps, or per-condition maximums.
3. **Not checking timely filing**: Verify the filing window matches the expected submission timeline.
4. **Not documenting**: Without documentation, you cannot prove verification occurred.
5. **Relying on old data**: Benefits change annually at plan renewal (often Jan 1).
6. **Forgetting about COB**: Not asking about other coverage leads to COB denials.

### Agent Q&A

**Q:** A patient's eligibility check (271) shows "Active Coverage" with a $30 copay. The claim processes and the patient is billed $300. What happened?
**A:** The $30 copay may apply only to a specific service (e.g., primary care office visit) but the patient received a different service (e.g., specialist visit, diagnostic test, procedure). The 271 response provides "snapshot" data -- it may show a generic copay that does not apply to all services. Common discrepancies: (1) The 271 copay is for a PCP visit, but the patient saw a specialist (different copay). (2) The 271 did not specify "deductible applies" -- some plans have copays that do not apply until the deductible is met. (3) The 271 was run for a different service than what was performed. (4) The 271 shows the "general" plan benefits, not the patient's specific benefit design (e.g., employer buy-down). (5) The patient has a deductible that was not reflected in the 271 because the system only shows copay for a specific service type. Best practice: Run eligibility for the SPECIFIC planned service (use service type codes). Document the copay and add a note: "Copay verified for [service]. Deductible status also checked." Call the payer for specific benefit details if the 271 is ambiguous.

**Q:** How far in advance can I verify eligibility before a service?
**A:** Most payers maintain eligibility information in "real-time" but coverage can change at any time. Best practices: (1) Verify eligibility no more than 7 days before the service date. (2) If verifying more than 7 days in advance, reverify on the day of service. (3) Some payers expire eligibility information within 24 hours. (4) Medicare eligibility can be verified up to 12 months ahead, but the patient's status can change (death, loss of coverage, etc.). (5) Medicaid eligibility changes frequently -- patients can lose coverage between monthly renewals. (6) Commercial plans can change when the employer changes carriers (common at year-end). (7) Always document: "Eligibility verified on [date] for service on [date]." (8) For scheduled procedures: verify at the time of scheduling AND on the day of service. (9) Some clearinghouses perform "batch eligibility" checks that run overnight -- these are useful for same-day/next-day patients but should not be used for appointments 2+ weeks out.

---

## 13. Glossary

| Term | Definition |
|---|---|
| **Actuarial Value** | Percentage of total average costs for covered benefits that a plan will pay (Bronze=60%, Silver=70%, Gold=80%, Platinum=90%) |
| **Allowed Amount** | The maximum amount an insurance plan will pay for a covered service |
| **Benefit Period** | Medicare Part A's measurement period (starts with admission, ends after 60 days out of hospital/SNF) |
| **Capitation** | Fixed monthly payment per member to a provider, regardless of services rendered |
| **COB** | Coordination of Benefits -- which plan pays first |
| **Coinsurance** | Percentage of costs the patient pays after deductible (e.g., 20%) |
| **Copay** | Fixed dollar amount the patient pays per service (e.g., $25 office visit) |
| **Deductible** | Amount the patient must pay before insurance starts paying |
| **Embedded Deductible** | Each family member has their own deductible within the family deductible |
| **Essential Health Benefits** | 10 categories of benefits all ACA plans must cover |
| **HSA** | Health Savings Account -- tax-advantaged savings for HDHP members |
| **MAC** | Medicare Administrative Contractor -- processes Medicare Part A/B claims for a region |
| **MCO** | Managed Care Organization -- private company managing Medicaid benefits |
| **Medigap** | Medicare Supplement Insurance -- fills gaps in Original Medicare |
| **OOP Max** | Out-of-Pocket Maximum -- most the patient pays per year (includes deductible + coinsurance + copays) |
| **PCP** | Primary Care Physician -- manages care for HMO/POS members |
| **UCR** | Usual, Customary, and Reasonable -- standard for OON allowable amounts |
| **Balance Billing** | Billing the patient for the difference between billed charges and allowed amount |
| **Creditable Coverage** | Previous health coverage that counts toward a new plan's pre-existing condition waiting period |
| **Grandfathered Plan** | Plan in existence before March 23, 2010 (ACA enactment) -- exempt from some ACA requirements |
| **Self-Funded (ASO)** | Employer bears insurance risk; payer only administers claims |
| **Formulary** | List of covered prescription drugs |
| **Medical Necessity** | Standard for determining whether a service is reasonable and necessary for diagnosis/treatment |
| **Network** | Group of providers contracted with a plan to provide services at negotiated rates |
| **Metal Tiers** | Bronze/Silver/Gold/Platinum -- categories of marketplace plan cost sharing |

---

## 14. Summary: Key Takeaways for LLM Agent

When processing insurance plan information:

1. **Plan type determines everything**: HMO, PPO, POS, EPO, HDHP -- each has different coverage rules, network requirements, and referral/authorization needs.
2. **Read the card carefully**: Member ID, group number, plan name, copays, deductibles, network -- all critical information.
3. **Know the MAC jurisdictions**: Medicare Part A/B claims go to the regional MAC, not a national address.
4. **Understand COB for each plan type**: Medicare is primary for 65+ with small employers; employer plan is primary for 20+ employees.
5. **Verify benefit limits**: Visit limits, dollar caps, lifetime maxes -- these can cause post-service denials.
6. **Check timely filing**: Each payer has a different window. Track it from the date of service.
7. **Watch for Medicare Advantage**: Claims go to the MA plan (not the MAC) and follow commercial-style rules.
8. **Remember Medicaid variations**: State-specific, MCO vs FFS, dual-eligible rules for Medicare crossover.
9. **ACA marketplace plans have special protections**: No pre-existing exclusions, preventive at 100%, no lifetime limits on EHBs.
10. **Verification is not the same as benefit confirmation**: The 271 shows eligibility, not coverage for a specific service.

---

*End of Insurance Plans Knowledge Base Document*