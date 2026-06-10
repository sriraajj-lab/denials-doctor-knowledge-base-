# EHR Systems: Integration Profiles and Patterns

## Overview

Electronic Health Record (EHR) systems are the primary source of clinical and billing data for Denials Doctor. Each major EHR platform has unique APIs, integration patterns, authentication methods, and data models. Understanding these differences is essential for building reliable integration adapters.

This document profiles the major EHR systems used in US healthcare, their API capabilities, billing modules, and integration patterns relevant to Denials Doctor.

---

## Epic Systems

### Market Position
- **Market share:** ~35% of US acute care hospitals, ~30% of ambulatory practices
- **Customer base:** Major health systems (Mayo Clinic, Cleveland Clinic, Kaiser Permanente), large hospitals, academic medical centers
- **Strengths:** Most comprehensive EHR, largest market share, most advanced API ecosystem
- **Weaknesses:** Complex implementation, expensive, requires dedicated interface team

### Integration Capabilities

#### Epic FHIR R4 API (Most Advanced)

Epic offers the most mature FHIR R4 implementation among all EHR vendors. Key capabilities:

| Feature | Status | Notes |
|---|---|---|
| FHIR R4 (US Core) | Full support | All US Core profiles implemented |
| SMART on FHIR | Full support | EHR launch, standalone launch, backend services |
| Bulk Data Export | Supported | System-level and group-level $export |
| Patient $everything | Supported | Comprehensive patient record export |
| FHIR Subscriptions | Supported | REST-hook subscriptions |
| FHIR Search | Full support | All standard search parameters |

Available FHIR resources on Epic:
- Patient, Practitioner, Organization, Location
- Encounter, Condition, Procedure, Observation, DiagnosticReport
- Coverage, Claim, ClaimResponse, ExplanationOfBenefit
- MedicationRequest, MedicationDispense, MedicationAdministration
- AllergyIntolerance, Immunization, DocumentReference, DiagnosticReport
- Appointment, Schedule, Slot
- Task, Communication, CarePlan, CareTeam, Goal
- Procedure, ImagingStudy, Specimen, FamilyMemberHistory

#### Epic Web Services (EWS)

Legacy SOAP-based web services for Epic integration:
- **Patient Data Access (PDA):** Read patient demographics, encounters, medications, labs
- **Clinical Data Access (CDA):** Read clinical data (results, reports, diagnoses)
- **Provider Data Access (PRDA):** Read provider information
- **Patient Visit Query (PVQ):** Query patient encounters and visits
- **Web Report Access (WRA):** Execute and retrieve Epic reports

EWS uses SOAP/XML and is being phased in favor of FHIR. New integrations should use FHIR.

#### Epic Bridges (HL7 v2)

Epic Bridges is Epic's built-in HL7 v2 interface engine. It manages real-time HL7 message routing between Epic and external systems:

| ADT Message | Use | Denials Doctor Relevance |
|---|---|---|
| ADT^A01 (Admit) | Patient admitted | Start of encounter, begin billing tracking |
| ADT^A03 (Discharge) | Patient discharged | Trigger charge capture and claim creation |
| ADT^A04 (Registration) | Outpatient registered | Outpatient visit tracking |
| ADT^A08 (Update) | Demographics update | Insurance changes, eligibility re-check |
| ADT^A40 (Merge) | Patient merge | Handle duplicate records |

#### Integration Patterns

**Pattern 1: SMART on FHIR (Recommended)**
```
Denials Doctor ──OAuth2──▶ Epic FHIR API
   │                            │
   │   SMART App Orchard        │ Patient, Encounter, EOB
   │   registration required    │ Coverage, Condition
   └────────────────────────────┘
```

**Pattern 2: HL7 v2 via Bridges**
```
EHR ──HL7 ADT/ORM/DFT──▶ Epic Bridges ──HL7──▶ Denials Doctor HL7 Adapter
```

**Pattern 3: Bulk Data Export (Initial Load)**
```
Denials Doctor ──$export──▶ Epic FHIR API
   │                     ╚══ NDJSON files
   └── Downloads ──▶ Initial database load
```

#### Epic Billing Modules

**Epic Resolute Hospital Billing (HB):** For facility/institutional billing. Manages UB-04 claim creation, charge capture, revenue codes, and contractual adjustments.

**Epic Resolute Professional Billing (PB):** For professional/physician billing. Manages CMS-1500 claim creation, CPT/HCPCS coding, and E&M coding.

