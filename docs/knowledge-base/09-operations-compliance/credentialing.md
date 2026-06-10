# Provider Credentialing for Denials Doctor RCM AI

## 1. Overview

Provider credentialing is the process of verifying a healthcare provider's qualifications, education, training, licensure, and professional background to participate in health insurance networks and practice at healthcare facilities. Credentialing is essential for claim reimbursement -- a provider cannot bill for services until credentialed with the applicable payer. This document covers NPI, TIN, Medicare enrollment, Medicaid enrollment, commercial payer enrollment, CAQH, provider enrollment maintenance, DEA registration, state medical licenses, board certification, CLIA certification, and hospital privileging.

---

## 2. NPI (National Provider Identifier)

### 2.1 Overview

The National Provider Identifier (NPI) is a unique 10-digit identifier for healthcare providers, required by HIPAA (45 CFR 162.406) for all standard transactions (claims, eligibility, remittance advice, etc.).

**Authorizing Statute:** HIPAA Administrative Simplification provisions (45 CFR Parts 160 and 162)

### 2.2 NPI Types

| NPI Type | Description | Example | Who Needs It |
|----------|-------------|---------|-------------|
| Type 1 (Individual) | Unique identifier for a single individual provider | 1234567890 | Physicians, dentists, nurses, therapists, chiropractors, all individual practitioners |
| Type 2 (Organization) | Unique identifier for an organization | 0987654321 | Hospitals, clinics, group practices, nursing homes, labs, home health agencies |

**Key Points:**
- NPIs are 10-digit numbers, with a check digit in the last position
- NPIs do not expire (unless the Taxonomy and/or Specialty/Provider Type changes)
- An individual provider needs only one Type 1 NPI regardless of how many states they practice in
- An organization needs one Type 2 NPI but may need multiple if separate subparts bill independently

### 2.3 NPI Application Process

**Application Channels:**
- **NPPES (National Plan and Provider Enumeration System):** Online portal at https://nppes.cms.hhs.gov
- **Paper form:** CMS-10114 (for individual providers who cannot access online)
- **Bulk enumeration:** Organizations can submit multiple applications via electronic file

**Application Steps (Online):**
1. Create an NPPES account (Identity Management System / I&A)
2. Complete the application (typically 30-45 minutes)
3. Provide: Legal name, date of birth, Social Security Number (Type 1) or EIN (Type 2), practice address, taxonomy code(s), contact information
4. Submit for processing
5. Receive NPI via email within approximately 10 business days

**Information Required:**
- Legal name (as it appears on the professional license)
- Date of birth (individual) or date of formation (organization)
- Social Security Number (Type 1) or EIN (Type 2)
- Mailing address and practice location address
- Taxonomy code(s) -- primary and any secondary
- License number and state
- Contact information (phone, fax, email)

### 2.4 Taxonomy Codes

Healthcare Provider Taxonomy Codes (HPTC) are 10-character alphanumeric codes that describe the provider type, classification, and specialization. Required for NPI enumeration and used in claims processing.

**Examples:**
- 207R00000X -- Internal Medicine Physician
- 207RC0000X -- Internal Medicine, Cardiovascular Disease
- 207Q00000X -- Family Medicine Physician
- 208D00000X -- General Practice Physician
- 363LF0000X -- Nurse Practitioner, Family
- 282N00000X -- General Acute Care Hospital

**Selecting Taxonomy Codes:**
- Each provider must select one primary taxonomy code (used in claims)
- Providers may have multiple taxonomy codes for different specialties
- The taxonomy code must match the scope of the state license

### 2.5 NPI Deactivation

NPIs are deactivated when:
- The provider dies (NPPES is updated by SSA death records)
- The provider retires and requests deactivation
- The provider fails to update their information (CMS may deactivate if records are stale)
- The provider's license is revoked or expired

**Reactivation:** Providers can submit a reactivation request through NPPES. Processing time varies.

---

## 3. TIN (Taxpayer Identification Number)

### 3.1 Types of TIN for Healthcare Providers

| TIN Type | Used By | Format |
|----------|---------|--------|
| SSN (Social Security Number) | Sole proprietors, individual providers | XXX-XX-XXXX |
| EIN (Employer Identification Number) | Corporations, LLCs, partnerships, group practices | XX-XXXXXXX |
| ITIN (Individual Taxpayer Identification Number) | Non-resident and resident aliens not eligible for SSN | 9XX-XX-XXXX |

### 3.2 TIN Matching for Claims

When a claim is submitted, the payer validates the NPI-to-TIN association:
- The claim must include both the billing provider NPI and the billing provider TIN
- The NPI must be associated with the correct TIN in the provider's enrollment file
- Mismatches result in claim rejections (not denials, but the claim is not accepted for processing)

**Common TIN Matching Issues:**
- NPI enumerated under old TIN (e.g., provider changed from sole proprietorship to PLLC)
- Group practice TIN used when individual provider NPI is expected
- Incorrect TIN on the claim due to data entry error
- Payer file not updated after TIN change

### 3.3 NPI-to-TIN Association

