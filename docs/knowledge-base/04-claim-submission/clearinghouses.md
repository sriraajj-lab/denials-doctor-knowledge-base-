# Clearinghouses

## Overview

A healthcare clearinghouse is an intermediary entity that receives healthcare claims from providers, translates them into the required formats for each payer, and transmits them to the appropriate destination. Clearinghouses also provide editing, validation, and status tracking services. Under HIPAA, clearinghouses are covered entities because they handle protected health information (PHI) in the claim process.

Clearinghouses add significant value by managing the complexity of multi-payer claim submission, but they add an additional step and cost to the revenue cycle.

---

## 1. Major Clearinghouses

### Change Healthcare (Emdeon/WebMD)

| Aspect | Details |
|--------|---------|
| **Market Position** | Largest clearinghouse in the US |
| **Former Names** | Emdeon, WebMD |
| **Services** | Claim submission, eligibility, payment posting, denial management |
| **Payer Network** | 900+ payers |
| **Claim Volume** | Over 5 billion transactions annually |
| **Technology** | ClaimRunner, InterChange, Payment360 |
| **Key Feature** | Extensive payer connectivity and real-time claim status |
| **Integration** | Major EHR and practice management systems |

### Waystar (ZirMed)

| Aspect | Details |
|--------|---------|
| **Market Position** | Top 3 clearinghouse in the US |
| **Former Names** | ZirMed |
| **Services** | Claim submission, RCM analytics, payment posting |
| **Payer Network** | 2,000+ payers |
| **Technology** | Waystar ONE Platform |
| **Key Feature** | Advanced analytics and denial management tools |
| **Integration** | Major EHR systems including Epic, Cerner |

### Availity

| Aspect | Details |
|--------|---------|
| **Market Position** | Largest multi-payer portal |
| **Services** | Claim submission, eligibility verification, prior authorization, referrals |
| **Payer Network** | 750+ payers |
| **Technology** | Availity Portal, Availity Essentials |
| **Key Feature** | Strong real-time eligibility and prior authorization |
| **Integration** | Wide EHR integration, especially in Florida and Texas |

### Office Ally

| Aspect | Details |
|--------|---------|
| **Market Position** | Popular among small to mid-sized practices |
| **Services** | Claim submission (free for electronic), patient statements |
| **Payer Network** | 3,500+ payers |
| **Technology** | Office Ally EHR 24/7 |
| **Key Feature** | Free electronic claim submission (basic tier) |
| **Integration** | Web-based, supports multiple practice sizes |

### Trizetto

| Aspect | Details |
|--------|---------|
| **Market Position** | Large enterprise-focused clearinghouse |
| **Services** | Claim submission, revenue cycle management, analytics |
| **Payer Network** | 700+ payers |
| **Technology** | Trizetto Provider Solutions |
| **Key Feature** | Full RCM suite, strong denial management |
| **Integration** | Major hospital systems and large practices |

### Navinet / NEA

| Aspect | Details |
|--------|---------|
| **Market Position** | Large clearinghouse with focus on integrated health systems |
| **Services** | Claim submission, eligibility, payment posting, analytics |
| **Payer Network** | 600+ payers |
| **Technology** | Navinet, NaviNet Open |
| **Key Feature** | Strong clinical data exchange |
| **Integration** | Major EHR systems |

### RelayHealth (McKesson)

| Aspect | Details |
|--------|---------|
| **Market Position** | Large clearinghouse under McKesson |
| **Services** | Claim submission, eligibility, payment posting |
| **Payer Network** | 700+ payers |
| **Technology** | RelayHealth Financial Exchange |
| **Key Feature** | Integration with McKesson practice management |
| **Integration** | McKesson practice systems |

---

## 2. How Clearinghouses Work

### Claim Submission Flow

