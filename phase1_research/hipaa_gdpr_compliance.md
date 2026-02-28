# HIPAA/GDPR Compliance Architecture - Phase 1

**Date:** February 28, 2026  
**Status:** Phase 1 Research & Planning

---

## Executive Summary

This document outlines the data handling architecture for Vital Lens AI to comply with:
- **HIPAA (Health Insurance Portability and Accountability Act)** - US healthcare data protection
- **GDPR (General Data Protection Regulation)** - EU/EEA personal data protection
- **CCPA (California Consumer Privacy Act)** - US state privacy (secondary)

**Key Principle:** Even though the app is positioned as "wellness only" (not medical diagnosis), biometric data (heart rate, facial images) requires strict privacy controls.

---

## Part 1: HIPAA Compliance Framework

### 1.1 HIPAA Applicability Assessment

**Is Vital Lens AI a HIPAA Covered Entity?**

| Criterion | Vital Lens AI Status |
|-----------|-------------------|
| Provides healthcare services | ❌ No (wellness app, not diagnostic) |
| Transmits health information electronically | ⚠️ Conditional (depends on implementation) |
| Is a Business Associate | ❓ If linked to healthcare provider |
| Handles Protected Health Information (PHI) | ✅ Yes (biometric vitals data) |

**Conclusion:** 
- **Direct HIPAA coverage:** Likely NOT (not healthcare provider)
- **Business Associate obligations:** YES if partnering with providers
- **Best practice:** Implement HIPAA-level security regardless (liability mitigation)

### 1.2 Key HIPAA Requirements for Vital Lens AI

#### **Protected Health Information (PHI) Definition**

**Vital Lens AI PHI Includes:**
- ✅ Heart rate measurements (derived from video)
- ✅ Facial images (biometric identifier)
- ✅ Timestamps of health measurements
- ✅ SpO2 estimates (if collected)
- ✅ Linked user demographic data (age, sex)

**Non-PHI (unless combined with above):**
- ❌ De-identified aggregate statistics
- ❌ General app usage metrics (without timestamps)

---

#### **Administrative Safeguards**

**1. Workforce Security:**
- Designated Security Officer responsible for compliance
- Staff training on privacy/security (annual requirement)
- Role-based access controls (staff with data access)
- Termination procedures (revoke access immediately)

**2. Information Access Management:**
- Principle of least privilege (staff sees only necessary data)
- Access logs for all PHI interactions (audit trail)
- Documented authorization for data access

**3. Workforce Security Training:**
- Initial onboarding: HIPAA/privacy fundamentals
- Annual refresher training for all staff
- Documentation of training completion
- Specialized training for data handlers

**4. Security Awareness Program:**
- Password policy enforcement
- Secure workstation procedures
- Incident response protocols
- Contingency planning (backup/disaster recovery)

---

#### **Physical Safeguards**

**Facility Access Controls:**
- Secure data centers (restricted physical access)
- Badge/key card access to server rooms
- Security cameras in restricted areas
- Visitor logs for data center access

**Workstation Use Policy:**
- Approved workstations only for PHI access
- Screen privacy (desk positioning away from public)
- Automatic screen locks (< 5 min inactivity)
- Clean desk policy (no printed PHI left visible)

**Workstation Security:**
- Endpoint security software (antivirus, anti-malware)
- Firewall enabled
- USB port restrictions (prevent unauthorized data transfer)
- Locked machines (physical security)

---

#### **Technical Safeguards (Critical)**

**1. Access Controls (Authentication & Authorization)**

**Encryption in Transit:**
```
Protocol: TLS 1.2 or higher
Certificate: Valid, signed by trusted CA
Cipher Suite: AES-256 minimum
Use Cases:
  - API endpoints: HTTPS only
  - Database connections: TLS encryption
  - Mobile-to-backend: TLS 1.2+
  - Email: SMTPS/STARTTLS
```

**Encryption at Rest:**
```
Database Encryption:
  - AES-256 (industry standard)
  - Hardware security module (HSM) for key management
  - Separate encryption keys per user (recommended)

File Storage:
  - Cloud storage: Enable default encryption (AWS KMS, GCP Cloud KMS)
  - Local device: iOS Keychain, Android Keystore

Backups:
  - Encrypted before transmission
  - Encrypted in backup storage
  - Separate encryption key from primary database
```

