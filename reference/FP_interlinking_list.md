# ADAudit Plus — Feature Page Interlinking Reference (Complete — Live Verified)

**Purpose:** Use this file during delivery to identify contextually relevant internal links for each draft. Every entry includes a "What this page actually covers" note. All notes marked **[LIVE READ]** were verified by reading the page body directly. Notes marked **[PRODUCT DOCS]** are based on ADAudit_Plus_product_docs.md where the page body was not reachable.

**Last updated:** April 2026

---

## Linking rules

1. **Link count** — up to 10–12 links per page if genuinely earned.
2. **Contextual only** — anchor must be a natural noun phrase already in the sentence.
3. **No self-links.**
4. **No competitor comparison pages.**
5. **No whitepaper or PDF pages.**
6. **Prefer specific over general.**
7. **Tag matching** — use the H2-to-tag table at the bottom to find candidates.
8. **Verify URL is live before inserting.**

---

## Topic-match test (required before every link)

**Test 1** — Anchor phrase appears verbatim in section content.
**Test 2** — The section explicitly discusses the anchor topic (not a passing mention or definitional sentence).
**Test 3** — Read the "What this page actually covers" note and confirm the anchor topic is this page's primary subject, not a sidebar mention.
**Test 4** — No Type A terms as anchors (report names, feature names, tab names).

---

## Tag index

---

### Tag: `lockout`

| Page title | URL | What this page actually covers |
|---|---|---|
| Account lockout analyzer | https://www.manageengine.com/products/active-directory-audit/windows-ad-user-account-lockout-analyzer.html | **[SELF-LINK — do not use on this page]** |
| Account lockout examiner | https://www.manageengine.com/products/active-directory-audit/account-lockout-examiner.html | **[LIVE READ]** Tracing the lockout source from a list of Windows components (services, apps, scheduled tasks, mapped drives, network drive mappings); correlating lockouts with recent logon data; summarising most-frequently locked-out users; audit trail of password resets and lockout sources for forensics; compliance (GDPR, SOX, HIPAA, PCI DSS, FISMA, GLBA). Best destination for anchors about: finding a lockout source, lockout history, lockout frequency analysis, lockout forensics. |

---

### Tag: `ad-change-auditing`

| Page title | URL | What this page actually covers |
|---|---|---|
| Active Directory auditing | https://www.manageengine.com/products/active-directory-audit/active-directory-auditing.html | **[LIVE READ]** Broad AD auditing hub — logon monitoring (interactive, remote, local, network), failed logon attempts, computer startup/shutdown, lockout analysis and troubleshooting (stale credentials, network drive mapping causes), brute-force detection, UBA-driven atypical behaviour alerts, employee productivity. Best destination for broad "Active Directory auditing" anchor phrases. |
| Active Directory audit reports | https://www.manageengine.com/products/active-directory-audit/active-directory-audit-reports.html | **[LIVE READ]** Pre-configured and custom Report Profile Based Reports — combining users, audit actions, and filters for granular reporting; compliance reports for SOX, HIPAA, PCI, GLBA; graphical summary dashboards. Best destination for anchors about: audit reports, report profiles, custom reports, pre-configured reports. |
| Active Directory change audit reports | https://www.manageengine.com/products/active-directory-audit/active-directory-change-audit-reports.html | **[LIVE READ]** Change auditing across users, groups, computers, OUs; 50+ predefined alert profiles; who-what-when-where detail; compliance (GDPR, PCI DSS, HIPAA, CCPA); single-console hybrid/cloud + on-premises view; UBA anomaly detection for user management spikes. Best destination for anchors about: AD change auditing, change reports, who-what-when-where of AD changes. |
| Monitor Active Directory changes | https://www.manageengine.com/products/active-directory-audit/monitor-active-directory-changes.html | **[LIVE READ]** Real-time tracking of all AD object changes (users, groups, OUs, computers); permission change alerts with old/new values; schema and FSMO role change detection; automated threat response (unlock accounts, disconnect sessions); UBA anomaly detection. Best destination for anchors about: monitoring AD changes in real time, real-time AD object change tracking. |
| Schedule Active Directory change reports | https://www.manageengine.com/products/active-directory-audit/schedule-active-directory-change-reports.html | **[LIVE READ]** Automated report scheduling (hourly, daily, weekly, monthly); email delivery to non-admin users (auditors, IT managers, help desk); both default and custom reports schedulable; report history maintained. Best destination for anchors about: scheduled reports, automated report delivery, email delivery of audit reports. |
| Active Directory monitoring | https://www.manageengine.com/products/active-directory-audit/windows-active-directory-monitoring.html | **[LIVE READ]** Real-time AD monitoring — privileged user tracking, password change/reset monitoring, security loopholes (passwords never expire), compliance (GDPR, HIPAA, SOX), insider threat automated response, logon data monitoring, UBA lockout spike detection. Best destination for anchors about: continuous real-time AD monitoring as an ongoing security operation. |
| Active Directory change alerts | https://www.manageengine.com/products/active-directory-audit/active-directory-change-alerts.html | **[LIVE READ]** Real-time alerting mechanism for AD changes — alert profiles for critical events (admin account access, domain policy changes, group membership changes); email/SMS delivery; automated response on trigger. Best destination for anchors about: AD change alerts, real-time notifications on AD changes, alert profiles. |
| Active Directory change reporter | https://www.manageengine.com/products/active-directory-audit/active-directory-change-reporter.html | **[LIVE READ]** Tracks all AD object changes (users, groups, OUs, computers, schema, FSMO roles, configuration); UBA anomaly detection; automated threat response. Largely overlaps with monitor-active-directory-changes.html — prefer that page as primary destination for change tracking anchors. |
| Audit Active Directory changes | https://www.manageengine.com/products/active-directory-audit/audit-active-directory-changes.html | **[LIVE READ]** Broad AD change auditing overview — logon activity, lockout detection, file access tracking, FIM, anomaly detection, automated response; compliance (SOX, HIPAA, PCI, FISMA, GLBA, GDPR). Functions as a hub page. Prefer more specific pages when a specific anchor topic is available. |
| Audit AD old and new attribute changes | https://www.manageengine.com/products/active-directory-audit/audit-ad-old-new-attribute-changes.html | **[LIVE READ]** Before/after attribute value tracking for all AD object types (users, computers, groups, OUs); ACL/permission attribute changes with old and new values; GPO extended attribute and permission changes. Best destination for anchors about: before-and-after values for AD object changes, old and new attribute values. |
| Change activity alerts | https://www.manageengine.com/products/active-directory-audit/change-activity-alerts.html | **[LIVE READ]** Real-time alerting for any AD change — notifies admins instantly when defined changes occur; focuses on the alert delivery mechanism; covers admin account access alerts. Older-style page, closely overlaps with active-directory-change-alerts.html. Prefer active-directory-change-alerts.html for alert anchors. |
| AD audit reports from archived data | https://www.manageengine.com/products/active-directory-audit/ad-audit-reports-from-archived-data.html | **[LIVE READ]** Generating audit reports FROM already-archived historical data; compliance requirements (SOX, HIPAA, GLBA require 3–10 years of log retention); restoring and querying archived event data. Best destination for anchors about: querying historical audit data, reporting from archived logs. **Distinct from archive-active-directory-audit-data.html (archival process) — these are different pages.** |
| Archive Active Directory audit data | https://www.manageengine.com/products/active-directory-audit/archive-active-directory-audit-data.html | **[LIVE READ]** Archiving Windows AD audit data — the archival process, compliance-driven retention (SOX, HIPAA, PCI), overcoming native security log size limitations, ADAudit Plus archiving advantages. Best destination for anchors about: archiving audit data, log retention, long-term data storage for compliance. **Distinct from ad-audit-reports-from-archived-data.html.** |
| User-based consolidated audit trail | https://www.manageengine.com/products/active-directory-audit/active-directory-user-based-consolidated-audit-trail.html | **[LIVE READ]** User-specific audit trail search — input a username + domain + time period and retrieve a consolidated timeline of all AD changes that user made (object history, logon activity). Best destination for anchors about: per-user investigation, tracing a single user's footprint in AD, user audit trail. |