```
Provider Practice Management System
  |-- Creates 837 claim file
  |-- Sends to clearinghouse via SFTP, AS2, or API
  |
  v
Clearinghouse Receives 837
  |-- Validates EDI structure (syntax check)
  |-- Validates codes (CPT, ICD-10, NPI, taxonomy)
  |-- Applies payer-specific edits (if configured)
  |-- Translates to payer-specific format if needed
  |-- Assigns internal claim tracking ID
  |
  v
Clearinghouse Routes to Payer
  |-- Determines correct payer EDI route
  |-- Submits to payer in required format
  |-- Captures payer acknowledgment (997, 277CA, 835)
  |
  v
Clearinghouse Returns Acknowledgments to Provider
  |-- 997 or TA1 (EDI acceptance)
  |-- 277CA (claim status)
  |-- 835 (payment/remittance)
```

### Clearinghouse Translation

Clearinghouses translate claims between different formats:

| Source Format | Target Format | Description |
|---------------|---------------|-------------|
| 837 v5010 | 837 v4010A1 | Standard translation between X12 versions |
| 837P | Payer Proprietary Format | Some payers use non-X12 formats internally |
| 837I | 837P | Institutional to professional (clearinghouse creates separate professional claims from institutional) |
| CMS-1500 | 837 | Paper-to-electronic conversion (scanned and EDI-encoded) |
| UB-04 | 837I | Paper institutional-to-electronic conversion |

---

## 3. Clearinghouse Value

### Key Value Additions

| Function | Value | Description |
|----------|-------|-------------|
| **Payer Connectivity** | High | Single connection reaches all payers; no need for individual payer EDI setup |
| **Format Translation** | High | Translates 837 to payer-required formats and versions |
| **Payer-Specific Editing** | High | Applies each payer's unique edit rules before submission |
| **Claim Status Tracking** | High | Provides 997/277CA/835 tracking in a single dashboard |
| **Rejection Management** | Medium | Returns clear rejection reasons from both clearinghouse and payer |
| **Eligibility Verification** | High | Real-time eligibility checks through payer connections |
| **Payment Posting** | Medium | 835 receipt and auto-posting capability |
| **Denial Analytics** | Medium | Aggregated denial reason data across all payers |
| **Reporting** | Medium | Claim volume, denial rate, payment time analytics |
| **Security/Compliance** | High | HIPAA-compliant transmission, audit trails |

### Advantages Over Direct Submission

| Aspect | Direct Submission | Via Clearinghouse |
|--------|-------------------|-------------------|
| **Payer Connections** | Must configure each payer individually | One connection to all payers |
| **Format Translation** | Must comply with each payer's format | Clearinghouse handles all formats |
| **Edit Checking** | Provider's system only | Clearinghouse adds additional edits |
| **Acknowledgment Handling** | Manual checking of each payer's responses | Unified dashboard for all acknowledgments |
| **Payer Changes** | Must update each payer connection individually | Clearinghouse manages payer updates |
| **Setup Time** | Weeks per payer | Days to connect to clearinghouse |
| **Technical Support** | Payer-dependent | Clearinghouse provides single support point |

---

## 4. Clearinghouse Rejection vs Payer Rejection

### Clearinghouse Rejection

A clearinghouse rejection occurs when the clearinghouse's editing system identifies an error before the claim is transmitted to the payer.

| Characteristic | Detail |
|----------------|--------|
| **When it happens** | Before claim is sent to the payer |
| **Common causes** | Invalid EDI format, missing required fields, invalid NPI, invalid taxonomy, invalid codes |
| **Response time** | Seconds to minutes |
| **Action needed** | Correct the error in the clearinghouse and resubmit |
| **Impact** | Claim never reaches the payer; no payer denial record |
| **Fix difficulty** | Usually easy (format/field corrections) |

### Payer Rejection

A payer rejection occurs after the clearinghouse has transmitted the claim to the payer and the payer's system identifies an error.

