# Payer IDs

## Overview

Payer IDs are unique identifiers assigned to healthcare payers for electronic claim submission and related transactions. They are essential for routing claims to the correct payer through clearinghouses or direct EDI connections. Different payers use different ID systems, and the correct ID must be used for each claim to ensure proper routing.

Payer IDs come from several sources:
- **CMS-assigned IDs** for Medicare Administrative Contractors (MACs)
- **Clearinghouse-assigned IDs** for each payer in their network
- **Payer-assigned IDs** for direct submission connections
- **State-assigned IDs** for Medicaid programs

---

## 1. Medicare Administrative Contractors (MACs)

Medicare claims are processed by Medicare Administrative Contractors (MACs). Each MAC handles claims for specific states (jurisdictions). The correct MAC payer ID must be used based on the state where the service was performed.

### MAC Jurisdictions

| Jurisdiction | MAC Name | States/Territories | Part A | Part B |
|-------------|----------|-------------------|--------|--------|
| **J5** | WPS | Iowa, Kansas, Missouri, Nebraska | Y | Y |
| **J6** | NGS | Illinois, Minnesota, Wisconsin (Part A) | Y | N |
| **J8** | Palmetto GBA | Indiana, Michigan (Part B) | N | Y |
| **J9** | NGS | Connecticut, Maine, Massachusetts, New Hampshire, Rhode Island, Vermont | Y | Y |
| **J10** | CGS | Kentucky, Ohio (Part B) | N | Y |
| **J11** | NGS | Alabama, Arkansas, Georgia, Louisiana, Mississippi, New Mexico, North Carolina, Oklahoma, South Carolina, Tennessee, Texas, Virginia | Y | Y |
| **J12** | Novitas | Arkansas, Colorado, Delaware, District of Columbia, Louisiana, Maryland, New Jersey, New Mexico, Oklahoma, Pennsylvania, Texas, Virginia | Y | Y |
| **J13** | Noridian | Arizona, California (Part A), Hawaii, Nevada, Northern Mariana Islands, American Samoa, Guam | Y | N |
| **J14** | Palmetto GBA | Alabama, Georgia, Mississippi, Tennessee, North Carolina, South Carolina, Virginia, West Virginia | Y | Y |
| **J15** | CGS | Kentucky, Ohio (Part A) | Y | N |
| **JE** | Noridian | California (Part B), Hawaii, Nevada, American Samoa, Guam, Northern Mariana Islands | N | Y |
| **JF** | Noridian | Alaska, Arizona, Idaho, Montana, North Dakota, Oregon, South Dakota, Washington, Wyoming | Y | Y |
| **JH** | Novitas | Arkansas, Colorado, Delaware, District of Columbia, Louisiana, Maryland, New Jersey, New Mexico, Oklahoma, Pennsylvania, Texas, Virginia, West Virginia | Y | Y |
| **JJ** | NGS | Alabama, Arkansas, Colorado, Georgia, Louisiana, Mississippi, New Mexico, North Carolina, Oklahoma, South Carolina, Tennessee, Texas, Virginia | Y | Y |
| **JK** | WPS | Illinois (Part B), Indiana (Part A), Kansas (Part B), Michigan (Part A), Minnesota (Part B), Missouri (Part B), Nebraska (Part B), Wisconsin (Part B) | Y | Y |
| **JL** | First Coast | Florida, Puerto Rico, U.S. Virgin Islands (Part B) | N | Y |

### Detailed MAC Information

#### Noridian Healthcare Solutions

| Jurisdiction | Part A/B | States |
|-------------|----------|--------|
| **J13** | Part A | AZ, CA (Part A only), HI, NV, American Samoa, Guam, N. Mariana Islands |
| **J15** | Part B | CA (Part B only at time), HI, NV (now moved to JE/JF) |
| **JE** | Part B | CA, HI, NV, American Samoa, Guam, N. Mariana Islands |
| **JF** | Part A & B | AK, AZ, ID, MT, ND, OR, SD, WA, WY |