---

### Tag: `ad-security`

| Page title | URL | What this page actually covers |
|---|---|---|
| Active Directory security audit tool | https://www.manageengine.com/products/active-directory-audit/active-directory-security-audit-tool.html | **[LIVE READ]** Broad AD security monitoring overview — user logon/logoff/lockout correlated to detect brute-force signs; 200+ graphical reports; DC activity monitoring; file access and permission change auditing; FIM. Older-style page. Prefer active-directory-security-software.html for modern ITDR/attack detection anchors. |
| Active Directory security software | https://www.manageengine.com/products/active-directory-audit/active-directory-security-software.html | **[LIVE READ]** Identity threat detection and response (ITDR) — 25+ AD attack detection (MITRE ATT&CK-aligned), real-time alerts, forensic event timeline (before/during/after breach), automated remediation, AD security posture assessment. Best destination for anchors about: AD security posture, identity threats, breach detection, ITDR, forensic investigation, AD attack detection generally. |
| Attack surface analyzer | https://www.manageengine.com/products/active-directory-audit/attack-surface-analyzer.html | **[LIVE READ]** Indicators of compromise (IoC) — detects 25+ named AD attacks: Kerberoasting, Golden Ticket, DCSync, pass-the-hash, pass-the-ticket, RID hijacking, ransomware; Indicators of exposure (IoE) — risky Azure/AWS/GCP configurations with NIST-based remediation; 15+ network attacks and 20+ process attacks via MITRE ATT&CK®; UBA; automated incident response (shut down device, auto-create ServiceNow tickets). Best destination for anchors about: specific named attack techniques, IoC, IoE, MITRE ATT&CK, cloud security posture by attack name. |
| Insider threat detection | https://www.manageengine.com/products/active-directory-audit/insider-threat-detection.html | **[LIVE READ]** UBA-driven detection of internal threats — multiple failed logons (source and reason), user activity anomalies (unusual volume or time), privilege escalations (password resets, user management), lateral movement (out-of-ordinary RDP, new process execution), data mishandling (file deletions, FIM), data exfiltration via USB. Scenarios: malicious insiders (rogue admin), careless insiders (accidental excessive privilege), inadvertent insiders (ransomware via malicious website). **Primary focus is threats originating from within the organisation. NOT the right destination for external attack techniques like password spray or brute-force where the attacker is external.** |
| Security misconfigurations | https://www.manageengine.com/products/active-directory-audit/security-misconfigurations.html | **[LIVE READ]** Detecting and remediating security misconfigurations across AD-managed servers and workstations — security exposure management, CIS benchmark compliance for GPO settings, 700+ misconfiguration policies for Azure/cloud, continuous automated daily scans. Best destination for anchors about: security misconfigurations, CIS benchmarks, attack surface reduction through configuration, endpoint configuration gaps. |
| CIS benchmark scanning tool | https://www.manageengine.com/products/active-directory-audit/cis-benchmark-scanning-tool.html | **[LIVE READ]** CIS benchmark compliance scanning for Windows — assessing Windows servers and workstations against CIS benchmark standards; identifying non-compliant settings; actionable remediation guidance. Best destination for anchors specifically about CIS benchmarks or configuration compliance standards for Windows. |
| Cloud security tool | https://www.manageengine.com/products/active-directory-audit/cloud-security-tool.html | **[LIVE READ]** Cloud security posture management (CSPM) for Azure, AWS, and GCP — detecting cloud misconfigurations, proactive attack surface reduction, 700+ misconfiguration policies (NIST and CIS), continuous monitoring, severity-based alerts. Best destination for anchors about: cloud misconfiguration, CSPM, multi-cloud security posture. **Not about cloud logon monitoring or cloud user activity.** |
| Windows security event log monitoring | https://www.manageengine.com/products/active-directory-audit/windows-security-eventlog-monitoring.html | **[LIVE READ]** Real-time Windows Security Event Log monitoring — centralised collection, monitoring, archiving, alerting on Windows security log events; named Event IDs (4768/4771 Kerberos, 4624/4625 logon, 5136/5137/5139/5141 AD object, 4670 permission, 4663/4660 file access/deletion); compliance-driven log retention (HIPAA 7 years, PCI 5 years); advanced audit policy guidance for DCs, file servers, member servers, workstations. Best destination for anchors about: security event logs, Windows event log monitoring, Event IDs specifically, Windows audit policy configuration. |

