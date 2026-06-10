# Agnostic EHR Integration Layer

## Overview

The Agnostic EHR Integration Layer is Denials Doctor's architectural solution for connecting to any EHR system through a unified, standardized interface. Rather than building custom point-to-point integrations for each EHR, the agnostic layer abstracts EHR-specific protocols (FHIR, HL7 v2, X12), authentication methods (OAuth2, API keys, certificates), and data models into a consistent internal API.

This approach enables Denials Doctor to:
- Add new EHR integrations without changing core denial analysis logic
- Support multiple EHRs simultaneously for multi-EHR customers
- Abstract protocol differences (FHIR R4, HL7 v2, X12, proprietary APIs)
- Provide a single API surface for internal components
- Handle EHR-specific errors, rate limits, and downtime consistently

---

## Architecture

```
                     ┌─────────────────────────────────────────┐
                     │         Denials Doctor Core             │
                     │  (Denial Analysis, ML Models, Workflow) │
                     └──────────────┬──────────────────────────┘
                                    │
                     ┌──────────────▼──────────────────────────┐
                     │        Internal Data Model / API        │
                     │  (Unified Patient, Claim, Denial, etc.) │
                     └──────────────┬──────────────────────────┘
                                    │
                     ┌──────────────▼──────────────────────────┐
                     │       Integration Layer (Agnostic)       │
                     │                                         │
                     │  ┌────────┐ ┌─────────┐ ┌────────────┐ │
                     │  │ API    │ │ Adapter │ │ Webhook    │ │
                     │  │ Gateway│ │ Manager │ │ Receiver   │ │
                     │  └───┬────┘ └────┬────┘ └─────┬──────┘ │
                     └──────┼───────────┼────────────┼─────────┘
                            │           │            │
          ┌─────────────────┼───────────┼────────────┼─────────────────┐
          │                 │           │            │                  │
          ▼                 ▼           ▼            ▼                  ▼
   ┌────────────┐   ┌────────────┐   ┌──────┐  ┌────────┐     ┌──────────────┐
   │ Epic       │   │ Cerner     │   │ Athena│  │Mirth   │     │Clearinghouse │
   │ Adapter    │   │ Adapter    │   │Adapter│  │Connect │     │ Adapter      │
   └─────┬──────┘   └─────┬──────┘   └──┬───┘  └───┬────┘     └──────┬───────┘
         │                 │             │          │                  │
         ▼                 ▼             ▼          ▼                  ▼
      Epic               Cerner       Athena   Meditech/          Change HC
      FHIR API           FHIR/HL7     REST API  NextGen            Waystar
                                                    (HL7 via Mirth)
```

### Component Layers

#### 1. EHR Adapters

Each EHR has a dedicated adapter that handles:
- **Authentication:** OAuth2 token management (refresh, retry), API key rotation, certificate management
- **Protocol translation:** EHR-specific API calls translated to the unified internal model
- **Rate limiting:** EHR-specific rate limit enforcement and backoff
- **Error handling:** EHR-specific error codes mapped to standard error types
- **Data mapping:** EHR-specific data formats mapped to Denials Doctor's internal model

Adapters are implemented as pluggable modules with a common interface:

```python
class EHRAdapter(ABC):
    @abstractmethod
    async def get_patient(self, patient_id: str) -> Patient: ...
    @abstractmethod
    async def get_claim(self, claim_id: str) -> Claim: ...
    @abstractmethod
    async def get_explanation_of_benefit(self, eob_id: str) -> EOB: ...
    @abstractmethod
    async def search_claims(self, params: ClaimSearchParams) -> List[Claim]: ...
    @abstractmethod
    async def search_eobs(self, params: EOBSearchParams) -> List[EOB]: ...
    @abstractmethod
    async def webhook_handler(self, payload: dict) -> Event: ...
```

Available adapters:
- **EpicAdapter:** SMART on FHIR to Epic FHIR API
- **CernerAdapter:** OAuth2 FHIR or HL7 v2 to Cerner/Oracle Health
- **AthenaAdapter:** athenaNet REST API
- **GenericFHIRAdapter:** Any FHIR R4 compliant EHR (US Core profiles)
- **MirthHL7Adapter:** HL7 v2 via Mirth Connect interface engine
- **ClearinghouseAdapter:** X12 835/837 via clearinghouse (Change Healthcare, Waystar)
- **ECWAdapter:** eClinicalWorks V12 API
- **DrChronoAdapter:** DrChrono REST API
- **CustomAdapter:** Extensible for any EHR

#### 2. API Gateway

The API Gateway serves as the single entry point for all EHR connections:

```
Denials Doctor Core → API Gateway → EHR Adapter → External EHR
```

Responsibilities:
- **Routing:** Direct requests to the correct EHR adapter based on tenant and EHR type
- **Authentication validation:** Validate internal API keys and session tokens
- **Request transformation:** Standardize incoming and outgoing data formats
- **Load balancing:** Distribute requests across adapter instances
- **Circuit breaking:** Stop calls to failing adapters to prevent cascading failures
- **Audit logging:** Log all integration requests and responses for HIPAA compliance

#### 3. Webhook Receiver

The Webhook Receiver handles asynchronous event notifications from EHRs:

- Receives FHIR subscription notifications (POST from EHR)
- Receives HL7 v2 messages forwarded by Mirth Connect
- Receives X12 835 remittance files from clearinghouses
- Validates webhook authenticity (HMAC signature, IP allowlisting, JWT verification)
- Queues events for processing by Denials Doctor Core
- Returns appropriate acknowledgments (200 OK, HL7 ACK, 202 Accepted)

#### 4. Connection Manager

The Connection Manager handles lifecycle management for EHR connections:

- **Credential vault:** Encrypted storage of OAuth2 tokens, API keys, certificates
- **Token refresh:** Automatic OAuth2 refresh token management
- **Rate limiter:** Per-EHR, per-tenant rate limiting with token bucket algorithm
- **Health checker:** Periodic health checks of EHR API endpoints
- **Circuit breaker:** Automatic failover when EHR is unresponsive
- **Retry queue:** Automatic retry with exponential backoff for failed requests
- **Credential expiry alerts:** Notify administrators of expiring credentials

---

## Adapter per EHR System

### EpicAdapter

```python
class EpicAdapter(EHRAdapter):
    def __init__(self, config: EpicConfig):
        self.fhir_base_url = config.fhir_base_url
        self.client_id = config.client_id
        self.private_key = config.private_key  # JWT signing key
        self.token_url = config.token_url
        self.http_client = httpx.AsyncClient()
        self.token_manager = SMARTTokenManager(
            client_id=config.client_id,
            private_key=config.private_key,
            token_url=config.token_url,
            scopes=["system/Patient.read", "system/Coverage.read",
                    "system/ExplanationOfBenefit.read", "system/Claim.read"]
        )

    async def get_patient(self, patient_id: str) -> Patient:
        token = await self.token_manager.get_token()
        response = await self.http_client.get(
            f"{self.fhir_base_url}/Patient/{patient_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            return FHIRPatientMapper.to_internal(response.json())
        elif response.status_code == 429:
            await self.rate_limiter.wait()
            return await self.get_patient(patient_id)
        else:
            raise EHRAdapterError(f"Epic error: {response.status_code}")

    async def search_eobs(self, params: EOBSearchParams) -> List[EOB]:
        token = await self.token_manager.get_token()
        url = f"{self.fhir_base_url}/ExplanationOfBenefit"
        query_params = {
            "patient": params.patient_id,
            "_sort": "-created"
        }
        if params.since:
            query_params["_lastUpdated"] = f"gt{params.since.isoformat()}"
        if params.claim_id:
            query_params["claim"] = params.claim_id
        response = await self.http_client.get(
            url, params=query_params,
            headers={"Authorization": f"Bearer {token}"}
        )
        bundle = response.json()
        eobs = []
        for entry in bundle.get("entry", []):
            eobs.append(FHIREOBMapper.to_internal(entry["resource"]))
        # Handle pagination
        while self._has_next(bundle):
            bundle = await self._follow_link(bundle, "next", token)
            for entry in bundle.get("entry", []):
                eobs.append(FHIREOBMapper.to_internal(entry["resource"]))
        return eobs
```

### CernerAdapter

```python
class CernerAdapter(EHRAdapter):
    def __init__(self, config: CernerConfig):
        self.fhir_base_url = config.fhir_base_url
        self.client_id = config.client_id
        self.client_secret = config.client_secret
        self.http_client = httpx.AsyncClient()
        self.token_manager = OAuth2ClientCredentialsManager(
            client_id=config.client_id,
            client_secret=config.client_secret,
            token_url=config.token_url,
            scopes=["system/Patient.read", "system/Encounter.read",
                    "system/Observation.read"]
        )
```

### AthenaAdapter

```python
class AthenaAdapter(EHRAdapter):
    def __init__(self, config: AthenaConfig):
        self.api_base = config.api_base  # e.g., "https://api.athenahealth.com/v1"
        self.practice_id = config.practice_id
        self.http_client = httpx.AsyncClient()
        self.token_manager = OAuth2AuthorizationCodeManager(
            client_id=config.client_id,
            client_secret=config.client_secret,
            auth_url=config.auth_url,
            token_url=config.token_url,
            redirect_uri=config.redirect_uri
        )

    async def get_patient(self, patient_id: str) -> Patient:
        token = await self.token_manager.get_token()
        response = await self.http_client.get(
            f"{self.api_base}/{self.practice_id}/patients/{patient_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        return AthenaPatientMapper.to_internal(response.json())
```

### GenericFHIRAdapter

The GenericFHIRAdapter works with ANY FHIR R4 compliant EHR that implements US Core profiles:

```python
class GenericFHIRAdapter(EHRAdapter):
    def __init__(self, config: GenericFHIRConfig):
        self.fhir_base_url = config.fhir_base_url
        self.auth_type = config.auth_type  # "oauth2", "apikey", "basic"
        self.http_client = httpx.AsyncClient()
        self.token_manager = self._create_token_manager(config)
        self.capability = None  # Fetched from $metadata on init

    async def initialize(self):
        """Fetch server capabilities to configure adapter behavior."""
        metadata = await self._get_metadata()
        self.capability = FHIRCapabilityParser(metadata)
        # Server supports Patient? Good to proceed.
        self._validate_resources(["Patient", "Coverage", "ExplanationOfBenefit",
                                  "Claim", "Encounter", "Condition"])

    async def get_patient(self, patient_id: str) -> Patient:
        token = await self.token_manager.get_token()
        response = await self.http_client.get(
            f"{self.fhir_base_url}/Patient/{patient_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return FHIRPatientMapper.to_internal(response.json())

    async def search_by_identifier(self, resource_type: str,
                                   identifier_system: str,
                                   identifier_value: str) -> list:
        """Search any resource by identifier."""
        token = await self.token_manager.get_token()
        response = await self.http_client.get(
            f"{self.fhir_base_url}/{resource_type}",
            params={"identifier": f"{identifier_system}|{identifier_value}"},
            headers={"Authorization": f"Bearer {token}"}
        )
        bundle = response.json()
        return [entry["resource"] for entry in bundle.get("entry", [])]
```

Generic FHIR adapter capabilities:
- **Read:** Patient, Coverage, Encounter, Condition, Procedure, DiagnosticReport, Observation, ExplanationOfBenefit, Claim, Practitioner, Organization, Location
- **Search:** By patient ID, identifier, date range, status, type
- **Write (where supported):** Claim updates (if EHR supports Claim write), Task creation for denial work items
- **Bulk:** $export for large data extraction
- **Subscription:** REST-hook subscriptions for real-time EOB updates

---

## Connection Management

### Credential Vault