Noridian payer IDs for claim submission:
- Part A (Noridian): 13101 (Jurisdiction J13)
- Part B (Noridian): 13101 (Jurisdiction JE) or 13201 (Jurisdiction JF)
- DME MAC (Noridian): 17001 (DME Jurisdiction D)

#### Palmetto GBA

| Jurisdiction | Part A/B | States |
|-------------|----------|--------|
| **J8** | Part B | IN, MI (Part B) |
| **J11** | Part A & B | Multi-state (see above) |
| **J14** | Part A & B | AL, GA, MS, TN, NC, SC, VA, WV |

Palmetto GBA payer IDs for claim submission:
- Part A (Palmetto): 14001
- Part B (Palmetto): 13101
- Railroad Retirement Medicare: 17001

#### NGS (National Government Services)

| Jurisdiction | Part A/B | States |
|-------------|----------|--------|
| **J6** | Part A | IL, MN, WI (Part A) |
| **J9** | Part A & B | CT, ME, MA, NH, RI, VT |
| **J11** | Part A & B | Multi-state |
| **JJ** | Part A & B | Multi-state |

NGS payer IDs for claim submission:
- Part A (NGS): 16101
- Part B (NGS): 13101

#### WPS (Wisconsin Physician Services)

| Jurisdiction | Part A/B | States |
|-------------|----------|--------|
| **J5** | Part A & B | IA, KS, MO, NE |
| **JK** | Part A & B | IL (Part B), IN (Part A), KS (Part B), MI (Part A), MN (Part B), MO (Part B), NE (Part B), WI (Part B) |

WPS payer IDs for claim submission:
- Part A (WPS): 15001
- Part B (WPS): 13101

#### First Coast Service Options

| Jurisdiction | Part A/B | States |
|-------------|----------|--------|
| **JL** | Part B | FL, PR, USVI (Part B) |

First Coast payer IDs for claim submission:
- Part B (First Coast): 13101

#### CGS (Cahaba Government Services)

| Jurisdiction | Part A/B | States |
|-------------|----------|--------|
| **J10** | Part B | KY, OH (Part B) |
| **J15** | Part A | KY, OH (Part A) |

CGS payer IDs for claim submission:
- Part A (CGS): 15101
- Part B (CGS): 13101

#### Novitas Solutions

| Jurisdiction | Part A/B | States |
|-------------|----------|--------|
| **J12** | Part A & B | Multi-state (AR, CO, DE, DC, LA, MD, NJ, NM, OK, PA, TX, VA) |
| **JH** | Part A & B | Multi-state (same as J12 for different service types) |

Novitas payer IDs for claim submission:
- Part A (Novitas): 12101
- Part B (Novitas): 13201

---

## 2. Medicare Part A vs Part B

### Key Differences

| Aspect | Part A | Part B |
|--------|--------|--------|
| **Services Covered** | Inpatient hospital, SNF, hospice, home health | Physician services, outpatient, DME, tests |
| **Claim Form** | UB-04 (CMS-1450) | CMS-1500 |
| **837 Version** | 837I (Institutional) | 837P (Professional) |
| **MAC Assignment** | May have different MAC than Part B in same state | Separate MAC or same |
| **Payer ID** | Different from Part B | Different from Part A |

### Examples of Different MACs for Part A and Part B in the Same State

| State | Part A MAC | Part B MAC |
|-------|------------|------------|
| Illinois | NGS (J6) | WPS (JK) |
| Kentucky | CGS (J15) | CGS (J10) |
| Ohio | CGS (J15) | CGS (J10) |
| Indiana | WPS (JK) | Palmetto GBA (J8) |
| Michigan | WPS (JK) | Palmetto GBA (J8) |

---

## 3. Commercial Payer Electronic IDs

### Major Commercial Payer IDs (Common Clearinghouse Values)

**Note**: Payer IDs vary by clearinghouse. These are common values used by major clearinghouses but should be verified with the specific clearinghouse being used.

