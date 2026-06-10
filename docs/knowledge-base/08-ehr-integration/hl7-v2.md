# HL7 v2: Healthcare Messaging Standard

## Overview

HL7 v2 (Health Level 7 version 2) is the most widely implemented healthcare messaging standard in the world. Developed by HL7 International, it defines a framework for exchanging clinical and administrative data between healthcare information systems. Despite its age (first released in 1989), HL7 v2 remains the backbone of healthcare interoperability, with virtually every EHR and practice management system supporting some version of the standard.

For Denials Doctor, HL7 v2 is the secondary integration protocol (after FHIR R4). It is essential for integration with older or smaller EHR systems that do not offer FHIR APIs. HL7 v2 messages carry patient registration data, encounter information, orders, and financial transactions directly relevant to revenue cycle management.

---

## HL7 v2 Versions

### Version Differences

| Version | Year | Key Features | Status |
|---|---|---|---|
| v2.3 | 1997 | Core message types (ADT, ORM, ORU, DFT), basic segments | Legacy, limited use |
| v2.3.1 | 1999 | Enhanced financial segments, improved query support | Legacy, some production systems |
| v2.4 | 2000 | Added SIU (scheduling), RGV (pharmacy), enhanced OBX | Legacy |
| v2.5 | 2003 | Major revision, Z-segment standardization, enhanced PID/PV1 | Widely deployed |
| v2.5.1 | 2007 | US-specific enhancements, immunization reporting (VXU) | Widely deployed (US meaningful use) |
| v2.6 | 2007 | New message types (MDM, QBP), SFT segment | Limited adoption |
| v2.7 | 2011 | Enhanced medication, immunization, regulatory reporting | Moderate adoption |
| v2.8 | 2014 | Enhanced privacy consent, device interaction, lab automation | Early adoption, growing |
| v2.9 | 2019 | Terminology updates, new segments for patient-generated data | Emerging |

### Backwards Compatibility

HL7 v2 maintains backwards compatibility across versions. A v2.3 message parser can typically process v2.5 messages with minimal changes (newer segments are simply ignored). This is by design — the standard adds segments and fields without breaking existing parsers. However, newer versions deprecate some fields and add new ones that may be critical for certain workflows.

For Denials Doctor, HL7 v2.5.1 is the minimum target version, as it is required for US meaningful use certification. v2.6+ support is preferred where available.

---

## Message Structure

HL7 v2 messages are delimited text with a hierarchical structure:

```
MSH|^~\&|SENDING_APP|SENDING_FACILITY|RECEIVING_APP|RECEIVING_FACILITY|20250203103045||ADT^A01|MSG001|P|2.5.1
EVN|A01|20250203103045|||
PID|1||MRN-98765^^^HOSP^MR||Smith^John^Michael^^^||19750315|M|||123 Main St^^Anytown^CA^90210^^H||(555)123-4567|||S||123-45-6789|||||||
PV1|1|O|ER^ER-1^123||||1234567893^Doe^Jane^M^^Dr.^MD^^^NPI|||||||||||V12345^Visit^2025|||||||||||||||||||||||||20250203083045|20250203093045
```

### Hierarchy

```
Message (one complete HL7 exchange)
  └── Segment (line of data, 3-character ID, fields separated by |)
       └── Field (data element, separated by | within segment)
            └── Component (sub-field, separated by ^ within field)
                 └── Sub-Component (sub-sub-field, separated by & within component)
```

### Encoding Characters (MSH-2)

The second field of the MSH segment defines the encoding characters used throughout the message:

```
MSH|^~\&|
  |  = field separator
  ^  = component separator
  ~  = repetition separator
  \  = escape character
  &  = sub-component separator
```

### Segment Delimiter

Segments are terminated with `\r\n` (carriage return + line feed, hexadecimal `0D 0A`). In some legacy implementations, just `\r` (carriage return, `0D`) is used. The segment delimiter is NOT the pipe character — each segment ends with a line break.

---

## Key Message Types

### ADT (Admit, Discharge, Transfer)

ADT messages carry patient registration and encounter data. These are the most common HL7 messages and are critical for maintaining patient demographics and visit status.

| Trigger Event | Description | Denials Doctor Relevance |
|---|---|---|
| **A01** | Admit/Visit Notification | Patient admitted; creates encounter context for billing |
| **A02** | Transfer Patient | Patient moved to different room/unit; updates encounter location |
| **A03** | Discharge/End Visit | Patient discharged; triggers charge capture and claim creation |
| **A04** | Register Patient | Outpatient registration (no admit); creates encounter record |
| **A05** | Pre-Admit Patient | Patient scheduled for future admission; creates pending encounter |
| **A06** | Change Outpatient to Inpatient | Important for billing — changes encounter class |
| **A07** | Change Inpatient to Outpatient | Important for billing — changes encounter class |
| **A08** | Update Patient Information | Demographics update (address, insurance, name change) |
| **A10** | Cancel Admission | Admission cancelled — clean up any charges/claims |
| **A11** | Cancel Discharge | Discharge undone; patient still in hospital |
| **A12** | Cancel Transfer | Transfer was cancelled |
| **A13** | Cancel Discharge/End Visit | Visit end was cancelled |
| **A18** | Merge Patient Information | Two patient records merged into one — critical for accurate billing |
| **A28** | Add Person Information | Create new patient record (registration without encounter) |
| **A31** | Update Person Information | Update patient demographics (non-encounter context) |
| **A34** | Merge Patient Information — Patient ID Only | Partial patient merge (IDs only) |
| **A35** | Merge Patient Information — Account Number Only | Merge account records |
| **A38** | Cancel Pre-Admit | Pre-admission cancelled |
| **A40** | Merge Patient — Patient Identifier List | Merge patient records with identifier updates |