**2. Audit Controls**

**Logging Requirements:**
- All PHI access events logged (user, timestamp, action, IP address)
- Failed authentication attempts logged
- Configuration changes logged
- Data modification/deletion logged
- Log retention: Minimum 6 years (HIPAA standard, often 7)

**Log Security:**
- Logs stored separately from application data
- Write-once storage (prevent tampering)
- Automated log analysis for anomalies
- Regular review (at least monthly)

**Example Log Entry:**
```
2026-02-28 14:35:22 | User: user@email.com | IP: 203.0.113.42 | Action: VIEW_HR_DATA | 
Resource: user_vitals_id_123 | Result: SUCCESS | Duration: 0.3s
```

**3. Data Integrity Controls**

**Checksums & Hashing:**
- MD5/SHA-1 NOT sufficient (cryptographically broken)
- Use SHA-256 or stronger for integrity verification
- HMAC for authenticated checksums

**Digital Signatures:**
- For critical operations (delete vitals history, export data)
- User must authenticate with strong password/biometric
- Timestamp included in signature

**Backup Integrity:**
- Regular restore testing (quarterly)
- Verify backup checksums after creation
- Test disaster recovery procedures

---

#### **Audit & Accountability Safeguards**

**Audit Trail Requirements:**
- Immutable record of all PHI access
- Includes: who, what, when, where, why, with what outcome
- Accessible for compliance reviews
- Retention: 6-7 years minimum

**Compliance Review Schedule:**
- Annual security risk assessment
- Quarterly audit log review
- Incident investigation procedures documented
- Remediation tracking

---

### 1.3 HIPAA Breach Notification Requirements

**Breach Definition:**
- Unauthorized access, use, or disclosure of PHI
- Presumed breach unless mitigated

**Notification Timelines:**
| Affected Party | Timeline | Method |
|----------------|----------|--------|
| Individual users | Within 60 calendar days | Email, postal mail, or phone |
| Media (if 500+ affected) | Without unreasonable delay | Press release |
| HHS (US Dept Health & Services) | Within 60 days | breach notification system.hhs.gov |

**Notification Contents:**
- Date of breach and discovery
- Description of information involved
- Steps user should take
- Company's mitigation steps
- Contact info for questions

**Example Breach Scenario:**
```
Database compromised on Feb 28, 2026
Discovered: March 2, 2026 (4-day delay)
Affected: 5,000 users
Notification deadline: April 1, 2026
Content: Explain what HR data was exposed, provide credit monitoring 
         (if sensitive), recommend password change
```

---

## Part 2: GDPR Compliance Framework

### 2.1 GDPR Applicability

**Does GDPR Apply?**
- ✅ Any user in EU/EEA = GDPR applies (globally)
- ✅ Personal data collected = GDPR applies
- ✅ Processing personal data = GDPR applies

**Key Principle:** GDPR is extraterritorial (applies worldwide if EU residents involved)

### 2.2 Core GDPR Requirements

#### **Lawful Basis for Processing**

**Valid Lawful Bases:**

| Basis | Vital Lens AI Use | Requirement |
|-------|------------------|-------------|
| **Consent** | ✅ Primary basis | Explicit, freely given, informed, easy to withdraw |
| **Contract** | Partial (ToS) | Processing necessary for service delivery |
| **Legal Obligation** | No | Not applicable for wellness app |
| **Vital Interest** | Partial | Only if life-threatening (not standard use case) |
| **Public Task** | No | Not a government service |
| **Legitimate Interest** | Conditional | Must balance against user rights |

**Recommended Approach:**
- Primary basis: **Explicit user consent** at app install
- Secondary: **Contract** (services cannot function without data)
- Avoid: Legitimate interest (too risky for health data)

---

#### **Transparency & User Rights (GDPR Articles 13-22)**

**Required Information to Provide (Privacy Notice):**

```
1. Identity of data controller (company name, address)
2. Purpose of processing (HR measurement, vitals tracking)
3. Legal basis (consent + contract)
4. Recipients (who else data shared with, if any)
5. Retention period (how long data kept)
6. User rights (access, deletion, portability, etc.)
7. Withdrawal of consent (how to opt-out)
8. Data processor details (third-party cloud provider, etc.)
9. Right to lodge complaint (GDPR authority contact)
```

**User Rights to Implement:**