| Payer Name | Common Electronic Payer ID |
|------------|---------------------------|
| Aetna (PPO/HMO) | 60054 |
| Aetna (Medicare) | 60054 (Medicare-specific suffix) |
| Anthem Blue Cross Blue Shield (varies by state) | 52138 (varies by state) |
| Blue Cross Blue Shield of Alabama | 52031 |
| Blue Cross Blue Shield of Arizona | 52135 |
| Blue Cross Blue Shield of California | 52136 |
| Blue Cross Blue Shield of Colorado | 52151 |
| Blue Cross Blue Shield of Florida | 52031 |
| Blue Cross Blue Shield of Georgia | 52031 |
| Blue Cross Blue Shield of Illinois | 52138 |
| Blue Cross Blue Shield of Massachusetts | 52074 |
| Blue Cross Blue Shield of Michigan | 52042 |
| Blue Cross Blue Shield of North Carolina | 52147 |
| Blue Cross Blue Shield of Texas | 52031 |
| Cigna | 62308 |
| Cigna (Behavioral) | 62308 |
| Cigna (Medicare Advantage) | 62308 |
| Cigna (LocalPlus) | 62308 |
| Humana (Commercial) | 61023 |
| Humana (Medicare Advantage) | 61023 |
| Humana (Medicaid) | Varies by state |
| UnitedHealthcare (Commercial) | 87726 |
| UnitedHealthcare (Medicare Advantage) | 87726 |
| UnitedHealthcare (Medicaid) | Varies by state |
| UnitedHealthcare (Community Plan) | Varies by state |
| Tricare (East) | 60001 |
| Tricare (West) | 60002 |
| Tricare for Life | 60003 |
| VA (Veterans Affairs) | 17003 |
| Workers' Compensation (varies by state) | Varies |

### Important Note on Payer IDs

Payer IDs are **not standardized across clearinghouses**. The same payer may have a different electronic payer ID in:
- Change Healthcare: 87726 for UnitedHealthcare
- Waystar: 87726 for UnitedHealthcare (same for some, different for others)
- Availity: 87726 for UnitedHealthcare
- Office Ally: 87726 for UnitedHealthcare

**Always verify the payer ID with your specific clearinghouse.** The clearinghouse provides a payer ID lookup tool or list.

---

## 4. State Medicaid Payer IDs

### Medicaid Billing by State

Each state administers its own Medicaid program with unique payer IDs and billing requirements.