#### ADT^A01 Message Example

```
MSH|^~\&|HIS|HOSPITAL|RCM|DENIALSDR|202502031030||ADT^A01|12345|P|2.5.1
EVN|A01|202502031030|||||
PID|1||98765^^^HOSP^MRN||Smith^John^Michael^^^||19750315|M|||123 Main St^^Anytown^CA^90210^^H||(555)123-4567|||S||123-45-6789|||||||
PV1|1|I|MED^MED-1^123|||1234567893^Doe^Jane^M^^Dr.^MD^^^NPI|||ATT|||||||ACC-12345||||||||||||||||||||||||202502030800|202502030830|
GT1|1||Smith^John^^^||123 Main St^^Anytown^CA^90210^^H||(555)123-4567|(555)987-6543||19750315|M|SELF|||||||||||
IN1|1|BCBS|BLUECROSS-123|Blue Cross Blue Shield|||BLAH12345678|||Group-1234|||COB|Smith^John^^^|SELF|19750315|123 Main St^^Anytown^CA^90210^^H||(555)123-4567|||||||Individual|PREFERRED|PPO|||2024|20250101|20251231|
```

#### ADT^A03 (Discharge) Message

```
MSH|^~\&|HIS|HOSPITAL|RCM|DENIALSDR|202502051430||ADT^A03|12346|P|2.5.1
EVN|A03|202502051430|||||
PID|1||98765^^^HOSP^MRN||Smith^John^Michael^^^||19750315|M|||123 Main St^^Anytown^CA^90210^^H||(555)123-4567|||S||123-45-6789|||||||
PV1|1|I|MED^MED-1^123|||1234567893^Doe^Jane^M^^Dr.^MD^^^NPI|||ATT|DIS|Home||ACC-12345||||||||||||||||||||||||202502030800|202502051430|
```

---

### ORM (Order Entry)

ORM messages communicate orders (lab, radiology, pharmacy, procedures) between systems.

| Trigger Event | Description | Relevance |
|---|---|---|
| **O01** | Order Message | General order placement (most common) |
| O02 | Order Message | Future use |
| O03 | Order Message | Diet order |
| O04 | Order Message | Nursing order |
| **O05** | Order Message | Pharmacy order |
| **O06** | Order Message | Radiology order |

ORM messages map to FHIR's ServiceRequest resource. For RCM, ORM messages identify ordered procedures and tests that will generate billable charges.

#### ORM^O01 Example

```
MSH|^~\&|ORDERING|HOSPITAL|LAB|LABS|202502031100||ORM^O01|ORD-123|P|2.5.1
PID|1||98765^^^HOSP^MRN||Smith^John^Michael^^^||19750315|M|||123 Main St^^Anytown^CA^90210^^H||(555)123-4567|
PV1|1|O|CLINIC^CL-1^123|||1234567893^Doe^Jane^M^^Dr.^MD^^^NPI|
ORC|NW|ORD-123|||CM||||202502031100|||1234567893^Doe^Jane^M^^Dr.^MD^^^NPI|
OBR|1|ORD-123||80061^Lipid Panel^L|||202502031050|||||||202502031100||1234567893^Doe^Jane^M^^Dr.^MD^^^NPI|||202502031050||||||F|
TQ1|1|||202502031100|||||R|
```

---

### ORU (Observation Result)

ORU messages carry result data from lab, pathology, radiology, and other diagnostic systems.

| Trigger Event | Description | Relevance |
|---|---|---|
| **R01** | Unsolicited Observation Result | Most common — lab results, pathology, radiology reports |

For Denials Doctor, ORU messages provide clinical evidence needed for medical necessity reviews and prior authorization compliance verification.

#### ORU^R01 Example

```
MSH|^~\&|LAB|LABS|RCM|HOSPITAL|202502031200||ORU^R01|RES-123|P|2.5.1
PID|1||98765^^^HOSP^MRN||Smith^John^Michael^^^||19750315|M|||123 Main St^^Anytown^CA^90210^^H||(555)123-4567|
PV1|1|O|CLINIC^CL-1^123|||1234567893^Doe^Jane^M^^Dr.^MD^^^NPI|
OBR|1|ORD-123|80061^Lipid Panel^L|||202502031050|||||||202502031100||1234567893^Doe^Jane^M^^Dr.^MD^^^NPI|||202502031050||||||F|
OBX|1|NM|2093-3^Cholesterol^LN||190|mg/dL|100-199|H|||F|||202502031050|
OBX|2|NM|2571-8^Triglycerides^LN||150|mg/dL|0-149||N|||F|||202502031050|
OBX|3|NM|18262-6^HDL Cholesterol^LN||45|mg/dL|40-60|N|||F|||202502031050|
```

---

### DFT (Detailed Financial Transaction)

DFT messages communicate financial data including charges, payments, and adjustments.

| Trigger Event | Description | Relevance |
|---|---|---|
| **P03** | Post Charge | Service charge posted to patient account |
| **P05** | Post Payment | Payment received and posted |