| Right | Implementation |
|------|-----------------|
| **Access** | Export user data in readable format within 30 days |
| **Rectification** | Allow correction of inaccurate data |
| **Erasure** ("Right to be Forgotten") | Delete user & associated vitals (with exceptions) |
| **Restriction** | Pause processing on request |
| **Portability** | Export data in machine-readable format (JSON/CSV) |
| **Objection** | Opt-out from data use |
| **Automated Decision-making** | If used for lending/credit, disclose + option to object |

**Example: Right to Deletion Request**
```
User requests deletion via Settings > Delete Account
System should:
  1. Prompt for confirmation
  2. Delete user account within 30 days
  3. Delete all associated vitals data
  4. Delete device tokens, session data
  5. Anonymize logs (remove user identifiers)
  6. Confirm deletion to user via email
```

---

#### **Data Protection Officer (DPO)**

**Required?**
- ✅ If processing large amounts of health data (> 50,000 users recommended)
- ⚠️ If in EU and data processing is core business
- ❌ Small app with < 10K users: Not legally required, but recommended

**Responsibilities (if appointed):**
- Monitor GDPR compliance
- Act as contact point for data subjects & authorities
- Conduct Data Protection Impact Assessments (DPIAs)
- Advise on data handling policies

---

#### **Data Protection Impact Assessment (DPIA)**

**Required When:**
- Processing health data (high risk)
- Processing biometric data for identification (Article 9 special category)
- Large-scale processing
- Using new technologies

**DPIA Sections:**

```
1. Description of Processing
   - What data collected? (facial images, HR, timestamps)
   - How is it used? (local analysis, cloud processing, storage)
   - Who has access? (users, staff, third parties)

2. Necessity Assessment
   - Is collection necessary? (Yes, for PPG algorithm)
   - Could less data achieve same purpose? (Likely no)

3. Risk Assessment
   - Unauthorized access risk: HIGH (biometric data)
   - Data breach impact: SEVERE (health data + facial images)
   - Discrimination risk: MEDIUM (if algorithms biased)

4. Safeguards Implemented
   - Encryption, access controls, audit logs
   - User consent mechanisms
   - Data minimization (delete after 30 days)

5. Residual Risk Evaluation
   - Acceptable? (with mitigations: YES)
   - Further measures needed? (annual audits, staff training)
```

---

### 2.3 Special Categories of Data (GDPR Article 9)

**Health Data is Special:**
- Biometric data (facial images used for identification)
- Health information (HR, SpO2, skin conditions)
- Genetic data (if included in future)

**Processing Restrictions:**
- ❌ Prohibited by default (with exceptions)
- ✅ Exception 1: Explicit consent (recommended path)
- ✅ Exception 2: Vital interest (emergency only)
- ✅ Exception 3: Healthcare provider processing (N/A here)

**For Vital Lens AI:**

```
CONSENT FLOW:
┌─────────────────────────────────────────────────────┐
│ User opens app for first time                        │
├─────────────────────────────────────────────────────┤
│ "Vital Lens uses your camera to measure heart rate  │
│  by analyzing facial color changes.                 │
│                                                      │
│  We will collect:                                    │
│  • Facial images (processed locally)                │
│  • Heart rate measurements                          │
│  • Device type & app usage                          │
│                                                      │
│  Data is encrypted and can be deleted anytime.     │
│                                                      │
│  [Detailed Privacy Policy]"                         │
│                                                      │
│  [ ] I agree to these terms                         │
│  [CONTINUE] [DECLINE]                               │
└─────────────────────────────────────────────────────┘

If DECLINE → App shows "Cannot proceed without consent"
If CONTINUE → Proceed, log consent timestamp + IP for audit
```

---

### 2.4 Data Retention & Deletion Policy

**Retention Schedule:**

| Data Type | Retention Period | Reason |
|-----------|-----------------|--------|
| **Facial images** | 0 days (delete immediately) | Not needed; only HR extracted |
| **Heart rate measurements** | 30-90 days | User wellness history |
| **User account data** | Until deletion request | Account management |
| **Audit logs** | 6 years | Compliance requirement |
| **Consent records** | 6 years | Legal defensibility |
| **Device tokens** | Until logout/uninstall | Session management |

**Deletion Mechanisms:**

