# FHIR R4: Fast Healthcare Interoperability Resources

## Overview

FHIR (Fast Healthcare Interoperability Resources, pronounced "fire") is an HL7 standard for exchanging healthcare information electronically. Release 4 (R4, version 4.0.1) is the normative version and the most widely adopted in production healthcare systems. FHIR combines features of prior HL7 standards (v2 and v3) with modern web technologies (RESTful APIs, JSON/XML serialization, OAuth2 security) to create a practical, implementable interoperability standard.

For Denials Doctor, FHIR R4 is the primary integration protocol because it offers the richest data model, broadest EHR support, and most developer-friendly API patterns among all healthcare interoperability standards.

---

## Core FHIR Concepts

### Resources

Resources are the fundamental building blocks of FHIR. Each resource represents a discrete piece of clinical or administrative data. Resources have:

- **A canonical URL**: e.g., `http://hl7.org/fhir/StructureDefinition/Patient`
- **An id**: unique identifier within a server (e.g., `Patient/12345`)
- **Metadata**: version id, last updated timestamp, profile assertions
- **Human-readable summary**: an XHTML `text` element for display
- **Structured data**: machine-readable elements in JSON, XML, or RDF/Turtle

Resources are identified by their type name (capitalized singular noun). Common resource types include `Patient`, `Coverage`, `Claim`, `ExplanationOfBenefit`, `Practitioner`, `Organization`, `Encounter`, `Condition`, and `Procedure`.

### Profiles and Extensions

**Profiles** constrain or extend a base resource for specific use cases. A profile declares which elements are required (mandatory), which are optional, and what value sets apply. For US healthcare, the **US Core Implementation Guide** defines profiles that align with USCDI (United States Core Data for Interoperability) requirements.

**Extensions** allow resources to carry additional data beyond the base specification. Extensions are identified by a URL that points to a definition. Examples:
- `http://hl7.org/fhir/us/core/StructureDefinition/us-core-race` — race extension on Patient
- `http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity` — ethnicity extension on Patient
- `http://hl7.org/fhir/StructureDefinition/patient-birthPlace` — birthplace extension on Patient

Extensions follow the format:
```json
{
  "extension": [
    {
      "url": "http://example.org/fhir/StructureDefinition/my-extension",
      "valueString": "extension value"
    }
  ]
}
```

### Bundles

A Bundle is a container for a collection of resources. Bundles are used for:
- **Transaction bundles**: multiple create/update/delete operations in a single HTTP request
- **Search result sets**: results of a search operation
- **Document bundles**: a clinical document composed of multiple resources
- **Message bundles**: messaging between systems
- **History lists**: version history of a resource

Bundle structure:
```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 42,
  "entry": [
    {
      "fullUrl": "http://example.org/fhir/Patient/123",
      "resource": { "resourceType": "Patient", ... },
      "search": { "mode": "match" }
    }
  ]
}
```

### Operations

FHIR defines operations as actions beyond standard CRUD. Operations are invoked via `$` prefix:
- `GET [base]/Patient/$everything` — return all patient data
- `GET [base]/Patient/[id]/$everything` — return everything for a specific patient
- `GET [base]/Group/[id]/$export` — bulk data export for a patient group
- `POST [base]/Patient/$match` — patient matching
- `POST [base]/Resource/$validate` — validate a resource against its profile

---

## RESTful API Paradigm

FHIR uses a RESTful API with the following HTTP methods mapped to CRUD operations:

| HTTP Method | CRUD Operation | FHIR Semantics |
|---|---|---|
| `GET` | Read | Retrieve a resource by ID, search by parameters |
| `POST` | Create | Create a new resource; `POST [base]/[type]` |
| `PUT` | Update | Replace an existing resource |
| `PATCH` | Partial Update | Update specific fields (JSON Patch or FHIRPath) |
| `DELETE` | Delete | Remove a resource (logical or physical deletion) |
| `GET` (history) | Read History | Retrieve version history of a resource |

Standard URL patterns:
```
GET  [base]/Patient/123                    — Read Patient with ID 123
GET  [base]/Patient/123/_history           — History of Patient 123
GET  [base]/Patient?identifier=MRN|12345   — Search Patient by identifier
POST [base]/Patient/_search                — Search using POST body
POST [base]/Patient                        — Create a new Patient
PUT  [base]/Patient/123                    — Update Patient 123
```

Response codes:
- `200 OK` — successful read, update, or search
- `201 Created` — successful create
- `204 No Content` — successful delete
- `400 Bad Request` — invalid request
- `401 Unauthorized` — missing/invalid authentication
- `403 Forbidden` — authenticated but not authorized
- `404 Not Found` — resource does not exist
- `422 Unprocessable Entity` — validation failure

---

## Key FHIR Resources for Denials Doctor

### Patient

The Patient resource represents a person receiving healthcare services. Critical fields for RCM:

```json
{
  "resourceType": "Patient",
  "id": "pat-12345",
  "identifier": [
    { "use": "usual", "type": { "coding": [{ "system": "http://hl7.org/fhir/v2/0203", "code": "MR" }] }, "system": "http://hospital.org/MRN", "value": "MRN-98765" },
    { "use": "official", "type": { "coding": [{ "system": "http://hl7.org/fhir/v2/0203", "code": "SS" }] }, "system": "http://hl7.org/fhir/sid/us-ssn", "value": "xxx-xx-xxxx" },
    { "use": "temp", "type": { "coding": [{ "system": "http://hl7.org/fhir/v2/0203", "code": "DL" }] }, "system": "urn:oid:2.16.840.1.113883.4.3.6", "value": "DL-123456" }
  ],
  "name": [{ "use": "official", "family": "Smith", "given": ["John", "Michael"] }],
  "telecom": [{ "system": "phone", "value": "555-123-4567", "use": "home" }],
  "gender": "male",
  "birthDate": "1975-03-15",
  "address": [{ "use": "home", "line": ["123 Main St"], "city": "Anytown", "state": "CA", "postalCode": "90210" }],
  "maritalStatus": { "coding": [{ "system": "http://hl7.org/fhir/v3/MaritalStatus", "code": "M" }] },
  "multipleBirthBoolean": false,
  "communication": [{ "language": { "coding": [{ "system": "urn:ietf:bcp:47", "code": "en-US" }] }, "preferred": true }],
  "managingOrganization": { "reference": "Organization/hosp-001" },
  "generalPractitioner": [{ "reference": "Practitioner/prac-456" }],
  "link": [{ "other": { "reference": "Patient/pat-67890" }, "type": "seealso" }]
}
```

Key identifier types in `identifier` array:
| Type Code | System | Description |
|---|---|---|
| `MR` | http://hl7.org/fhir/v2/0203 | Medical Record Number |
| `SS` | http://hl7.org/fhir/sid/us-ssn | Social Security Number |
| `DL` | urn:oid:2.16.840.1.113883.4.3.6 | Driver's License |
| `PI` | http://hl7.org/fhir/v2/0203 | Patient Internal Identifier |
| `MA` | http://hl7.org/fhir/v2/0203 | Member Number (insurance) |

---

### Coverage

The Coverage resource represents an insurance plan or program that covers a patient. Essential for revenue cycle:

```json
{
  "resourceType": "Coverage",
  "id": "cov-789",
  "status": "active",
  "subscriber": { "reference": "Patient/pat-12345" },
  "beneficiary": {
    "reference": "Relationship/01",
    "coding": [{ "system": "http://hl7.org/fhir/v3/RoleCode", "code": "SELF" }]
  },
  "payor": [{ "reference": "Organization/ins-001" }],
  "class": [
    { "type": { "coding": [{ "system": "http://hl7.org/fhir/coverage-class", "code": "group" }] }, "value": "G12345", "name": "ABC CORP GROUP PLAN" },
    { "type": { "coding": [{ "system": "http://hl7.org/fhir/coverage-class", "code": "plan" }] }, "value": "P98765", "name": "GOLD PPO PLAN" },
    { "type": { "coding": [{ "system": "http://hl7.org/fhir/coverage-class", "code": "network" }] }, "value": "N-123", "name": "NETWORK A" }
  ],
  "period": { "start": "2025-01-01", "end": "2025-12-31" },
  "dependent": "01",
  "relationship": {
    "coding": [{ "system": "http://hl7.org/fhir/v3/RoleCode", "code": "SELF" }]
  },
  "order": 1
}
```

In revenue cycle management:
- `order: 1` = primary insurance, `order: 2` = secondary
- `class` array contains group number, plan name, and network information
- `payor` references the insurance Organization
- `period` defines effective coverage dates
- `relationship` indicates subscriber-to-beneficiary relationship (self, spouse, child)

---

### Claim

The Claim resource represents a request for payment for healthcare services. Two primary types:
- **Professional** (Claim.type = `professional`): billing from individual providers
- **Institutional** (Claim.type = `institutional`): billing from facilities/hospitals

```json
{
  "resourceType": "Claim",
  "id": "claim-001",
  "status": "active",
  "type": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/claim-type", "code": "professional" }] },
  "use": "claim",
  "patient": { "reference": "Patient/pat-12345" },
  "billablePeriod": { "start": "2025-02-01", "end": "2025-02-01" },
  "created": "2025-02-03",
  "provider": { "reference": "Practitioner/prac-456" },
  "priority": { "coding": [{ "code": "normal" }] },
  "insurance": [
    {
      "sequence": 1,
      "focal": true,
      "identifier": [{ "system": "http://payer.org/plan-id", "value": "PLAN-001" }],
      "coverage": { "reference": "Coverage/cov-789" },
      "businessArrangement": "BA-12345"
    }
  ],
  "diagnosis": [
    {
      "sequence": 1,
      "diagnosisCodeableConcept": { "coding": [{ "system": "http://hl7.org/fhir/sid/icd-10-cm", "code": "E11.9" }] },
      "type": [{ "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/ex-diagnosistype", "code": "principal" }] }]
    }
  ],
  "item": [
    {
      "sequence": 1,
      "careTeamSequence": [1],
      "diagnosisSequence": [1],
      "servicedDate": "2025-02-01",
      "productOrService": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/ex-USCLS", "code": "99213" }] },
      "modifier": [{ "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/modifier", "code": "25" }] }],
      "net": { "value": 150.00, "currency": "USD" },
      "encounter": [{ "reference": "Encounter/enc-001" }]
    }
  ],
  "total": { "value": 150.00, "currency": "USD" }
}
```

Claim elements critical for denial management:
- `item[].productOrService` — CPT/HCPCS procedure codes
- `item[].modifier` — CPT modifiers (25, 59, etc.)
- `diagnosis[].diagnosis[x]` — ICD-10 codes, linked to items via `diagnosisSequence`
- `insurance[].focal` — which coverage is the target for this claim
- `supportingInfo` — additional claim data (referral numbers, medical necessity documentation)
- `careTeam[].provider` — rendering, referring, and ordering providers

---

### ExplanationOfBenefit (EOB)