- Each Type 1 NPI can be associated with multiple TINs (e.g., provider works at a hospital and a private practice)
- Each Type 2 NPI is associated with one TIN (the organization's TIN)
- The association is established during Medicare enrollment and payer credentialing
- Claims submitted under a specific TIN must reference the NPI associated with that TIN

---

## 4. Medicare Enrollment

### 4.1 CMS Enrollment Applications

| Form Number | Title | Who Uses | Key Information |
|-------------|-------|----------|-----------------|
| CMS-855I | Medicare Enrollment Application for Individual Practitioners | Individual physicians, non-physician practitioners (NPs, PAs, CRNAs, etc.) | Professional information, license, practice locations, billing arrangements, disclosure information |
| CMS-855B | Medicare Enrollment Application for Clinics/Group Practices and Other Suppliers | Group practices, clinics, DME suppliers, labs, therapy practices | Group information, practice locations, reassignment of benefits, managing employees |
| CMS-855R | Reassignment of Medicare Benefits | Any provider reassigning benefits to another entity | Authorization for Medicare payments to be sent to a different provider/organization |
| CMS-855A | Medicare Enrollment Application for Institutional Providers | Hospitals, SNFs, HHAs, hospices, ESRD facilities | Facility information, ownership, chain organization, managing employees |
| CMS-588 | Electronic Funds Transfer (EFT) Agreement | Any enrolled provider | Bank account information for Medicare payment deposits |

### 4.2 Medicare Enrollment Process

**Timeline:** 60-120 days on average (longer if there are issues or if OIG/CIG scrutiny is triggered)

**Steps:**
1. **Obtain NPI:** If the provider does not already have one
2. **Complete the Application:** Submit the appropriate CMS-855 form with all supporting documentation
3. **Submit to MAC:** The application is submitted to the Medicare Administrative Contractor (MAC) for the provider's jurisdiction
4. **Application Review:** The MAC reviews for completeness and accuracy
5. **Verification:** The MAC verifies credentials, license status, and screens against OIG/GSA exclusion lists
6. **Site Visit (if applicable):** Some provider types require an on-site review
7. **Approval:** The provider receives a Medicare billing number (PTAN -- Provider Transaction Access Number)
8. **EFT Setup:** Complete CMS-588 for electronic payment

**Supporting Documentation:**
- Copy of state professional license
- Copy of DEA certificate (if applicable)
- Board certification documentation (if applicable)
- Malpractice insurance face page
- EIN confirmation letter (from IRS)
- Proof of business entity (articles of incorporation, LLC filing)
- Voided check (for EFT setup)

### 4.3 PECOS (Provider Enrollment, Chain, and Ownership System)

PECOS is the web-based system for Medicare enrollment management.

**Functions:**
- Submit initial Medicare enrollment applications
- Make changes to existing enrollment (address, ownership, reassignment)
- View enrollment status
- Revalidate enrollment
- Order and certify Medicare items and services

**PECOS Enrollment Status:**
- **Approved:** Provider is enrolled and may bill Medicare
- **Pending:** Application is under review
- **Deactivated:** Enrollment has been deactivated (failure to revalidate, death, retirement)
- **Rejected:** Application was denied
- **Withdrawn:** Provider withdrew their application
- **Opt-Out:** Provider has opted out of Medicare (private contracting)

### 4.4 Medicare Opt-Out Affidavit

Providers may opt out of the Medicare program by signing an affidavit that:
- Opts the provider out of Medicare Part B for all covered items and services for 2 years
- Allows the provider to enter into private contracts with Medicare beneficiaries
- Prohibits the provider from billing Medicare directly
- Requires the beneficiary to pay for services out of pocket (or through private insurance)

**Opt-Out Requirements:**
- Must opt out for ALL Medicare patients (cannot selectively opt out)
- Must renew every 2 years (new affidavit required)
- Must be a physician or practitioner type eligible to opt out
- Must not have billed Medicare in the prior 2 years for the services being opted out

### 4.5 Medicare Revalidation

- **Frequency:** Every 5 years (may be more frequent based on risk screening)
- **Process:** Provider receives a notice to revalidate via PECOS
- **Required:** Updated information, including license verification, exclusion screening
- **Consequence of Failure:** Deactivation of Medicare billing privileges
- **Risk Categories:** Limited (revalidate every 5 years), Moderate (every 3 years), High (every 3 years but higher level of screening)

---

## 5. Medicaid Enrollment

### 5.1 Overview

Medicaid enrollment is state-specific. Each state operates its own Medicaid program with its own enrollment forms, processes, and requirements. There is no centralized system analogous to Medicare PECOS for Medicaid enrollment.

### 5.2 State-Specific Enrollment

**Common Requirements Across States:**
- Completed state-specific enrollment application
- Copy of professional license (state-issued)
- NPI and EIN
- DEA registration (if applicable)
- Malpractice insurance proof
- W-9 form
- Disclosure of ownership and control
- Fingerprinting and background check (some states)
- Site visit (some states, some provider types)
- Application fee (varies by state)

**Enrollment Process:**
1. Contact the state's Medicaid agency or fiscal agent
2. Obtain the specific application form (may be online or paper)
3. Complete all sections and provide all requested documentation
4. Submit to the state's provider enrollment unit
5. Processing time: 30-120 days depending on the state

### 5.3 Managed Care Organization (MCO) Enrollment

Most Medicaid beneficiaries are enrolled in managed care plans. Providers must enroll with each MCO individually, in addition to the state's fee-for-service enrollment.

**MCO Enrollment Requirements:**
- Proof of state Medicaid enrollment
- CAQH application (most MCOs use CAQH)
- Credentialing verification (education, training, board certification, malpractice history)
- Site visit (some MCOs)
- Contract execution

### 5.4 Medicare/Medicaid Dual Enrollment

Providers serving dually eligible beneficiaries (Medicare and Medicaid) must:
- Enroll in Medicare (via PECOS and MAC)
- Enroll in Medicaid (state-specific)
- Enroll in applicable Medicare-Medicaid Plans (MMPs) or Dual Eligible Special Needs Plans (D-SNPs)

### 5.5 National Provider Identifier for Medicaid

- All Medicaid claims require NPI
- Some states require both Type 1 and Type 2 NPI
- NPI must be enrolled in the state's Medicaid program before billing

---

## 6. Commercial Payer Enrollment

### 6.1 Network Participation Application

Becoming a participating provider in a commercial insurance network involves:

**Application Components:**
1. **Provider Demographic Information:** Name, NPI, TIN, practice address, phone, fax
2. **License and Credentials:** State license, DEA, board certification, education, training
3. **Practice Information:** Hours, languages spoken, hospital affiliations, accepting new patients
4. **Ownership and Disclosure:** Ownership information, conflicts of interest, prior sanctions
5. **Signature and Agreement:** Acceptance of payer's participation agreement and fee schedule

### 6.2 Provider Contract Negotiation

**Key Contract Terms to Review:**
- Fee schedule (percentage of Medicare, or negotiated rates)
- Timely filing limits (typically 90-180 days from date of service)
- Claims submission requirements (electronic, clearinghouse, direct)
- Credentialing timeframe (typically 90-120 days)
- Termination provisions (30-90 days notice)
- Clean claim payment timeline (typically 15-45 days)
- Retroactive effective date (typically date of application or date of approval)
- Out-of-network billing policies

### 6.3 Provider Directory Requirements (No Surprises Act)

The No Surprises Act (effective January 1, 2022) requires:
- **Accurate Provider Directories:** Health plans must maintain accurate, up-to-date provider directories
- **Verification of Directory Information:** Plans must verify and update directory information at least every 90 days
- **Continuity of Care:** If a provider leaves a network, patients in active treatment have continuity of care protections

**Provider Requirements Under the No Surprises Act:**
- Notify payers within 30 days of any change in practice information
- Respond to payer directory verification requests
- Maintain accurate participation information
- Good faith estimate requirements for uninsured/self-pay patients (effective 2022)

### 6.4 Timely Filing

Commercial payers have specific timely filing requirements:
- **Typical limits:** 90-180 days from date of service (or date of discharge for inpatient)
- **Medicare:** Generally 12 months (Part A Billed 12 months, Part B sometimes 12 months but can vary by MAC)
- **Medicaid:** Varies by state (typically 90-365 days)
- **Timely Filing Waiver:** For delays beyond the provider's control (e.g., out-of-network gap fill, credentialing delays)

**Credentialing and Timely Filing:**
- If a provider's credentialing is delayed, they may be unable to bill for services rendered during the pending period
- Many payers will allow retroactive billing once credentialing is approved (typically back to the date of application)
- Retroactive billing periods vary (some payers allow 90 days, others only back to the approval date)

---

## 7. CAQH (Council for Affordable Quality Healthcare)

### 7.1 Overview

CAQH ProView is a standardized credentialing database used by most commercial health plans, hospitals, and healthcare organizations. It allows providers to enter their credentialing information once, and multiple organizations can access it, avoiding duplicate data entry.

**Key Facts:**
- Used by over 1,000 health plans, hospitals, and healthcare organizations
- Used by over 2 million healthcare providers
- Streamlines the credentialing process but does not replace individual payer credentialing
- Must be updated quarterly (auto-attestation every 90 days)

### 7.2 CAQH ProView

ProView collects and maintains provider data in the following categories:

**Demographic Information:**
- Legal name, date of birth, gender
- Practice name, address, phone, fax, email
- Web presence (website, social media)
- Languages spoken

**Professional Education:**
- Medical school or professional school
- Internship, residency, fellowship
- Dates of attendance, completion, degrees

**Licensing and Certification:**
- State medical licenses (all states)
- DEA registration
- Medicare/Medicaid identification
- Board certification(s) and recertification dates
- Other certifications (ACLS, BLS, PALS, ATLS)

**Practice History:**
- Work history for the past 5-10 years
- Practice locations and affiliations
- Hospital privileges

**Hospital Privileges:**
- Current and past hospital affiliations
- Privilege types (active, courtesy, provisional)
- Privilege start and end dates

**Malpractice History:**
- Current malpractice insurance carrier and policy limits
- Claims history (usually past 10 years)
- Any settlements or judgments

**Professional References:**
- Peer references
- Department chairs or medical directors

**Sanction/Exclusion History:**
- OIG exclusions
- State Medicaid exclusions
- Medicare sanctions
- License restrictions or reprimands
- Other adverse actions

### 7.3 CAQH Attestation

Every 90 days, CAQH requires the provider to either:
- Review all data and attest to its accuracy (auto-attest), or
- Update information and then attest

**Consequences of Missed Attestation:**
- CAQH data is marked as "not current" and is no longer available to requesting organizations
- Payer credentialing may be delayed or suspended
- Re-credentialing may be triggered manually

### 7.4 Claims Attestation

CAQH Claims Attestation verifies provider information before it is imported into payer systems. Payers may request this as part of the credentialing or re-credentialing process.

### 7.5 DirectData

CAQH DirectData allows providers to share credentialing data directly with specific organizations (not through the standard ProView access list).

### 7.6 Best Practices for CAQH Management

- Designate a credentialing specialist to manage CAQH updates
- Set calendar reminders for the 90-day attestation cycle
- Update information immediately when changes occur (address, license renewal, DEA renewal)
- Verify that all data is complete and accurate before each attestation
- Maintain copies of all supporting documentation (licenses, diplomas, board certifications)
- Review CAQH data sharing permissions periodically

---

## 8. Provider Enrollment Maintenance

### 8.1 Ongoing Maintenance Requirements

Provider enrollment is not a one-time event. Continuing obligations include:

| Requirement | Frequency | Action Required |
|-------------|-----------|----------------|
| Medicare Revalidation | Every 5 years | Submit updated CMS-855 through PECOS |
| CAQH Attestation | Every 90 days | Review and attest to data accuracy |
| State License Renewal | Every 1-4 years (state-dependent) | Renew with state medical board, report to payers |
| DEA Registration Renewal | Every 3 years (Schedule II-V) | Renew online or by paper, report to payers |
| Board Certification Renewal | Varies by specialty board | Complete MOC requirements, renew certification |
| Malpractice Insurance Renewal | Annually | Provide updated proof of coverage |
| OIG Exclusion Screening | Monthly | Verify no exclusion from federal programs |
| Payer Directory Verification | Every 90 days (NSA requirement) | Respond to verification requests |
| Address / Ownership Changes | As they occur | Update all payer enrollment files within 30 days |

### 8.2 Address / Ownership Change Updates

**Changes That Must Be Reported (within 30-90 days depending on payer):**
- Practice location address
- Mailing address
- Billing address
- Change of ownership (CHOW) for organizations
- Addition/removal of practice locations
- New or closed office locations

**Process:**
1. Update CAQH ProView
2. Update NPPES (NPI record)
3. Update PECOS (Medicare enrollment)
4. Update state Medicaid enrollment
5. Update each commercial payer enrollment
6. Update hospital medical staff office
7. Update practice management system and billing software

### 8.3 Tax ID Changes

When a provider changes their tax ID (e.g., from SSN to EIN, or to a new EIN):
1. Obtain the new EIN from the IRS
2. Update NPPES (add new TIN to NPI record)
3. Submit Medicare enrollment change (CMS-855)
4. Submit new state Medicaid applications (this is a new enrollment, not an update)
5. Re-credential with commercial payers (new contract typically required)
6. Update practice management system
7. Reprocess any pending claims (old TIN claims will reject)

**Timeline:** 60-90 days for Medicare TIN changes, 60-120 days for commercial payers

### 8.4 Practice Location Changes

**When adding a new location:**
1. Verify the new location is within the provider's existing payer networks
2. Update CAQH with the new location
3. Update NPPES (add practice location address)
4. Update PECOS (add practice location)
5. Update each payer's provider directory
6. Submit credentialing application for the new location (if required)

**When closing a location:**
1. Notify payers within 30 days
2. Notify patients (transfer of records, continuity of care)
3. Update CAQH, NPPES, PECOS
4. Arrange medical records storage (per state record retention laws)
5. Notify hospital medical staff office (if applicable)

---

## 9. DEA Registration

### 9.1 Overview

The Drug Enforcement Administration (DEA) registration is required for practitioners who prescribe, dispense, or administer controlled substances.

**Authorizing Statute:** Controlled Substances Act (21 U.S.C. Section 823)

### 9.2 DEA Schedules

| Schedule | Definition | Examples | Registration Period |
|----------|------------|----------|-------------------|
| Schedule II | High potential for abuse, currently accepted medical use, severe dependence | Morphine, oxycodone, fentanyl, Adderall | 3 years |
| Schedule III | Lower potential for abuse than II, moderate to low dependence | Tylenol with codeine, testosterone, ketamine | 3 years |
| Schedule IV | Low potential for abuse relative to III, limited dependence | Xanax, Valium, Ambien, Ativan | 3 years |
| Schedule V | Lowest potential for abuse, limited dependence | Cough preparations with codeine, Lyrica | 3 years |
| Schedule I | No accepted medical use, high abuse potential | Heroin, LSD, marijuana (federal) | Not prescribable |

**Note:** Most physicians with prescribing privileges need Schedule II-V registration.

### 9.3 Application Process

**Initial Registration:**
1. Complete DEA Form 224 (online or paper)
2. Provide: Name, state license number and state, NPI, EIN/SSN, business address
3. Pay application fee (varies by registration category, approximately $888 for 3 years as of recent fee schedule)
4. Processing time: 4-6 weeks

**Renewal:**
- Automatic renewal notice sent 60 days before expiration
- Renew online via DEA's secure portal
- Must have an active state license to renew
- Fee required each renewal period

**DEA Number Format:** XX0000000 (two letters, seven numbers)

### 9.4 Reporting Requirements

- **Change of address:** Must notify DEA within 30 days
- **Change of name:** Must obtain amended registration
- **Theft or significant loss:** Must notify DEA immediately (Form 106)
- **Closure of practice:** Must surrender DEA certificate

### 9.5 State-Level Controlled Substance Registrations

Some states require additional controlled substance registration beyond the federal DEA registration. These are typically handled by the state pharmacy board or state health department.

---

## 10. State Medical Licenses

### 10.1 Overview

Each state independently issues medical licenses. There is no national medical license, and state medical boards operate autonomously. A physician must hold a license in each state where they practice.

### 10.2 Licensing by State

**Typical Requirements for State Medical Licensure:**
- Graduation from an accredited medical school (LCME or AOA for US schools)
- Completion of ACGME or AOA accredited residency (minimum 1-3 years, varies by state)
- Passing scores on USMLE (Steps 1, 2, 3) or COMLEX-USA (Levels 1, 2, 3)
- Board certification or eligibility
- Letter of recommendation or professionalism
- Fingerprinting and criminal background check
- Hospital affiliation or employment verification
- Personal interview (some state boards)
- Licensure by endorsement (if already licensed in another state)

**Application Materials Required:**
- Completed state-specific application form
- Transcripts (medical school, residency)
- USMLE/COMLEX score reports
- Licensure verification from all states where currently or previously licensed
- Personal statement (some state boards)
- Verification of prior employment and practice history
- Malpractice insurance history
- OIG clearance
- NPI
- EIN or SSN
- Photo identification
- Application fee (varies, typically $300-$1,000+)

**Processing Time:** 30-180 days depending on the state

### 10.3 License Renewal

| Renewal Cycle | States | Typical Requirements |
|-------------|--------|---------------------|
| Annual | A few states | CE credits, license fee |
| Biennial (2 years) | Most common | CME credits (typically 25-50 per year), license fee |
| Triennial (3 years) | Some states | CME credits, license fee |
| Quadrennial (4 years) | Rare | CME credits, license fee |

**Continuing Medical Education (CME):**
- Most states require 25-50 hours of CME per year
- Some states have specific CME requirements (pain management, controlled substances, ethics, cultural competency)
- Many states accept AMA PRA Category 1 Credits
- Some accept AOA Category 1-A Credits (DOs)

### 10.4 IMLC (Interstate Medical Licensure Compact)

The IMLC is an agreement among participating states that expedites multi-state medical licensing for physicians who qualify.

**Participating States (as of current data):** 39+ states, including most but not all US states

**Benefits:**
- Reduced time to obtain additional state licenses
- Single application for the compact ("Compact Application")
- Expedited processing (typically 30-60 days)
- Reduced fees compared to individual state applications

**Eligibility Requirements:**
- Hold a full, unrestricted license in a state that is a member of the IMLC
- No history of disciplinary action
- No criminal convictions
- Not currently under investigation
- Meet the IMLC's licensure requirements

**Limitations:**
- Does not replace individual state licensure
- Some states participate in the compact but have additional state-specific requirements
- Not available for all provider types (primarily MDs and DOs)

### 10.5 FSMB (Federation of State Medical Boards)

The FSMB maintains the **Physician Data Center**, a database of disciplinary actions, medical licenses, and board certifications. Used by state medical boards to verify physician credentials during the licensing process.

---

## 11. Board Certification

### 11.1 ABMS (American Board of Medical Specialties)

The ABMS represents 24 member specialty boards that certify physicians in medical specialties and subspecialties.

**ABMS Member Boards (partial list):**
- American Board of Internal Medicine (ABIM)
- American Board of Family Medicine (ABFM)
- American Board of Pediatrics (ABP)
- American Board of Surgery (ABS)
- American Board of Anesthesiology (ABA)
- American Board of Emergency Medicine (ABEM)
- American Board of Obstetrics and Gynecology (ABOG)
- American Board of Radiology (ABR)
- American Board of Psychiatry and Neurology (ABPN)
- American Board of Orthopaedic Surgery (ABOS)

**Certification Requirements:**
- Graduation from an accredited medical school
- Completion of an accredited residency program
- Satisfactory completion of training (verified by program director)
- Passing the board certification examination (written and/or oral)
- Maintenance of Certification (MOC) requirements

### 11.2 Maintenance of Certification (MOC)

Board certification is no longer a one-time event. ABMS member boards require ongoing MOC:

**MOC Components (Cycle varies by board):**
1. **Part I: Professional Standing** -- Maintain a valid, unrestricted medical license
2. **Part II: Lifelong Learning and Self-Assessment** -- Earn CME credits, complete self-assessment modules
3. **Part III: Assessment of Knowledge** -- Pass a secure examination periodically (typically every 10 years)
4. **Part IV: Improvement in Medical Practice** -- Participate in practice improvement activities, outcomes measurement

**Consequences of Lapsed Certification:**
- Some payers require board certification for network participation
- Hospital privileges may require board certification
- Medical staff reappointment may be contingent on active board certification
- Some employment contracts require board certification

### 11.3 Other Certification Bodies

- **AOA (American Osteopathic Association):** Certifies DOs in specialty areas
- **Non-ABMS Certifications:** Some professions have their own certification bodies (e.g., American Board of Podiatric Medicine for podiatrists, American Board of Oral and Maxillofacial Surgery for oral surgeons)

---

## 12. CLIA Certification

### 12.1 Overview

The Clinical Laboratory Improvement Amendments of 1988 (CLIA) establish quality standards for all laboratory testing performed on human specimens. Any facility performing laboratory testing on human specimens for health assessment or disease diagnosis must have a CLIA certificate.

**Authorizing Statute:** 42 U.S.C. Section 263a; 42 CFR Part 493

### 12.2 CLIA Certificate Types

| Certificate Type | Test Complexity | Description | Examples |
|-----------------|-----------------|-------------|----------|
| Certificate of Waiver (CoW) | Waived tests only | Simple tests with low risk of error | Urine dipstick, pregnancy test, blood glucose fingerstick, flu test |
| Registration Certificate | Provider-performed microscopy (PPM) | Moderate complexity tests that are considered simple | Wet mounts, urinalysis, KOH preps, pinworm exams |
| Certificate for PPM | Moderate complexity | Tests that are categorized as moderate complexity | CBC, chemistry panels, coagulation studies |
| Certificate of Compliance | High complexity | Complex tests requiring more rigorous standards | Histopathology, flow cytometry, molecular diagnostics |
| Certificate of Accreditation | All complexities | Replaces CoC for laboratories accredited by a deemed accrediting organization | Joint Commission, CAP, COLA |

### 12.3 Application Process

1. **Determine test complexity:** Identify the tests to be performed (waived, moderate, or high)
2. **Complete CMS-116:** CLIA Application for Certification
3. **Submit to state agency:** The state's CLIA certification agency (or CMS regional office)
4. **Pay the fee:** Fee varies by certificate type and test volume
5. **Receive certificate:** Typically issued for 2 years

**Fee Schedule (Approximate):**
- Certificate of Waiver: $180-$600 (biennial, based on test volume)
- PPM Certificate: $300-$900
- Moderate/High Complexity: $600-$6,000+ (based on test volume and specialty)

### 12.4 CLIA and Provider Offices

- Physician office laboratories (POLs) require CLIA certification if performing any lab tests
- Tests performed outside of the physician office setting (reference lab) do not require a CLIA certificate for the ordering provider
- CLIA certification is site-specific (not provider-specific)

### 12.5 Consequences of Non-Compliance

- Civil monetary penalties
- Suspension, limitation, or revocation of CLIA certificate
- Criminal penalties for willful violations
- Exclusion from Medicare/Medicaid

---

## 13. Hospital Privileging

### 13.1 Overview

Hospital privileging is the process by which a hospital grants a provider permission to practice at the hospital and perform specific clinical services. It is governed by hospital medical staff bylaws and must comply with CMS Conditions of Participation and accreditation standards (The Joint Commission, DNV, HFAP).

### 13.2 Medical Staff Appointment

**Types of Medical Staff Membership:**
- **Active:** Full privileges, required participation in committee and medical staff activities
- **Courtesy:** Limited privileges (rare admissions)
- **Provisional:** New appointees, monitored for a period before advancement to full
- **Consulting:** Access only for consultation (no admitting privileges)
- **Honorary/Emeritus:** Retired providers, limited or no clinical privileges
- **Allied Health Professionals:** NPs, PAs, CRNAs, midwives, psychologists

### 13.3 Credentialing Committee

The hospital's credentialing committee (a subcommittee of the medical staff) reviews initial applications and reappointment applications.

**Review Process:**
1. **Application Receipt:** Provider submits completed application with supporting documents
2. **Primary Source Verification:** Hospital verifies credentials directly from the source:
   - Medical school transcripts and degrees
   - Residency and fellowship completion
   - State medical license (verified online or through FSMB)
   - DEA registration (verified through DEA database)
   - Board certification (verified through ABMS or AOA)
   - Malpractice insurance (certificate of coverage)
   - Malpractice claims history (National Practitioner Data Bank query)
   - OIG/GSA exclusion list check
   - Work history and gap analysis
   - Professional references
3. **Department Chair Review:** Clinical department head reviews qualifications
4. **Credentialing Committee:** Reviews and recommends to the medical board
5. **Governing Board:** Final approval
6. **Privilege Delineation:** Specific list of procedures and services the provider may perform

### 13.4 Reappointment Cycle

- **Typical cycle:** Every 2 years
- **Requirements:**
  - Updated application
  - Current license verification
  - Current DEA verification
  - CME documentation
  - Case log or activity summary
  - Quality metrics (OPPE data)
  - Malpractice claims update
  - NPDB query
  - OIG/GSA exclusion screening
  - Peer review summary

### 13.5 OPPE (Ongoing Professional Practice Evaluation)

The Joint Commission standard MS.08.01.03 requires OPPE for all practitioners with clinical privileges.

**OPPE Components:**
- Ongoing monitoring of clinical competence
- Data collection at least every 6 months (typically quarterly)
- Review of:
  - Patient outcomes
  - Procedure complications
  - Infection rates
  - Readmission rates
  - Patient satisfaction
  - Compliance with medical record requirements
  - Peer review feedback
  - Morbidity and mortality data

### 13.6 FPPE (Focused Professional Practice Evaluation)

FPPE is required for:
- New applicants for privileges (all new providers)
- Existing providers requesting new or additional privileges
- Providers with identified performance issues

**FPPE Methods:**
- Chart review (predetermined number of cases, typically 5-20)
- Direct observation
- Proctoring
- Simulation
- External review

### 13.7 National Practitioner Data Bank (NPDB)

The NPDB is a confidential database of:
- Medical malpractice payments
- Adverse licensure actions
- Adverse clinical privileges actions
- Adverse professional society membership actions
- Exclusion actions (OIG, DEA)
- Healthcare-related criminal convictions and civil judgments

**NPDB Query Requirements:**
- Hospitals must query the NPDB when granting initial privileges
- Hospitals must query the NPDB at reappointment (every 2 years)
- Managed care plans may query the NPDB for credentialing
- Providers may self-query

---

## 14. Agent Q&A Pairs

**Q: What is the difference between a Type 1 and Type 2 NPI?**

**A:** A Type 1 NPI identifies an individual healthcare provider (e.g., a physician, nurse, dentist). A Type 2 NPI identifies an organization (e.g., a hospital, group practice, clinic). Individual providers need only one Type 1 NPI regardless of how many states they practice in. Organizations need one Type 2 NPI but may need multiple if separate subparts bill independently. Both are 10-digit numbers.

**Q: What is CAQH and how does it work?**

**A:** CAQH (Council for Affordable Quality Healthcare) ProView is a centralized credentialing database used by over 1,000 health plans, hospitals, and healthcare organizations. Providers enter their credentialing information once, and authorized organizations can access it. The provider must review and attest to the accuracy of their data every 90 days (auto-attestation). CAQH does not replace individual payer credentialing but streamlines the process by providing verified data.

**Q: What is the Medicare enrollment process and how long does it take?**

**A:** The provider submits the appropriate CMS-855 form (855I for individuals, 855B for groups, 855A for institutions) to their Medicare Administrative Contractor (MAC). The MAC reviews the application, verifies credentials, screens for exclusions, and issues a PTAN (Provider Transaction Access Number) upon approval. The process typically takes 60-120 days. The provider also needs to complete CMS-588 for electronic funds transfer.

**Q: What is PECOS and what is it used for?**

**A:** PECOS (Provider Enrollment, Chain, and Ownership System) is CMS's web-based system for Medicare enrollment management. Providers use PECOS to: submit initial enrollment applications, make changes to existing enrollment (address, ownership, reassignment), view enrollment status, revalidate enrollment (every 5 years), and order/certify Medicare items and services.

**Q: What happens when a provider misses their CAQH 90-day attestation?**

**A:** When a provider misses the 90-day attestation, their CAQH data is marked as "not current" and becomes inaccessible to requesting organizations. This can delay or suspend payer credentialing and re-credentialing. The provider must log in, update any outdated information, attest to the data's accuracy, and the data becomes available again. Payer credentialing processes that were waiting on CAQH data may need to be re-initiated.

**Q: What is the 5-level Medicare appeals process?**

**A:** Level 1: Redetermination by the MAC (120 days to appeal). Level 2: Reconsideration by a QIC (180 days from Level 1 decision). Level 3: ALJ Hearing before an HHS ALJ (60 days from Level 2, $180 minimum threshold). Level 4: Medicare Appeals Council review (60 days from Level 3). Level 5: Federal District Court (60 days from Level 4, $1,840 minimum threshold).

**Q: What is the NPI-to-TIN association, and why does it matter for claims?**

**A:** The NPI-to-TIN association links a provider's NPI to the tax ID used for billing. When a claim is submitted, the payer validates that the NPI on the claim is associated with the TIN on the claim. If the NPI is not associated with the correct TIN, the claim is rejected (not paid). This commonly happens when a provider changes from sole proprietorship (SSN-based) to an LLC (EIN-based) without updating the association.

**Q: What are the requirements under the No Surprises Act for provider directories?**

**A:** The No Surprises Act requires: (1) Health plans to maintain and periodically verify accurate provider directories, (2) Providers to notify payers within 30 days of any change in practice information (address, phone, hours, accepting new patients, network participation status), (3) Plans to verify directory information at least every 90 days, (4) Continuity of care protections when a provider leaves a network. Inaccurate directories can result in patient balance billing protections.

**Q: What is the difference between initial credentialing and re-credentialing?**

**A:** Initial credentialing is the first-time verification of a provider's qualifications when joining a network or hospital. Re-credentialing is the periodic (typically every 2-3 years) review to confirm the provider continues to meet standards. Re-credentialing is generally less intensive than initial credentialing, focusing on any changes since the last review and verifying continued good standing. Most payers use CAQH data for re-credentialing.

**Q: What is the IMLC and what are its benefits?**

**A:** The Interstate Medical Licensure Compact (IMLC) is an agreement among 39+ states that expedites multi-state medical licensing for physicians (MDs and DOs). Benefits include: reduced time to obtain additional state licenses (30-60 days), single application process, reduced fees, and faster processing compared to individual state applications. The IMLC does not replace individual state licensure but streamlines it.

**Q: What is hospital privileging and how does it differ from state licensure?**

**A:** State licensure is issued by the state medical board and grants the provider the legal right to practice medicine in that state. Hospital privileging is granted by the hospital's governing board and gives the provider permission to treat patients and perform specific clinical services at that particular hospital. Licensure is a prerequisite for privileging, but a licensed provider is not automatically granted privileges. Privileging involves a separate credentialing committee review, primary source verification, and delineation of specific clinical privileges.

**Q: What is the CLIA certification requirement for physician offices?**

**A:** Any physician office that performs laboratory testing on human specimens for health assessment or disease diagnosis must have a CLIA certificate. The type of certificate depends on the complexity of tests performed: Certificate of Waiver (simple tests like urinalysis, strep tests, glucose), PPM Certificate (microscopy), or Moderate/High Complexity Certificate (CBC, chemistry panels). CLIA certification is site-specific (applies to the office location) and must be renewed biennially.

**Q: What is OPPE and what does it track?**

**A:** OPPE (Ongoing Professional Practice Evaluation) is a Joint Commission standard requiring hospitals to continuously monitor the clinical competence of all practitioners with clinical privileges. Data is collected at least every 6 months (typically quarterly) and tracks: patient outcomes, procedure complications, infection rates, readmission rates, patient satisfaction, medical record compliance, peer review feedback, and morbidity/mortality data.

**Q: What is the process for changing a provider's tax ID?**

**A:** When a provider changes tax ID (e.g., from SSN to EIN): (1) Obtain the new EIN from the IRS, (2) Update NPPES (add the new TIN to the NPI record), (3) Submit Medicare enrollment change via CMS-855 (this is treated as a new enrollment in some cases), (4) Submit new state Medicaid applications (considered a new enrollment), (5) Re-credential with commercial payers (requires a new contract in most cases), (6) Update practice management system. Processing time is 60-90 days for Medicare, 60-120 days for commercial payers. Claims submitted with the old TIN after the change will be rejected.

**Q: What is the National Practitioner Data Bank (NPDB)?**

**A:** The NPDB is a confidential federal database that collects and reports adverse actions against healthcare practitioners. It includes: medical malpractice payments, adverse licensure actions, adverse clinical privileges actions, adverse professional society actions, exclusion actions (OIG, DEA), and healthcare-related criminal convictions. Hospitals must query the NPDB when granting initial privileges and at reappointment. Providers may self-query.

**Q: What is the difference between an opt-out and deactivation in Medicare?**

**A:** Opt-out is a voluntary decision by a provider to not participate in Medicare Part B, allowing them to enter into private contracts with Medicare beneficiaries. The opt-out lasts 2 years and must be renewed. Deactivation is the involuntary suspension of Medicare billing privileges (typically for failure to revalidate, failure to respond to enrollment inquiries, death, or retirement). A deactivated provider cannot bill Medicare but can reactivate by submitting updated information.

**Q: What is the CMS-855R (Reassignment of Medicare Benefits) and when is it needed?**

**A:** The CMS-855R authorizes Medicare to send payments for a provider's services to a different entity (e.g., the provider's group practice or employer). It is needed when: (1) A provider works as an employee or independent contractor of a group practice, (2) A provider wants payments sent to a billing company, or (3) A provider or group reassigns benefits to a hospital or facility-based arrangement. The form must be signed by the reassigning provider.