```
Automatic Deletion (Privacy-by-Design):
- Facial image frames: Deleted immediately after PPG extraction
- Temporary buffers: Cleared after processing
- Short-term vitals cache: 24-hour purge

On-Demand Deletion (User Request):
- Vitals history: Deleted within 30 days of request
- Account: Full deletion within 30 days
- Logs: Anonymized (user ID removed, kept for security)

Backup/Disaster Recovery:
- Same encryption as primary data
- Deleted from backups after retention period
- Separate deletion workflows for backup systems
```

---

### 2.5 Data Processors & Third Parties

**Data Processor Agreement (DPA):**

If using cloud provider (AWS, GCP, Azure), must have Data Processing Agreement:

```
Required Clauses:
✅ Purpose & scope of processing
✅ Data categories & data subjects
✅ Processor obligations (security, confidentiality)
✅ Subprocessor disclosure & approval
✅ Data subject rights (access, deletion)
✅ Assistance with DPIAs & breaches
✅ Data return/deletion upon contract end
✅ Audit rights & inspections
✅ International transfer mechanisms (if applicable)

Example Processors for Vital Lens AI:
1. Cloud Storage (AWS S3 / GCP Storage)
   - DPA: Standard AWS/GCP DPA available
   - Jurisdiction: Data centers in EU (to meet residency)
   
2. Analytics Platform (optional)
   - DPA: Must verify processor has GDPR-compliant agreement
   - Alternative: Self-hosted analytics (avoid third party)
   
3. Email Service (SendGrid, Mailchimp)
   - DPA: Verify processor compliance
   - Data: Minimal (email address only, not health data)
```

---

### 2.6 International Data Transfers

**Challenge:** If data center is outside EU, transfers are restricted

**Solutions:**

| Solution | Status | Viable? |
|----------|--------|---------|
| **Standard Contractual Clauses (SCC)** | ✅ Valid (post-Schrems II) | ✅ Yes |
| **Adequacy Decision** | ⚠️ Limited (few countries) | ❌ Probably not |
| **Binding Corporate Rules** | ✅ Valid for enterprise | ❌ Overkill for startup |
| **EU Data Residency** | ✅ Best practice | ✅ Recommended |

**Recommended Approach:**
```
OPTION 1 (Simplest): EU-only data residency
- Store all data in AWS EU regions (Frankfurt, Ireland, Paris)
- No transfers = No compliance complexity
- Cost: Slightly higher (EU regions premium)

OPTION 2 (Flexible): SCC + Standard Contractual Clauses
- Store in US regions (cheaper)
- Processor signs SCC with controller
- Conduct Transfer Impact Assessment (TIA)
- Add supplementary measures (encryption)
- Cost: Lower but more complex compliance
```

**For Phase 1:** Recommend **OPTION 1** (EU-only residency) for simplicity

---

## Part 3: CCPA Compliance (California)

### 3.1 CCPA Applicability
- Applies to CA residents only
- Easier to implement than GDPR
- Often "covered" by GDPR-compliant design

### 3.2 CCPA Requirements

**Consumer Rights:**

| Right | Requirement | Implementation |
|------|-------------|-----------------|
| **Know** | Disclose collection of personal info | Privacy Policy |
| **Access** | Provide copy of collected data | Data export feature |
| **Delete** | Erase consumer data | Account deletion flow |
| **Opt-Out** | Stop selling/sharing data | Privacy dashboard |

**Vital Lens AI Implementation:**
- No data sale (not planned, disclose in Privacy Policy)
- Opt-out mechanism: Disable analytics if optional
- Access/delete: Same GDPR mechanisms

---

## Part 4: Practical Implementation Roadmap

### Phase 1 Deliverables

**Documentation:**
- [ ] Privacy Policy (plain language)
- [ ] Data Processing Agreement (with vendors)
- [ ] Data Retention Policy
- [ ] Incident Response Plan
- [ ] Breach Notification Template

**Technical Controls:**
- [ ] Encryption at rest (AES-256) specification
- [ ] Encryption in transit (TLS 1.2+) implementation plan
- [ ] Audit logging system design
- [ ] Access control policy document

**Consent & Transparency:**
- [ ] Consent UI design (GDPR compliant)
- [ ] Privacy notice content (detailed)
- [ ] Terms of Service draft
- [ ] Data Subject Rights request mechanism

---

### Phase 2 Deliverables