---

### Tag: `permission-changes`

| Page title | URL | What this page actually covers |
|---|---|---|
| Permission change auditing | https://www.manageengine.com/products/active-directory-audit/windows-servers-active-directory-permission-change-auditing.html | **[LIVE READ — nav only reached, body confirmed exists]** Real-time permission and ACL change auditing across Active Directory objects and Windows file servers — who changed what permission, when, from where, with old and new permission values; covers AD object ACLs (domain, OU, container, GPO, user, group, computer, schema) and file server permissions. Best destination for anchors about: permission changes, ACL changes, access control changes with before/after values. |

---

### Tag: `group-management`

| Page title | URL | What this page actually covers |
|---|---|---|
| Active Directory group audit report | https://www.manageengine.com/products/active-directory-audit/active-directory-group-audit-report.html | **[PRODUCT DOCS]** Auditing AD group membership changes — who was added to or removed from security and distribution groups (especially privileged groups); group creation, deletion, and modification; before/after group attribute values. Best destination for anchors about: group membership changes, adding/removing users from groups, security group auditing. |

---

### Tag: `ou-management`

| Page title | URL | What this page actually covers |
|---|---|---|
| Audit organizational unit changes | https://www.manageengine.com/products/active-directory-audit/audit-organizational-unit-changes.html | **[PRODUCT DOCS]** Auditing changes to Organizational Units — OU creation, deletion, movement, modification, and renaming; delegation changes; GPO link changes at the OU level. Best destination for anchors about: OU changes, organizational unit auditing, OU delegation changes. |

---

### Tag: `dns-schema`

| Page title | URL | What this page actually covers |
|---|---|---|
| DNS and schema auditing | https://www.manageengine.com/products/active-directory-audit/active-directory-schema-contacts-dns-auditing.html | **[PRODUCT DOCS]** Auditing DNS record changes (records added, modified, deleted), AD schema changes, configuration partition changes, and contact object changes. Best destination for anchors about: DNS change auditing, AD schema modifications, DNS record tracking. |

---

### Tag: `gpo`

| Page title | URL | What this page actually covers |
|---|---|---|
| GPO change audit reports | https://www.manageengine.com/products/active-directory-audit/gpo-change-audit-reports-list.html | **[PRODUCT DOCS]** Group Policy tracking and reporting — real-time audit of GPO creation, deletion, modification, and link changes across the domain; who changed what GPO, when, and from where. Best destination for anchors about: GPO changes at the object level, GPO creation/deletion/modification tracking. |
| GPO settings changes audit | https://www.manageengine.com/products/active-directory-audit/gpo-settings-changes-audit.html | **[LIVE READ — in earlier session]** Advanced real-time auditing of settings within GPOs — named reports include: Password Policy Changes, Account Lockout Policy Changes, Security Settings Changes, Administrative Template Changes, Computer Configuration Changes, User Configuration Changes, User Rights Assignment Changes, Windows Settings Changes, Group Policy Permission Changes, Group Policy Preferences Changes, Group Policy Settings History, Extended Attribute Changes. Each shows who changed what, when, from where, with old and new values. Best destination for anchors about: GPO settings changes specifically, lockout policy setting changes, password policy changes, security settings changes within GPOs. |
| Group Policy object audit reports | https://www.manageengine.com/products/active-directory-audit/group-policy-object-audit-reports.html | **[PRODUCT DOCS]** GPO-level change tracking including creation, deletion, modification, and linking of GPOs. Overlaps with gpo-change-audit-reports-list.html. Best destination when the anchor is specifically about "Group Policy object" changes rather than settings within GPOs. |

---

### Tag: `logon`

| Page title | URL | What this page actually covers |
|---|---|---|
| User login history | https://www.manageengine.com/products/active-directory-audit/active-directory-user-login-history.html | **[LIVE READ]** Comprehensive user logon history for any domain user — consolidated logon audit trail per user, UBA anomaly detection (irregular logon time, abnormal failure volume, unusual file activity), tracking users logged into multiple machines, employee productivity/idle time analysis, RADIUS logon history aggregation. Best destination for anchors about: user logon history, login history tracking, user logon patterns, per-user logon audit trail. |
| Logon failure auditing | https://www.manageengine.com/products/active-directory-audit/active-directory-audit-logon-failure.html | **[LIVE READ]** Auditing all failed logon attempts — bad password failures (brute-force indicator), bad username failures (password spray indicator), RADIUS/NPS failed logons, interactive logon failures, service account logon failures; account lockout source tracing; automated threat response. Best destination for anchors about: failed logon attempts, logon failures, brute-force detection via logon events, password spray detection via logon events, service account logon failures. |
| User logon audit reports | https://www.manageengine.com/products/active-directory-audit/user-logon-audit-reports.html | **[LIVE READ]** Named report library — contains: Logon Failure Report (bad password/username with failure reason), Logon Activity on Domain Controllers, Logon Activity on Member Servers, Logon Activity on Workstations, User Logon Activity (full history for a selected user), Recent User Logon Activity, Last Logon on Workstations, Users Logged into Multiple Computers, RADIUS Logon on Computers. Best destination for anchors about: user logon audit reports library, logon activity reports, RADIUS logon auditing. |
| Monitor user logon actions | https://www.manageengine.com/products/active-directory-audit/monitor-user-logon-actions.html | **[LIVE READ]** Same content as user-logon-audit-reports.html — identical named report set (Logon Failure, DC Logon Activity, Member Server Logon Activity, Workstation Logon Activity, User Logon Activity, Recent Logon Activity, Last Logon on Workstations, RADIUS Logon). Also explains why native AD is insufficient for logon auditing. These two pages are effectively duplicates. Prefer user-logon-audit-reports.html as the more specific destination. |
| Track user logon and logoff | https://www.manageengine.com/products/active-directory-audit/track-user-logon-logoff-active-directory.html | **[LIVE READ]** Real-time logon and logoff tracking — user attendance (active/idle time), logon session duration, users logged onto multiple computers (with IP addresses and logon times), currently logged-on users overview, Remote Desktop Gateway logon/logoff, UBA-driven unusual logon activity (unusual volume, time, host). Best destination for anchors about: tracking logon AND logoff activity, user attendance monitoring, session duration, users on multiple computers, currently logged-on users. |
| Member server local users logon auditing | https://www.manageengine.com/products/active-directory-audit/windows-member-servers-local-users-logon-logoff-auditing.html | **[LIVE READ — nav only reached]** Local user logon and logoff auditing on Windows member servers — tracking local (non-domain) account logon events on servers. Best destination for anchors specifically about local user logon activity on member servers. |
| Mac workstation logon audit | https://www.manageengine.com/products/active-directory-audit/mac-workstation-logon-audit.html | **[PRODUCT DOCS]** Logon auditing for Mac workstations — tracking logon and logoff events on macOS endpoints in an AD environment. Best destination for anchors specifically about Mac or macOS logon auditing. |
| Remote desktop session monitoring | https://www.manageengine.com/products/active-directory-audit/monitor-remote-desktop-sessions.html | **[PRODUCT DOCS]** Remote desktop session monitoring — tracking RDP logon and logoff activity, RD Gateway sessions, successful and failed RDP connections, session duration. Best destination for anchors about: remote desktop monitoring, RDP session tracking, Remote Desktop Gateway auditing. |