**Q: How long does credentialing typically take with commercial payers?**

**A:** Commercial payer credentialing typically takes 60-120 days from the date of application. Some factors that affect timing include: (1) Completeness of the application, (2) CAQH data accuracy and attestation status, (3) Credentialing volume at the payer, (4) Verification requirements (primary source verifications), (5) Practitioner type (physicians versus allied health professionals), (6) Contract negotiation (if a new contract is needed), (7) Cleanliness of the provider's background (no disciplinary history, malpractice claims, or gaps in employment).

**Q: What provider information must be reported within 30 days of a change?**

**A:** The following changes must typically be reported within 30 days: (1) Practice location address, (2) Mailing address, (3) Phone and fax numbers, (4) Email address, (5) License renewal or change, (6) DEA registration change, (7) Hospital affiliation changes, (8) Medicare/Medicaid sanction or exclusion, (9) Adverse legal actions, (10) Change in accepting new patient status.

**Q: How does the No Surprises Act good faith estimate requirement work?**

**A:** For uninsured or self-pay patients, the No Surprises Act requires providers to deliver a good faith estimate (GFE) of expected charges for scheduled services. The GFE must include: (1) Expected charges for items and services, (2) Items and services reasonably expected to be provided as part of the scheduled visit, (3) Expected charges for each item or service, (4) A disclaimer that the actual charges may differ. The GFE must be provided within specific timeframes (1-3 business days depending on when the service is scheduled).