| Characteristic | Detail |
|----------------|--------|
| **When it happens** | After clearinghouse sends to payer |
| **Common causes** | Payer-specific edit failures, missing medical policy requirements, payer enrollment issues |
| **Response time** | 24-48 hours (sometimes longer) |
| **Action needed** | Correct the issue and resubmit through the clearinghouse |
| **Impact** | Claim was received by payer but not entered into adjudication |
| **Fix difficulty** | Moderate to difficult (may require payer-specific resolution) |

### Clearinghouse vs Payer Rejection Comparison

| Aspect | Clearinghouse Rejection | Payer Rejection |
|--------|------------------------|-----------------|
| **Response Format** | Clearinghouse-specific error report | 999 or 277CA from payer |
| **Error Details** | Usually detailed and actionable | May be cryptic or require lookup |
| **Turnaround** | Immediate | Usually 24-48 hours |
| **Can Appeal?** | No (fix and resubmit) | Sometimes (fix and resubmit or appeal) |
| **Cost to Provider** | Low (quick correction) | Higher (delayed payment, rework) |

---

## 5. Clearinghouse Fees

### Fee Structures

| Model | Description | Typical Cost |
|-------|-------------|--------------|
| **Per-Claim Fee** | Charge per claim submitted | $0.10 - $0.40 per claim |
| **Monthly Subscription** | Flat monthly fee based on volume | $50 - $500+ per month |
| **Transaction-Based** | Fee per transaction type (claim, eligibility, status) | Varies by transaction |
| **Bundled with EHR** | Cleaned-included in EHR subscription cost | No separate fee |
| **Tiered Pricing** | Different rates based on claim volume tiers | Lower per-claim cost at higher volume |
| **Value-Based Pricing** | Cost based on services used (edits, analytics, etc.) | Typically higher but more comprehensive |

### Cost Comparison by Practice Size

| Practice Size | Approx Monthly Claims | Estimated Monthly Cost (Per-Claim) | Estimated Monthly Cost (Subscription) |
|---------------|----------------------|-----------------------------------|---------------------------------------|
| Solo Provider | 200-400 | $20-$80 | $50-$100 |
| Small Practice (2-5) | 500-2,000 | $50-$400 | $100-$300 |
| Medium Practice (5-20) | 2,000-8,000 | $200-$1,600 | $300-$1,000 |
| Large Practice (20+) | 8,000+ | $800+ | $1,000+ |

---

## 6. Direct Submission vs Clearinghouse

### When to Use Direct Submission

| Scenario | Rationale |
|----------|-----------|
| Single payer | Only one payer, no need for multi-payer routing |
| Payer portal submission | Payer's portal handles formatting (e.g., Medicare Direct Data Entry) |
| Low claim volume | Very low volume may not justify clearinghouse costs |
| Integrated health system | Full EDI capability, payer connections already established |
| Payer-specific agreements | Payer requires direct submission or has special arrangement |

### When to Use a Clearinghouse

| Scenario | Rationale |
|----------|-----------|
| Multiple payers | Clearinghouse handles routing and formatting for all payers |
| Diverse claim types | Professional, institutional, dental all through one connection |
| Need for editing | Clearinghouse provides pre-submission edits that practice system lacks |
| Limited IT resources | Clearinghouse manages EDI connectivity and payer updates |
| Real-time eligibility | Clearinghouse provides multi-payer eligibility verification |
| Claim status tracking | Clearinghouse provides unified claim status dashboard |
| Growing practice | Clearinghouse easily handles increasing volume without adding payer connections |

### Decision Matrix

| Factor | Score 1 (Direct) | Score 3 (Either) | Score 5 (Clearinghouse) |
|--------|------------------|-------------------|------------------------|
| Number of Payers | 1 | 2-5 | 6+ |
| Monthly Claim Volume | <100 | 100-2,000 | 2,000+ |
| In-House IT/EDI Expertise | High | Moderate | Low |
| Payer Connectivity | Already established | Some connections | None established |
| Need for Payer Edits | Low | Moderate | High |
| Budget | Tight | Moderate | Flexible |