| State | Medicaid Payer ID (Common) | Notes |
|-------|---------------------------|-------|
| Alabama | 51011 | Alabama Medicaid |
| Alaska | 51030 | Alaska Medicaid |
| Arizona | 51012 | AHCCCS (Arizona Health Care Cost Containment System) |
| Arkansas | 51013 | Arkansas Medicaid |
| California | 51014 | Medi-Cal |
| Colorado | 51015 | Colorado Medicaid |
| Connecticut | 51016 | Connecticut Medicaid |
| Delaware | 51017 | Delaware Medicaid |
| District of Columbia | 51018 | DC Medicaid |
| Florida | 51019 | Florida Medicaid |
| Georgia | 51020 | Georgia Medicaid |
| Hawaii | 51021 | Hawaii Medicaid (Med-QUEST) |
| Idaho | 51023 | Idaho Medicaid |
| Illinois | 51024 | Illinois Medicaid |
| Indiana | 51025 | Indiana Medicaid |
| Iowa | 51026 | Iowa Medicaid |
| Kansas | 51027 | Kansas Medicaid |
| Kentucky | 51028 | Kentucky Medicaid |
| Louisiana | 51029 | Louisiana Medicaid |
| Maine | 51010 | MaineCare |
| Maryland | 51030 | Maryland Medicaid |
| Massachusetts | 51031 | MassHealth |
| Michigan | 51032 | Michigan Medicaid |
| Minnesota | 51033 | Minnesota Medicaid |
| Mississippi | 51034 | Mississippi Medicaid |
| Missouri | 51035 | Missouri Medicaid |
| Montana | 51036 | Montana Medicaid |
| Nebraska | 51037 | Nebraska Medicaid |
| Nevada | 51038 | Nevada Medicaid |
| New Hampshire | 51040 | New Hampshire Medicaid |
| New Jersey | 51041 | New Jersey Medicaid |
| New Mexico | 51042 | New Mexico Medicaid |
| New York | 51043 | New York Medicaid (eMedNY) |
| North Carolina | 51044 | North Carolina Medicaid |
| North Dakota | 51046 | North Dakota Medicaid |
| Ohio | 51047 | Ohio Medicaid |
| Oklahoma | 51048 | Oklahoma Medicaid |
| Oregon | 51049 | Oregon Health Plan |
| Pennsylvania | 51050 | Pennsylvania Medicaid |
| Rhode Island | 51051 | Rhode Island Medicaid |
| South Carolina | 51052 | South Carolina Medicaid |
| South Dakota | 51053 | South Dakota Medicaid |
| Tennessee | 51054 | TennCare |
| Texas | 51055 | Texas Medicaid / TMHP |
| Utah | 51056 | Utah Medicaid |
| Vermont | 51057 | Vermont Medicaid |
| Virginia | 51058 | Virginia Medicaid |
| Washington | 51059 | Washington Medicaid |
| West Virginia | 51060 | West Virginia Medicaid |
| Wisconsin | 51061 | Wisconsin Medicaid (ForwardHealth) |
| Wyoming | 51063 | Wyoming Medicaid |
| Puerto Rico | 51066 | Puerto Rico Medicaid |

### State Medicaid Billing Characteristics

| Aspect | Detail |
|--------|--------|
| **Claim Format** | Typically 837P or 837I, state dependent |
| **Payer ID Source** | Clearinghouse-assigned or state-assigned |
| **NPI Requirements** | All states accept NPI, some require legacy IDs |
| **Taxonomy Requirements** | Required by most states |
| **Modifier Requirements** | Vary by state |
| **Timely Filing** | Varies by state (typically 90-365 days) |
| **COB Handling** | Medicaid is typically payer of last resort |

### Managed Medicaid

Many states have transitioned to managed Medicaid where private insurers manage Medicaid benefits. In these states, the payer ID is the managed care organization's ID, not the state Medicaid ID.

| State | Managed Care Example | Payer ID |
|-------|---------------------|----------|
| Florida | Florida Healthy Kids | Use MCO's payer ID |
| Texas | STAR, STAR+PLUS | Use MCO's payer ID (e.g., UnitedHealthcare Community Plan) |
| California | Medi-Cal Managed Care | Use MCO's payer ID (e.g., Anthem Blue Cross Medi-Cal) |
| New York | NYS Medicaid Managed Care | Use MCO's payer ID |

---

## 5. Payer ID Lookup Methods

### Clearinghouse Payer ID Lookup

Most clearinghouses provide a payer ID lookup tool:

1. Log into the clearinghouse portal.
2. Navigate to the "Payer ID Lookup" or "Payer Search" section.
3. Enter the payer name, state, or plan type.
4. Select the correct payer from the search results.
5. Note the payer ID and any special routing requirements.

### Medicare Payer ID Lookup

For Medicare MAC payer IDs:

1. Visit the CMS MAC Jurisdiction page.
2. Find the MAC for the provider's state.
3. Contact the MAC for payer ID and trading partner information.
4. Verify payer ID with the clearinghouse.

### Direct Submission Payer IDs

For direct submission, the payer provides:
- EDI submission ID
- Trading partner agreement
- Payer-specific connection details
- Acknowledgment configuration

---

## 6. Agent Training: Q&A Pairs for Payer IDs

**Q: What is the difference between a Medicare Part A and Part B MAC?**