**Q: What is the process for a provider who wants to add a new practice location?**

**A:** (1) Verify the new location is within the provider's existing payer networks, (2) Update CAQH ProView with the new location, (3) Update NPPES (add practice location address to NPI record), (4) Update PECOS (add practice location to Medicare enrollment), (5) Update each payer's provider directory (per No Surprises Act requirements), (6) Submit credentialing application for the new location if the payer requires separate credentialing per location, (7) Obtain state license for the new location (if in same state, no new license needed; if different state, new license required).

**Q: What is a Taxonomy Code and why is it important?**

**A:** A Healthcare Provider Taxonomy Code is a 10-character alphanumeric code that describes a provider's type, classification, and specialization (e.g., 207R00000X for Internal Medicine). It is required for NPI enumeration and is used in claim processing. The taxonomy code must match the scope of the provider's state license. Selecting the correct taxonomy code is critical for claim payment and network participation.

**Q: What is FPPE and when is it required?**

**A:** FPPE (Focused Professional Practice Evaluation) is a hospital privileging process for: (1) New applicants for privileges (all new providers being granted initial privileges), (2) Existing providers requesting new or additional privileges (e.g., a cardiologist requesting interventional cardiology privileges), (3) Providers with identified performance issues (e.g., higher than expected complication rates). FPPE methods include chart review, direct observation, proctoring, simulation, and external review. The period typically covers 5-20 cases.