DFT messages are critical for real-time charge capture and payment posting. When a charge is posted in the EHR's billing module, a DFT^P03 can be sent to Denials Doctor for claim validation before submission.

#### DFT^P03 Example

```
MSH|^~\&|BILLING|HOSPITAL|RCM|DENIALSDR|202502031400||DFT^P03|DFT-123|P|2.5.1
PID|1||98765^^^HOSP^MRN||Smith^John^Michael^^^||19750315|M|||123 Main St^^Anytown^CA^90210^^H||(555)123-4567|
PV1|1|I|MED^MED-1^123|||1234567893^Doe^Jane^M^^Dr.^MD^^^NPI|||ATT|||Home||ACC-12345||||||||||||||||||||||||202502030800|202502051430|
FT1|1|20250203|20250203|1|99213^Office Visit^CPT||25^Modifier^CPT||150.00||CH|||REV-1234|
FT1|2|20250203|20250203|1|80048^Basic Metabolic Panel^CPT|||75.00||CH|||REV-5678|
```

---

### SIU (Schedule Information Unsolicited)

SIU messages carry appointment scheduling information.

| Trigger Event | Description | Relevance |
|---|---|---|
| **S12** | Notification of New Appointment | New appointment booked |
| **S13** | Notification of Appointment Rescheduling | Existing appointment changed |
| **S14** | Notification of Appointment Modification | Appointment details updated |
| **S15** | Notification of Appointment Cancellation | Appointment cancelled |
| S16 | Notification of Appointment Discontinuation | Appointment series ended |
| S17 | Notification of Appointment Deletion | Appointment removed |

SIU messages help Denials Doctor maintain the encounter schedule and predict upcoming billing volumes.

---

### MDM (Medical Document Management)

MDM messages carry clinical documents.

| Trigger Event | Description |
|---|---|
| **T01** | Document Creation Notification |
| T02 | Document Update Notification |
| T03 | Document Status Change |
| T04 | Document Transcription |
| T05 | Document Amendment |
| T06-T11 | Various document management events |

---

### MFN (Master File Notification)

MFN messages update master files (provider registries, charge masters, diagnosis code tables).

| Trigger Event | Description |
|---|---|
| **M01** | Master File Change Notification |
| M02 | Staff/Practitioner Master File |
| M03 | Clinical Trial Master File |
| M04 | Charge Description Master File |
| M05 | Patient Location Master File |
| M06 | CDM (Charge Description Master) Update |

---

## Key Segment Details

### MSH — Message Header

Every HL7 v2 message starts with MSH. It identifies the message type, sender, receiver, and processing control.

| Field | Description | Example |
|---|---|---|
| MSH-1 | Field Separator | `|` |
| MSH-2 | Encoding Characters | `^~\&` |
| MSH-3 | Sending Application | `HIS` |
| MSH-4 | Sending Facility | `HOSPITAL` |
| MSH-5 | Receiving Application | `RCM` |
| MSH-6 | Receiving Facility | `DENIALSDR` |
| MSH-7 | Date/Time of Message | `20250203103045` (YYYYMMDDHHMMSS) |
| MSH-9 | Message Type | `ADT^A01` (trigger event) |
| MSH-10 | Message Control ID | `MSG001` — unique message identifier |
| MSH-11 | Processing ID | `P` (production), `T` (test), `D` (debug) |
| MSH-12 | Version ID | `2.5.1` |
| MSH-15 | Accept Acknowledgment Type | `AL` (always), `NE` (never), `ER` (error/reject only), `SU` (successful only) |
| MSH-16 | Application Acknowledgment Type | Same values as MSH-15 |

### PID — Patient Identification

The PID segment contains patient demographic data.

| Field | Description | Example |
|---|---|---|
| PID-1 | Set ID | `1` |
| PID-2 | Patient ID (external) | `98765^^^HOSP^MRN` — Patient ID with assigning authority |
| PID-3 | Patient Identifier List | `98765^^^HOSP^MRN~123456789^^^SSA^SS` — Multiple identifiers |
| PID-5 | Patient Name | `Smith^John^Michael^^^` (last^first^middle^suffix^prefix^degree) |
| PID-6 | Mother's Maiden Name | `Jones` |
| PID-7 | Date/Time of Birth | `19750315` |
| PID-8 | Administrative Sex | `M`, `F`, `U` (unknown), `O` (other) |
| PID-9 | Patient Alias | Alternate names (previous married name) |
| PID-10 | Race | `2106-3^White^CDCREC` |
| PID-11 | Patient Address | `123 Main St^^Anytown^CA^90210^^H` (street^other^city^state^zip^country^type) |
| PID-12 | County Code | `037` |
| PID-13 | Phone Number — Home | `(555)123-4567` |
| PID-14 | Phone Number — Business | `(555)987-6543` |
| PID-15 | Primary Language | `English^English^HL70436` |
| PID-16 | Marital Status | `M` (married), `S` (single), `D` (divorced), `W` (widowed) |
| PID-17 | Religion | `PRO^Protestant^HL70066` |
| PID-18 | Patient Account Number | `ACC-12345` — CRITICAL field for billing |
| PID-19 | SSN Number | `123-45-6789` |
| PID-22 | Ethnicity | `2186-5^Not Hispanic^CDCREC` |
| PID-23 | Birth Place | `Anytown General Hospital` |
| PID-24 | Multiple Birth Indicator | `N` |
| PID-25 | Birth Order | `1` |
| PID-29 | Patient Death Date and Time | `20250205163000` |
| PID-30 | Patient Death Indicator | `Y` |