**A:** A Medicare Part A MAC processes claims for institutional services such as inpatient hospital stays, skilled nursing facility care, hospice care, and home health services. A Medicare Part B MAC processes claims for professional services such as physician visits, outpatient services, diagnostic tests, and durable medical equipment. The same MAC may handle both Part A and Part B in some states, while different MACs handle them in other states. For example, in Illinois, NGS handles Part A and WPS handles Part B. The provider must use the correct MAC and payer ID based on the claim type.

---

**Q: How does a provider determine which MAC processes their claims?**

**A:** A provider determines which MAC processes their claims based on the state where the service was performed and the type of service (Part A vs Part B). CMS divides the United States into MAC jurisdictions. The provider can check the CMS MAC Jurisdiction lookup tool on the cms.gov website, or contact their current MAC for verification. The MAC jurisdiction is determined by the physical location where the service was rendered, not the provider's home address or the patient's residence.

---

**Q: What is a clearinghouse payer ID and why is it important?**

**A:** A clearinghouse payer ID is a unique identifier assigned by a specific clearinghouse to each payer in its network. It is used to route claims to the correct payer during electronic submission. It is important because submitting a claim with the wrong payer ID results in the claim being routed to the wrong payer, resulting in rejection or denial. Payer IDs are not standardized across clearinghouses -- the same payer may have different IDs in Change Healthcare, Waystar, Availity, and Office Ally. Providers must use the payer ID assigned by their specific clearinghouse.

---

**Q: What is the Medicare payer ID for Part B claims in Florida?**

**A:** The Medicare Part B payer ID for claims submitted in Florida (Jurisdiction JL) is typically assigned by the clearinghouse as related to First Coast Service Options (the MAC for Florida Part B). The MAC number for First Coast is typically mapped to clearinghouse ID 13101 for Part B. However, the exact payer ID depends on the clearinghouse being used. The provider should verify the payer ID with their clearinghouse's payer ID lookup tool. First Coast Service Options is the MAC for Part B in Florida, Puerto Rico, and the U.S. Virgin Islands.

---

**Q: What is the difference between a MAC payer ID and a clearinghouse payer ID?**

**A:** A MAC payer ID (also called a Medicare CCN or Contract Number) is the CMS-assigned identifier for the Medicare Administrative Contractor. For example, Noridian has contract number 13101. A clearinghouse payer ID is the identifier assigned by a specific clearinghouse to that MAC for routing purposes. While they may be the same number in some clearinghouses, the clearinghouse may use a different internal ID. The provider should use the clearinghouse's payer ID, not the raw MAC contract number, unless they are submitting directly to the MAC.

---

**Q: How does a provider handle claims for a patient with Medicare and a commercial secondary insurance?**

**A:** When a patient has Medicare as primary and a commercial secondary insurance, the provider must first submit the claim to Medicare using the Medicare MAC payer ID (Part A or Part B depending on the service). After Medicare processes the claim and issues a payment/remittance, the provider then submits the claim to the commercial secondary payer using that payer's ID. The secondary claim must include the Medicare payment information. The clearinghouse can help route both claims if configured correctly. The provider needs both the Medicare payer ID and the commercial payer ID in their system.

---

**Q: What is the correct payer ID for Cigna claims?**

**A:** The correct payer ID for Cigna claims depends on the clearinghouse being used. In Change Healthcare and many other clearinghouses, Cigna's electronic payer ID is 62308. However, the provider should verify this with their specific clearinghouse. Cigna also has different products (Cigna PPO, Cigna HMO, Cigna Medicare Advantage, Cigna Behavioral Health) that may use the same payer ID or different IDs. The provider should check the specific product and clearinghouse to ensure the correct ID is used.

---

**Q: How does a provider submit claims to Medicaid in a managed care state?**

**A:** In a state where Medicaid is managed by private health plans (such as Texas STAR, California Medi-Cal Managed Care, or Florida Healthy Kids), the provider submits claims to the managed care organization (MCO), not to the state Medicaid agency. The payer ID is the MCO's payer ID, not the state Medicaid ID. For example, a provider in Texas seeing a patient enrolled in UnitedHealthcare Community Plan (STAR) would use the UnitedHealthcare Community Plan payer ID, not the Texas Medicaid payer ID (51055). The provider must enroll with each MCO individually.