---

### Tag: `privileged-users`

| Page title | URL | What this page actually covers |
|---|---|---|
| Privileged user monitoring | https://www.manageengine.com/products/active-directory-audit/privileged-user-monitoring.html | **[LIVE READ]** Continuous privileged user activity auditing and UBA — auditing administrator activity on AD (schema, configuration, users, groups, OUs, GPOs), tracking privileged user access to critical data (file activities), detecting privilege escalation (first-time use of privilege reports), alerting on suspicious privileged activity (clearing audit logs, accessing data outside business hours), UBA behavioural anomaly detection for stolen/shared credentials. Best destination for anchors about: privileged user monitoring, administrator activity auditing, privilege escalation detection, admin account auditing. |
| Track users and administrators actions | https://www.manageengine.com/products/active-directory-audit/track-users-administrators-actions.html | **[LIVE READ]** Despite the URL suggesting admin tracking, this page is actually the **user management audit reports page** — its H1 is "Real Time Audit of User Management Actions." It covers: user lifecycle changes (created/deleted/modified), password status changes (password set/changed, locked out/unlocked), user status changes (enabled/disabled), user administrative activity (actions by a selected helpdesk technician or admin on users/computers/groups), user history reports. The "administrators" in the URL refers to administrators as actors performing user management tasks, not to admin activity auditing in general. **Best destination for anchors about: user management actions by delegated staff or admins, user lifecycle change auditing, who made what changes to user objects.** For privileged admin activity tracking specifically, use privileged-user-monitoring.html instead. |

---

### Tag: `user-management`

| Page title | URL | What this page actually covers |
|---|---|---|
| User management reports | https://www.manageengine.com/products/active-directory-audit/user-management-reports.html | **[PRODUCT DOCS]** Auditing user account management events — user creation, deletion, modification, password resets, password changes, account enable/disable, account expiry changes; group membership additions and removals. Best destination for anchors about: user account management auditing, user creation/deletion tracking, password reset auditing. |

---

### Tag: `uba`

| Page title | URL | What this page actually covers |
|---|---|---|
| User behavior analytics | https://www.manageengine.com/products/active-directory-audit/user-behavior-analytics.html | **[LIVE READ]** UBA engine — machine learning baselines per individual user (not domain-wide averages); anomaly detection for: malicious logins (unusual hours, unusual failure volume), lateral movement (machine accessed for first time, dormant account becomes active), privilege abuse (unusual user management activity volume), data breaches (data exfiltration/deletion attempt), malware (unusual process running). Threat investigation (who/what/when/where per anomaly) and automated threat mitigation. Best destination for anchors about: user behavior analytics, UBA, machine learning baselines, anomaly detection for user activity, behavioural anomalies. |

---

### Tag: `entra-id`

| Page title | URL | What this page actually covers |
|---|---|---|
| Microsoft Entra ID audit tool | https://www.manageengine.com/products/active-directory-audit/azure-active-directory-logs-audit-tool.html | **[LIVE READ]** Comprehensive Azure AD / Entra ID auditing — sign-in monitoring (successful, failed, suspicious), MFA usage and failures, user object changes (created/deleted/updated with old/new values), password changes and resets, group and role management (membership changes, ownership changes, dynamic group rule updates, license changes), application and device management (consent tracking, OAuth permission changes), conditional access policy changes, sign-in risk detection (risky logons, anonymous IPs, malicious IPs, password spray, atypical locations, leaked credentials); hybrid AD correlated view (on-premises SID/GUID/DN with cloud events); compliance reports (SOX, HIPAA, FISMA, GLBA, GDPR, ISO). Best destination for broad Entra ID / Azure AD auditing anchor phrases. |
| Azure password protection auditing | https://www.manageengine.com/products/active-directory-audit/azure-password-protection-auditing.html | **[LIVE READ — nav only reached]** Auditing Azure AD Password Protection — tracking banned password policy events, password validation events, proxy service health; detecting attempts to use banned passwords in hybrid environments. Best destination for anchors specifically about Azure password protection, banned password policies, or password validation auditing in Entra ID. |
| Azure Conditional Access policy auditing | https://www.manageengine.com/products/active-directory-audit/azure-conditional-access-policy-auditing.html | **[PRODUCT DOCS]** Auditing changes to Azure Conditional Access policies — who created, modified, or deleted Conditional Access policies; what the policies cover (MFA enforcement, device compliance, location restrictions). Best destination for anchors specifically about Conditional Access policy changes or auditing. |
| Azure AD reporting | https://www.manageengine.com/products/active-directory-audit/azure-reporting.html | **[PRODUCT DOCS]** Entra ID (Azure AD) reporting — pre-built reports for Azure AD sign-ins, user management events, role changes, group changes, application activity; compliance-ready Entra ID reports. Best destination for anchors about: Entra ID reports, Azure AD reporting, cloud directory reports. |
| Azure risk detection | https://www.manageengine.com/products/active-directory-audit/azure-risk-detection.html | **[PRODUCT DOCS]** Azure AD / Entra ID risk detection — detecting risky sign-ins, leaked credentials, anonymous IP usage, atypical travel, malware-linked IP addresses; risk-based alerts for Entra ID sign-in events. Best destination for anchors about: Entra ID risk detection, risky sign-ins, Azure AD risk events, cloud identity risk signals. |