PID-3 (Patient Identifier List) is critical for patient matching. It uses the format:
`ID^^^Assigning Authority^Identifier Type`

Standard identifier types:
- `MR` — Medical Record Number
- `SS` — Social Security Number
- `DL` — Driver's License Number
- `PI` — Patient Internal Identifier
- `MA` — Member Number (insurance)
- `NI` — National Identifier
- `PT` — Patient External Identifier

### PV1 — Patient Visit

The PV1 segment contains encounter/visit-specific information.

| Field | Description | Example |
|---|---|---|
| PV1-1 | Set ID | `1` |
| PV1-2 | Patient Class | `I` (inpatient), `O` (outpatient), `E` (emergency), `P` (preadmit) |
| PV1-3 | Assigned Patient Location | `ER^ER-1^123` (nursing unit^room^bed) |
| PV1-4 | Admission Type | `R` (routine), `E` (emergency), `U` (urgent), `N` (newborn) |
| PV1-7 | Attending Doctor | `1234567893^Doe^Jane^M^^Dr.^MD^^^NPI` |
| PV1-8 | Referring Doctor | `9876543210^Brown^Robert^^^Dr.^MD^^^NPI` |
| PV1-9 | Consulting Doctor | `555555555^White^Susan^^^Dr.^MD^^^NPI` |
| PV1-10 | Hospital Service | `MED` (medicine), `SUR` (surgery), `PED` (pediatrics), etc. |
| PV1-14 | Admit Source | `1` (physician referral), `2` (clinic referral), `7` (emergency room) |
| PV1-15 | Ambulatory Status | `A0` (no functional limitations) |
| PV1-17 | Admitting Diagnosis | `E11.9^Type 2 diabetes^I10` |
| PV1-19 | Visit Number | `V12345` — unique visit/encounter identifier |
| PV1-36 | Discharge Disposition | `01` (home), `02` (left AMA), `03` (transferred) |
| PV1-44 | Admit Date/Time | `20250203080000` |
| PV1-45 | Discharge Date/Time | `20250205163000` |
| PV1-50 | Alternate Visit ID | `ACC-12345` — financial account number |

### OBX — Observation/Result

OBX segments carry the actual result data in ORU messages.

| Field | Description | Example |
|---|---|---|
| OBX-1 | Set ID | `1` |
| OBX-2 | Value Type | `NM` (numeric), `ST` (string), `CE` (coded), `DT` (date), `TX` (text) |
| OBX-3 | Observation Identifier | `2093-3^Cholesterol^LN` (code^name^coding system) |
| OBX-4 | Observation Sub-ID | `1` — for sub-observations |
| OBX-5 | Observation Value | `190` — the actual result |
| OBX-6 | Units | `mg/dL` |
| OBX-7 | Reference Range | `100-199` — normal range |
| OBX-8 | Abnormal Flags | `H` (high), `L` (low), `A` (abnormal), `N` (normal) |
| OBX-11 | Observation Result Status | `F` (final), `P` (preliminary), `C` (corrected) |
| OBX-14 | Date/Time of Observation | `202502031050` |
| OBX-16 | Responsible Observer | `9876543210^Pathologist^Path^^^Dr.^MD^^^NPI` |
| OBX-17 | Observation Method | `LN^Liquid Chromatography^99LAB` |

### DG1 — Diagnosis

DG1 segments carry diagnosis information.

| Field | Description | Example |
|---|---|---|
| DG1-1 | Set ID | `1` |
| DG1-2 | Diagnosis Coding Method | `I10` (ICD-10-CM), `I9` (ICD-9-CM) |
| DG1-3 | Diagnosis Code | `E11.9` |
| DG1-4 | Diagnosis Description | `Type 2 diabetes mellitus without complications` |
| DG1-5 | Diagnosis Date/Time | `20250203` |
| DG1-6 | Diagnosis Type | `A` (admitting), `W` (working), `F` (final) |
| DG1-10 | Diagnosis Classification | `DX` (diagnosis), `ICD10` |
| DG1-26 | Diagnosis Priority | `1` (principal), `2` (secondary), etc. |
| DG1-29 | Present on Admission | `Y`, `N`, `U`, `W` |

### PR1 — Procedures

PR1 segments carry procedure information.

| Field | Description | Example |
|---|---|---|
| PR1-1 | Set ID | `1` |
| PR1-2 | Procedure Coding Method | `CPT4` |
| PR1-3 | Procedure Code | `47562` |
| PR1-4 | Procedure Description | `Laparoscopic cholecystectomy` |
| PR1-5 | Procedure Date/Time | `20250204` |
| PR1-6 | Procedure Functional Type | `1` (surgery), `2` (diagnostic procedure) |
| PR1-7 | Procedure Minutes | `75` |
| PR1-8 | Anesthesiologist | `1234567893^Doe^Jane^M^^Dr.^MD^^^NPI` |
| PR1-9 | Anesthesia Minutes | `90` |
| PR1-14 | Consent Code | `Y` |

### IN1/IN2/IN3 — Insurance

The IN series of segments carries insurance information for a patient.

**IN1 — Insurance:**