---

**Q: What happens if a claim is submitted with the wrong payer ID?**

**A:** If a claim is submitted with the wrong payer ID, one of the following occurs: the claim is routed to the wrong payer, which will reject it because the patient is not a member; the claim is rejected by the clearinghouse because the payer ID is not recognized; or the claim is sent to the correct payer but the wrong plan type is used, resulting in incorrect adjudication. In all cases, the claim is delayed, requiring correction and resubmission. This can result in timely filing issues if not caught early. Most clearinghouses validate payer IDs against provider routing before transmission.

---

**Q: What is the Noridian Medicare Part A payer ID for California?**

**A:** Noridian Healthcare Solutions is the Medicare Part A MAC for California (Jurisdiction J13). The MAC contract number is typically referenced as 13101, but the specific payer ID for electronic claim submission depends on the clearinghouse. For Noridian Part A in California, clearinghouses commonly use payer ID 13101 or a clearinghouse-specific alternate ID. The provider should confirm the ID with their clearinghouse. California Part A and Part B are handled by different Noridian jurisdictions (J13 for Part A, JE for Part B).

---

**Q: How are UnitedHealthcare payer IDs handled across different product lines?**

**A:** UnitedHealthcare uses different payer IDs (or the same ID with different plan codes) for different products. Common configurations include: UnitedHealthcare Commercial (PPO/HMO) -- clearinghouse ID 87726; UnitedHealthcare Medicare Advantage -- also often 87726 but may require a specific plan code or suffix; UnitedHealthcare Community Plan (Medicaid) -- varies by state; UnitedHealthcare Individual Marketplace -- may be 87726 or a different ID. The provider must check the specific plan when selecting the payer ID. Some clearinghouses provide plan-level lookup to identify the correct ID.

---

**Q: Can a provider use the same Medicare payer ID for all states?**

**A:** No. Each MAC has its own jurisdiction. A provider in Texas (Novitas jurisdiction) cannot use the Medicare payer ID for a provider in California (Noridian jurisdiction). The claim must be routed to the MAC that covers the state where the service was performed. Even within the same MAC, different jurisdictions may have different payer IDs. For example, Noridian J13 (Part A in California) and Noridian JF (Part A & B in multiple western states) have different payer routing even though they are the same MAC entity.

---

**Q: What is a "payer ID look-up" tool in a clearinghouse?**

**A:** A payer ID look-up tool is a searchable database within a clearinghouse portal that allows the provider to find the correct electronic payer ID for any payer in the clearinghouse's network. The provider searches by payer name, state, plan type, or product. The tool returns the payer ID and may also show: the payer's name and address, the routing instructions, whether the payer accepts electronic claims, the payer's EDI requirements, and special notes or requirements. Providers should use this tool to verify payer IDs before configuring their billing systems.

---

**Q: What is the First Coast Service Options payer ID for Part B?**

**A:** First Coast Service Options is the Medicare Part B MAC for Florida (Jurisdiction JL). The clearinghouse payer ID for First Coast Part B is typically 13101 (the same base identifier used by multiple MACs for Part B). The specific routing depends on the clearinghouse's configuration for the JL jurisdiction. The provider should confirm the ID with their clearinghouse and should also have the correct MAC jurisdiction code (JL) configured. First Coast only handles Part B; Part A in Florida is handled by a different MAC.

---

**Q: How does a provider handle payer IDs for Tricare?**

**A:** Tricare claims are routed by region: Tricare East (Humana Military) uses payer ID 60001 in most clearinghouses; Tricare West (Health Net Federal Services) uses 60002; and Tricare for Life (for Tricare beneficiaries with Medicare) uses 60003. The provider must use the correct regional payer ID based on the beneficiary's home address or duty station. Tricare also requires specific data elements such as the sponsor's SSN, branch of service, and duty status. The provider should verify payer IDs with their clearinghouse and check the Tricare contractor for the region.