The EOB resource represents the payer's adjudication response. This is THE critical resource for denial analysis:

```json
{
  "resourceType": "ExplanationOfBenefit",
  "id": "eob-001",
  "status": "active",
  "disposition": "Claim was partially paid. Service line 1 was denied.",
  "type": { "coding": [{ "code": "professional" }] },
  "use": "claim",
  "patient": { "reference": "Patient/pat-12345" },
  "created": "2025-02-15",
  "insurer": { "reference": "Organization/ins-001" },
  "provider": { "reference": "Practitioner/prac-456" },
  "claim": { "reference": "Claim/claim-001" },
  "claimResponse": { "reference": "ClaimResponse/cr-001" },
  "outcome": "partial",
  "payeeType": { "coding": [{ "code": "provider" }] },
  "careTeam": [
    { "sequence": 1, "provider": { "reference": "Practitioner/prac-456" }, "role": { "coding": [{ "code": "primary" }] } }
  ],
  "insurance": {
    "coverage": { "reference": "Coverage/cov-789" },
    "focal": true
  },
  "item": [
    {
      "sequence": 1,
      "careTeamSequence": [1],
      "productOrService": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/ex-USCLS", "code": "99213" }] },
      "adjudication": [
        { "category": { "coding": [{ "code": "allowed" }] }, "amount": { "value": 100.00, "currency": "USD" } },
        { "category": { "coding": [{ "code": "denied" }] }, "amount": { "value": 50.00, "currency": "USD" } },
        { "category": { "coding": [{ "code": "submitted" }] }, "amount": { "value": 150.00, "currency": "USD" } }
      ],
      "adjudication": [
        { "category": { "coding": [{ "code": "denialreason" }] }, "reason": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/adjudication-reason", "code": "CO-97" }] } }
      ]
    }
  ],
  "payment": {
    "type": { "coding": [{ "code": "payment" }] },
    "adjustment": { "value": 50.00 },
    "amount": { "value": 100.00, "currency": "USD" },
    "date": "2025-02-20"
  },
  "processNote": [
    { "number": 1, "type": "display", "text": "Service not medically necessary per plan criteria. Documentation insufficient." }
  ]
}
```

Key EOB elements for Denials Doctor:
- `outcome`: `complete` (paid), `partial` (partial payment), `denial-error` (claim error), `queued` (pending)
- `item[].adjudication[].category` — adjudication types: `submitted`, `allowed`, `deductible`, `coinsurance`, `denied`, `paid`
- `item[].adjudication[].reason` — CARC (Claim Adjustment Reason Code) — CRITICAL for denial categorization
- `processNote` — payer explanatory text about denials and adjustments
- `payment` — payment summary including adjustments and final payment amount
- `addItem` — items added by the payer (not on original claim)

---

### Practitioner

```json
{
  "resourceType": "Practitioner",
  "id": "prac-456",
  "identifier": [
    { "system": "http://hl7.org/fhir/sid/us-npi", "value": "1234567893" },
    { "system": "http://hospital.org/provider-id", "value": "PROV-001" }
  ],
  "name": [{ "use": "official", "family": "Doe", "given": ["Jane", "M"] }],
  "qualification": [
    {
      "identifier": [{ "system": "http://hl7.org/fhir/sid/us-npi", "value": "1234567893" }],
      "code": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/v2-0360", "code": "MD" }] },
      "period": { "start": "2000-06-01" },
      "issuer": { "reference": "Organization/state-board" }
    }
  ]
}
```

### Organization

```json
{
  "resourceType": "Organization",
  "id": "org-001",
  "identifier": [
    { "system": "http://hl7.org/fhir/sid/us-tin", "value": "12-3456789" },
    { "system": "http://hl7.org/fhir/sid/us-npi", "value": "9876543210" }
  ],
  "type": [{ "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/organization-type", "code": "prov" }] }],
  "name": "Anytown Medical Center",
  "address": [{ "line": ["500 Hospital Dr"], "city": "Anytown", "state": "CA", "postalCode": "90210" }],
  "contact": [{ "telecom": [{ "system": "phone", "value": "555-987-6543" }] }]
}
```

### Encounter

```json
{
  "resourceType": "Encounter",
  "id": "enc-001",
  "status": "finished",
  "class": { "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "AMB", "display": "ambulatory" },
  "type": [{ "coding": [{ "system": "http://snomed.info/sct", "code": "185463005", "display": "Office visit" }] }],
  "subject": { "reference": "Patient/pat-12345" },
  "participant": [
    { "individual": { "reference": "Practitioner/prac-456" }, "type": [{ "coding": [{ "code": "PPRF" }] }] }
  ],
  "period": { "start": "2025-02-01T09:00:00Z", "end": "2025-02-01T09:30:00Z" },
  "location": [{ "location": { "reference": "Location/loc-001" } }],
  "serviceProvider": { "reference": "Organization/org-001" },
  "diagnosis": [
    { "condition": { "reference": "Condition/dx-001" }, "use": { "coding": [{ "code": "chief complaint" }] } }
  ],
  "hospitalization": {
    "admitSource": { "coding": [{ "code": "emergency" }] },
    "dischargeDisposition": { "coding": [{ "code": "home" }] }
  }
}
```

### Condition