---

### Tag: `compliance`

| Page title | URL | What this page actually covers |
|---|---|---|
| Active Directory compliance reports | https://www.manageengine.com/products/active-directory-audit/active-directory-compliance-reports.html | **[PRODUCT DOCS]** Overview of ADAudit Plus compliance reporting capabilities across all supported standards — SOX, HIPAA, PCI DSS, FISMA, GLBA, GDPR, ISO 27001; out-of-the-box compliance report sets; custom report profiles for compliance use cases. Best destination for anchors about: compliance reporting generally, multi-standard compliance, audit-ready compliance reports. |
| Aggregated summary reports for compliance | https://www.manageengine.com/products/active-directory-audit/aggregated-summary-reports-security-compliance.html | **[PRODUCT DOCS]** Aggregated summary reports combining data from multiple AD domains and sources into a single consolidated compliance view — cross-domain summary reports, high-level security dashboards for compliance officers and auditors. Best destination for anchors about: aggregated reports, summary dashboards for compliance, cross-domain compliance views. |
| FISMA compliance reporting | https://www.manageengine.com/products/active-directory-audit/fisma-compliance-reporting-software.html | **[PRODUCT DOCS]** FISMA-specific compliance reports covering NIST SP 800-53 controls mapped to AD audit events; access control, audit and accountability, configuration management. Best destination for anchors specifically about FISMA compliance or NIST 800-53 controls. |
| GDPR compliance reporting | https://www.manageengine.com/products/active-directory-audit/gdpr-compliance-reporting-software.html | **[PRODUCT DOCS]** GDPR-specific compliance reports — data access auditing, personal data access tracking, breach detection reports, data subject access audit trail. Best destination for anchors specifically about GDPR compliance reporting. |
| GLBA compliance reporting | https://www.manageengine.com/products/active-directory-audit/glba-compliance-reporting-tool.html | **[PRODUCT DOCS]** GLBA-specific compliance reports — safeguarding customer financial data; access controls, authentication events, and security incident reporting mapped to GLBA Safeguards Rule requirements. Best destination for anchors specifically about GLBA compliance. |
| HIPAA compliance reporting | https://www.manageengine.com/products/active-directory-audit/hipaa-compliance-reporting-tool.html | **[PRODUCT DOCS]** HIPAA-specific compliance reports — access to ePHI, user logon and logoff auditing, system activity reviews, security incident reporting; 7-year log retention for HIPAA; mapped to HIPAA Security Rule administrative safeguards. Best destination for anchors specifically about HIPAA compliance reporting. |
| ISO 27001 compliance tool | https://www.manageengine.com/products/active-directory-audit/iso-27001-tool.html | **[PRODUCT DOCS]** ISO 27001-specific compliance reports — AD change audit events mapped to ISO 27001 Annex A controls (access control, operations security, information security incident management). Best destination for anchors specifically about ISO 27001 compliance. |
| PCI-DSS compliance reports | https://www.manageengine.com/products/active-directory-audit/pci-dss-compliance-reports.html | **[PRODUCT DOCS]** PCI DSS-specific compliance reports — access control to cardholder data environments, logon monitoring, privileged account activity, 5-year log retention; mapped to PCI DSS requirements 7, 8, 10. Best destination for anchors specifically about PCI DSS compliance reporting. |
| SOX compliance auditing | https://www.manageengine.com/products/active-directory-audit/sox-compliance-auditing-reporting.html | **[PRODUCT DOCS]** SOX-specific compliance reports — change auditing for financial system access controls, admin activity on critical systems, GPO changes, privileged user activity; 7-year log retention; mapped to SOX Section 404 IT controls. Best destination for anchors specifically about SOX compliance or Sarbanes-Oxley audit requirements. |

---

### Tag: `file-auditing`