| Field | Description | Example |
|---|---|---|
| IN1-1 | Set ID | `1` |
| IN1-2 | Insurance Plan ID | `BCBS` |
| IN1-3 | Insurance Company ID | `BLUECROSS-123` |
| IN1-4 | Insurance Company Name | `Blue Cross Blue Shield` |
| IN1-8 | Group Number | `Group-1234` |
| IN1-10 | Insurance Company Name | Detailed company name |
| IN1-11 | Group Name | `ABC CORP EMPLOYEE GROUP` |
| IN1-12 | Insured Group Employer Name | `ABC Corporation` |
| IN1-13 | Plan Effective Date | `20250101` |
| IN1-14 | Plan Expiration Date | `20251231` |
| IN1-15 | Authorization Information | Pre-authorization number |
| IN1-16 | Plan Type | `PPO`, `HMO`, `POS`, `IND` (indemnity) |
| IN1-18 | Insured's Name | `Smith^John^^^` |
| IN1-19 | Insured's Relationship to Patient | `SELF`, `SPOUSE`, `CHILD` |
| IN1-22 | Coordination of Benefits | `COB` — indicates coordination |
| IN1-36 | Policy Number | `POL-12345` |

**IN2 — Insurance Additional Info:**
Carries additional insured person demographic data, employer information, and coverage details.

**IN3 — Insurance Certification:**
Carries certification and authorization numbers, certification period, and renewal information.

### GT1 — Guarantor

The GT1 segment identifies the guarantor (person financially responsible):

| Field | Description | Example |
|---|---|---|
| GT1-1 | Set ID | `1` |
| GT1-2 | Guarantor Number | `G-12345` |
| GT1-3 | Guarantor Name | `Smith^John^^^` |
| GT1-4 | Guarantor Spouse Name | `Smith^Jane^^^` |
| GT1-5 | Guarantor Address | `123 Main St^^Anytown^CA^90210^^H` |
| GT1-6 | Guarantor Phone - Home | `(555)123-4567` |
| GT1-7 | Guarantor Phone - Business | `(555)987-6543` |
| GT1-8 | Guarantor Date/Time of Birth | `19750315` |
| GT1-9 | Guarantor Sex | `M` |
| GT1-10 | Guarantor Relationship | `SELF` |
| GT1-12 | Guarantor SSN | `123-45-6789` |
| GT1-22 | Guarantor Employer Name | `ABC Corporation` |
| GT1-43 | Guarantor Employment Status | `FT` (full-time) |

### Z Segments (Custom/Local)

Z segments are user-defined segments for custom data not covered by standard HL7 segments. Naming convention: Z followed by two characters (e.g., Z01, ZPR, ZCL).

Common Z segments include:
- `ZCL` — Additional claim information (prior authorization, referring provider)
- `ZPR` — Additional provider information (supervising provider, billing provider)
- `ZPV` — Additional visit information (financial class, charity care status)
- `ZCA` — Custom account data
- `ZAL` — Additional allergy/alerts

Z segments must be documented in the interface specification and are not portable across systems.

---

## HL7 Trigger Events

HL7 is an event-driven messaging standard. Every message is triggered by a real-world event:

| Event | Message |
|---|---|
| Patient registers for outpatient visit | ADT^A04 |
| Patient admitted to hospital | ADT^A01 |
| Patient transferred to different unit | ADT^A02 |
| Patient discharged | ADT^A03 |
| Patient demographics updated | ADT^A08 |
| Lab test ordered | ORM^O01 |
| Lab result available | ORU^R01 |
| Charge posted to patient account | DFT^P03 |
| Appointment booked | SIU^S12 |
| Appointment cancelled | SIU^S15 |
| Document transcribed | MDM^T02 |

---

## HL7 Interface Engines

Interface engines receive, transform, route, and translate HL7 messages between healthcare systems.

| Engine | Vendor | Type | Notes |
|---|---|---|---|
| **Mirth Connect** | NextGen Healthcare | Open Source (Java) | Most widely used, free, large community, extensive channel library |
| **Corepoint Integration Engine** | Corepoint Health | Commercial | HIPAA-compliant, visual mapping, high reliability |
| **Interfaceware Iguana** | Interfaceware | Commercial (Lua-based) | Uses Lua scripting for transformations, visual message viewer |
| **Lyniate Rhapsody** | Lyniate (formerly Rhapsody) | Commercial | High-throughput, enterprise-grade, extensive protocol support |
| **InterSystems HealthShare/Ensemble** | InterSystems | Commercial | Deep EHR integration, ObjectScript-based, data platform capabilities |
| **Epic Bridges** | Epic Systems | Built-in | Epic-specific interface engine, manages HL7 connections to/from Epic |

For Denials Doctor integration, Mirth Connect is the most common choice because it is free, highly configurable, and supports HL7 v2, FHIR, X12, and custom formats. Hospitals already using Mirth for other interfaces can add Denials Doctor channels without licensing additional software.

---

## HL7 v2 to FHIR Conversion

Mapping HL7 v2 messages to FHIR resources enables bridging between legacy and modern systems.