Both modules generate claims that can be interfaced to Denials Doctor for:
- Pre-submission claim validation and scrub
- Real-time denial detection through HL7 interfaces
- Payment posting and adjustment tracking

#### Epic App Orchard

Epic's app marketplace and SMART on FHIR registration portal. To register Denials Doctor:
1. Create an App Orchard account
2. Register the application with:
   - App name and description
   - Redirect URIs
   - Required SMART scopes (patient/*.read, user/*.read, system/*.*)
   - Launch URLs (EHR launch and standalone)
3. Undergo security review
4. Obtain client ID and secret
5. Distribute to Epic customer organizations

##### Epic Configuration Requirements

For each Epic customer, Denials Doctor needs:
- **FHIR base URL:** `https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/`
- **SMART on FHIR endpoints:** Authorize URL, Token URL
- **Client ID:** App Orchard registered ID (per customer or global)
- **Patient population:** Which patients to monitor (by facility, provider, department)
- **Scopes:** Minimum required scope set for RCM operations

---

### Cerner (Oracle Health)

#### Market Position
- **Market share:** ~25% of US acute care hospitals
- **Customer base:** Veterans Health Administration (VA), Department of Defense (DoD), HCA Healthcare, Intermountain Healthcare
- **Current status:** Acquired by Oracle in 2022, transitioning to Oracle Health branding. Oracle is modernizing the platform with cloud-native infrastructure and enhanced API capabilities.

#### Integration Capabilities

**Cerner Millennium / Oracle Health**

| Feature | Status | Notes |
|---|---|---|
| FHIR R4 | Supported | Oracle Health FHIR API, growing capabilities |
| SMART on FHIR | Supported | EHR launch and standalone |
| HL7 v2 | Full support | Real-time ADT, ORM, ORU, DFT via iBus |
| Cerner iBus (Open Development Platform) | Active | SOAP/REST services, legacy |
| Bulk Data | Limited | System-level export available |
| Ignite APIs | Newer | Modern REST APIs for Oracle Health |

**Cerner FHIR Resources:**
- Patient, Practitioner, Organization, Location
- Encounter, Condition, Procedure, Observation
- AllergyIntolerance, DocumentReference, Immunization
- Coverage, Claim, ClaimResponse (limited availability)

Note: Coverage and Claim/EOB resources are not as widely available on Cerner as on Epic. Many Cerner customers require HL7 v2 integration for billing data.

**Cerner iBus API (Legacy):**
- iBus supports SOAP/XML services
- Services include: Patient Demographics, Clinical Summary, Medication Profile, Lab Results
- Being replaced by FHIR and Ignite APIs
- New integrations should target FHIR where available

**Oracle Health Ignite APIs:**
- New RESTful API framework
- More consistent data model
- Cloud-native architecture
- OAuth2 authentication
- Available through Oracle Health marketplace

#### Integration Patterns

**Pattern 1: FHIR API (Preferred for new integrations)**
```
Denials Doctor ──OAuth2──▶ Oracle Health FHIR API
   │                            │
   │                            Patient, Encounter, Observation
   └────────────────────────────┘
```

**Pattern 2: HL7 v2 via iBus (Most common currently)**
```
EHR ──HL7 v2──▶ Cerner Millennium ──HL7──▶ Denials Doctor HL7 Adapter
```

**Pattern 3: Bulk Extract (For initial data loads)**
```
Cerner Discern Analytics ──Report──▶ CSV/XML ──▶ Denials Doctor
```

#### Cerner Revenue Cycle

**Cerner Revenue Cycle Solutions:** Manages patient access, charge capture, claim submission, payment posting, and denial management.

Key integration points:
- **HL7 DFT^P03:** Real-time charge posting feeds
- **ADT messages:** Patient registration and encounter management
- **Cerner's integrated claim workflow:** Claims created in Cerner can be exported via HL7 or batch files for Denials Doctor validation

Special Considerations:
- Cerner's FHIR API is less mature than Epic's — coverage and claim resources may not be available
- Many Cerner customers use third-party clearinghouses (Change Healthcare, Waystar) for claim submission rather than direct Cerner billing
- Billing data (charges, payments, adjustments) may require HL7 DFT interfaces rather than FHIR

---

### Meditech

#### Market Position
- **Market share:** ~15% of US acute care hospitals
- **Customer base:** Community hospitals, rural hospitals, some large health systems
- **Platforms:** Meditech Expanse (newer, web-based), Meditech 6.x (Magic, legacy), Meditech Client Server (older)

#### Integration Capabilities

| Platform | FHIR | HL7 v2 | Web Services |
|---|---|---|---|
| Meditech Expanse | FHIR R4 (limited) | Full HL7 v2 support | REST APIs available |
| Meditech 6.x (Magic) | Not available | HL7 v2 (primary) | Mirth-based integration |
| Meditech Client Server | Not available | HL7 v2 (primary) | Custom interfaces |

**Meditech Expanse FHIR:**
- Limited FHIR R4 support (evolving)
- Resources: Patient, Encounter, Practitioner, Organization
- SMART on FHIR: Limited availability
- US Core profiles: Partial support

**Meditech HL7 v2 (Primary Integration Method):**
- ADT^A01, A03, A04, A08 — patient registration and encounter updates
- ORM^O01 — order placement
- ORU^R01 — results delivery
- DFT^P03 — charge posting (may not be available on all Meditech versions)
- MFN — master file updates

#### Integration Pattern

```
Meditech ──HL7 v2──▶ Interface Engine (Mirth) ──HL7/FHIR──▶ Denials Doctor
```

Meditech almost always requires an intermediate interface engine (typically Mirth Connect) because:
1. Meditech's native HL7 v2 parsing is limited
2. Mirth provides transformation, routing, and error handling
3. Meditech Expanse may offer FHIR but it is not yet widely deployed
4. Interface engine provides buffering and retry for reliability

#### Meditech Billing

**Meditech Patient Finance:** Manages patient financials, charge capture, and billing.

- Billing data typically accessed via HL7 v2 DFT messages or batch file exports
- Claims generated within Meditech and submitted to clearinghouses
- Denials Doctor receives billing data via HL7 interface for validation and analysis

---

### Athenahealth (athenaOne)

#### Market Position
- **Market share:** ~8% of US ambulatory practices
- **Customer base:** Physician practices, community health centers, ambulatory clinics
- **Strengths:** Cloud-based, integrated billing (athenaCollector), strong API ecosystem
- **Model:** Unified platform (EHR + PM + billing) — athenaCollector is the billing module

#### Integration Capabilities

**athenaNet APIs:**

| API | Type | Notes |
|---|---|---|
| **athenaNet REST API** | REST/JSON | Mature, comprehensive |
| **athenaNet FHIR API** | FHIR R4 | Growing coverage |
| **MDP (Marketplace Developer Platform)** | App marketplace | Publish apps for athena customers |

**athenaNet REST API Resources:**
- Patient demographics, patient chart
- Appointments, encounters, scheduling
- Clinical documentation, lab results, medications
- **Charge capture** and encounter billing
- **Claim status** and claim data
- **Provider information**, practice locations

**athenaNet FHIR API:**
- Resources: Patient, Encounter, Practitioner, Organization
- SMART on FHIR: Supported
- US Core profiles: Supported

**athenaCollector (Billing Module):**
athenaCollector is athenahealth's built-in revenue cycle management platform. Key features:
- Charge capture integrated with clinical documentation
- Automated claim submission and management
- Denial tracking and management
- Payment posting (automated via ERA/835)
- Patient statement processing

#### Integration Patterns

**Pattern 1: athenaNet REST API (Recommended)**
```
Denials Doctor ──OAuth2──▶ athenaNet API
   │                            │
   │                            Patients, appointments, charges
   │                            claims, claim status
   └────────────────────────────┘
```

**Pattern 2: athenaNet FHIR API**
```
Denials Doctor ──OAuth2──▶ athenaNet FHIR API
   │                            │
   │                            Patient, Encounter
   └────────────────────────────┘
```

**Pattern 3: Webhooks / Notifications**
```
athenaNet ──Event Notification──▶ Denials Doctor Webhook
    (charge entered, claim status change, denial)
```

#### Authentication

- OAuth2 with client credentials or authorization code
- athenaNet provides both practice-level and provider-level access
- API keys for development, OAuth2 tokens for production
- Rate limiting: 10 requests per second per practice (configurable)

---

### eClinicalWorks

#### Market Position
- **Market share:** ~10% of US ambulatory practices
- **Customer base:** Medium to large physician practices, community health centers
- **Platform:** Cloud-based EHR with integrated PM and billing

#### Integration Capabilities

| API | Type | Notes |
|---|---|---|
| **eClinicalWorks Web APIs** | SOAP/XML | Legacy, being deprecated |
| **V12 FHIR API** | FHIR R4 | Newer, recommended |
| **HealthGrid** | HIE/Exchange | Data sharing network |

**V12 FHIR API:**
- Resources: Patient, Encounter, Practitioner, Organization, Location
- Observations, Conditions, Procedures
- MedicationRequest, MedicationAdministration
- Appointments, Schedule
- SMART on FHIR: Supported
- US Core profiles: Supported

**eClinicalWorks HL7 v2:**
- ADT, ORM, ORU messages
- DFT (financial transactions) — may be limited
- Requires interface engine configuration

#### eClinicalWorks Billing

**Built-in RCM Module:** eClinicalWorks offers integrated revenue cycle management:
- Charge capture and coding
- Claim submission (direct and via clearinghouse)
- Payment posting
- Denial management
- Patient statements

#### Integration Patterns

**Pattern 1: V12 FHIR API (Recommended for new integrations)**
```
Denials Doctor ──OAuth2──▶ eCW V12 FHIR API
```

**Pattern 2: Legacy Web APIs (SOAP)**
```
Denials Doctor ──SOAP/XML──▶ eCW Web Services
```

**Pattern 3: HL7 v2 via Interface**
```
eCW ──HL7──▶ Interface Engine ──▶ Denials Doctor
```

---

### Other EHR Systems

#### Practice Fusion (Veradigm / Allscripts)

- **Market:** Small ambulatory practices
- **Integration:** Web-based, REST APIs, FHIR API
- **Billing:** Integrated billing module (Practice Fusion Billing)
- **API auth:** API key-based (legacy), OAuth2 for FHIR
- **Notes:** Acquired by Allscripts (now Veradigm). API ecosystem has limited depth. Best integrated via clearinghouse for claims data.

#### NextGen Healthcare

- **Market:** Ambulatory practices, behavioral health, community health centers
- **Integration:** NextGen Mirth Connect (HL7), NextGen API (SOAP/REST), FHIR (limited)
- **Billing:** NextGen Practice Management (PM) with integrated billing
- **Connection:** Typically uses Mirth Connect as the interface engine for HL7 integration
- **Notes:** Mirth is owned by NextGen (both now under the same company). FHIR adoption is incremental.

#### Allscripts (Veradigm)

- **Market:** Large ambulatory practices, hospitals (TouchWorks, Sunrise Acute Care)
- **Platforms:** TouchWorks (ambulatory), Sunrise (acute care), Professional (EMR)
- **Integration:** HL7 v2 (primary), web services, FHIR (growing)
- **Billing:** Allscripts Practice Management, Allscripts Revenue Cycle Management
- **Notes:** Allscripts rebranded to Veradigm. Multiple legacy platforms with varying API maturity.

#### Kareo (Tebra)

- **Market:** Small independent practices (1-10 providers)
- **Platforms:** Kareo Clinical (EHR), Kareo Billing (PM)
- **Integration:** REST APIs available through Tebra platform, FHIR limited
- **Billing:** Kareo Billing — cloud-based RCM, claim submission, payment posting
- **Notes:** Simpler integration than enterprise EHRs. Data export via clearinghouse or API.

#### AdvancedMD

- **Market:** Small to mid-size practices
- **Platforms:** Cloud-based EHR, PM, billing
- **Integration:** REST APIs, HL7 v2 via interface engine
- **Billing:** AdvancedMD Billing Services, integrated denial management
- **Notes:** All-in-one cloud platform. Billing data accessible via API.

#### Greenway Health (Intergy)

- **Market:** Ambulatory practices, specialty clinics
- **Platform:** Intergy EHR + Intergy PM
- **Integration:** HL7 v2 (primary), Greenway API (limited REST)
- **Billing:** Greenway Revenue Cycle Management
- **Notes:** Legacy architecture, best interfaced via HL7 or batch file exchange.

#### DrChrono

- **Market:** Small to medium practices, specialty clinics
- **Platform:** Cloud-based EHR + PM + billing
- **Integration:** REST API (comprehensive), FHIR API supported, SMART on FHIR
- **Billing:** Integrated billing with claim submission, ERA auto-posting
- **Notes:** Developer-friendly, modern API, good FHIR support among smaller EHRs.

---

## Common EHR Integration Challenges

### Rate Limiting

Most EHR APIs enforce rate limits to prevent abuse:

| EHR | Rate Limit | Notes |
|---|---|---|
| Epic | 100 req/sec (configurable) | Higher limits available with App Orchard approval |
| Cerner/Oracle Health | 50-100 req/sec | Varies by customer and contract |
| athenahealth | 10 req/sec/practice | Configurable with athena approval |
| eClinicalWorks | 30 req/min | Very restrictive, requires optimization |
| Practice Fusion | 1 req/sec | Extremely restrictive, batch operations preferred |

**Mitigation strategies:**
1. Implement client-side rate limiting
2. Use bulk operations ($export) for initial data loads
3. Cache frequently accessed data (patient demographics, provider info)
4. Use subscription/webhook mechanisms instead of polling
5. Implement exponential backoff for retry on 429 responses

### API Versioning

EHRs version their APIs independently:
- Epic: Versioned by API endpoint path (R4, R5, future)
- Cerner: Versioned via request header
- athenahealth: Versioned in URL path (e.g., `/v1/`, `/v2/`, `/preview1/`)
- eClinicalWorks: V12 is current major version

**Best practices:**
1. Always specify API version in requests
2. Monitor deprecation notices from each vendor
3. Run integration tests against new API versions during preview periods
4. Maintain version-aware adapters that can handle multiple API versions
5. Subscribe to vendor developer newsletters and changelogs

### Data Consistency

- **Real-time vs near-real-time:** EHR systems may not provide truly real-time data. Cerner and Meditech often have 5-15 minute delays in data availability.
- **Eventual consistency:** FHIR APIs may return stale data immediately after a write; subsequent reads may show different results.
- **Asynchronous processing:** Some EHR operations (like $export or subscription notifications) are asynchronous and may have significant delays.

### Patient Matching Across Systems

- Different EHRs use different patient identifiers (MRN, account number, visit number)
- Patient merges (ADT^A18, ADT^A40) change identifier mappings over time
- Cross-enterprise patient matching is complex and may require probabilistic matching
- Denials Doctor must maintain an internal patient identity map (EHR ID → Denials Doctor ID)

### Credential Management

- OAuth2 tokens expire (typically 60 minutes for access tokens, 30-90 days for refresh tokens)
- Multiple practice credentials may be needed (one OAuth2 client per practice)
- Certificate-based authentication (Epic App Orchard requires JWT signing certificates)
- API keys may need rotation per security policy

### EHR Downtime Handling

| Downtime Type | Duration | Impact | Mitigation |
|---|---|---|---|
| Planned maintenance | 2-8 hours | API unavailable | Queue requests, retry after maintenance window |
| Unplanned outage | 30 min - 4 hours | API unavailable | Circuit breaker, queue, alert |
| Scheduled upgrade | Weekend | API version change | Test in sandbox before go-live |
| Network issue | Variable | Intermittent failures | Retry with backoff, health check alerts |

**Downtime procedures:**
1. Detect failure (timeout or non-5xx response)
2. Open circuit breaker to stop cascading failures
3. Queue incoming requests for replay
4. Alert on-call team
5. Health-check endpoint every 30 seconds
6. When health check passes, close circuit breaker
7. Replay queued requests in order

---

## EHR API Authentication Patterns

| EHR | Primary Auth | Secondary Auth | Notes |
|---|---|---|---|
| Epic | SMART on FHIR OAuth2 | JWT Client Assertion | Most complex, most secure |
| Cerner (Oracle Health) | SMART on FHIR OAuth2 | Basic Auth (legacy) | OAuth2 recommended |
| athenahealth | OAuth2 | API Key | Well-documented OAuth2 flow |
| eClinicalWorks | OAuth2 | API Key | OAuth2 for V12 API |
| Practice Fusion | API Key | — | Simple but rate-limited |
| NextGen | Basic Auth / Certificate | — | Varies by customer setup |
| Kareo/Tebra | OAuth2 | — | Modern OAuth |
| DrChrono | OAuth2 | API Key | Both supported |

---

## EHR Sandbox Environments

| EHR | Sandbox URL | Notes |
|---|---|---|
| **Epic** | `https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/` | open.epic.com — comprehensive sandbox with test patients |
| **Cerner/Oracle Health** | `https://fhir-ehr-staging.cerner.com/` | code-console.cerner.com (now code-console.oracle.com) |
| **athenahealth** | `https://sandbox.athenahealth.com/` | developer.athenahealth.com — requires API key |
| **eClinicalWorks** | `https://developer.eclinicalworks.com/` | V12 sandbox available |
| **Practice Fusion** | `https://www.practicefusion.com/api/` | Limited sandbox |
| **DrChrono** | `https://app.drchrono.com/api/v1/` | Test mode available in developer portal |

---

## EHR Comparison Summary

| Feature | Epic | Cerner | Meditech | Athena | ECW | NextGen | DrChrono |
|---|---|---|---|---|---|---|---|
| FHIR R4 | Excellent | Good | Limited | Good | Good | Limited | Good |
| HL7 v2 | Full | Full | Full | Partial | Good | Full | Partial |
| SMART on FHIR | Yes | Yes | Limited | Yes | Yes | Limited | Yes |
| Bulk Data | Yes | Limited | No | Limited | No | No | No |
| REST API | Yes | Yes | Limited | Excellent | Good | Limited | Excellent |
| SOAP/Legacy | EWS | iBus | No | No | Legacy | Mirth | No |
| Billing Integration | Deep | Moderate | Moderate | Deep | Deep | Moderate | Moderate |
| API Documentation | Excellent | Good | Poor | Excellent | Moderate | Poor | Excellent |
| Sandbox | Excellent | Good | Poor | Excellent | Good | Poor | Good |
| Rate Limits | Generous | Moderate | N/A | Moderate | Severe | N/A | Moderate |
| Ease of Integration | Moderate | Moderate | Difficult | Easy | Moderate | Difficult | Easy |

---

## Agent Training: Q&A Pairs

**Q:** Which EHR has the best FHIR API for revenue cycle management?
**A:** Epic Systems has the most advanced FHIR R4 API for RCM purposes. Epic supports the widest range of FHIR resources including Patient, Coverage, Claim, ExplanationOfBenefit, Encounter, Condition, and Procedure — all critical for denial management. Epic also offers SMART on FHIR with all three launch scenarios (EHR launch, standalone, backend services), bulk data export, FHIR subscriptions, and excellent sandbox environments. While Cerner and athenahealth also offer FHIR APIs, Epic's implementation is the most comprehensive and production-ready for RCM workflows.

**Q:** How does Denials Doctor integrate with Epic for denial data?
**A:** Denials Doctor integrates with Epic through three primary methods: (1) SMART on FHIR to query ExplanationOfBenefit resources directly — this provides adjudication outcomes with denial reasons (CARC codes) and process notes; (2) HL7 v2 via Epic Bridges for real-time ADT (patient movement), DFT (charge posting), and ORU (result) messages; (3) Epic App Orchard registration for OAuth2 credentials and secure API access. The recommended primary integration is SMART on FHIR for querying clinical and billing data, supplemented by HL7 Bridges for real-time event notifications.

**Q:** What integration options exist for Cerner/Oracle Health systems?
**A:** Cerner/Oracle Health offers three integration paths: (1) Oracle Health FHIR API — the recommended path for new integrations, supporting Patient, Encounter, Observation, and some billing resources; (2) Cerner iBus (legacy SOAP/REST) — still widely deployed, especially for clinical data access, but being phased out in favor of FHIR/Ignite APIs; (3) HL7 v2 via Cerner's Open Engine interface — the most reliable method for real-time data delivery, especially for ADT and ORU messages. For claims data specifically, many Cerner customers use a clearinghouse (Change Healthcare, Waystar) as an intermediary.

**Q:** What is the most reliable way to get real-time charge data from an EHR?
**A:** The most reliable method is HL7 v2 DFT^P03 (Detailed Financial Transaction - Post Charge) messages. When supported by the EHR, DFT messages are triggered in real-time as charges are posted to patient accounts. This works across Epic, Cerner, Meditech, and many other EHRs. For EHRs that do not support DFT (some cloud-based systems), alternatives include: polling a FHIR Claim or ChargeItem resource, checking athenaNet's charge API endpoint, or receiving batch charge files via SFTP on a scheduled basis.

**Q:** Does athenahealth provide access to ExplanationOfBenefit resources via FHIR?
**A:** athenahealth's FHIR API supports Patient and Encounter resources but does not yet offer full ExplanationOfBenefit support. For billing and adjudication data, Denials Doctor uses the athenaNet REST API which provides claim status information and charge data. For detailed EOB data with CARC codes, Denials Doctor connects to the athenaCollector module or integrates directly with clearinghouse ERA (835) data.

**Q:** How does EHR API rate limiting affect Denials Doctor's data collection?
**A:** Rate limiting varies significantly by EHR. Epic offers generous limits (100 req/sec), but eClinicalWorks is very restrictive (30 req/min). For restrictive EHRs, Denials Doctor implements: (1) request queuing and throttling to stay within limits; (2) bulk operations (like FHIR $export) for initial or periodic full data loads; (3) webhook/subscription mechanisms to receive pushed notifications instead of polling; (4) data caching with TTLs to reduce redundant API calls; (5) prioritized API usage (critical denial data first, analytics data during off-peak).

**Q:** What is the best integration pattern for a Meditech hospital?
**A:** Meditech hospitals are best integrated via HL7 v2 through an interface engine (typically Mirth Connect). Meditech's native FHIR capabilities are limited, and its Expanse platform is still being deployed. The recommended approach: (1) Connect Meditech's HL7 output to Mirth Connect; (2) Configure ADT messages (A01, A03, A04, A08) for patient and encounter data; (3) Configure DFT messages for charge data; (4) Use Mirth to transform HL7 to FHIR or internal JSON format; (5) Forward transformed data to Denials Doctor via HTTPS API.

**Q:** How do you handle patient merges across different EHR systems?
**A:** Patient merges are handled through: (1) ADT^A18 or ADT^A40 HL7 messages — the MRG segment contains the source patient identifier(s), and the PID segment contains the surviving/master patient record; (2) FHIR Patient.link element — indicates linked patient records with relationship type (seealso, replaces, refer); (3) Denials Doctor maintains a patient identity mapping table that tracks EHR patient IDs, Denials Doctor internal IDs, and merge history; (4) When a merge notification is received, all historical claim and encounter data under the old ID is re-associated with the new surviving ID; (5) A merge audit log tracks all identity changes for HIPAA compliance and data integrity.

**Q:** What is Epic Bridges and how does it relate to HL7 integration?
**A:** Epic Bridges is Epic's built-in HL7 v2 interface engine. It manages bidirectional HL7 message flow between Epic and external systems. Key capabilities: (1) Receives HL7 messages from external systems (orders, ADT updates, results); (2) Routes messages to the correct Epic application module (Inpatient, Ambulatory, Emergency); (3) Sends HL7 messages to external systems (ADT notifications, charge posting, results); (4) Provides message logging, error handling, and retry. For Denials Doctor, Bridges is the gateway for receiving ADT and DFT messages from Epic.

**Q:** What are the key differences between integrating with Epic vs Cerner for denial data?
**A:** Key differences: (1) FHIR maturity — Epic has full EOB resource support with adjudication details; Cerner's FHIR is more clinically focused with less billing resource availability; (2) Authentication — both use SMART on FHIR OAuth2, but Epic requires App Orchard registration while Cerner uses the Oracle Health developer portal; (3) HL7 — both support HL7 v2, but Epic Bridges is more streamlined than Cerner's Open Engine; (4) Claim data access — Epic provides ExplanationOfBenefit via FHIR; Cerner often requires a clearinghouse intermediary for claim data; (5) Bulk data — Epic has robust $export support; Cerner's bulk export is more limited.

**Q:** How does EHR downtime affect Denials Doctor operations?
**A:** EHR downtime causes: (1) API unavailability — all FHIR/REST calls fail with 502/503 errors; (2) Missing data — claims and denials generated during downtime may not be captured; (3) Data backlogs — when the EHR comes back online, there may be a flood of queued messages. Denials Doctor handles this with: circuit breaker pattern (stop calling failing API), request queuing (store-and-forward for non-time-sensitive data), catch-up sync (batch process missed data after recovery), and alerting (notify operations team of extended downtime).

**Q:** What is athenahealth's Marketplace Developer Platform (MDP)?
**A:** The athenahealth MDP (Marketplace Developer Platform) is athena's app marketplace and integration framework. It allows third-party developers to create applications that integrate with athenaNet and publish them to the athena marketplace. For Denials Doctor, publishing through MDP provides: (1) streamlined OAuth2 credential management; (2) access to athenaNet's full REST API; (3) customer discovery through the marketplace; (4) standardized integration lifecycle management. Denials Doctor publishes through MDP to simplify deployment for athenahealth customers.

**Q:** How does Denials Doctor get claim status updates from EHRs that don't support real-time notifications?
**A:** For EHRs without real-time notification support: (1) Scheduled polling — Denials Doctor queries the EHR's claim or EOB endpoint every N minutes (configurable per EHR, typically 15-60 minutes); (2) Batch file processing — the EHR generates periodic batch files (typically nightly or every 4 hours) containing claim status updates, which are delivered via SFTP; (3) Clearinghouse intermediary — claim status is tracked through the clearinghouse (Change Healthcare, Waystar) which provides real-time 277/277CA responses; (4) ERA processing — when the 835 ERA is received (typically daily), it provides the definitive claim status update.

**Q:** What EHR supports require special handling for multi-tenant integrations?
**A:** Multi-tenant EHR integrations require: (1) Per-tenant credentials — each EHR customer has unique OAuth2 client IDs, API keys, and tokens; (2) Per-tenant base URLs — each customer's EHR instance has a unique FHIR base URL; (3) Isolated data storage — patient and claim data from different customers must be segregated; (4) Per-tenant rate limits — rate limits are enforced per customer EHR instance; (5) Per-tenant configuration — integration settings (which resources to sync, sync frequency, webhook endpoints) per customer; (6) Separate BAA/HIPAA agreements — each customer requires a signed Business Associate Agreement.

**Q:** What is the typical timeline for setting up a new EHR integration?
**A:** Typical integration timelines: Epic — 6-12 weeks (App Orchard review, OAuth2 setup, FHIR credential configuration, testing); Cerner/Oracle Health — 4-8 weeks (developer portal registration, API key setup, HL7 interface configuration); athenahealth — 2-4 weeks (MDP registration, OAuth2 setup, API testing); Meditech — 4-8 weeks (Mirth Connect setup, HL7 interface testing); eClinicalWorks — 3-6 weeks (V12 API registration, credential setup); DrChrono — 1-2 weeks (OAuth2 setup, API testing). Smaller EHRs generally have simpler integration but may have less mature APIs.

**Q:** Does Denials Doctor support on-premise EHR integration?
**A:** Yes. Denials Doctor supports on-premise EHR integration through: (1) A local integration agent deployed on-premise that connects to the EHR's internal HL7 feed or FHIR endpoint; (2) The agent encrypts and forwards data to the Denials Doctor cloud platform over TLS; (3) For EHRs without internet-facing APIs (legacy Meditech, some NextGen installations), the agent acts as a proxy; (4) The agent also provides local caching and buffering to handle network interruptions; (5) Deployment can be via Docker container or Windows service.

**Q:** What EHR-specific data fields are important for denial analysis that may not be available via standard APIs?
**A:** EHR-specific data fields that may require custom interfaces: (1) Financial class (Medicare, Medicaid, Commercial, Self-Pay) — often in custom EHR fields; (2) Attending vs. rendering provider breakdown — may require HL7 PV1 parsing; (3) Point-of-service entries and corrections — charge creation timestamps and modification history; (4) Authorization/referral numbers — sometimes stored in EHR-specific fields; (5) Patient financial responsibility estimates — calculated by the EHR's billing module; (6) Visit-level write-off policies — charity care, courtesy adjustments. These may require direct HL7 DFT parsing or custom reports from the EHR.

**Q:** How does the integration differ for an EHR that uses a clearinghouse for claim submission vs. direct submission?
**A:** Direct submission requires Denials Doctor to generate and submit 837 claim files directly to the payer, manage all trading partner agreements, and handle acknowledgments (277CA, 999). Clearinghouse-based submission simplifies integration — Denials Doctor sends claims to the clearinghouse (Change Healthcare, Waystar, Office Ally), which handles payer-specific formatting, validation, routing, and acknowledgment management. For denial management, the clearinghouse also provides consolidated 835 ERA files from all payers, simplifying the payment and denial data ingestion.

---

## Summary

Each EHR system has unique integration characteristics that Denials Doctor must handle. Epic offers the most advanced FHIR API for RCM data, while Cerner and Meditech rely more heavily on HL7 v2 messaging. Cloud-based EHRs (athenahealth, DrChrono, eClinicalWorks) provide modern REST APIs but may have tighter rate limits. Legacy EHRs (NextGen, Greenway) often require interface engines like Mirth Connect for integration.

The key to successful EHR integration is building EHR-specific adapters that handle authentication, rate limiting, data mapping, and error handling for each target system, all behind a unified agnostic integration layer.