| Page title | URL | What this page actually covers |
|---|---|---|
| File auditor | https://www.manageengine.com/products/active-directory-audit/file-auditor.html | **[PRODUCT DOCS]** Primary Windows file server auditing hub — file access (read, write, create, delete, rename), permission changes, share-level access, FIM across Windows file servers and failover clusters. Best destination for broad "file auditing" or "file server auditing" anchor phrases. |
| File server audit | https://www.manageengine.com/products/active-directory-audit/file-server-audit.html | **[PRODUCT DOCS]** File server audit overview — auditing all file server events (access, modification, deletion, permission changes) with who-what-when-where detail; compliance-ready file server audit reports. Best destination for anchors about: file server audit, auditing file server activity generally. |
| File share auditing | https://www.manageengine.com/products/active-directory-audit/file-share-auditing.html | **[PRODUCT DOCS]** Auditing Windows file share access and changes — who accessed which share, when, from where; share permission changes; share creation and deletion. Best destination for anchors specifically about file share access or network share auditing. |
| File server monitoring tool | https://www.manageengine.com/products/active-directory-audit/file-server-monitoring-tool.html | **[PRODUCT DOCS]** Continuous real-time file server monitoring — monitoring file activity as it happens, real-time alerts on file events, file server activity dashboards. Best destination for anchors about: file server monitoring (continuous/real-time). |
| File integrity monitoring | https://www.manageengine.com/products/active-directory-audit/windows-file-integrity-monitoring.html | **[PRODUCT DOCS]** File Integrity Monitoring (FIM) — detecting unauthorised changes to system files, program files, configuration files; hash-based integrity verification; compliance-required FIM for PCI DSS, HIPAA, SOX. Best destination for anchors specifically about file integrity monitoring, FIM, detecting unauthorised file modifications. |
| File access monitoring software | https://www.manageengine.com/products/active-directory-audit/file-access-monitoring-software.html | **[PRODUCT DOCS]** Monitoring who accessed which files and when — successful and failed file access attempts, file read tracking, access pattern analysis; detecting unauthorised file access. Best destination for anchors about: file access monitoring, tracking who accessed which files. |
| File activity monitoring software | https://www.manageengine.com/products/active-directory-audit/file-activity-monitoring-software.html | **[PRODUCT DOCS]** Monitoring all file activities — creates, modifications, deletions, renames, moves, permission changes; file activity dashboards and reports. Best destination for anchors about: file activity monitoring, tracking all file operations. |
| Monitor file changes on Windows | https://www.manageengine.com/products/active-directory-audit/monitor-file-changes-windows.html | **[PRODUCT DOCS]** Monitoring file changes on Windows file servers — tracking file modifications, deletions, renames, and moves; real-time change detection and alerting. Best destination for anchors about: monitoring file changes, file change detection on Windows. |
| Windows file server auditing | https://www.manageengine.com/products/active-directory-audit/windows-file-server-auditing.html | **[PRODUCT DOCS]** Windows file server auditing — comprehensive auditing of all Windows file server events; file access, modification, deletion, permission changes, share access; reports and alerts. Best destination for anchors specifically about Windows file server auditing. |
| Windows file server auditing — access and permissions | https://www.manageengine.com/products/active-directory-audit/windows-file-server-auditing-access-permissions.html | **[PRODUCT DOCS]** File server access and permission change auditing specifically — who accessed files, what permissions changed, old and new permission values on files and folders. Best destination for anchors about: file permission changes specifically. |
| Windows file server auditing — reports and alerts | https://www.manageengine.com/products/active-directory-audit/windows-file-server-auditing-reports-and-alerts.html | **[PRODUCT DOCS]** File server audit reports and real-time alerts — scheduled file server reports, alert profiles for critical file events, email/SMS notification on file server changes. Best destination for anchors about: file server reports and alerts specifically. |
| Windows file server change audit reports | https://www.manageengine.com/products/active-directory-audit/windows-file-server-change-audit-reports.html | **[PRODUCT DOCS]** All Windows file server change audit reports — complete report library for file server changes. Best destination for anchors about: file server change reports library. |
| Windows file system auditing | https://www.manageengine.com/products/active-directory-audit/windows-file-system-auditing.html | **[PRODUCT DOCS]** Windows file system auditing — auditing at the file system level across Windows environments; NTFS auditing. Best destination for anchors about: Windows file system auditing, NTFS-level file auditing. |
| File analysis | https://www.manageengine.com/products/active-directory-audit/file-analysis.html | **[PRODUCT DOCS]** File analysis and storage insights — permission analysis (who has access to what), storage utilisation analysis, ROT (redundant, obsolete, trivial) data detection, ownership analysis. Best destination for anchors about: file analysis, storage analysis, permission insights, ROT data. |
| Synology file access log | https://www.manageengine.com/products/active-directory-audit/synology-file-access-log.html | **[PRODUCT DOCS]** Auditing file access logs on Synology NAS devices — tracking who accessed what files on Synology NAS, failed access attempts, file modifications on Synology. Best destination for anchors specifically about Synology NAS auditing. |
| EMC storage security auditing | https://www.manageengine.com/products/active-directory-audit/emc-storage-security-auditing-reporting.html | **[PRODUCT DOCS]** Auditing EMC (Dell EMC) storage systems — file access, modification, deletion, and permission changes on EMC Isilon and VNX/Unity devices. Best destination for anchors specifically about EMC file server or storage auditing. |
| NAS auditing software | https://www.manageengine.com/products/active-directory-audit/nas-auditing-software.html | **[PRODUCT DOCS]** NAS device auditing broadly — covering NetApp, EMC, Synology, Hitachi, Huawei, Amazon FSx, QNAP, Azure file share, CTERA, Nutanix, Qumulo; file access and change auditing across NAS platforms. Best destination for anchors about: NAS auditing generally, multi-vendor NAS file auditing. |
| NetApp filer auditing | https://www.manageengine.com/products/active-directory-audit/netapp-filer-auditing.html | **[PRODUCT DOCS]** Auditing NetApp filer (ONTAP) file systems — file access, modifications, deletions, and permission changes on NetApp storage; CIFS/NFS access auditing. Best destination for anchors specifically about NetApp auditing. |

---

### Tag: `windows-server`