| HL7 v2 | FHIR Resource | Key Mapping |
|---|---|---|
| ADT^A01/A04/A08 → Patient | Patient | PID-3 (identifiers) → Patient.identifier; PID-5 (name) → Patient.name; PID-7 (DOB) → Patient.birthDate; PID-8 (sex) → Patient.gender; PID-11 (address) → Patient.address; PID-13 (phone) → Patient.telecom |
| ADT^A01/A04 → Encounter | Encounter | PV1-2 (class) → Encounter.class; PV1-44/45 (period) → Encounter.period; PV1-7/8/9 (providers) → Encounter.participant; PV1-19 (visit number) → Encounter.identifier |
| ORM^O01 → ServiceRequest | ServiceRequest | OBR-2/3 (order ID/code) → ServiceRequest.code; OBR-7 (date) → ServiceRequest.authoredOn; OBR-16 (ordering provider) → ServiceRequest.requester |
| ORU^R01 → Observation | Observation | OBR (order info) → parent; OBX-3 (code) → Observation.code; OBX-5 (value) → Observation.value; OBX-6 (units) → Observation.valueQuantity; OBX-7 (ref range) → Observation.referenceRange; OBX-8 (abnormal) → Observation.interpretation |
| ORU^R01 → DiagnosticReport | DiagnosticReport | OBR-3 (test code) → DiagnosticReport.code; OBR-7 (date) → DiagnosticReport.effectiveDateTime; OBX entries → DiagnosticReport.result |
| DFT^P03 → Claim | Claim | FT1-7 (CPT) → Claim.item.productOrService; FT1-8 (modifier) → Claim.item.modifier; FT1-10 (charge) → Claim.item.net; FT1-12 (diagnosis pointer) → Claim.item.diagnosisSequence |
| IN1 → Coverage | Coverage | IN1-2 (plan) → Coverage.type; IN1-8 (group) → Coverage.class; IN1-13/14 (period) → Coverage.period; IN1-36 (policy) → Coverage.identifier |

---

## HL7 Acknowledgment

HL7 uses two acknowledgment modes:

### Original Mode (MSH-15/16 = AL, MSH-16 blank)

The receiver sends an ACK message for every message. The ACK uses the same Message Control ID (MSH-10) as the original:

```
MSH|^~\&|RECEIVING|FACILITY|SENDING|APP|202502031031||ACK^A01|ACK-123|P|2.5.1
MSA|AA|MSG001|Message accepted|
```

### Enhanced Mode (MSH-15/16 = AL)

The receiver sends both a commit ACK and an application ACK:
1. **Commit ACK**: Confirms message was received and structurally valid (MSH-15)
2. **Application ACK**: Confirms message was processed at application level (MSH-16)

### MSA Segment Fields

| Field | Description | Values |
|---|---|---|
| MSA-1 | Acknowledgment Code | `AA` (Application Accept), `AE` (Application Error), `AR` (Application Reject), `CA` (Commit Accept), `CE` (Commit Error), `CR` (Commit Reject) |
| MSA-2 | Message Control ID | MSA-16 of original message |
| MSA-3 | Text Message | Human-readable error/accept description |

### ERR Segment (Error)

```
ERR|^^^PID^PID-3&1&Identifier ID||207^^HL70057^Unknown key identifier|
```

| Field | Description |
|---|---|
| ERR-1 | Error Code and Location — includes segment, field, and component where error occurred |
| ERR-2 | Error Location |
| ERR-3 | HL7 Error Code — standard HL7 error code |
| ERR-4 | Severity — `E` (Error), `W` (Warning), `I` (Information) |

---

## Error Handling

### Common HL7 Errors

| Error Type | Example | Handling |
|---|---|---|
| Segment Sequence Error | OBX before OBR | Message structure violation; reject and resend |
| Invalid Field Value | PID-8 = "X" (invalid sex code) | Accept with warning, log, use default |
| Missing Required Field | PID-5 (patient name) missing | Reject message; trigger error alert |
| Encoding Character Mismatch | MSH-2 doesn't match delimiter | Parse failure; log and discard |
| Identifier Conflict | Duplicate PID-3 value | Accept but flag for review |
| Version Mismatch | MSH-12 version unsupported | Log, attempt best-effort parse |
| Field Too Long | MSH-9 (message type) > 9 chars | Truncate or reject based on spec |

### Error Response Strategies

1. **Accept and Log**: For minor issues (non-critical field errors), accept the message, process what's possible, and log the error
2. **Reject and NAK**: For structural or missing critical data, send an AR (Application Reject) or AE (Application Error) acknowledgment
3. **Requeue**: For transient errors (system busy, temporary connection issues), queue the message for retry
4. **Dead Letter Queue**: Messages that fail repeatedly go to a dead letter queue for manual review

---

## Agent Training: Q&A Pairs

**Q:** What is the difference between HL7 v2.3 and v2.5.1?
**A:** HL7 v2.3 (1997) is a legacy version with basic ADT, ORM, ORU, and DFT support. v2.5.1 (2007) is a major enhancement that added US-specific fields (race/ethnicity in PID, enhanced insurance fields), standardized Z-segment usage, and introduced new message types. v2.5.1 is required for US meaningful use certification and is the minimum recommended version for new integrations.

**Q:** How does HL7 v2 handle patient record merging?
**A:** HL7 v2 uses the ADT^A40 and ADT^A18 trigger events for patient merging. ADT^A40 merges patient identifier lists — the source patient identifiers are merged into the target record, and the source becomes inactive. ADT^A18 performs a full person merge where the source patient's entire record is merged into the target. The format includes the source identifiers in the MRG (Merge Patient Information) segment, which tells the receiving system which old identifiers to cross-reference.