---

## 7. Clearinghouse Implementation

### Setup Process

1. **Select clearinghouse**: Evaluate based on payer network, cost, integration, and features.
2. **Complete enrollment**: Submit provider information, NPI, TIN, practice demographics.
3. **Configure EDI connection**: Establish connectivity method (SFTP, AS2, API) between practice system and clearinghouse.
4. **Map provider taxonomy**: Configure taxonomy codes for each provider and payer.
5. **Configure payer routing**: Define which claims go to which payers and in which format.
6. **Set up acknowledgments**: Configure how 997, 277CA, and 835 responses are received and processed.
7. **Test with payers**: Submit test claims to confirm each payer's acceptance.
8. **Go live**: Transition from pre-production to production.
9. **Monitor and optimize**: Track submission success rates, rejection reasons, and denial patterns.

### Common Implementation Issues

| Issue | Solution |
|-------|----------|
| NPI/TIN mismatch | Verify provider enrollment with each payer before connecting |
| Missing taxonomy | Ensure taxonomy is configured for each provider and payer |
| Inconsistent provider addresses | Verify address matches payer credentialing records |
| Payer connectivity failures | Confirm payer ID and route with clearinghouse support |
| Error mapping differences | Map clearinghouse error codes to practice management codes |
| Acknowledgment not received | Verify acknowledgment configuration and delivery method |

---

## 8. Agent Training: Q&A Pairs for Clearinghouses

**Q: What is the primary role of a healthcare clearinghouse?**

**A:** The primary role of a healthcare clearinghouse is to act as an intermediary between healthcare providers and payers for electronic claim submission and related transactions. The clearinghouse receives claims from providers in a standard format (typically 837), validates and edits them, translates them into the payer's required format, and routes them to the appropriate payer. Clearinghouses also manage acknowledgments (997, 277CA, 835), provide claim status tracking, and often offer additional services like eligibility verification and denial analysis.

---

**Q: What is the difference between a clearinghouse rejection and a payer rejection?**

**A:** A clearinghouse rejection occurs when the clearinghouse's editing system identifies an error before the claim is transmitted to the payer. The claim never reaches the payer. Common causes include invalid EDI format, missing required fields, or invalid NPI. A payer rejection occurs after the clearinghouse has successfully transmitted the claim to the payer and the payer's system rejects it. The payer rejection indicates the claim was received but failed the payer's front-end edits. Clearinghouse rejections are typically faster to fix and resolve, while payer rejections may require more complex corrections.

---

**Q: What are the major clearinghouses in the United States?**

**A:** The major clearinghouses in the United States include: Change Healthcare (formerly Emdeon/WebMD) -- the largest clearinghouse by transaction volume; Waystar (formerly ZirMed) -- a top clearinghouse with strong analytics; Availity -- the largest multi-payer portal with strong eligibility features; Office Ally -- popular with small practices, offering free basic electronic claims; Trizetto Provider Solutions -- serving large practices and enterprise clients; Navinet -- serving integrated health systems; and RelayHealth (McKesson) -- part of the McKesson ecosystem.

---

**Q: How does a clearinghouse add value beyond simple claim routing?**

**A:** Beyond simple claim routing, clearinghouses add value by: applying payer-specific edit rules that catch errors before submission (reducing denial rates); translating between X12 versions and payer formats (ensuring claims are in the correct format for each payer); managing technical connectivity updates when payers change their EDI requirements (saving provider IT resources); providing unified claim status tracking across multiple payers through a single dashboard; offering real-time eligibility verification through established payer connections; and providing analytics and reporting on claim volume, denial reasons, and payment trends.

---

**Q: What is the typical fee structure for clearinghouse services?**

**A:** The typical fee structures for clearinghouse services include: per-claim fees ($0.10 to $0.40 per claim), which are common for smaller practices; monthly subscriptions ($50 to $500+ per month), often used by medium to large practices; transaction-based fees where different transaction types (claim submission, eligibility check, claim status) have separate fees; bundled pricing where clearinghouse services are included in an EHR or practice management subscription; and tiered pricing where per-claim costs decrease at higher volumes.