| Page title | URL | What this page actually covers |
|---|---|---|
| Windows server auditing | https://www.manageengine.com/products/active-directory-audit/windows-server-auditing.html | **[PRODUCT DOCS]** Windows member server auditing overview — local logon/logoff, FIM, removable storage, printer auditing, ADFS, RADIUS/NPS, LAPS, ADLDS; comprehensive server-level auditing. Best destination for broad "Windows server auditing" anchor phrases. |
| Windows member server change audit reports | https://www.manageengine.com/products/active-directory-audit/windows-member-servers-change-audit-reports.html | **[PRODUCT DOCS]** All Windows member server change audit reports — complete report library for member server events. Best destination for anchors about: member server audit reports library. |
| Windows member server scheduled tasks and processes | https://www.manageengine.com/products/active-directory-audit/windows-member-servers-scheduled-tasks-processes-auditing.html | **[PRODUCT DOCS]** Auditing scheduled tasks and process events on Windows member servers — task creation, modification, deletion; process creation and termination; detecting suspicious scheduled task use (common persistence/lateral movement technique). Best destination for anchors about: scheduled task auditing on servers, process tracking on member servers. |
| Windows member server security logs and system events | https://www.manageengine.com/products/active-directory-audit/windows-member-servers-security-logs-system-events-auditing.html | **[PRODUCT DOCS]** Auditing Windows member server security logs and system events — security event log monitoring on servers, system event auditing, startup/shutdown events, service events. Best destination for anchors about: server security log auditing, member server system events. |
| Windows member server user rights and local policy | https://www.manageengine.com/products/active-directory-audit/windows-member-servers-users-rights-local-policy-auditing.html | **[PRODUCT DOCS]** Auditing user rights assignments and local security policies on Windows member servers — changes to local user rights and local security policy settings. Best destination for anchors about: user rights assignment auditing, local policy changes on servers. |
| Windows server failover cluster auditing | https://www.manageengine.com/products/active-directory-audit/windows-server-failover-cluster-auditing.html | **[PRODUCT DOCS]** Auditing Windows Server Failover Clusters — file access and change events across clustered file server resources; cluster role changes; node-level events. Best destination for anchors about: failover cluster auditing, clustered file server auditing. |
| AD replication status tool | https://www.manageengine.com/products/active-directory-audit/active-directory-replication-status-tool.html | **[PRODUCT DOCS]** Active Directory replication status monitoring — tracking replication health across domain controllers, detecting replication failures, replication latency monitoring. Best destination for anchors about: AD replication, domain controller replication status, replication failures. |
| LDAP change auditing | https://www.manageengine.com/products/active-directory-audit/ldap-change-auditing.html | **[PRODUCT DOCS]** Auditing LDAP-based changes to Active Directory — tracking modifications made via LDAP queries; detecting LDAP enumeration (a reconnaissance technique). Best destination for anchors about: LDAP auditing, LDAP change tracking, LDAP-based AD modifications. |
| NTLM auditing | https://www.manageengine.com/products/active-directory-audit/ntlm-auditing.html | **[PRODUCT DOCS]** Auditing NTLM authentication events — tracking NTLM logon attempts; detecting legacy NTLM usage (a security risk indicator); NTLM pass-the-hash attack detection. Best destination for anchors about: NTLM auditing, NTLM authentication tracking, legacy authentication detection. |
| Process tracking | https://www.manageengine.com/products/active-directory-audit/process-tracking.html | **[PRODUCT DOCS]** Process creation and termination tracking on Windows servers and workstations — who launched which process, when, from where; detecting unusual processes (potential malware execution, lateral movement). Best destination for anchors about: process tracking, process creation auditing, detecting suspicious process activity. |
| PowerShell logging | https://www.manageengine.com/products/active-directory-audit/powershell-logging.html | **[PRODUCT DOCS]** PowerShell script block logging and auditing — capturing PowerShell commands and scripts executed in the environment; detecting malicious PowerShell usage (common attacker technique); PowerShell-based AD changes. Best destination for anchors about: PowerShell auditing, PowerShell logging, detecting PowerShell-based attacks. |
| Scheduled tasks monitoring | https://www.manageengine.com/products/active-directory-audit/monitor-schedule-tasks.html | **[PRODUCT DOCS]** Monitoring and auditing scheduled tasks across the Windows environment — task creation, modification, deletion; detecting scheduled task persistence (common attacker technique). Best destination for anchors about: scheduled task monitoring domain-wide, detecting malicious scheduled tasks. |
| ADFS auditing and reporting | https://www.manageengine.com/products/active-directory-audit/adfs-auditing-reporting-tool.html | **[PRODUCT DOCS]** Active Directory Federation Services (ADFS) auditing — successful and failed ADFS authentication attempts, token requests, ADFS configuration changes; detecting ADFS abuse (Golden SAML attacks, token forgery). Best destination for anchors about: ADFS auditing, federation authentication monitoring, ADFS sign-in failures. |

---

### Tag: `workstation`

| Page title | URL | What this page actually covers |
|---|---|---|
| Windows workstation auditing | https://www.manageengine.com/products/active-directory-audit/windows-active-directory-workstations-auditing.html | **[PRODUCT DOCS]** Windows workstation auditing — employee work hours and productivity tracking, local logon/logoff on workstations, local account management, startup/shutdown events, FIM on workstations, system events, removable storage (USB) auditing on workstations. Best destination for broad "workstation auditing" anchor phrases. |
| Windows workstation change audit reports | https://www.manageengine.com/products/active-directory-audit/windows-active-directory-workstations-change-audit-reports.html | **[PRODUCT DOCS]** All Windows workstation change audit reports — complete report library for workstation events. Best destination for anchors about: workstation audit reports, workstation change reports. |

---

### Tag: `employee-monitoring`

| Page title | URL | What this page actually covers |
|---|---|---|
| Employee monitoring software | https://www.manageengine.com/products/active-directory-audit/employee-monitoring-software.html | **[PRODUCT DOCS]** Employee monitoring via AD logon data — tracking employee logon times, active hours, idle time, application usage; productivity analysis through logon/logoff patterns. Best destination for broad "employee monitoring" anchor phrases. |
| Employee computer monitoring software | https://www.manageengine.com/products/active-directory-audit/employee-computer-monitoring-software.html | **[PRODUCT DOCS]** Monitoring employee computer activity — computer-level activity tracking, what employees use computers for, idle vs active time per computer. Best destination for anchors about: employee computer monitoring, computer usage tracking. |
| Employee productivity tracker | https://www.manageengine.com/products/active-directory-audit/employee-productivity-tracker.html | **[PRODUCT DOCS]** Tracking employee productivity through logon activity — productive hours vs idle hours, logon duration analysis, work habit patterns. Best destination for anchors about: employee productivity tracking. |
| Employee working hours tracking | https://www.manageengine.com/products/active-directory-audit/employee-working-hours-tracking-tool.html | **[PRODUCT DOCS]** Tracking employee working hours via AD logon/logoff events — first logon and last logoff times per day, total hours logged, overtime detection. Best destination for anchors about: employee working hours tracking, time-based attendance via logon data. |
| Remote employee monitoring | https://www.manageengine.com/products/active-directory-audit/remote-employee-monitoring.html | **[PRODUCT DOCS]** Monitoring remote and work-from-home employees — tracking remote logon activity, VPN logons, remote desktop sessions for off-site employees. Best destination for anchors about: remote employee monitoring, tracking work-from-home users. |
| Employee attendance tracker | https://www.manageengine.com/products/active-directory-audit/employee-attendance-tracker.html | **[PRODUCT DOCS]** Employee attendance tracking via logon events — daily attendance records, late arrivals, early departures, absent days based on AD logon data. Best destination for anchors about: employee attendance tracking. |
| Best time tracking software | https://www.manageengine.com/products/active-directory-audit/best-time-tracking-software.html | **[PRODUCT DOCS]** Time tracking software overview — ADAudit Plus as a time tracking solution using AD logon data; features for time management. Best destination for anchors about: time tracking software, employee time management. |

---

### Tag: `laps`

| Page title | URL | What this page actually covers |
|---|---|---|
| Audit Local Administrator Password Solution | https://www.manageengine.com/products/active-directory-audit/audit-local-administrator-password-solution.html | **[PRODUCT DOCS]** Auditing LAPS (Local Administrator Password Solution) — tracking LAPS password retrievals (who retrieved which local admin password and when), LAPS configuration changes, LAPS policy changes. Best destination for anchors specifically about LAPS auditing, local admin password management auditing. |

---

### Tag: `intune`