```json
{
  "resourceType": "Condition",
  "id": "dx-001",
  "clinicalStatus": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active" }] },
  "verificationStatus": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed" }] },
  "category": [{ "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/condition-category", "code": "problem-list-item" }] }],
  "code": { "coding": [{ "system": "http://hl7.org/fhir/sid/icd-10-cm", "code": "E11.9", "display": "Type 2 diabetes mellitus without complications" }] },
  "subject": { "reference": "Patient/pat-12345" },
  "onsetDateTime": "2020-01-01",
  "recordedDate": "2020-01-05",
  "recorder": { "reference": "Practitioner/prac-456" },
  "note": [{ "text": "Patient manages with oral medication and diet." }]
}
```

### Procedure

```json
{
  "resourceType": "Procedure",
  "id": "proc-001",
  "status": "completed",
  "code": { "coding": [{ "system": "http://snomed.info/sct", "code": "6025007", "display": "Laparoscopic appendectomy" }] },
  "subject": { "reference": "Patient/pat-12345" },
  "performedDateTime": "2025-02-01",
  "performer": [{ "actor": { "reference": "Practitioner/prac-456" }, "onBehalfOf": { "reference": "Organization/org-001" } }],
  "reasonReference": [{ "reference": "Condition/dx-002" }],
  "complication": [{ "coding": [{ "system": "http://snomed.info/sct", "code": "123456", "display": "Post-operative infection" }] }]
}
```

### MedicationRequest, MedicationDispense, MedicationAdministration

These three resources form the medication workflow:
- **MedicationRequest**: prescriber's order for medication (analogous to e-prescribing)
- **MedicationDispense**: pharmacist's fulfillment of the order
- **MedicationAdministration**: record of medication given to patient (inpatient)

For RCM, MedicationAdministration is most relevant because it generates billable charges.

### DiagnosticReport and Observation

- **DiagnosticReport**: A report (lab, imaging, pathology) containing a set of observations or a narrative
- **Observation**: Individual measurement or finding (lab result, vital sign, social history)

Key for medical necessity reviews — Observations provide the clinical evidence that supports (or fails to support) billed procedures.

### Appointment, Schedule, Slot