---

**Q: When should a provider use direct submission instead of a clearinghouse?**

**A:** A provider should consider direct submission when: they only bill one or two payers (e.g., only Medicare); they have established EDI connections with those payers; they have the in-house technical expertise to manage EDI connectivity, format versions, and acknowledgment processing; their claim volume is very low, making clearinghouse costs hard to justify; or they have a direct agreement with a specific payer that requires direct submission. Direct submission is less common for most providers because of the complexity of managing multiple payer connections individually.

---

**Q: What happens to a claim after it is submitted to a clearinghouse?**

**A:** After a claim is submitted to a clearinghouse, the following happens: the clearinghouse validates the EDI structure (syntax check); the clearinghouse validates codes (CPT/HCPCS, ICD-10, NPI, taxonomy); the clearinghouse applies pre-submission edits (format, required fields, NCCI if configured); the clearinghouse translates the claim into the payer's required format; the clearinghouse routes the claim to the correct payer; the clearinghouse captures the payer's acknowledgment (997, 277CA); the clearinghouse returns the acknowledgment to the provider; and if the claim is rejected by either the clearinghouse or the payer, the clearinghouse generates a rejection report.

---

**Q: How does a clearinghouse handle claims for multiple payers?**

**A:** A clearinghouse handles multiple payers by: maintaining a database of payer-specific routing rules, EDI requirements, and format preferences; receiving the claim file in a standard format (837 v5010); examining the claim to determine which payer it is for (based on payer ID, provider information, or patient insurance); applying the correct translation and routing rules for that payer; transmitting the claim to the payer in the required format; tracking the claim status across all payers; and returning all acknowledgments and payments to the provider in a unified format. The provider needs only one connection to the clearinghouse rather than separate connections to each payer.

---

**Q: What information does a provider need to set up with a clearinghouse?**

**A:** To set up with a clearinghouse, a provider needs: provider enrollment information (NPI, TIN, practice name and address); taxonomy code(s) for each provider; contact information for EDI and billing support; practice management system details (software vendor and version); connectivity method (SFTP, AS2, API); payer list (which payers the provider bills); provider enrollment status with each payer; claim type (professional, institutional, dental); and testing credentials for the payer's testing environment.

---

**Q: Can a clearinghouse deny a claim before it reaches the payer?**

**A:** Yes, a clearinghouse can reject (deny) a claim before it reaches the payer. This is called a clearinghouse rejection. The clearinghouse's editing system identifies format errors, missing data, or invalid codes that would cause the claim to be rejected by the payer. Clearinghouse rejections are valuable because they catch errors early, before the claim enters the payer's adjudication system, saving time and reducing the number of formal denials on the provider's record. The provider corrects the error and resubmits through the clearinghouse.

---

**Q: What is the difference between Change Healthcare and Waystar?**

**A:** Change Healthcare (formerly Emdeon/WebMD) is the largest clearinghouse in the US by transaction volume, processing billions of transactions annually across a network of 900+ payers. Waystar (formerly ZirMed) is also a top-3 clearinghouse with a network of 2,000+ payers. Change Healthcare has stronger integration with legacy practice management systems and a broader EDI infrastructure. Waystar is known for its advanced analytics, denial management tools, and user-friendly portal. Both offer similar core clearinghouse services, but the best choice depends on a provider's specific payer mix, practice management system integration, and desired analytics features.

---

**Q: How does a clearinghouse handle claim rejections?**

**A:** A clearinghouse handles claim rejections by: detecting the rejection in the 999 (Functional Acknowledgment) or 277CA (Claim Status) response from the payer; translating the payer's rejection codes into readable error messages; categorizing the rejection by type (format, edit, enrollment); returning the rejection report to the provider's practice management system; generating a rejection file that can be imported into the provider's worklist; and tracking the rejection for reporting and denial management analysis. The provider reviews the rejection, corrects the issue, and resubmits the claim.