```python
@dataclass
class EHRCredentials:
    client_id: str
    client_secret: EncryptedField  # AES-256-GCM encrypted
    private_key: EncryptedField    # PEM-encoded, encrypted
    token_url: str
    scopes: List[str]
    refresh_token: Optional[EncryptedField] = None
    token_expiry: Optional[datetime] = None
```

The credential vault provides:
- **Encryption at rest:** All credentials encrypted with AES-256-GCM
- **Encryption in transit:** TLS 1.2+ for all credential transmission
- **Access control:** Role-based access to credential management
- **Rotation:** Automated credential rotation with notification
- **Audit logging:** All credential access logged for HIPAA compliance
- **Hardware Security Module (HSM):** Optional HSM integration for enterprise deployments

### OAuth2 Token Management

```python
class OAuth2TokenManager:
    def __init__(self, credentials: EHRCredentials, vault: CredentialVault):
        self.credentials = credentials
        self.vault = vault
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
        self.lock = asyncio.Lock()

    async def get_token(self) -> str:
        async with self.lock:
            if self._token_valid():
                return self.access_token
            if self.refresh_token and not self._token_expired_long_ago():
                return await self._refresh()
            return await self._obtain_new_token()

    async def _refresh(self) -> str:
        response = await self._post_token_request({
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.credentials.client_id,
            "client_secret": self.credentials.client_secret
        })
        self._update_tokens(response)
        return self.access_token

    async def _obtain_new_token(self) -> str:
        response = await self._post_token_request({
            "grant_type": "client_credentials",
            "client_id": self.credentials.client_id,
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": self._generate_jwt(),
            "scope": " ".join(self.credentials.scopes)
        })
        self._update_tokens(response)
        return self.access_token
```

### Rate Limiting

```python
class EHRRateLimiter:
    def __init__(self, max_requests: int, time_window_seconds: int, name: str):
        self.max_requests = max_requests
        self.time_window = timedelta(seconds=time_window_seconds)
        self.name = name
        self.tokens = max_requests
        self.last_refill = datetime.utcnow()
        self.lock = asyncio.Lock()

    async def acquire(self) -> float:
        """Wait for a token, return wait time in seconds."""
        async with self.lock:
            self._refill()
            if self.tokens >= 1:
                self.tokens -= 1
                return 0.0
            wait = self._time_until_next_token()
        await asyncio.sleep(wait)
        return wait

    def _refill(self):
        elapsed = (datetime.utcnow() - self.last_refill).total_seconds()
        tokens_to_add = elapsed * self.max_requests / self.time_window.total_seconds()
        self.tokens = min(self.max_requests, self.tokens + tokens_to_add)
        self.last_refill = datetime.utcnow()
```

Rate limit configuration per EHR:
```yaml
rate_limits:
  epic:
    max_requests: 100
    time_window_seconds: 1
  cerner:
    max_requests: 50
    time_window_seconds: 1
  athena:
    max_requests: 10
    time_window_seconds: 1
  ecw:
    max_requests: 30
    time_window_seconds: 60
  generic_fhir:
    max_requests: 30
    time_window_seconds: 1
```

### Retry Logic with Exponential Backoff