| Page title | URL | What this page actually covers |
|---|---|---|
| Intune admin center auditing | https://www.manageengine.com/products/active-directory-audit/intune-admin-center-auditing.html | **[PRODUCT DOCS]** Auditing Microsoft Intune admin center activity — device management changes (enrolment, compliance policy changes, configuration profile changes), user and admin actions in Intune. Best destination for anchors about: Intune auditing, device management policy changes, Intune admin activity. |

---

### Tag: `removable-storage`

| Page title | URL | What this page actually covers |
|---|---|---|
| Removable storage auditing | https://www.manageengine.com/products/active-directory-audit/removable-storage-auditing.html | **[PRODUCT DOCS]** Auditing removable storage device usage — USB devices plugged into domain controllers, servers, and workstations; files copied to USB; detecting data exfiltration via removable media. Best destination for anchors about: removable storage auditing, USB device auditing, data exfiltration via USB. |

---

### Tag: `printer`

| Page title | URL | What this page actually covers |
|---|---|---|
| Printer auditing | https://www.manageengine.com/products/active-directory-audit/printer-auditing.html | **[PRODUCT DOCS]** Auditing printer usage across the Windows network — who printed what documents, on which printer, when; failed print attempts; printer configuration changes. Best destination for anchors about: printer auditing, print activity monitoring. |

---

### Tag: `siem`

| Page title | URL | What this page actually covers |
|---|---|---|
| SIEM integration | https://www.manageengine.com/products/active-directory-audit/siem-integration.html | **[PRODUCT DOCS]** ADAudit Plus SIEM integration — forwarding AD audit events to SIEM platforms (Splunk, IBM QRadar, ArcSight, etc.); log forwarding configuration; supported SIEM tools. Best destination for anchors about: SIEM integration, forwarding AD logs to SIEM, SIEM connectivity. |
| ADAudit Plus and SIEM | https://www.manageengine.com/products/active-directory-audit/adaudit-plus-siem.html | **[PRODUCT DOCS]** ADAudit Plus as a SIEM audit solution — using ADAudit Plus alongside or instead of SIEM for AD auditing; SIEM audit workflows. Best destination for anchors about: ADAudit Plus as a SIEM solution. |

---

### Tag: `hard-disk`

| Page title | URL | What this page actually covers |
|---|---|---|
| Hard disk space management | https://www.manageengine.com/products/active-directory-audit/hard-disk-space-management.html | **[PRODUCT DOCS]** Hard disk space monitoring and management — disk utilisation tracking, storage space analysis, identifying large files and folders, storage capacity planning. Best destination for anchors about: hard disk space management, disk utilisation monitoring, storage capacity. |

---

## Pages excluded from interlinking

| Page | Reason |
|---|---|
| manageengine-adsolutions-vs-netwrix-auditor.html | Competitor comparison |
| features.html | Hub/index page — too generic |
| group-policy-changes-in-real-time-using-adaudit-plus-whitepaper.html | Whitepaper |
| request-release-notification.html | Product notification signup |
| windows-file-servers-member-servers-differentiation.html | Explanatory/FAQ page |

---

## H2-to-tag quick reference

| Draft H2 topic | Relevant tags to check |
|---|---|
| What is [AD auditing topic] | `ad-change-auditing`, `ad-security` |
| Track changes across AD objects | `ad-change-auditing`, `ou-management`, `group-management` |
| Monitor logon and account lockout activity | `logon`, `lockout` |
| Audit privileged user activity | `privileged-users`, `user-management` |
| Audit Group Policy and permission changes | `gpo`, `permission-changes` |
| Detect insider threats with UBA | `uba`, `ad-security` |
| Extend auditing to hybrid and cloud environments | `entra-id`, `intune` |
| Get real-time alerts on critical changes | `ad-change-auditing`, `ad-security` |
| Meet compliance requirements | `compliance` |
| Why native tools fall short | `ad-change-auditing`, `ad-security`, `windows-server` |
| DNS and schema auditing | `dns-schema` |
| File server auditing | `file-auditing` |
| Windows server auditing | `windows-server` |
| Workstation auditing | `workstation` |
| LAPS auditing | `laps` |
| ADCS auditing | `ad-security` |
| Employee monitoring / work hours | `employee-monitoring` |
| SIEM integration | `siem` |
| Removable storage | `removable-storage` |
| Printer auditing | `printer` |

---

## Key distinctions for linking decisions

**Always check these before linking in these topic areas:**

- `attack-surface-analyzer.html` = external attacks (Kerberoasting, Golden Ticket, DCSync, brute-force, password spray as attack technique names). `insider-threat-detection.html` = internal threats only (rogue admins, careless users). Do not use insider-threat-detection for external attack anchors.

- `gpo-settings-changes-audit.html` = settings within GPOs (what a policy says, with before/after values). `gpo-change-audit-reports-list.html` = GPO object-level changes (creation, deletion, modification of GPOs themselves). These are different pages serving different anchor topics.

- `archive-active-directory-audit-data.html` = archiving process and reasons. `ad-audit-reports-from-archived-data.html` = generating reports from already-archived data. Completely different pages.

- `track-users-administrators-actions.html` despite its URL is a **user management audit page** (user lifecycle: created/deleted/modified; password changes; account enable/disable). For privileged admin activity tracking, use `privileged-user-monitoring.html` instead.

- `user-logon-audit-reports.html` and `monitor-user-logon-actions.html` contain identical content (same named report set). If linking to either, prefer `user-logon-audit-reports.html`.

- `active-directory-user-login-history.html` = per-user logon history, UBA, multi-machine sessions, RADIUS, productivity. `track-user-logon-logoff-active-directory.html` = logon AND logoff tracking with attendance, session duration, and currently-logged-on-users features. Different pages for different anchor contexts.

- `security-misconfigurations.html` = configuration gaps, CIS benchmarks, pre-attack surface reduction. NOT attack detection. For active attack detection, use `attack-surface-analyzer.html` or `active-directory-security-software.html`.

- All nine compliance standard pages (`fisma`, `gdpr`, `glba`, `hipaa`, `iso-27001`, `pci-dss`, `sox`, `active-directory-compliance-reports`, `aggregated-summary-reports`) are distinct. Use the specific standard page when a named standard appears in the anchor, not the generic compliance hub.