---

**Q: What is the relationship between a clearinghouse and an EHR system?**

**A:** Many EHR systems have built-in integrations with clearinghouses. The EHR generates the claim data, formats it into a 837 file, and sends it to the clearinghouse for routing. The clearinghouse returns acknowledgments, eligibility information, and payment data to the EHR. This integration automates the claim submission process and eliminates the need for separate software. Some EHR vendors charge additional fees for clearinghouse integration, while others include it as a standard feature. Not all clearinghouses integrate with all EHRs, so the clearinghouse selection should consider EHR compatibility.

---

**Q: What is the role of a clearinghouse in the 277CA claim status process?**

**A:** The clearinghouse plays a key role in the 277CA (Claim Status Response) process by: receiving the 277CA from each payer on behalf of the provider; translating the payer-specific 277CA into a readable format; delivering the 277CA data to the provider's practice management system or portal; and tracking claim status across multiple payers for a unified view. Without a clearinghouse, the provider would need to request and process 277CA responses from each payer individually, which is inefficient for multi-payer practices.

---

**Q: How does a clearinghouse manage payer EDI version changes?**

**A:** When a payer changes their EDI version requirements (for example, from 4010A1 to 5010), the clearinghouse: updates its translation rules to support the new version; notifies providers of the upcoming change and any required action; continues to accept claims in the previous version during a transition period (if supported); translates provider claims into the new version before sending to the payer; and manages the dual-version environment. This significantly reduces the burden on providers, who would otherwise need to update their practice management systems each time a payer changes version.

---

**Q: What is the difference between a "clean claim" and a claim that passes clearinghouse edits?**

**A:** A "clean claim" is a claim that can be processed without additional information or investigation from the medical record. A claim that passes clearinghouse edits has passed format and coding validation but may still require additional information or documentation for processing. The clearinghouse checks technical edits (format, codes, required fields), but does not verify clinical documentation. A claim that passes clearinghouse edits may still become a "dirty claim" (one requiring manual intervention) if the payer determines additional information is needed.

---

**Q: Can a provider use multiple clearinghouses?**

**A:** Yes, a provider can use multiple clearinghouses. This is sometimes necessary when: certain payers only accept claims through a specific clearinghouse; the provider wants to use different clearinghouses for different claim types (e.g., professional vs. institutional); the provider uses multiple practice management systems that connect to different clearinghouses; or the provider is transitioning from one clearinghouse to another and needs both operational during the transition. However, using multiple clearinghouses adds complexity, so most providers prefer a single clearinghouse if possible.

---

**Q: How does a clearinghouse handle claims for Medicare?**

**A:** A clearinghouse handles Medicare claims by: identifying the correct Medicare Administrative Contractor (MAC) based on the provider's geographic location; applying CMS-specific editing rules (NCCI edits, MUEs, LCD validation); verifying the NPI/TIN enrollment for Medicare; routing the claim to the correct MAC; capturing the MAC's acknowledgment (997, 277CA); and returning the MAC-specific 835 payment/remittance to the provider. The clearinghouse maintains the MAC connection, so the provider does not need to set up EDI with each MAC individually.

---

**Q: What is the typical turnaround time for a claim submitted through a clearinghouse?**

**A:** The typical turnaround time for a claim submitted through a clearinghouse includes: clearinghouse acceptance and validation (seconds to minutes); clearinghouse-to-payer transmission (minutes to hours, depending on batch processing); payer acknowledgment (997 within minutes, 277CA within 24-48 hours); and payment/remittance (7-30 days depending on payer, claim type, and clean vs. dirty claim). Real-time claims through some clearinghouses can receive a response in seconds, but most claims are processed in batch mode.

---

**Q: How does a clearinghouse handle NPI validation?**