```python
class RetryHandler:
    def __init__(self, max_retries: int = 5, base_delay: float = 1.0,
                 max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    async def execute_with_retry(self, request_func, *args, **kwargs):
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                response = await request_func(*args, **kwargs)
                if response.status_code == 429:  # Rate limited
                    retry_after = int(response.headers.get("Retry-After", self.base_delay))
                    await asyncio.sleep(min(retry_after, self.max_delay))
                    continue
                if response.status_code >= 500:  # Server error
                    delay = min(self.base_delay * (2 ** attempt) + random.uniform(0, 1), self.max_delay)
                    await asyncio.sleep(delay)
                    continue
                response.raise_for_status()
                return response
            except (httpx.TimeoutException, httpx.ConnectionError) as e:
                last_exception = e
                delay = min(self.base_delay * (2 ** attempt) + random.uniform(0, 1), self.max_delay)
                await asyncio.sleep(delay)
        raise MaxRetriesExceededError(f"Failed after {self.max_retries} retries")
```

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    STATES = ["CLOSED", "OPEN", "HALF_OPEN"]

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60,
                 half_open_max_requests: int = 3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_requests = half_open_max_requests
        self.state = "CLOSED"
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_requests = 0
        self.lock = asyncio.Lock()

    async def call(self, func, *args, **kwargs):
        async with self.lock:
            if self.state == "OPEN":
                if self._recovery_timeout_elapsed():
                    self.state = "HALF_OPEN"
                    self.half_open_requests = 0
                else:
                    raise CircuitBreakerOpenError("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)
            async with self.lock:
                if self.state == "HALF_OPEN":
                    self.half_open_requests += 1
                    if self.half_open_requests >= self.half_open_max_requests:
                        self.state = "CLOSED"
                        self.failure_count = 0
                if self.state == "CLOSED":
                    self.failure_count = 0
            return result
        except Exception as e:
            async with self.lock:
                self.failure_count += 1
                self.last_failure_time = datetime.utcnow()
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
            raise
```

---

## Data Mapping Layer

The data mapping layer translates EHR-specific data formats into Denials Doctor's unified internal model.

### FHIR to Internal Model

```python
class FHIRPatientMapper:
    @staticmethod
    def to_internal(fhir_patient: dict) -> Patient:
        identifiers = FHIRPatientMapper._extract_identifiers(fhir_patient.get("identifier", []))
        name = FHIRPatientMapper._extract_name(fhir_patient.get("name", []))
        address = FHIRPatientMapper._extract_address(fhir_patient.get("address", []))
        telecom = FHIRPatientMapper._extract_telecom(fhir_patient.get("telecom", []))

        return Patient(
            internal_id=str(uuid.uuid4()),
            ehr_patient_id=fhir_patient.get("id"),
            identifiers=identifiers,
            name=name,
            gender=fhir_patient.get("gender"),
            birth_date=fhir_patient.get("birthDate"),
            address=address,
            telecom=telecom,
            managing_organization=fhir_patient.get("managingOrganization", {}).get("reference"),
            race=FHIRPatientMapper._extract_extension(fhir_patient, "us-core-race"),
            ethnicity=FHIRPatientMapper._extract_extension(fhir_patient, "us-core-ethnicity"),
            source_system="epic",  # Set by adapter
            raw_data=fhir_patient  # Keep original for reference
        )

    @staticmethod
    def _extract_identifiers(identifiers: list) -> List[PatientIdentifier]:
        return [
            PatientIdentifier(
                type=id_entry.get("type", {}).get("coding", [{}])[0].get("code"),
                system=id_entry.get("system"),
                value=id_entry.get("value"),
                use=id_entry.get("use")
            )
            for id_entry in identifiers if id_entry.get("value")
        ]

    @staticmethod
    def _extract_name(names: list) -> PatientName:
        official = next((n for n in names if n.get("use") == "official"), names[0] if names else {})
        return PatientName(
            family=official.get("family", ""),
            given=official.get("given", []),
            prefix=official.get("prefix", []),
            suffix=official.get("suffix", [])
        )
```

### HL7 v2 to Internal Model

```python
class HL7ADTMapper:
    @staticmethod
    def parse_admission(message: HL7Message) -> Encounter:
        """Parse ADT^A01 (admit) into internal Encounter model."""
        pid_segment = message.segment("PID")
        pv1_segment = message.segment("PV1")

        return Encounter(
            internal_id=str(uuid.uuid4()),
            ehr_encounter_id=pv1_segment.field(19).value(),  # PV1-19 Visit Number
            patient_id=pid_segment.field(3).component(1).value(),  # PID-3.1 MRN
            patient_class=pv1_segment.field(2).value(),  # PV1-2: I, O, E
            admit_date=parse_hl7_datetime(pv1_segment.field(44).value()),
            discharge_date=parse_hl7_datetime(pv1_segment.field(45).value()) if pv1_segment.field(45).value() else None,
            attending_provider=pv1_segment.field(7).component(1).value(),  # PV1-7 NPI
            facility=pv1_segment.field(3).component(1).value(),  # PV1-3.1 unit
            account_number=pid_segment.field(18).value(),  # PID-18 account
            encounter_type="admission",
            raw_data=str(message)
        )
```

### X12 to Internal Model

```python
class X12835Mapper:
    @staticmethod
    def parse_remittance(edi_text: str) -> Remittance:
        """Parse X12 835 into internal Remittance model."""
        parser = X12Parser(edi_text)
        st_segments = parser.find_all("ST")
        remittances = []

        for st in st_segments:
            transactions = parser.find_loops(st, "CLP")
            for clp in transactions:
                claim_id = clp.element(1)
                status_code = clp.element(2)
                billed_amount = Decimal(clp.element(3))
                paid_amount = Decimal(clp.element(4))
                patient_resp = Decimal(clp.element(5))

                denials = []
                for svc in parser.find_loops(clp, "SVC"):
                    cpt_code = svc.element(1).sub_element(2)
                    billed = Decimal(svc.element(2))
                    allowed = Decimal(svc.element(3)) if svc.element(3) else Decimal("0")

                    for cas in parser.find_loops(svc, "CAS"):
                        group_code = cas.element(1)
                        for i in range(2, len(cas.elements), 3):
                            reason_code = cas.element(i)
                            amount = Decimal(cas.element(i + 1))
                            denials.append(DenialLine(
                                service_line=cpt_code,
                                group_code=group_code,
                                carc_code=reason_code,
                                adjustment_amount=amount,
                                billed_amount=billed,
                                allowed_amount=allowed
                            ))

                remittances.append(Remittance(
                    payer_claim_id=claim_id,
                    status_code=status_code,
                    billed_amount=billed_amount,
                    paid_amount=paid_amount,
                    patient_responsibility=patient_resp,
                    denial_lines=denials,
                    raw_data=edi_text
                ))

        return remittances
```

---

## Field Mapping Specifications

### Patient Data Mapping

| Internal Field | FHIR Path | HL7 v2 Path | X12 Path | Required |
|---|---|---|---|---|
| `patient_id` | Patient.id | PID-3.1 (MRN) | 837: NM1*QC/REF*EA | Yes |
| `first_name` | Patient.name[0].given[0] | PID-5.2 (given name) | 837: NM1*QC.3 | Yes |
| `last_name` | Patient.name[0].family | PID-5.1 (family name) | 837: NM1*QC.2 | Yes |
| `dob` | Patient.birthDate | PID-7 | 276: DMG*D8 | Yes |
| `gender` | Patient.gender | PID-8 | 276: DMG.3 | Yes |
| `ssn` | Patient.identifier where type=SS | PID-19 | 837: REF*SY | If available |
| `mrn` | Patient.identifier where type=MR | PID-3 | 837: REF*EA | Yes |
| `address` | Patient.address[0] | PID-11 | 837: N3/N4 | Yes |
| `phone` | Patient.telecom where system=phone | PID-13 | 837: PER | If available |
| `race` | Patient.extension (US Core race) | PID-10 | — | If available |
| `ethnicity` | Patient.extension (US Core ethnicity) | PID-22 | — | If available |

### Claim Data Mapping

| Internal Field | FHIR Path | HL7 v2 Path | X12 Path |
|---|---|---|---|
| `claim_id` | Claim.id | DFT: FT1-2 | 837: CLM01 |
| `patient_id` | Claim.patient | PID-3 | 837: NM1*QC |
| `service_date` | Claim.billablePeriod | FT1-3 (service date) | DTP*434 |
| `cpt_code` | Claim.item[].productOrService.coding[].code | FT1-7 | 837: SV101 |
| `modifier` | Claim.item[].modifier[].coding[].code | FT1-8 | 837: SV109 |
| `charge_amount` | Claim.item[].net.value | FT1-10 | 837: SV102 |
| `diagnosis_code` | Claim.diagnosis[].diagnosisCodeableConcept | DG1-3 | 837: HI |
| `rendering_provider` | Claim.provider | PV1-7 | 837: NM1*82 |
| `visit_number` | Claim.item[].encounter[].reference | PV1-19 | 837: CLM01 (or REF) |

### Denial Data Mapping

| Internal Field | FHIR Path | X12 Path (835) |
|---|---|---|
| `claim_id` | ExplanationOfBenefit.claim.reference | CLP01 |
| `denial_carc_codes` | EOB.item[].adjudication[].reason.coding[].code | CAS*CO/*PR/*OA |
| `denial_amount` | EOB.item[].adjudication[].amount where category=denied | CAS element 3 |
| `paid_amount` | EOB.payment.amount | CLP04 |
| `allowed_amount` | EOB.item[].adjudication[].amount where category=allowed | SVC03 |
| `patient_responsibility` | EOB.item[].adjudication[].amount where category=deductible/coinsurance | CLP05 |
| `process_notes` | EOB.processNote[].text | MSG segments (in 835) |
| `payer_name` | EOB.insurer.display | N1*PR |
| `denial_date` | EOB.created | DTM*050 (processed date) |
| `service_date` | EOB.item[].servicedDate | DTM*232 |

---

## Webhook-Based Integration

### Architecture

```
EHR ──Event──▶ Denials Doctor Webhook Receiver
                      │
                      ▼
                 Event Queue (Redis/Amazon SQS)
                      │
                      ▼
              Event Processor (Async Workers)
                      │
                      ▼
              Denials Doctor Core
```

### Webhook Receiver Endpoints

| Endpoint | Source | Event Type | Payload Format |
|---|---|---|---|
| `POST /webhook/fhir/subscription` | FHIR EHR (Epic, Cerner) | EOB update, Claim update, Patient update | FHIR Bundle |
| `POST /webhook/hl7/v2` | HL7 Interface Engine (Mirth) | ADT, DFT, ORU, ORM | HL7 v2 text |
| `POST /webhook/x12/835` | Clearinghouse | Payment/Remittance | X12 835 text |
| `POST /webhook/athena/notification` | athenahealth | Appointment, Charge, Claim status | athenaNet JSON |

### Webhook Authentication

```python
class WebhookAuthenticator:
    def verify(self, request: Request, tenant: Tenant) -> bool:
        if tenant.webhook_auth_type == "hmac":
            return self._verify_hmac(request, tenant)
        elif tenant.webhook_auth_type == "jwt":
            return self._verify_jwt(request, tenant)
        elif tenant.webhook_auth_type == "ip_allowlist":
            return self._verify_ip(request, tenant)
        elif tenant.webhook_auth_type == "api_key":
            return self._verify_api_key(request, tenant)
        return False

    def _verify_hmac(self, request: Request, tenant: Tenant) -> bool:
        payload = await request.body()
        signature = request.headers.get("X-Signature", "")
        expected = hmac.new(
            tenant.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected)
```

### Event Processing Pipeline

```python
class EventProcessor:
    EVENT_TYPES = {
        "eob_update": [ProcessEOBUpdate()],
        "claim_update": [ProcessClaimUpdate()],
        "admission": [CreateEncounter(), CheckEligibility()],
        "discharge": [FinalizeCharges(), ReviewDenialPotential()],
        "charge_posted": [ValidateCharge(), CheckAuthorization()],
        "835_received": [Parse835(), IdentifyDenials(), CreateWorkItems()],
        "new_patient": [CreatePatientRecord(), LinkCoverage()],
    }

    async def process(self, event: Event):
        handlers = self.EVENT_TYPES.get(event.type, [])
        for handler in handlers:
            try:
                await handler.handle(event)
            except Exception as e:
                await self.error_handler.handle(event, e)
                await self.retry_queue.enqueue(event, retry_count=event.retry_count + 1)
```

---

## Integration Deployment

### Docker Containers

```yaml
# docker-compose.yml
services:
  integration-gateway:
    image: denialsdoctor/integration-gateway:latest
    ports:
      - "8080:8080"
    environment:
      - DB_HOST=postgres
      - REDIS_HOST=redis
      - VAULT_ADDR=http://vault:8200
    depends_on:
      - postgres
      - redis
      - vault
    volumes:
      - ./config:/etc/denialsdoctor

  webhook-receiver:
    image: denialsdoctor/webhook-receiver:latest
    ports:
      - "8081:8081"
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis

  event-processor:
    image: denialsdoctor/event-processor:latest
    environment:
      - REDIS_HOST=redis
      - DB_HOST=postgres
    depends_on:
      - redis
      - postgres

  credential-vault:
    image: hashicorp/vault:latest
    environment:
      - VAULT_DEV_ROOT_TOKEN_ID=dev-token
    ports:
      - "8200:8200"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=denialsdoctor
      - POSTGRES_PASSWORD=changeme
    volumes:
      - postgres-data:/var/lib/postgresql/data
```

### Cloud-Hosted (Multi-Tenant)

```
┌─────────────────────────────────────────────────────┐
│                Denials Doctor Cloud                  │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │           Load Balancer (AWS ALB)             │   │
│  └──┬────────────┬──────────────┬───────────────┘   │
│     │            │              │                    │
│  ┌──▼──┐    ┌────▼────┐   ┌────▼────┐              │
│  │API  │    │ Webhook │   │ Admin   │              │
│  │GW   │    │ Receiver│   │ API     │              │
│  └──┬──┘    └────┬────┘   └────┬────┘              │
│     │            │              │                    │
│  ┌──▼────────────▼──────────────▼────┐              │
│  │        ECS Fargate (Tasks)        │              │
│  │  ┌────────┐ ┌────────┐ ┌──────┐  │              │
│  │  │Epic    │ │Cerner  │ │Athena│  │              │
│  │  │Handler │ │Handler │ │Hndlr │  │              │
│  │  └────────┘ └────────┘ └──────┘  │              │
│  └───────────────────────────────────┘              │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │         RDS (PostgreSQL / Aurora)             │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │          ElastiCache (Redis)                  │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### On-Premise Deployment

For customers requiring on-premise deployment:
- Single Docker Compose stack per customer
- Local credential vault for security
- Local database for data residency
- Encrypted sync back to cloud for centralized ML model training
- VPN or private link for remote monitoring and support

---

## Security

### HIPAA Compliance

| Requirement | Implementation |
|---|---|
| Access control | Role-based access (RBAC), least privilege principle |
| Audit controls | All API calls logged: timestamp, user, action, resource, IP |
| Integrity controls | Checksums on all data transmissions, version tracking |
| Person/entity authentication | OAuth2, JWT, API keys, client certificates |
| Transmission security | TLS 1.2+ mandatory for all external communications |
| Encryption at rest | AES-256-GCM for stored credentials, AES-256 for database |
| BAA | Signed Business Associate Agreement with each customer |
| Breach notification | Automated alert on security events, 60-day notification window |

### Encryption at Rest

- Database: AES-256 encryption (PostgreSQL TDE or application-level encryption)
- Credential vault: Hashicorp Vault or AWS KMS for master key management
- File storage: Server-side encryption for cached data (S3 SSE-S3 or SSE-KMS)
- Key rotation: Automated every 90 days

### Encryption in Transit

- All external API calls: TLS 1.2 minimum, TLS 1.3 preferred
- Mutable cipher suite configuration (support: TLS_AES_256_GCM_SHA384)
- Certificate pinning for known EHR endpoints
- Mutual TLS (mTLS) for partner-to-partner connections

### Audit Logging

```python
@dataclass
class AuditLogEntry:
    timestamp: datetime
    tenant_id: str
    user_id: Optional[str]
    action: str  # "ehr_read", "ehr_write", "webhook_receive", "credential_rotate"
    resource_type: str  # "Patient", "Claim", "EOB"
    resource_id: str
    source: str  # "ehr:epic", "webhook:mirth", "api:internal"
    status: str  # "success", "failure", "rate_limited"
    response_time_ms: int
    ip_address: str
    correlation_id: str
    details: dict  # Error details, response metadata
```

Audit logs are:
- Written to an append-only log database
- Tamper-evident with hash chaining
- Retained for 6 years (HIPAA requirement)
- Searchable by tenant, date range, action, and resource
- Exportable for customer audits

---

## Monitoring

### Integration Health Dashboard

| Metric | Description | Alert Threshold | Severity |
|---|---|---|---|
| API Success Rate | % of successful API calls | < 95% over 5 min | Critical |
| API Latency P95 | 95th percentile response time | > 5 seconds | Warning |
| Rate Limit Hit Rate | % of calls rate-limited | > 5% over 15 min | Warning |
| Token Refresh Failures | Failed OAuth2 refreshes | > 0 in 10 min | Critical |
| Webhook Delivery Rate | % of webhooks successfully processed | < 99% | Critical |
| Data Sync Lag | Time since last successful sync | > 60 min | Warning |
| Circuit Breaker State | Number of open circuits | > 0 | Critical |
| Credential Expiry | Days until credential expiration | < 30 days | Warning |
| Error Rate by Code | 4xx/5xx by error type | Spike > 2x baseline | Warning |
| DB Connection Pool | % pool utilization | > 80% | Warning |

### Error Rate Tracking

```python
class ErrorTracker:
    EHR_ERROR_CODES = {
        "EPIC-AUTH-001": "Token expired",
        "EPIC-AUTH-002": "Invalid client assertion",
        "EPIC-RATE-001": "Rate limit exceeded",
        "CERNER-404-001": "Patient not found",
        "ATHENA-403-001": "Practice access denied",
        "ECW-429-001": "Rate limit exceeded (30/min)",
        "MIRTH-ERR-001": "HL7 parse error",
        "MIRTH-ERR-002": "HL7 ACK timeout",
    }

    def track_error(self, error: IntegrationError):
        code = self._resolve_error_code(error)
        self.metrics.increment(f"error.{code}")
        self.metrics.increment(f"error.ehr.{error.ehr_type}")
        if error.is_critical():
            self.alerter.alert_critical(error)
        self._log_error(error, code)

    def get_ehr_health_score(self, ehr_type: str) -> float:
        """Calculate health score (0.0 to 1.0) for an EHR."""
        recent = self._get_recent_errors(ehr_type, minutes=60)
        total_calls = self._get_total_calls(ehr_type, minutes=60)
        if total_calls == 0:
            return 1.0
        return 1.0 - (len(recent) / total_calls)
```

### Webhook Delivery Tracking

| Metric | Description |
|---|---|
| webhooks_received | Total webhooks received |
| webhooks_processed | Successfully processed |
| webhooks_failed | Processing failures |
| webhooks_retried | Retried due to failure |
| webhooks_dead_letter | Moved to dead letter queue |
| avg_processing_time_ms | Average processing time |
| webhook_latency_p99 | 99th percentile delivery latency |

---

## Agent Training: Q&A Pairs

**Q:** What is the purpose of the agnostic EHR integration layer?
**A:** The agnostic EHR integration layer provides a unified interface between Denials Doctor and any EHR system. It abstracts EHR-specific protocols (FHIR R4, HL7 v2, X12, proprietary REST APIs), authentication methods (OAuth2, API keys, certificates), and data models into a consistent internal representation. This means Denials Doctor's core denial analysis engine does not need to know which EHR it is connected to — it works with a standard Patient, Claim, and EOB object regardless of the source. Adding a new EHR integration requires only implementing a new adapter, not modifying core logic.

**Q:** How does the GenericFHIRAdapter work with EHR systems that only partially implement FHIR?
**A:** The GenericFHIRAdapter uses the FHIR CapabilityStatement ($metadata endpoint) to discover which resources, operations, and search parameters the EHR supports. If an EHR does not support ExplanationOfBenefit, the adapter falls back to ClaimResponse resources or, if neither is available, HL7 v2 DFT messages. It can also be configured with a priority list: "try FHIR EOB first, fall back to ClaimResponse, fall back to HL7 DFT." The adapter logs unsupported resources for transparency and alerts when critical data is unavailable.

**Q:** How does Denials Doctor handle OAuth2 token expiry across hundreds of EHR connections?
**A:** Denials Doctor uses a centralized token manager per EHR tenant that: (1) tracks token expiry with buffer time (refreshes 5 minutes before actual expiry); (2) uses a distributed lock (Redis) to prevent concurrent token refreshes for the same tenant; (3) stores refresh tokens in an encrypted vault with automatic rotation; (4) monitors refresh failure rates and alerts when a credential needs manual intervention; (5) implements backoff for persistent failures (e.g., revoked client credentials); (6) provides a dashboard showing token health for all tenants.

**Q:** What happens when an EHR API is down during a denial analysis?
**A:** The integration layer's circuit breaker pattern handles this: (1) after configurable failures (default: 5 consecutive errors), the circuit breaker opens and stops calling the EHR; (2) requests are queued in Redis for replay when the EHR recovers; (3) Denials Doctor uses its last-known-good cached data for analysis; (4) alerts are sent to the operations team; (5) the health checker polls the EHR's health endpoint every 30 seconds; (6) when the EHR responds successfully again, the circuit breaker transitions to half-open, tests with a limited number of requests, then fully closes. The queued requests are replayed in order.

**Q:** How does Denials Doctor map HL7 v2 data to its internal model?
**A:** HL7 v2 messages are parsed into structured segment/field/component objects. Dedicated mappers (HL7ADTMapper, HL7DFTMapper, HL7ORUMapper) extract data from specific segments and field positions and map them to Denials Doctor's internal Patient, Encounter, Claim, and Coverage models. The mapping is configurable per trading partner because HL7 implementations vary between EHRs (some put the MRN in PID-3.1, others in PID-2). The mapper uses a configuration file that defines the field-to-field mapping for each trading partner.

**Q:** How does the webhook receiver handle duplicate event delivery?
**A:** The webhook receiver uses idempotency keys. Each webhook payload must include an idempotency key (either in the header or embedded in the payload). The receiver checks if this key has already been processed by looking it up in Redis with a TTL of 24 hours. If it is a duplicate, the receiver returns 200 OK (so the sender doesn't retry) but does not process the event again. For HL7 v2, the MSH-10 (Message Control ID) serves as the idempotency key. For FHIR subscriptions, the subscription notification ID is used.

**Q:** What security measures are in place for the credential vault?
**A:** The credential vault uses: (1) AES-256-GCM encryption for all stored credentials; (2) Master key management via Hashicorp Vault or AWS KMS; (3) Key rotation every 90 days (automated); (4) Access control via IAM roles or Vault policies — each service has minimum necessary access; (5) Credentials never logged or exposed in error messages; (6) Audit trail for every credential access (read, write, delete, rotate); (7) Optional HSM integration for enterprise customers; (8) Automatic credential rotation notification to administrators 30 days before OAuth2 client secret expiry.

**Q:** How does the integration layer support rate limiting across different EHRs?
**A:** Each EHR adapter has a configurable rate limiter using a token bucket algorithm. The rate limits are set per EHR tenant based on the EHR's documented limits and the specific customer's negotiated rate. For example, an Epic customer with 100 req/sec uses a different limiter than a Cerner customer with 50 req/sec. The rate limiter also respects `Retry-After` headers sent by the EHR. When multiple tenants share the same EHR instance (rare but possible), a shared rate limiter prevents any single tenant from consuming all the capacity.

**Q:** What data is cached and for how long in the integration layer?
**A:** Caching policies: (1) Patient demographics — 1 hour (unchanged frequently); (2) Provider data — 24 hours (rarely changes); (3) Organization data — 24 hours; (4) Coverage data — 6 hours (may change with plan updates); (5) EOB data — 5 minutes (may update as claims are adjudicated); (6) Encounter data — 15 minutes (status may change); (7) Code value sets (CPT, ICD-10) — 7 days; (8) FHIR CapabilityStatement — 24 hours. Cache TTLs are configurable per tenant and can be reduced for near-real-time requirements.

**Q:** How does the integration layer handle X12 835 files from clearinghouses?
**A:** The X12 835 parser: (1) Receives the 835 file via SFTP, HTTPS upload, or AS2 connection; (2) Parses the ISA/GS/ST envelope to validate structure; (3) Extracts each CLP (claim payment) loop; (4) Within each CLP, extracts SVC (service line) and CAS (adjustment) segments; (5) Maps CAS group codes (CO/PR/OA) and CARC reason codes to internal denial categories; (6) Identifies denial lines (lines with CLP02=4 or CAS CO-* with $0 paid); (7) Creates Denial objects with CARC codes, amounts, and service dates; (8) Passes to Denials Doctor Core for analysis; (9) Logs all parsed data for audit.

**Q:** Can the integration layer handle multiple EHRs for a single customer?
**A:** Yes. A single customer (health system) may use different EHRs for different facilities or divisions. The integration layer supports this by: (1) registering each EHR instance as a separate integration source with its own adapter configuration; (2) routing data from each source to the correct patient/claim records using identifier cross-referencing; (3) maintaining a unified patient identity across EHR sources; (4) presenting a single view of all claims and denials regardless of source EHR; (5) handling different data refresh schedules per source. The core denial analysis system is completely EHR-agnostic at this point.

**Q:** What is the dead letter queue and when is it used?
**A:** The dead letter queue (DLQ) stores events that cannot be processed after exhausting all retry attempts. Events are moved to the DLQ when: (1) the event payload is malformed and cannot be parsed; (2) the EHR returns a persistent error (e.g., patient not found, credential revoked); (3) a required resource reference (patient, claim) does not exist in Denials Doctor; (4) business logic validation fails (e.g., impossible dates, negative charges). DLQ events are reviewed manually by operations, corrected if possible, and either replayed or archived with documentation.

**Q:** How is the integration layer configured for a new customer?
**A:** Configuration steps: (1) Determine EHR type and available interfaces (FHIR, HL7, clearinghouse); (2) Create a new tenant configuration in the integration layer; (3) Configure the EHR adapter (base URL, authentication type, credentials); (4) Set up the data sync schedule (initial bulk load + continuous sync); (5) Configure webhook endpoints if using HL7 or subscription-based integration; (6) Run interface tests with EHR sandbox or test environment; (7) Map any EHR-specific data fields or codes; (8) Set rate limits and circuit breaker thresholds; (9) Configure monitoring alerts; (10) Switch to production and validate data flow.

**Q:** What logging is required for HIPAA compliance in the integration layer?
**A:** HIPAA-required logging includes: (1) All access to PHI — every API call that reads or writes patient data, with timestamp, user/tenant, action, resource ID; (2) Authentication events — logins, token grants, token refreshes, failed authentication attempts; (3) Data modifications — creation, updates, and deletions of patient/claim/EOB records; (4) System access — who accessed the integration layer and when; (5) Configuration changes — changes to integration settings, credential updates; (6) Error events — security errors, access denied, validation failures. All logs are immutable (append-only), timestamped, and retained for 6 years.

**Q:** How does the integration layer handle EHR-specific data quality issues?
**A:** Data quality filtering and correction: (1) Missing required fields — if patient name or MRN is missing, the event is moved to DLQ; (2) Invalid codes — CPT or ICD-10 codes that don't match current code sets are flagged for review; (3) Duplicate claims — matched by claim ID and service date, duplicates are deduplicated; (4) Out-of-range dates — future dates or dates before patient birth are flagged; (5) Format inconsistencies — phone numbers, SSNs, and ZIP codes are normalized to standard formats; (6) Missing insurance — claims without attached coverage data are flagged for follow-up; (7) Mismatched provider NPI — validation against the provider registry.

**Q:** How does the integration layer support EHR credential rotation without downtime?
**A:** Credential rotation is handled through: (1) Dual credential support — maintain both old and new credentials simultaneously during rotation; (2) The token manager uses the old credentials until they fail, then automatically switches to the new credentials; (3) For OAuth2, the new client secret or certificate is pre-provisioned and stored in the vault; (4) The rotation is logged and auditable; (5) Alerts are sent on successful rotation and on any rotation failures; (6) For API key-based auth, a similar dual-key approach allows overlapping validity windows; (7) Automated rotation occurs 7 days before credential expiry to provide a safety margin.

**Q:** What is the data flow for an HL7 v2 ADT message through the integration layer?
**A:** Flow: (1) HL7 message arrives at the webhook receiver (from Mirth Connect or direct); (2) Receiver validates message structure (MSH header, segment ordering); (3) Message is parsed into segment/field objects; (4) Message type is determined (MSH-9 identifies ADT^A01, A03, etc.); (5) Specific mapper (e.g., HL7ADTMapper) extracts data fields; (6) Mapped data is validated (required fields present, valid codes); (7) Internal event is created (e.g., "admission" event for A01); (8) Event is queued in Redis; (9) Event processor picks up the event; (10) Processor creates/updates the Encounter record; (11) If admission, it checks patient eligibility; (12) If discharge, it triggers charge review; (13) Events are logged for audit.

**Q:** How does the integration layer handle different identifier formats across EHRs?
**A:** The integration layer maintains an identifier normalization engine: (1) All identifiers are stored with a type (MRN, SSN, DL, account number, visit number) and system URI; (2) EHR-specific formats are normalized: e.g., "123-45-6789" and "123456789" both become standardized SSN format; (3) MRNs are stored as-is (they are organization-specific); (4) The system maintains a cross-reference table mapping EHR IDs to internal patient IDs; (5) Patient matching uses multiple identifiers (MRN + DOB + name) for verification; (6) Merge events (ADT^A40) update the cross-reference table; (7) Duplicate patient detection uses probabilistic matching on demographics.

**Q:** Can the integration layer process data in batches for historical denial analysis?
**A:** Yes. For historical analysis: (1) Bulk export ($export for FHIR, batch HL7 replay, or SFTP file ingestion) pulls historical data; (2) The integration layer processes data in parallel with configurable batch sizes (default 1000 records/batch); (3) Rate limiting still applies but uses accumulated burst capacity; (4) Progress is tracked per batch with checkpoint/resume for large datasets; (5) Deduplication prevents double-processing of already-seen records; (6) Processing occurs in a dedicated historical analysis pipeline with lower priority than real-time processing; (7) Results are stored in an analytics database optimized for historical query patterns.

---

## Summary

The Agnostic EHR Integration Layer is Denials Doctor's architectural foundation for multi-EHR support. It consists of pluggable EHR adapters (Epic, Cerner, athenahealth, eClinicalWorks, generic FHIR, HL7 v2 via Mirth, clearinghouse), an API gateway for request routing, a webhook receiver for event-driven data, and a connection manager handling authentication, rate limiting, retry, and circuit breaking.

The data mapping layer provides consistent translation between EHR-specific formats (FHIR, HL7 v2, X12) and Denials Doctor's internal model. Security encompasses HIPAA-compliant encryption, auditing, and credential management.

Deployment supports cloud-hosted multi-tenant (SaaS), on-premise Docker, and hybrid models. Monitoring covers integration health, error rates, data sync lag, and credential expiry across all connected EHRs.

This architecture enables Denials Doctor to add EHR integrations without modifying core denial analysis logic, scale to support hundreds of EHR customers, and handle the diversity of protocols, authentication methods, and data models across the US healthcare EHR landscape.