Used for scheduling and encounter management:
- **Schedule**: provider availability (e.g., Dr. Smith's office hours)
- **Slot**: individual time slots within a schedule
- **Appointment**: booked appointment referencing a Slot and Patient

These resources help Denials Doctor understand the encounter context for claim validation.

---

## FHIR Operations

### $everything (Patient Record Export)

Returns all resources related to a patient in a single Bundle:
```
GET [base]/Patient/[id]/$everything
GET [base]/Patient/[id]/$everything?_since=2025-01-01&_type=Encounter,Condition,Observation
```

Parameters:
- `_since`: return only resources modified after this date
- `_type`: limit to specific resource types

### $export (Bulk Data Export)

FHIR Bulk Data API (aka Bulk FHIR) for exporting large datasets:
```
GET [base]/Group/[id]/$export        — Group-level export
GET [base]/Patient/$export            — Patient-level export  
GET [base]/$export                    — System-level export
```

Response is a manifest file listing NDJSON files for each resource type:
```json
{
  "transactionTime": "2025-01-01T00:00:00Z",
  "request": "https://server/Group/123/$export",
  "requiresAccessToken": true,
  "output": [
    { "type": "Patient", "url": "https://server/bulk-data/patient-1.ndjson", "count": 1000 },
    { "type": "Observation", "url": "https://server/bulk-data/obs-1.ndjson", "count": 50000 }
  ],
  "error": []
}
```

### $validate (Resource Validation)

Validates a resource against a profile:
```
POST [base]/Patient/$validate
```
Returns validation outcomes (errors, warnings, information).

### $match (Patient Matching)

Matches patient records across systems using demographic data:
```
POST [base]/Patient/$match
Body: { "resourceType": "Parameters", "parameter": [...] }
```

### $convert (Format Conversion)

Converts between healthcare formats:
```
POST [base]/$convert
```
Converts HL7 v2 messages to FHIR, CDA to FHIR, or FHIR to other formats.

---

## SMART on FHIR

SMART (Substitutable Medical Applications and Reusable Technologies) on FHIR provides the security framework for FHIR API access.

### OAuth2 Authorization

SMART on FHIR uses OAuth2 with several grant types:

| Grant Type | Use Case | Example |
|---|---|---|
| Authorization Code | EHR launch, standalone launch | Provider accesses Denials Doctor from Epic |
| Client Credentials | Backend services | Denials Doctor server-to-server data sync |
| Refresh Token | Long-lived access | Maintaining data subscriptions |

### Launch Scenarios

**EHR Launch (Provider-facing)**:
1. User logs into EHR (e.g., Epic)
2. User clicks Denials Doctor button within EHR
3. EHR sends SMART launch request with patient context
4. Denials Doctor receives `patient` and `encounter` IDs
5. App uses access token to call FHIR APIs

**Standalone Launch (App-facing)**:
1. User opens Denials Doctor independently
2. User selects their EHR from a list
3. Denials Doctor redirects to EHR's authorization endpoint
4. User authenticates and consents
5. EHR returns authorization code, exchanged for access token

**Patient-Facing Launch**:
1. Patient opens patient portal
2. Portal launches Denials Doctor patient-facing module
3. Patient authorizes data sharing
4. App accesses patient's data via patient-scoped scopes

### SMART Scopes

```
patient/*.read        — Read all patient data
patient/*.write       — Write all patient data  
patient/*.*           — Full patient data access
user/*.read           — Read all data user has access to
user/*.write          — Write data on behalf of user
user/*.*              — Full user-level access
system/*.read         — Read all system data (backend services)
system/*.write        — Write system data (backend services)
system/*.*            — Full system access
openid                — OpenID Connect for user identity
fhirUser              — FHIR resource for authenticated user
launch                — EHR launch context
launch/patient        — Access to launch patient
offline_access        — Request refresh token
```

### Clinical Scopes

Scopes can be resource-specific:
- `patient/Patient.read` — read Patient resources only
- `user/ExplanationOfBenefit.read` — read EOBs on behalf of current user
- `system/Claim.write` — write Claims at system level

---

## US Core Implementation Guide

The **US Core Implementation Guide** (http://hl7.org/fhir/us/core/) defines FHIR profiles for US healthcare data exchange, aligned with USCDI requirements.

### Core Profiles

| Profile | Based On | Key Requirements |
|---|---|---|
| US Core Patient | Patient | Must support: name, identifier (MRN, SSN), gender, birthDate, address, telecom, race, ethnicity extension |
| US Core Encounter | Encounter | Must support: status, class, type, subject, participant, period, reasonCode, diagnosis, location, serviceProvider |
| US Core Condition | Condition | Must support: clinicalStatus, verificationStatus, code, subject, onset, recordedDate |
| US Core Procedure | Procedure | Must support: status, code, subject, performed[x], reasonReference |
| US Core Observation Lab | Observation | Must support: status, code, subject, effective[x], value, interpretation, referenceRange |
| US Core Practitioner | Practitioner | Must support: identifier (NPI), name |
| US Core Organization | Organization | Must support: identifier (NPI, TIN), name, address |

### USCDI Requirements

USCDI (United States Core Data for Interoperability) defines the minimum data elements that EHRs must support. US Core profiles implement these requirements.

### Mandatory vs Must-Support

- **Mandatory**: the element MUST be present in every resource instance
- **Must-Support**: the system MUST populate the element if it has the data, and consuming systems MUST process it if present

---

## FHIR Subscription Mechanism

Subscriptions enable real-time notifications when resources change:

```json
{
  "resourceType": "Subscription",
  "status": "active",
  "criteria": "ExplanationOfBenefit?patient=Patient/pat-12345&status:not=active",
  "channel": {
    "type": "rest-hook",
    "endpoint": "https://denials-doctor.com/webhook/eob-updates",
    "payload": "application/fhir+json",
    "header": ["Authorization: Bearer <token>"]
  }
}
```

Channel types:
| Type | Description |
|---|---|
| `rest-hook` | POST notification to URL |
| `websocket` | Send via WebSocket |
| `email` | Send email notification |
| `message` | Send via FHIR messaging |

Subscription criteria use FHIR search syntax:
- `Patient?name=Smith` — notify when matching Patient changes
- `ExplanationOfBenefit?patient=Patient/pat-123&_lastUpdated=gt2025-01-01` — EOB updates for a patient

---

## FHIR Search

FHIR search is powerful and flexible:

### Basic Search
```
GET [base]/Patient?family=Smith&given=John
```

### Included Resources (_include, _revinclude)
```
GET [base]/Encounter?patient=Patient/123&_include=Encounter:participant:Practitioner
GET [base]/Patient?_revinclude=Provenance:target
```

### Reverse Chaining (_has)
```
GET [base]/Patient?_has:Provenance:target:agent=Practitioner/456
```

### Chained Parameters
```
GET [base]/Encounter?participant:Practitioner.name=Smith
GET [base]/Observation?subject:Patient.identifier=MRN|12345
```

### Pagination and Sorting
```
GET [base]/Claim?patient=Patient/123&_count=50&_page=2&_sort=-created
```

### Element Selection (_elements)
```
GET [base]/Patient/123?_elements=identifier,name
```

---

## Bulk Data Export (FHIR Bulk API)

### NDJSON Format

Bulk export returns newline-delimited JSON (NDJSON) where each line is one resource:

```json
{"resourceType":"Patient","id":"1","name":[{"family":"Smith"}]}
{"resourceType":"Patient","id":"2","name":[{"family":"Jones"}]}
```

### Export Levels

| Level | Endpoint | Use Case |
|---|---|---|
| System | `GET [base]/$export` | Entire EHR data |
| Group | `GET [base]/Group/[id]/$export` | Defined patient population |
| Patient | `GET [base]/Patient/$export` | All patients (no CareTeam filtering) |

### Export Workflow

1. Client initiates export with `Prefer: respond-async` header
2. Server returns `202 Accepted` with `Content-Location` header
3. Client polls `Content-Location` URL
4. When complete, server returns `200 OK` with manifest JSON
5. Client downloads each NDJSON file listed in manifest
6. Files may be large (gigabytes); streaming download recommended

---

## SMART Backend Services

For server-to-server integrations (Denials Doctor system-to-EHR):

1. Denials Doctor generates a JWT using its private key
2. JWT is exchanged for an access token at EHR's token endpoint
3. Access token carries `system/*.*` scopes
4. Denials Doctor uses the access token for FHIR API calls

JWT structure:
```json
{
  "iss": "denials-doctor-client-id",
  "sub": "denials-doctor-client-id",
  "aud": "https://ehr.example.com/token",
  "exp": 1700000000,
  "jti": "unique-token-id-12345"
}
```

---

## FHIR R4 vs R5

| Feature | R4 (4.0.1) | R5 (5.0.0) |
|---|---|---|
| Release Status | Normative (balloted) | Normative |
| Key New Resources | — | InventoryReport, DeviceDispense, Transport, SubscriptionTopic, SubscriptionStatus |
| Subscription | Basic criteria/channel | SubscriptionTopic with richer filtering |
| Search | Standard parameters | Improved search with more modifiers |
| Terminology | ValueSet expansions | Enhanced terminology operations |
| Adoption | Widely adopted by EHRs | Early adoption, Epic/Cerner not yet R5 |
| Backward Compatibility | — | Breaking changes to some resource structures |

For Denials Doctor integration, R4 is the current standard. R5 integration should be planned for 2027+.

---

## Agent Training: Q&A Pairs

**Q:** What is the difference between FHIR R4 and FHIR R5 for a revenue cycle management system?
**A:** FHIR R4 (4.0.1) is the normative standard currently adopted by major EHRs including Epic, Cerner, and athenahealth. R5 introduces new resources like InventoryReport and SubscriptionTopic with richer filtering, but no major EHR has adopted R5 in production. For Denials Doctor, R4 is the primary integration target. R5 support should be planned as a future enhancement when EHR vendors begin adopting it (estimated 2027+).

**Q:** How does the Claim resource relate to ExplanationOfBenefit in FHIR?
**A:** The Claim resource represents a request for payment submitted by a provider. The ExplanationOfBenefit (EOB) represents the payer's adjudication response — the EOB is generated after the claim is processed and contains the payment decision, adjudication details per service line, denial reasons (CARC codes), payment amounts, and process notes. In the RCM workflow: Claim is sent out, EOB comes back. The connection is maintained via the EOB's `claim` reference field pointing back to the original Claim.

**Q:** What FHIR resources are most important for denial analysis?
**A:** The most critical resources are: (1) ExplanationOfBenefit — contains adjudication results, denial reasons (CARC codes), and process notes for each service line; (2) Claim — the original submitted claim with diagnosis codes, procedure codes, and charges; (3) Coverage — insurance plan details including plan type, network, and effective dates; (4) Patient — demographic data and identifiers for patient matching; (5) Encounter — visit context including date, place of service, and type; (6) Condition/Procedure — clinical context for medical necessity review.

**Q:** How do you identify denial reasons in a FHIR ExplanationOfBenefit resource?
**A:** Denial reasons are found in multiple places in an EOB: (1) In each item's `adjudication` array where `category.code = "denied"` and the accompanying `reason` field contains a CARC (Claim Adjustment Reason Code) coding; (2) In the `disposition` field which provides a human-readable summary of the adjudication outcome; (3) In `processNote` entries which contain payer explanatory text; (4) In `item[].adjudication[]` where `category` indicates denied amounts and `reason` provides the specific denial code.

**Q:** What is SMART on FHIR and why is it needed?
**A:** SMART on FHIR is the security and authorization framework that sits on top of FHIR APIs. It provides OAuth2-based authentication and authorization, defining how applications authenticate with EHR systems and what data they can access. It supports three launch scenarios: EHR launch (app opened from within the EHR), standalone launch (app opened independently), and patient-facing launch. For Denials Doctor, SMART on FHIR is essential because EHRs like Epic require SMART authentication before granting access to patient data via FHIR.

**Q:** How does the FHIR Bulk Data Export work for large-scale data extraction?
**A:** The Bulk Data Export ($export) operation is designed for extracting large datasets. The workflow: (1) The client sends a GET request to `[base]/Group/[id]/$export` with `Prefer: respond-async`; (2) The server returns HTTP 202 Accepted with a Content-Location URL; (3) The client polls the Content-Location URL; (4) When processing completes, the server returns 200 OK with a JSON manifest listing NDJSON files by resource type; (5) Each NDJSON file contains one resource per line. For Denials Doctor, this is used for initial data loads and periodic full syncs of patient populations.

**Q:** What are the key differences between Claim.use = "claim" and Claim.use = "preauthorization"?
**A:** `Claim.use = "claim"` is a standard claim for payment — the provider is requesting reimbursement for services already rendered. `Claim.use = "preauthorization"` is a request for prior authorization — the provider is asking the payer to approve coverage before services are rendered (or for concurrent review). The corresponding response resource also differs: claims generate ExplanationOfBenefit, while preauthorizations may generate a ClaimResponse with preAuthRef.

**Q:** How does FHIR handle patient matching across different systems?
**A:** FHIR provides the `$match` operation on the Patient resource for patient matching. The operation accepts patient demographic data (name, DOB, gender, address, identifiers) and returns potential matches with confidence scores. Implementations vary by EHR — Epic uses its own patient matching algorithm, while Cerner uses a probabilistic matching engine. For best results, Denials Doctor should pass multiple identifiers (MRN, SSN, driver's license) when available. The `link` element in Patient resources also tracks links between duplicate records.

**Q:** What is the purpose of the US Core Implementation Guide?
**A:** The US Core Implementation Guide defines FHIR profiles, extensions, and conformance expectations for US healthcare data exchange. It implements the USCDI (United States Core Data for Interoperability) requirements mandated by the 21st Century Cures Act. It specifies which elements are mandatory (must be present) and which are must-support (must be populated if available). EHRs certified for US meaningful use must support US Core profiles. For Denials Doctor, aligning with US Core ensures maximum compatibility with EHR FHIR APIs.

**Q:** How do you handle pagination when searching for patients or claims in FHIR?
**A:** FHIR uses Bundle-based pagination. The search response includes a Bundle with `entry[]` containing resources and a `link[]` array with navigation URLs: `first`, `prev`, `next`, `last`, and `self`. The client follows the `next` link relation to get subsequent pages. Pagination parameters include `_count` (page size, server-enforced maximum) and `_page` (page number). Some servers also support `_offset` for offset-based pagination. Denials Doctor should handle pagination with exponential backoff on rate-limited servers.

**Q:** What FHIR search parameters are most useful for querying claims and denials?
**A:** Key search parameters: (1) `ExplanationOfBenefit?patient=[id]&created=ge[date]` — find EOBs for a patient after a certain date; (2) `ExplanationOfBenefit?claim=[id]` — find EOB for a specific claim; (3) `ExplanationOfBenefit?outcome=denial-error` — find all denied claims; (4) `ExplanationOfBenefit?insurer=[org-id]` — find EOBs from a specific payer; (5) `Claim?patient=[id]&status=active` — find active (unprocessed) claims; (6) `Coverage?beneficiary=[patient-id]&status=active` — find active insurance coverages.

**Q:** How do FHIR subscriptions enable real-time denial notifications?
**A:** FHIR Subscriptions allow Denials Doctor to receive real-time notifications when new ExplanationOfBenefit resources are created or modified. The integration creates a Subscription resource with criteria like `ExplanationOfBenefit?_lastUpdated=gt[today]` and a `rest-hook` channel pointing to Denials Doctor's webhook endpoint. When a new EOB is posted, the EHR sends a POST notification to the webhook URL. For Epic specifically, this is handled through the Subscription mechanism in Epic's FHIR API.

**Q:** What is the difference between a required and a must-support element in a FHIR profile?
**A:** A required (mandatory) element marked with `cardinality 1..1` or `1..*` must always be present in every instance of the resource. For example, US Core Patient requires `name` (1..*) and `identifier` (1..*). A must-support element (flagged in the profile definition) means that if the system has the data for that element, it must populate it, and consuming systems must be able to process it. For example, US Core Patient `race` extension is must-support but not mandatory — EHRs must include it if they have the data, but a Patient resource without race data is still valid.

**Q:** How does the FHIR `_include` search parameter work for retrieving related resources?
**A:** The `_include` parameter tells the FHIR server to include related resources referenced by the searched resources in the same response bundle. For example: `GET [base]/ExplanationOfBenefit?patient=Patient/123&_include=ExplanationOfBenefit:claim` would return the EOBs matching the search AND the Claim resources they reference. `_revinclude` does the reverse — it includes resources that reference the searched resources. This reduces the number of API calls needed to assemble related data.

**Q:** What FHIR resource types are used for medication management and how do they relate?
**A:** Three medication resources form a workflow: (1) MedicationRequest — the prescriber's order for a medication (includes medication, dosage, quantity, refills); (2) MedicationDispense — the pharmacist's fulfillment of that order (what was actually dispensed, when, and how much); (3) MedicationAdministration — the record of medication actually given to a patient (inpatient setting, includes dose administered, time, route). For RCM purposes, MedicationAdministration is most relevant as it generates billable charges (especially for infusion or injectable drugs).

**Q:** How does FHIR handle attachments and documents for claim supporting information?
**A:** FHIR uses the DocumentReference resource for attachments and clinical documents. For claim supporting information, the Claim resource includes a `supportingInfo` array where each entry can reference a DocumentReference via `supportingInfo[x]`. The DocumentReference resource contains metadata (type, date, author, size) and refers to the actual content (PDF, CDA, image) stored as Binary resources or external URLs. This is used for attaching medical records, referral forms, and medical necessity documentation to claims.

**Q:** What is an OperationOutcome in FHIR and when is it returned?
**A:** OperationOutcome is a resource used to convey error, warning, or information messages from FHIR operations. It is returned when: (1) a validation operation ($validate) finds issues with a resource; (2) a create/update operation fails due to business rules; (3) a search encounters warnings or partial results; (4) an authentication/authorization error occurs. Each OperationOutcome contains one or more `issue` entries with severity (fatal, error, warning, information), code (required, invalid, not-found, etc.), and details about the issue. Denials Doctor should log and alert on OperationOutcome responses.

**Q:** How do you model a patient's insurance coverage history using FHIR?
**A:** Use the Coverage resource with `period` dates to define coverage effective periods. Each Coverage instance represents a plan covering a patient for a specific time range. Multiple Coverage resources for the same patient represent coverage changes over time, with `order` distinguishing primary (order=1), secondary (order=2), and tertiary (order=3) coverage. The Coverage resource's `status` indicates whether coverage is currently `active`, `cancelled`, or `entered-in-error`. Denials Doctor queries `Coverage?beneficiary=[patient-id]&status=active` to determine current active coverage for claim submission.

**Q:** What FHIR search modifiers are available and when should they be used?
**A:** FHIR search modifiers refine search behavior: `:exact` — exact match (case-sensitive); `:contains` — substring match; `:missing` — find resources where a field is present/absent (`true`/`false`); `:not` — negation; `:above`/`:below` — hierarchy navigation (for codes); `:text` — text search within coded fields; `:in` — match codes in a value set; `:of-type` — search by identifier type; `iterate` modifier — used with `_include` and `_revinclude` to chain includes on included resources. Example: `GET [base]/Condition?code:in=http://valueset.example.org/conditions` finds all conditions with codes in that value set.

**Q:** How does FHIR support tracking changes over time with versioning?
**A:** FHIR resources have a `meta.versionId` field that changes each time the resource is updated. The read history endpoint (`GET [base]/[type]/[id]/_history`) returns a Bundle of all versions of the resource, each with a unique versionId. Clients can read a specific version: `GET [base]/Patient/123/_history/5`. The If-Match header (`If-Match: W/"5"`) enables version-aware updates that fail if the resource was modified since the client last read it (optimistic locking). This is important for Denials Doctor when multiple systems may update the same claim or coverage data.

**Q:** What is a FHIR CapabilityStatement and how is it used in integration?
**A:** A CapabilityStatement (accessed via `GET [base]/metadata`) describes the FHIR server's capabilities: what resource types it supports, what operations are available, what search parameters are supported for each resource, what security schemes are implemented, what formats are available (JSON, XML), and what profiles the server conforms to. Denials Doctor uses the CapabilityStatement to configure its integration adapters — knowing which resources the EHR supports determines which integration features are available. For example, if the server doesn't support the `$export` operation, Denials Doctor falls back to individual resource queries.

**Q:** What are the common FHIR server response codes and how should Denials Doctor handle each?
**A:** 200 OK — success (read, update, search); 201 Created — resource created successfully; 204 No Content — successful delete; 400 Bad Request — malformed request, retry with correct syntax; 401 Unauthorized — token expired or invalid, trigger credential refresh; 403 Forbidden — valid token but insufficient scope, log and alert; 404 Not Found — resource doesn't exist, likely data sync issue; 409 Conflict — version conflict, re-read resource and retry; 422 Unprocessable Entity — validation failure, check profile conformance; 429 Too Many Requests — rate limited, implement exponential backoff; 500 Internal Server Error — EHR server error, retry with backoff; 503 Service Unavailable — EHR maintenance, retry with backoff.

**Q:** What is the FHIR `x-fhir-request` header and when should it be used?
**A:** The `x-fhir-request` header, set to the FHIR server base URL, is used for tracking and auditing FHIR requests across intermediaries. When Denials Doctor accesses FHIR through an API gateway or intermediary, this header helps the EHR server identify the original request source. It's also used in the subscription notification body to indicate which server generated the notification.

**Q:** How does FHIR R4's Task resource relate to revenue cycle workflows?
**A:** The Task resource represents a unit of work to be performed and can track status through states: `draft`, `requested`, `received`, `accepted`, `rejected`, `in-progress`, `on-hold`, `completed`, `cancelled`, `failed`. For RCM, Tasks can model denial work items: a Task is created when a denial is identified (`code: denial-review`), assigned to a billing specialist (`owner`), with due dates (`executionPeriod`), and associated with the relevant EOB and Claim via `focus` and `reasonReference`. As the denial is worked, the task status transitions through `in-progress` to `completed`.

**Q:** What is `_elements` in FHIR search and how does it impact performance?
**A:** The `_elements` parameter specifies a subset of resource elements to return (e.g., `_elements=id,status,created` on ExplanationOfBenefit). This reduces response size and improves query performance by excluding large, non-critical fields like text, narrative, and full data payloads. For Denials Doctor's dashboard operations that need only summary status information (not full EOB details), using `_elements` significantly reduces bandwidth and latency.

**Q:** How does FHIR handle non-US healthcare identifiers?
**A:** FHIR uses an `identifier` array with a `system` (URI defining the identifier namespace) and `value` (the identifier string). Each jurisdiction defines its own identifier systems: US uses `http://hl7.org/fhir/sid/us-npi` for NPI, `http://hl7.org/fhir/sid/us-ssn` for SSN, and `http://hl7.org/fhir/sid/us-tin` for TIN. Other countries define their own: Canada uses Canadian PKI, UK uses NHS number, Australia uses Medicare number. FHIR's extensible identifier system means any recognized identifier namespace can be represented.

**Q:** What is the Encounter `class` element and why is it important for claim processing?
**A:** The Encounter `class` element (using ActCode from HL7 v3) categorizes the encounter type: AMB (ambulatory), IMP (inpatient), OBSEN (observation), EMER (emergency), HH (home health), VR (virtual/telehealth), etc. This is critical for claim processing because: (1) it determines which claim type (professional vs institutional) should be generated; (2) it affects coverage and benefit determination — some plans have different benefits for inpatient vs ambulatory; (3) place of service codes on claims must align with the encounter class; (4) denial analysis must account for class-specific rules (e.g., medical necessity criteria differ for inpatient vs observation).

**Q:** How do you use FHIR's List resource in an RCM context?
**A:** The List resource manages collections of resources. In RCM contexts: (1) a "Work Queue" list contains claims needing review with status and ordering; (2) a "Denial Watch" list tracks patients with recurring denial patterns; (3) a "Follow-Up" list contains claims requiring follow-up action with due dates. Lists support ordering, status tracking, and empty reasons. They can be shared across users and updated atomically.

**Q:** What is the most reliable way to get a complete patient record for a denial review?
**A:** The `Patient/$everything` operation returns all resources linked to a patient in a single Bundle. However, for production use with large patient records, this can time out. A more reliable approach: (1) query specific resources needed for the review using `_include` and `_revinclude`; (2) limit date ranges with `_since` parameter; (3) use `_type` to specify only relevant resources (EOB, Claim, Encounter, Condition, Procedure, Coverage); (4) for large data volumes, use Bulk Data Export and filter locally.

---

## Summary

FHIR R4 is the foundation of Denials Doctor's EHR integration strategy. Its RESTful API model, comprehensive resource definitions, SMART on FHIR security framework, and broad EHR vendor adoption make it the primary integration protocol. Key resources for RCM include Patient, Coverage, Claim, ExplanationOfBenefit, Encounter, Condition, Procedure, Practitioner, and Organization.

The US Core Implementation Guide ensures compliance with US healthcare data standards. Bulk Data Export enables large-scale data extraction, while FHIR Subscriptions provide real-time event-driven integration. SMART on FHIR's authorization framework ensures HIPAA-compliant, auditable access to protected health information.