**A:** A clearinghouse validates NPIs by: checking the NPI format (10 digits, Luhn algorithm validation); confirming the NPI is active in the NPPES database (if the clearinghouse has an active NPPES connection); validating the NPI/TIN pair against the provider's enrollment; and checking that the NPI is associated with the correct taxonomy on the claim. If the NPI fails validation, the clearinghouse rejects the claim or flags it for review. NPI validation helps prevent denials due to invalid or mismatched provider identifiers.

---

**Q: What is a "trading partner agreement" in the context of clearinghouses?**

**A:** A trading partner agreement is a contract between a provider and a clearinghouse (or between a clearinghouse and a payer) that establishes the terms of EDI claim submission. The agreement specifies: the EDI standards and version to be used; the connectivity method (FTP, SFTP, AS2, API); transmission schedules and expectations; acknowledgment handling; error correction procedures; security requirements (encryption, authentication); liability for transmission failures; and dispute resolution procedures. The trading partner agreement ensures both parties have clear expectations for the electronic claim exchange.

---

**Q: Can a clearinghouse help with denial management?**

**A:** Yes. Many clearinghouses offer denial management tools that: aggregate denial data across all payers; categorize denials by reason code (CARC/RARC), payer, and provider; identify denial trends (most common reasons, worst payers); provide dashboards and reports for denial monitoring; generate worklists for appeal or correction; and automate the resubmission of corrected claims. Clearinghouse denial management features are often a key differentiator when choosing a clearinghouse, especially for practices with high denial rates.

---

**Q: How does a clearinghouse handle provider credentialing changes?**

**A:** When a provider's credentialing status changes (new NPI, new TIN, new provider added or termed), the clearinghouse handles it by: requiring the provider to update their enrollment information; validating the new NPI/TIN/taxonomy with the provider's practice management system; testing the new configuration with the relevant payers; updating the routing rules for the changed provider; and ensuring that claims submitted under the old configuration are handled appropriately during the transition. The provider is responsible for notifying the clearinghouse of credentialing changes.

---

**Q: What happens if a clearinghouse goes out of business?**

**A:** If a clearinghouse goes out of business, providers must transition to a new clearinghouse. The transition involves: selecting a new clearinghouse; completing enrollment with the new clearinghouse; configuring EDI connections; updating payer routing; enrolling in payer-specific accounts; testing with payers; changing connectivity in the practice management system; and transitioning from the old clearinghouse. To minimize disruption, providers should have a contingency plan, including current payer enrollment information, practice management system connectivity details, and a backup clearinghouse relationship.

---

**Q: What is the difference between a real-time and batch clearinghouse transmission?**

**A:** Real-time transmission submits each claim individually and typically receives a response within seconds. It is suitable for point-of-service claim adjudication, urgent claims, and low-volume submission. Batch transmission groups multiple claims into a single file and submits them together. The response time is hours to days. Batch is suitable for high-volume submission, institutional claims, and scheduled claim processing. Most clearinghouses support both modes, and providers can choose based on their needs.

---

**Q: How does a clearinghouse handle claims for workers' compensation?**

**A:** Workers' compensation claims can be complex because each state has its own regulations and each workers' comp payer has its own claim requirements. The clearinghouse handles workers' comp claims by: identifying the claim as workers' compensation based on the claim filing indicator; applying state-specific edits if available; routing to the correct workers' comp payer; and handling the unique data requirements of workers' comp claims (e.g., employer information, date of injury, claim number). Some clearinghouses have specialized workers' comp capability, while others are limited in their workers' comp support.

---

**Q: Can a provider submit claims directly to a clearinghouse without a practice management system?**

**A:** Yes, many clearinghouses offer a web-based portal that allows providers to enter and submit claims manually without a practice management system. The portal provides forms that map to the 837 standard and handles the translation and routing to payers. However, manual entry is time-consuming and error-prone. Most providers use a practice management system that is integrated with the clearinghouse to automate claim creation and submission.