---

**Q: What is the difference between a MAC number and a clearinghouse payer ID?**

**A:** A MAC number (Medicare Administrative Contractor number) is the CMS-assigned identifier for the MAC entity itself. For example, Noridian's MAC numbers include 13101 and 13201. A clearinghouse payer ID is the identifier used by a specific clearinghouse to route claims to that MAC. In some cases, the clearinghouse payer ID matches the MAC number, but clearinghouses may use different internal identifiers. The provider should always use the clearinghouse's payer ID, not the raw MAC number, unless submitting directly to the MAC.

---

**Q: How are payer IDs configured in a practice management system?**

**A:** Payer IDs are configured in a practice management system in the payer setup or fee schedule configuration area. The provider creates a payer record with the payer's name, address, and billing rules, and enters the electronic payer ID associated with that payer in the clearinghouse's system. The provider must: obtain the payer ID from the clearinghouse; enter the ID in the payer record; configure the claim submission method (electronic or paper); set up claim format requirements (837P or 837I); configure claim routing rules; and test the configuration with the clearinghouse to confirm the claim is routed correctly.

---

**Q: What is the CGS payer ID for Part B claims?**

**A:** CGS (Cahaba Government Services) is the Medicare Part B MAC for Kentucky and Ohio (Jurisdiction J10). The clearinghouse payer ID for CGS Part B is typically 13101 in many clearinghouses, but the provider should verify with their specific clearinghouse. CGS also handles Part A for Kentucky and Ohio (Jurisdiction J15) with a different payer ID. Providers in Kentucky and Ohio should ensure they use the correct CGS payer ID based on whether the claim is Part A or Part B.

---

**Q: How does a provider find the correct payer ID for a new payer?**

**A:** To find the correct payer ID for a new payer, the provider should: log into their clearinghouse portal; go to the payer ID lookup tool; search for the payer by name, state, and product type; note the payer ID displayed; and verify that the ID is correct for the specific product (HMO vs PPO, Medicare Advantage vs commercial). If the payer is not in the clearinghouse's network, the provider may need to submit claims via paper or use a different clearinghouse. The clearinghouse's support team can also help identify the correct payer ID.

---

**Q: What is the WPS payer ID for Part A claims?**

**A:** WPS (Wisconsin Physician Services) handles Medicare Part A in several states including Iowa, Kansas, Missouri, and Nebraska (Jurisdiction J5). The clearinghouse payer ID for WPS Part A is typically 15001. WPS also handles Part B (Jurisdiction JK) in multiple states. The provider should verify the payer ID with their clearinghouse and ensure they are using the correct ID for the claim type (Part A vs Part B) and jurisdiction. WPS Part A uses a different ID than WPS Part B.

---

**Q: How are payer IDs for Blue Cross Blue Shield plans handled?**

**A:** Blue Cross Blue Shield plans are state-specific. Each BCBS plan has its own payer ID. For example, BCBS of Alabama is 52031, BCBS of Illinois is 52138, BCBS of Texas is 52031, and BCBS of California is 52136. In some states where one BCBS plan operates multiple products, the same payer ID may be used for all products, or different IDs may exist for PPO vs HMO vs Medicare Advantage. Providers should use the BCBS payer ID specific to the state where the patient is enrolled, not necessarily where the service is performed (for PPO plans).

---

**Q: What is the Novitas Solutions payer ID for Part B claims?**

**A:** Novitas Solutions is the Medicare Part B MAC for Jurisdiction JH (which covers Arkansas, Colorado, Delaware, District of Columbia, Louisiana, Maryland, New Jersey, New Mexico, Oklahoma, Pennsylvania, Texas, Virginia, and West Virginia). The clearinghouse payer ID for Novitas Part B is typically 13201. Novitas Part A uses a different payer ID (typically 12101). Providers in Novitas jurisdictions should verify the correct ID with their clearinghouse based on the claim type.