**Implementation:**
- [ ] Deploy encryption infrastructure
- [ ] Implement audit logging
- [ ] Build user consent flow
- [ ] Create data export/deletion endpoints
- [ ] Setup GDPR request handling process

**Training & Governance:**
- [ ] Privacy/security training for staff
- [ ] Data controller role assignment
- [ ] DPIA completion & sign-off
- [ ] Processor DPA execution

---

### Phase 3+ Deliverables

**Maturity:**
- [ ] Annual security audit
- [ ] DPIA refresh (if scope changes)
- [ ] Compliance metrics dashboard
- [ ] DPO engagement (if needed)
- [ ] Clinical partnership data agreements

---

## Part 5: Compliance Checklist

### Pre-Launch (Phase 1-2)

- [ ] **Privacy Policy** drafted and reviewed by legal counsel
- [ ] **Terms of Service** include health data disclaimer ("not for medical diagnosis")
- [ ] **Consent mechanism** implemented & tested
- [ ] **Data retention policy** documented & enforced
- [ ] **Encryption** implemented (AES-256 at rest, TLS in transit)
- [ ] **Audit logging** enabled & tested
- [ ] **User access/delete endpoints** built & tested
- [ ] **Breach notification plan** documented
- [ ] **GDPR DPIA** completed (if >50K users expected)
- [ ] **Staff privacy training** scheduled
- [ ] **Data processor agreements** signed with cloud providers

### Post-Launch (Phase 3+)

- [ ] **Monthly audit log review** for anomalies
- [ ] **Quarterly security assessment** for vulnerabilities
- [ ] **Annual GDPR/HIPAA compliance audit** by external firm
- [ ] **User consent renewal** every 1-2 years
- [ ] **Incident log review** (tracking breaches)
- [ ] **DPO engagement** (if data scale warrants)

---

## Part 6: Risk Assessment & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-----------|-----------|
| **Data breach (unauthorized access)** | Severe (hefty fines, user trust loss) | High | Encryption, access controls, intrusion detection |
| **User privacy violations (non-compliant processing)** | Severe (GDPR fines up to 4% revenue) | Medium | Privacy Policy, consent, DPA with vendors |
| **Breach notification failure** | Severe (additional fines) | Low | Automated breach handling, legal review |
| **Facial image misuse** | High (biometric ethics) | Low | Immediate deletion of images, encryption |
| **SpO2 liability (non-clinical data)** | Medium (medical device classification risk) | Medium | Clear disclaimers, "wellness only" positioning |
| **Algorithm bias (discriminatory outcomes)** | Medium (reputational, potential legal) | Medium | Diverse dataset testing, fairness metrics |

---

## Part 7: Key Disclaimers & Legal Positioning

### Privacy Policy Must Include:

```
⚠️ IMPORTANT DISCLAIMERS:

1. NOT A MEDICAL DEVICE
   "Vital Lens is a wellness app for general interest. 
    Heart rate estimates are for informational use only 
    and should not be used for medical diagnosis or treatment."

2. DATA NOT SHARED WITH HEALTHCARE PROVIDERS
   "Your data is not transmitted to doctors, insurers, or 
    any healthcare entities unless you explicitly choose to share."

3. NO GUARANTEE OF ACCURACY
   "Heart rate estimates may vary from medical-grade 
    pulse oximeters by ±3-5 bpm depending on lighting, 
    skin tone, and movement."

4. FACIAL IMAGES NOT STORED
   "Facial video frames are processed locally and deleted 
    immediately. They are never uploaded or permanently stored."

5. GDPR RIGHTS
   "You have the right to access, correct, or delete your data 
    at any time. Contact privacy@vitallensai.com for requests."
```

---

## References & Resources

### HIPAA Resources:
- **HHS HIPAA Guidance:** www.hhs.gov/hipaa
- **HIPAA Security Rule:** 45 CFR Parts 160 & 164

### GDPR Resources:
- **GDPR Full Text:** https://gdpr-info.eu/
- **EDPB Guidelines:** https://edpb.ec.europa.eu/
- **GDPR Template DPA:** https://edpb.ec.europa.eu/

### Legal Considerations:
- Consult healthcare attorney for medical device classification
- Consult privacy attorney for jurisdiction-specific laws
- Consider cyber liability insurance

---

**Status:** Complete - Phase 1 Foundation  
**Next Task:** Task 6 - Create comprehensive Phase 1 research documentation