**Q:** What is the MRG segment and when is it used?
**A:** The MRG segment is used in patient merge messages (ADT^A18, ADT^A34, ADT^A35, ADT^A40). It contains the prior patient identifier(s) that should be merged into the patient identified in the PID segment. Example: `MRG|98765^^^HOSP^MRN~OLD-123^^^HOSP^PI` — this tells the receiving system that patient identifiers 98765 (MRN) and OLD-123 (internal ID) should point to the patient in the PID segment.

**Q:** What is the difference between OBX-5 value types?
**A:** OBX-2 specifies the data type of OBX-5: NM (numeric) — quantitative results like lab values; ST (string) — short text; TX (text) — longer narrative; CE/CWE (coded) — coded values from a terminology system; DT (date) — date only; TM (time) — time only; DTN (date/time) — date and time; SN (structured numeric) — numeric with comparator; FT (formatted text) — formatted text with line breaks. For medical necessity review, NM with reference ranges (OBX-7) and abnormal flags (OBX-8) are most important.

**Q:** How do you handle repeating fields in HL7 messages?
**A:** Repeating fields are separated by the tilde (~) character defined in MSH-2. Example in PID-3: `98765^^^HOSP^MRN~123-45-6789^^^SSA^SS~DL-12345^^^DMA^DL` — three patient identifiers separated by tildes. When parsing, the application must split on `~` to get each repetition and then on `^` to get components within each repetition.

**Q:** What is the purpose of the OBR segment in an ORU message?
**A:** The OBR (Observation Request) segment in an ORU message serves as the order header that groups related OBX observations. It contains the order information — what test or panel was ordered (OBR-3), when it was ordered (OBR-7), who ordered it (OBR-16), the specimen if applicable (OBR-15), and the date/time of collection or performance. In the ORU context, OBR is a header for the result set, and each individual result is carried in an OBX segment following the OBR.

**Q:** How does HL7 v2 define the Patient Class in PV1-2?
**A:** PV1-2 (Patient Class) uses standard values: I (inpatient — admitted to hospital, typically overnight stay); O (outpatient — visit without admission); E (emergency — emergency department visit); P (preadmit — patient scheduled for future admission); R (recurring patient — e.g., dialysis); B (obstetrics — inpatient obstetrics); N (newborn); U (unknown). The patient class determines claim type (institutional for I/N/B, professional for O/E) and affects coverage, benefits, and billing rules.

**Q:** What are Z segments and when should they be used?
**A:** Z segments are user-defined segments for data not covered by standard HL7 segments. They follow the naming convention Z + two characters (Z01-Z99). They should be used ONLY when no standard segment or field exists for the data being transmitted. Best practices: (1) always document Z segments in the interface specification; (2) use the HL7 website's segment proposal process before creating Z segments — a standard segment may already exist; (3) prefix Z-segment field names clearly; (4) note that Z segments are not portable — another system or custom parser would need explicit documentation.

**Q:** What is the role of an HL7 interface engine in Denials Doctor integration?
**A:** An HL7 interface engine (Mirth Connect, Corepoint, Iguana, Rhapsody) sits between the EHR and Denials Doctor, handling: (1) message routing — directing ADT messages to patient management, DFT messages to billing; (2) protocol translation — converting HL7 v2 to FHIR or internal JSON; (3) data transformation — reformatting, mapping codes; (4) message queuing and retry — ensuring reliable delivery; (5) error handling and logging; (6) acknowledgments — sending ACKs back to the source system. The interface engine reduces the integration burden on both Denials Doctor and the EHR.

**Q:** How does the DFT^P03 message relate to claim creation?
**A:** DFT^P03 (Detailed Financial Transaction - Post Charge) is sent after a service is provided and a charge is posted in the EHR's billing module. The FT1 segments carry the charge details: CPT code (FT1-7), modifiers (FT1-8), charge amount (FT1-10), and revenue code (FT1-15). Denials Doctor receives DFT messages to: (1) queue new charges for claim validation before submission; (2) match charges to encounters via PID-18 (account number) and PV1-19 (visit number); (3) flag potential billing errors in real-time; (4) track charge capture completion.

**Q:** What is the difference between HL7 v2 Original and Enhanced acknowledgment modes?
**A:** In Original mode (MSH-15 set, MSH-16 blank), the receiver sends one ACK for each message received, indicating whether the message was accepted (AA) or rejected (AR/AE). In Enhanced mode (both MSH-15 and MSH-16 set), the receiver sends two ACKs: a commit-level ACK (MSA-1 = CA/CE/CR) confirming the message was received and structurally valid, then an application-level ACK (AA/AE/AR) confirming the data was successfully processed. Enhanced mode provides better error isolation — a commit ACK with application error tells the sender the message arrived fine but the data content was problematic.

**Q:** How do you determine the HL7 version from a message?
**A:** The HL7 version is in MSH-12 of the message header. Example: `MSH|^~\&|...|||2.5.1` — version 2.5.1. The version determines which segments, fields, and field definitions are valid. A parser should read MSH-12 first to determine which version-specific rules to apply. Common values: 2.3, 2.3.1, 2.4, 2.5, 2.5.1, 2.6, 2.7, 2.8.