**Q: What is the Medicare opt-out process and who is eligible?**

**A:** Providers eligible to opt out include physicians (MDs, DOs) and certain non-physician practitioners (NPs, PAs, CRNAs, clinical social workers, psychologists). To opt out: (1) Sign an affidavit stating the provider will not bill Medicare for Part B services for 2 years, (2) File the affidavit with all MACs in the provider's jurisdiction, (3) Enter into private contracts with Medicare beneficiaries (required for each patient). The provider must opt out for ALL Medicare patients and cannot selectively opt out. The opt-out renews automatically every 2 years unless revoked.

**Q: What are the consequences of credentialing lapses for claim payment?**

**A:** If a provider's credentialing lapses with a payer (e.g., due to missed re-credentialing, license expiration, or CAQH attestation failure): (1) Claims for services rendered during the lapsed period may be denied, (2) The provider may be removed from the payer's network, (3) Retroactive reinstatement and billing may be possible but depends on the payer's policies, (4) Patients may be balance-billed (if out-of-network), (5) Provider directory information becomes inaccurate. Timely re-credentialing is essential to avoid these consequences.

**Q: What is the difference between a clean claim and a dirty claim?**

**A:** A clean claim is one that can be processed without additional information or documentation. It has: correct patient and provider identifiers, valid ICD-10 and CPT codes, accurate modifiers, correct place of service, valid dates of service, and no data errors. A dirty (or "unclean") claim requires manual review or additional documentation before it can be processed. Examples: invalid NPI/TIN, mismatched NPI-to-TIN, missing or invalid modifiers, non-covered procedure codes, unbundling, incorrect patient demographics.

---

## 15. References

- 45 CFR Part 162 (HIPAA Administrative Simplification -- NPI)
- 42 CFR Part 424 (Medicare Enrollment)
- 42 CFR Part 493 (CLIA)
- 21 U.S.C. Section 823 (DEA Registration)
- 42 U.S.C. Section 263a (CLIA)
- CMS NPI Overview: https://www.cms.gov/Regulations-and-Guidance/Administrative-Simplification/NationalProvIdentStand
- PECOS: https://pecos.cms.hhs.gov
- NPPES: https://nppes.cms.hhs.gov
- CAQH ProView: https://proview.caqh.org
- IMLC: https://www.imlcc.org
- ABMS: https://www.abms.org
- OIG Exclusion List: https://oig.hhs.gov/exclusions/
- NPDB: https://www.npdb.hrsa.gov
- FSMB Physician Data Center: https://www.fsmb.org/physician-data-center/
- The Joint Commission Credentialing Standards: https://www.jointcommission.org