**Q:** Can HL7 v2 handle real-time charge posting?
**A:** Yes. The DFT^P03 message is designed for real-time charge posting. When a service is provided and the charge entered in the EHR, the EHR immediately sends a DFT message. This enables Denials Doctor to: (1) perform real-time claim validation as charges are posted; (2) detect coding errors or missing information before the claim is batched for submission; (3) track expected charges vs. actual charges across an encounter. Some EHRs batch DFT messages on a schedule (hourly, end-of-day) rather than sending them in real-time.

**Q:** What happens if a required field is missing from an HL7 message?
**A:** Behavior depends on HL7 version and implementation. In general: (1) if a required field is missing from the PID segment (e.g., PID-5 patient name), some systems reject the entire message with an AR acknowledgment; (2) if the field is missing from a less critical segment, the system may accept and log the issue; (3) Denials Doctor should be configured with configurable validation rules — strict mode (reject all missing required fields) for production, relaxed mode for testing; (4) the ERR segment in the acknowledgment should specify exactly which field was missing.

**Q:** What is the MSH-9 format and what does each part mean?
**A:** MSH-9 (Message Type) has three components separated by `^`: Message Code ^ Trigger Event ^ Message Structure. Example: `ADT^A01^ADT_A01`. The Message Code is the three-character message type (ADT, ORM, ORU, DFT). The Trigger Event is the specific event type (A01 admit, A03 discharge, etc.). The Message Structure is the optional third component indicating the segment structure pattern. In v2.5+, the message structure is often included to make the segment order unambiguous.

**Q:** How do SIU scheduling messages relate to claim processing?
**A:** SIU messages (S12-S15) notify Denials Doctor when appointments are booked, rescheduled, or cancelled. This allows Denials Doctor to: (1) predict upcoming billing volumes by appointment type; (2) check that scheduled procedures have required prior authorizations before the appointment date; (3) track no-shows and cancelled appointments for denial pattern analysis; (4) pre-validate appointment data (patient insurance eligibility, provider credentialing) before service delivery.

**Q:** What is the MFN message and why is it important for billing?
**A:** MFN (Master File Notification) updates master file data across systems. The MFN^M04 (Charge Description Master File) is particularly important — it updates the CDM (Charge Description Master) with new procedure codes, pricing changes, and revenue code mappings. When the EHR updates charge master data, the MFN message informs Denials Doctor so that: (1) claim validation rules reflect current pricing; (2) new procedure codes are recognized for charge capture validation; (3) obsolete codes are flagged for review.

**Q:** How are multiple insurance plans handled in HL7 v2?
**A:** Multiple insurance plans are represented by repeating IN1 segments. Each IN1 segment represents one insurance plan, and their order indicates priority (IN1-1: Set ID 1 = primary, Set ID 2 = secondary, Set ID 3 = tertiary). Each IN1 carries the plan details (company, group number, policy number, effective dates, COB order). For coordination of benefits, the IN1-22 (Coordination of Benefits) and IN1-36 (Policy Number) fields indicate how plans coordinate payment.

**Q:** What is the difference between PID-18 (Account Number) and PV1-19 (Visit Number)?
**A:** PID-18 (Patient Account Number) is the financial account identifier used by billing systems — it groups all charges, payments, and adjustments for a patient encounter into a single financial account. PV1-19 (Visit Number) is the clinical encounter identifier used by the EHR to track the patient's visit. In many implementations, these are different values because billing and clinical systems use different numbering schemes. Denials Doctor must map between these identifiers to reconcile clinical data with financial data.

**Q:** How does HL7 v2 handle corrections to previously sent data?
**A:** HL7 v2 handles corrections through: (1) ADT^A08 (Update Patient Information) for correcting patient demographics — the updated fields replace previous values; (2) ORU^R01 with corrected OBX segments — the OBX-11 (Observation Result Status) is set to `C` (corrected) when a previous result was wrong; (3) ADT^A11-A13 (Cancel) and ADT^A02 (Transfer) for encounter corrections; (4) For deleted transactions, some implementations send the original message with a cancel trigger event (e.g., ORC with status = CA for cancelled orders).

**Q:** What encoding issues commonly arise with HL7 v2 interfaces?
**A:** Common encoding issues: (1) character encoding mismatches — ASCII vs UTF-8, especially for non-English characters; (2) escape character usage — improper escaping of separator characters within data fields (e.g., using `\F\` for field separator in text, `\S\` for component separator); (3) segment terminator — some systems use `\r` vs `\r\n` vs `\n` as segment terminators; (4) field padding — trailing spaces in fields that cause parsing or matching failures; (5) date/time format variations — MSH-7 uses YYYYMMDDHHMMSS but some implementations omit trailing fields for time-invariant messages.

---

## Summary

HL7 v2 remains the most widely deployed healthcare messaging standard despite its age. For Denials Doctor, it serves as the secondary integration protocol for EHRs that do not offer modern FHIR APIs. Key message types include ADT (patient registration/encounter data), ORM (orders), ORU (results), DFT (financial transactions), SIU (scheduling), and MFN (master file updates).

HL7 v2.5.1 is the minimum recommended version for Denials Doctor integrations, with v2.6+ preferred. Interface engines like Mirth Connect provide the protocol translation layer between HL7 v2 and Denials Doctor's internal data model. Understanding HL7 v2 segment structure (MSH, PID, PV1, DG1, PR1, IN1, GT1, FT1, OBX) is essential for accurate data mapping and integration configuration.