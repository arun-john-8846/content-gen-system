# ADAudit Plus — Product Documentation Reference

**Purpose:** Capability verification for ME content production. Before writing any ADAudit Plus capability claim, check this file. Only describe features, reports, navigation paths, and capabilities documented here. Do not describe product features from training data memory alone.

**Source:** Live demo at demo.adauditplus.com — all report names and column headers extracted directly from the product UI. Report descriptions are derived from verified column headers, not inferred from report names.

**Product version:** Verified April 2026
**Last updated:** April 2026

---

## How to use this file

- **Before drafting any capability claim:** Search this file for the feature or report name. If it is not here, do not include the claim.
- **Before describing what a report shows:** Check the columns listed — they define exactly what data the report captures.
- **Before describing an attack the product detects:** Check Section 9 (Attack Surface Analyzer).
- **Before describing a compliance report:** Check Section 10.
- **If a capability is not in this file:** Do not include it. Flag it for verification against the live demo before adding.

---

## 1. Product overview

ADAudit Plus is a UBA-driven Active Directory change auditing and IT compliance solution. It provides real-time visibility into AD, Microsoft Entra ID (previously Azure Active Directory), Windows servers, workstations, file servers, and NAS devices.

**Core positioning (verified from product UI):**
- Real-time AD change auditing and reporting — 300+ pre-configured reports
- User behavior analytics (UBA) using machine learning to detect insider threats and privilege abuse
- Attack surface analysis for AD, Azure, AWS, and GCP environments
- IT compliance reporting for SOX, HIPAA, PCI-DSS, FISMA, GLBA, GDPR, and ISO 27001
- Centralized auditing of on-premises, cloud, and hybrid AD environments from a single console

**Scale claim (from marketing pages — verify currency before use):**
Over 280,000 organizations across 190 countries

---

## 2. Main navigation tabs

| Tab | What it covers |
|---|---|
| Active Directory | AD logon audit, AD object changes, GPO changes, compliance, DNS, LAPS, ADCS, ADFS |
| Cloud Directory | Microsoft Entra ID sign-ins, user/group/device/app/role changes, Intune, MFA, Conditional Access |
| File Audit | Windows file servers and 13 NAS device types |
| Server Audit | Windows Server, workstation, FIM, print, replication, LDAP, Sysmon, PowerShell |
| Endpoint | Workstation logon, user work hours, local user/group management |
| AD Backup | AD object backup and recovery (standalone module) |
| Analytics | UBA anomaly detection — 31 reports |
| Alerts | Alert profiles and alert history |

---

## 3. Active Directory tab

### 3.1 Logon Audit reports

**User Logon Reports**

| Report name | What it shows | Key columns verified |
|---|---|---|
| Logon Failures | All failed logon attempts across the domain with failure reason | User, Client IP, Client Host, DC, Logon Time, Event Type, Failure Reason, Event Number |
| Logon Failures based on users | Failed logons grouped by user | User, Client IP, Count, Client Host |
| Failures due to Bad Password | Logon failures caused specifically by incorrect passwords | Client Host, User, Logon Time, Client IP |
| Failures due to Bad User Name | Logon failures caused by unknown usernames | User, Client IP, Client Host, DC, Logon Time, Failure Reason |
| Day based Logon Errors | Logon errors broken down by day for trend analysis | Date, Error Count, User |
| Users First and Last Logon By Computers | First and last logon times per user per workstation | User, Client Host, First In, Last In, Client IP, Count |
| Logon Activity based on DC | All logon events grouped by domain controller | DC, User, Client IP, Logon Time, Event Type |
| Logon Activity based on IP Address | All logon events grouped by client IP address | Client IP, User, Logon Time, Count, DC |
| Domain Controller Logon Activity | All logon activity originating from domain controllers | DC, User, Logon Time, Event Type, Client IP |
| User Logon Activity | Logon events grouped by user with count | User, Client IP, Count, Client Host |
| Member Server Logon Activity | Logon activity on member servers | Server, User, Logon Time, Event Type |
| Workstation Logon Activity | Logon activity on workstations | Workstation, User, Logon Time, Event Type |
| Recent User Logon Activity | Logon events from the most recent period | User, Logon Time, Client IP, Client Host, DC |
| Last Logon on Workstations | Each user's most recent logon time on each workstation | User, Client Host, Last Logon Time |
| User's Last Logon | Most recent logon time across all systems per user | User, Last Logon Time, DC, Client Host |
| Users logged into multiple computers | Users who have concurrent or recent sessions on more than one machine | User, Computer 1, Computer 2, Logon Time |
| Currently Logged On Users | Users with active sessions at time of report generation | User, Client Host, Logon Time, DC |
| Local Logon Failures | Failed local (non-network) logon attempts on workstations | User, Client Host, Logon Time, Failure Reason |
| Interactive Logon Failure | Failed interactive (console) logon attempts | User, Client Host, Logon Time, Failure Reason |
| Logon Activity | All logon events (success and failure) | User, Logon Time, Client IP, Event Type, DC |
| Logon Duration | Time each user was logged on per session | User, Client Host, Logon Time, Logoff Time, Duration |
| Users Logon Duration on Computers | Logon duration per user per workstation | User, Client Host, Duration, Logon Time |
| User Work Hours | Active hours each user spent logged on to workstations | User, Client Host, Start Time, End Time, Work Hours |
| Remote Desktop Services Activity | RDP session activity including connections and disconnections | User, Client Host, Client IP, Session Start, Session End |
| Terminated Users Session | Sessions terminated by administrators or policy | User, Client Host, Session Time, Terminated By |
| Remote Desktop Gateway | Logon activity through Remote Desktop Gateway | User, Client IP, Gateway, Connection Time |
| RADIUS Logon Failures (NPS) | Failed Network Policy Server authentication attempts | User, Client IP, NPS Server, Failure Reason, Time |
| RADIUS Logon History (NPS) | All NPS authentication events | User, Client IP, NPS Server, Event Type, Time |
| Computer Startup and Shutdown | System startup and shutdown events per computer | Computer, Event Type, Time, Initiated By |
| Computer Last Startup and Shutdown | Most recent startup and shutdown per computer | Computer, Last Startup, Last Shutdown |
| Computers not Shutdown | Computers that have not had a recorded shutdown event | Computer, Last Startup, Days Running |
| Recently Detected Replay Attack | Kerberos replay attack detection events | User, DC, Time, Event Number |
| Special Groups have been assigned to a New Logon | Logon events where special group membership was applied | User, Group, DC, Logon Time |
| Logon Attempts by Locked out users | Logon attempts made by accounts that are currently locked out | User, Client IP, Client Host, Attempt Time |
| Logon Failures Summary | Aggregated count of logon failures by failure reason | Failure Reason, Count, Period |

**Local Logon-Logoff**

| Report name | What it shows |
|---|---|
| Logon Success | Successful local logon events |
| Logon Failure | Failed local logon events |
| Extranet Lockout | ADFS extranet lockout events |

**ADFS Auditing**

| Report name | What it shows |
|---|---|
| Logon Success | Successful ADFS authentication events |
| Logon Failure | Failed ADFS authentication events |
| Extranet Lockout | Accounts locked out via ADFS extranet lockout policy |

**Cumulative Reports**

| Report name | What it shows |
|---|---|
| All AD Changes | Every change made to any AD object across the domain |
| All AD Changes By User | All AD changes grouped by the user who made them |
| All AD Changes on DCs | All AD changes grouped by the domain controller that recorded them |
| All Users Activities | All actions performed by users across AD |
| User Activities | Activity log for a specific user |

---

### 3.2 AD Changes — User Management

All user management reports share the same core column pattern: **USER NAME | CALLER USER NAME | MODIFIED TIME | DOMAIN CONTROLLER | MODIFIED ATTRIBUTES | EVENT TYPE | CALLER MACHINE NAME | CALLER MACHINE IP | OLD VALUE | NEW VALUE**

| Report name | What it shows |
|---|---|
| Recently Created Users | New user accounts created, with creator identity and time |
| Recently Deleted Users | User accounts deleted, with who deleted them and when |
| Recently Enabled Users | User accounts re-enabled after being disabled |
| Recently Disabled Users | User accounts disabled, with who disabled them |
| Recently Moved Users | User accounts moved to a different OU |
| Renamed Users | User accounts that had their name changed |
| Recently Locked Out Users | Accounts that were locked out, with lockout source and analyzer details (columns: User, Caller, Machine, Locked Out Time, DC, Analyzer Details, Caller IP, Logon History) |
| Recently Unlocked Users | Locked accounts that were unlocked, with who unlocked them |
| Recently Password Changed Users | Accounts where the user changed their own password |
| Recently Password Set Users | Accounts where an admin reset the password |
| Password Never Expires Set Users | Accounts where the password never expires flag was enabled |
| Recently Modified Users | All user attribute changes with old and new values |
| Extended Attribute Changes | Changes to non-standard user attributes |
| User Attribute New and Old Value | Detailed before/after view of every user attribute change |
| Last Modification on Users | Most recent change made to each user account |
| Account Lockout Analyzer | Root cause analysis of account lockouts with lockout source identification |
| Recently Undeleted Users | User accounts restored from the AD Recycle Bin |

---

### 3.3 AD Changes — Group Management

Column pattern: **GROUP NAME | CALLER USER NAME | MODIFIED TIME | DOMAIN CONTROLLER | GROUP TYPE | GROUP SCOPE | MEMBER NAME | EVENT TYPE | CALLER MACHINE NAME**

| Report name | What it shows |
|---|---|
| Recently Added Members to Security Groups | Users added to security groups, with who added them |
| Recently Added Members to Distribution Groups | Users added to distribution groups |
| Recently Removed Members from Security Groups | Users removed from security groups |
| Recently Removed Members from Distribution Groups | Users removed from distribution groups |
| Group Attribute New and Old Value | Before/after view of group attribute changes |
| Recently Undeleted Groups | Groups restored from the AD Recycle Bin |
| Group Object History | Full change history for a group object |

---

### 3.4 AD Changes — Computer Management

Column pattern: **ACCOUNT NAME | CALLER USER NAME | MODIFIED TIME | DOMAIN CONTROLLER | MODIFIED ATTRIBUTES | OLD VALUE | NEW VALUE | CALLER MACHINE NAME | CALLER MACHINE IP**

| Report name | What it shows |
|---|---|
| Recently Created Computers | New computer accounts added to AD |
| Recently Deleted Computers | Computer accounts deleted from AD |
| Recently Modified Computers | Computer accounts with attribute changes |
| Recently Enabled Computers | Computer accounts re-enabled |
| Recently Disabled Computers | Computer accounts disabled |
| Recently Moved Computers | Computer accounts moved to a different OU |
| Computer Attribute New and Old Value | Before/after view of computer attribute changes |
| Recently Undeleted Computers | Computer accounts restored from the AD Recycle Bin |
| Computer Object History | Full change history for a computer object |

---

### 3.5 AD Changes — OU Management

| Report name | What it shows |
|---|---|
| Recently Created OUs | New organizational units created |
| Recently Deleted OUs | OUs deleted from AD |
| Recently Moved OUs | OUs moved within the AD hierarchy |
| Recently Modified OUs | OUs with attribute or setting changes |
| Renamed OUs | OUs that had their name changed |
| OU History | Full change history for an OU |
| Recently Undeleted OUs | OUs restored from the AD Recycle Bin |

---

### 3.6 GPO Changes

Column pattern: **GPO NAME | MODIFIED TIME | DOMAIN CONTROLLER | MODIFIED BY | SUMMARY | MODIFICATION HISTORY**

| Report name | What it shows |
|---|---|
| Recently Created GPOs | New Group Policy Objects created |
| Recently Deleted GPOs | GPOs deleted from the domain |
| Recently Modified GPOs | GPOs with any setting changes, including what changed |
| GPO Link changes | GPOs linked or unlinked from OUs, sites, or the domain |
| Recently Undeleted GPOs | GPOs restored from the AD Recycle Bin |
| GPO History | Full change history for a GPO |
| Group Policy Settings Changes | All GPO setting changes with before/after values |
| Computer Configuration Changes | Changes to the computer configuration section of GPOs |
| User Configuration Changes | Changes to the user configuration section of GPOs |
| Password Policy Changes | Changes to password policy settings within GPOs |
| Account Lockout Policy Changes | Changes to account lockout policy settings |
| Security Settings Changes | Changes to security settings within GPOs |
| Administrative Template Changes | Changes to administrative template settings |
| User Rights Assignment Changes | Changes to user rights assignments in GPOs |
| Windows Settings Changes | Changes to Windows settings within GPOs |
| Group Policy Permission Changes | Changes to GPO permissions |
| Group Policy Preferences Changes | Changes to GPO preferences |
| Group Policy Settings History | Historical record of all GPO setting changes |

---

### 3.7 Permission Changes

| Report name | What it shows |
|---|---|
| Domain Level Permission Changes | Changes to permissions at the domain root |
| OU Permission Changes | Changes to permissions on organizational units |
| Container Permission Changes | Changes to permissions on AD containers |
| GPO Permission Changes | Changes to who can edit, link, or read GPOs |
| User Permission Changes | Changes to permissions on user objects |
| Group Permission Changes | Changes to permissions on group objects |
| Computer Permission Changes | Changes to permissions on computer objects |
| Schema Permission Changes | Changes to permissions on the AD schema |
| Configuration Permission Changes | Changes to permissions on the configuration partition |
| DNS Permission Changes | Changes to permissions on DNS objects |
| AdminSDHolder Permission Changes | Changes to AdminSDHolder permissions, which propagate to protected accounts |

---

### 3.8 DNS Changes

| Report name | What it shows |
|---|---|
| DNS Nodes Added | New DNS records created |
| DNS Nodes Removed | DNS records deleted |
| DNS Nodes Modified | DNS records modified |
| DNS Zones Removed | DNS zones deleted |
| DNS Zones Modified | DNS zone settings changed |
| DNS Scavenging Activity | Automatic DNS record cleanup activity |
| DNS Zone Changes | All changes to DNS zones |
| Activity on DNS Zone | All activity on a specific DNS zone |
| DNS Node deleted | Individual DNS node deletion events |
| DNS Record Changes | All DNS record changes |
| DNS Configuration Changes | Changes to DNS server configuration |
| DNS Server Autoconfiguration | DNS server automatic configuration events |
| DNS Server Service Status | DNS service start/stop events |
| DNS Server Active Directory Integration | DNS integration with AD events |
| Advanced DNS Auditing | Extended DNS audit events including queries |

---

### 3.9 LAPS Audit

| Report name | What it shows |
|---|---|
| LAPS Password Read | Who read a LAPS-managed local administrator password, when, and from where |
| LAPS Password Expiry Changes | Changes to LAPS password expiry settings |
| Windows LAPS Password Read | Who read a Windows LAPS-managed password |
| Windows LAPS Password Expiry Changes | Changes to Windows LAPS expiry settings |
| DSRM Administrator Password Read | Who read the Directory Services Restore Mode password |

---

### 3.10 ADCS Auditing

| Report name | What it shows |
|---|---|
| All ADCS activities | All Certificate Services events |
| Certificate Request Status | Status of certificate requests (approved, denied, pending) |
| Recently Modified Requests | Certificate requests with recent changes |
| Recently Modified CA Properties | Changes to Certificate Authority properties |
| Recently Retrieved Keys | Key archival retrieval events |
| Certificate Template Changes | Changes to certificate templates |

---

### 3.11 AzureAD Password Protection

| Report name | What it shows |
|---|---|
| Password Set Success | Successful password sets that passed Azure AD password protection |
| Password Change Success | Successful password changes that passed policy |
| Password Set Failure | Password sets blocked by Azure AD banned password list |
| Password Change Failure | Password changes blocked by policy |
| Audit-only Password Set | Password sets that would have been blocked in enforced mode |
| Audit-only Password Change | Password changes that would have been blocked in enforced mode |

---

### 3.12 Compliance reports

Seven compliance standards with dedicated pre-configured report sets:

| Standard | What it covers in ADAudit Plus |
|---|---|
| SOX | SOX 302/404 — authorized/unauthorized system and data access, user logon/logoff, permission changes, GPO changes, admin activity |
| HIPAA | User access tracking, data modification records, logon failures, permission changes |
| PCI-DSS | Cardholder data environment access, logon activity, permission changes, user management |
| GLBA | Financial data access and change tracking |
| FISMA | Continuous monitoring, logon reports, change audit reports |
| GDPR | File access on sensitive shares, PII attribute changes, permission changes, logon to executive servers |
| ISO 27001 | Information security management — full AD and file audit coverage |

---

## 4. Cloud Directory tab (Microsoft Entra ID)

### 4.1 User Logon Reports

Column pattern (verified): **EVENT TYPE | USER NAME | USER DISPLAY NAME | LOGIN TIME | TENANT NAME | IP ADDRESS | DEVICE INFORMATION | GEO LOCATION | CITY | STATE | COUNTRY | ERROR CODE | FAILURE REASON | APPLICATION | MFA REQUIRED | MFA RESULT | MFA METHOD | CONDITIONAL ACCESS**

| Report name | What it shows |
|---|---|
| Logon Activity | All Entra ID sign-in events with geo-location, device info, MFA status, and Conditional Access result |
| Logon Activity by Legacy Authentication | Sign-ins using older protocols (SMTP, IMAP, POP3) that bypass MFA |
| User Last Logon | Most recent sign-in time per user |
| Logon Failures | Failed Entra ID sign-in attempts with failure reason |
| Logon Failure due to bad password | Sign-in failures caused by incorrect passwords |
| Logon Activity by IP Address | Sign-in events grouped by source IP address |
| Hybrid Logon Activity | Sign-in events for hybrid AD/Entra ID users |
| Logon Activity by Applications | Sign-in events grouped by the application accessed |
| Account Locked Out Users | Accounts locked out in Entra ID (columns include User, App, Login Time, IP, Geo, MFA details) |
| Sign-in Using Disabled Account | Attempts to sign in with a disabled Entra ID account |
| Password Change Required For Risky User | Sign-ins flagged because the account is marked as risky and requires a password change |
| Failed due to unknown username | Sign-in failures caused by a username not found in the directory |
| Logon using expired On-Premises password | Sign-ins blocked because the on-premises AD password has expired |
| Logon by using guest account redemption pending | Guest user sign-ins where the invitation has not yet been accepted |
| Unauthorized Access | Sign-in attempts blocked due to Conditional Access or policy |
| Logon using expired password | Sign-ins blocked because the Entra ID password has expired |
| Tried log-in using old password | Sign-in attempts using a previously used password |
| Tried log-in using newly created weak password | Sign-in attempts where the newly set password does not meet complexity requirements |
| Password contains username | Sign-in failures where the password contains the username (policy violation) |
| Login using invalid client secret | Application sign-in failures due to an expired or invalid client secret |
| Login on disabled application | Sign-in attempts to an application that has been disabled |
| Logon failed due to device Conditional Policy | Sign-in blocked because the device does not meet Conditional Access device compliance requirements |
| Logon failed due to conditional policy | Sign-in blocked by a Conditional Access policy |

---

### 4.2 Risk Detection

| Report name | What it shows |
|---|---|
| Risky Logon Activity | All sign-ins flagged as risky by Entra ID Identity Protection |
| Login by unfamiliarFeatures | Sign-ins from properties unfamiliar to that user |
| Login by Anonymized IP Address | Sign-ins from Tor or other IP anonymization services |
| Login by PasswordSpray Account | Sign-ins detected as part of a password spray attack |
| Impossible travel to atypical locations | Sign-ins from two geographically distant locations within an impossible travel time |
| Login by Malicious IP Address | Sign-ins from IPs flagged as malicious |
| Login by Malware Infected IPAddress | Sign-ins from IPs associated with malware-infected machines |
| Login by Suspicious IPAddress | Sign-ins from IPs with suspicious activity history |
| Login with leaked credentials | Sign-ins where the credentials appear in known breach data |

---

### 4.3 User Management (Entra ID)

| Report name | What it shows |
|---|---|
| Recently Created Users | New Entra ID user accounts created |
| Recently Deleted Users | Entra ID user accounts deleted |
| Recently Updated Users | Entra ID user accounts with attribute changes |
| Recently Enabled Users | Entra ID accounts re-enabled |
| Recently Disabled Users | Entra ID accounts disabled |
| Recently Password Changed Users | Entra ID accounts with admin-initiated password changes |
| Recently Password Reset Users | Entra ID accounts with self-service password resets |
| Recently Password Changed Users (Self-Service) | Password changes made by users through SSPR |
| Recently Restored Users | Entra ID accounts restored from the deleted users list |

---

### 4.4 Role Management

| Report name | What it shows |
|---|---|
| Recently Added Member to Role | Users or service principals assigned to Entra ID roles |
| Recently Removed Member from Role | Users or service principals removed from Entra ID roles |

---

### 4.5 Group Management (Entra ID)

| Report name | What it shows |
|---|---|
| Recently Created Groups | New Entra ID groups created |
| Recently Deleted Groups | Entra ID groups deleted |
| Recently Updated Groups | Entra ID groups with attribute changes |
| Recently Added Members to Groups | Users added to Entra ID groups |
| Recently Removed Members from Groups | Users removed from Entra ID groups |
| Recently Added Owners to Groups | Owners assigned to Entra ID groups |
| Recently Removed Owners from Groups | Owners removed from Entra ID groups |

---

### 4.6 Device Management

| Report name | What it shows |
|---|---|
| Recently Created Devices | New devices registered in Entra ID |
| Recently Deleted Devices | Devices removed from Entra ID |
| Recently Updated Devices | Devices with configuration changes |
| Recently Added Users to Devices | Users assigned to devices |
| Recently Removed Users from Devices | Users removed from devices |
| Recently Added Owners to Devices | Owners assigned to devices |
| Recently Removed Owners from Devices | Owners removed from devices |
| Recently Updated Device Configuration | Device configuration changes |
| Recently Enabled Devices | Devices re-enabled in Entra ID |
| Recently Disabled Devices | Devices disabled in Entra ID |

---

### 4.7 Application Management

| Report name | What it shows |
|---|---|
| Recently Added Application | New applications registered in Entra ID |
| Recently Deleted Application | Applications removed from Entra ID |
| Recently Updated Application | Applications with configuration changes |
| Recently Added OAuth2.0 Permission | OAuth2.0 permissions granted to applications |
| Recently Removed OAuth2.0 Permission | OAuth2.0 permissions removed from applications |
| Recently Consent to Application | User or admin consent granted to applications |
| Recently Revoke Consent Application | Consent revoked from applications |

---

### 4.8 License Management

| Report name | What it shows |
|---|---|
| Recently License Changed Users | Users with Entra ID license additions or removals |
| Recently License Changed Groups | Groups with Entra ID license changes |

---

### 4.9 Directory Management

| Report name | What it shows |
|---|---|
| Recently Updated Domains | Changes to verified or federated domains |
| Recently Updated DirSync | Changes to directory synchronization settings |
| Recently Updated Password Policy | Changes to the Entra ID password policy |

---

### 4.10 Logon Activity By MFA

| Report name | What it shows |
|---|---|
| Login with MFA disabled account | Sign-ins where MFA is not enforced for the account |
| Login with MFA enabled account | Sign-ins where MFA is enforced and completed |
| Logon Failure due to MFA failed | Sign-ins blocked because MFA verification failed |
| Logon based on MFA method | Sign-ins broken down by the MFA method used |
| Logon Activity by MFA | All sign-in activity with MFA status and method |
| MFA Usage | Summary of MFA method usage across the tenant |

---

### 4.11 Conditional Policy Changes

| Report name | What it shows |
|---|---|
| Add Conditional Policy | New Conditional Access policies created |
| Update Conditional Policy | Existing Conditional Access policies modified |
| Delete Conditional Policy | Conditional Access policies deleted |

---

### 4.12 Intune Reports

| Report name | What it shows |
|---|---|
| Intune Device Enrollment | Devices enrolled in Intune with enrollment details |
| Intune Device Sync Action | Device sync actions initiated in Intune |
| Intune Application Activity | Application deployment and usage in Intune |
| Create App Protection Policies | New app protection policies created |
| Delete Managed Device From Intune | Devices removed from Intune management |
| Restart Managed Device | Remote restart actions on managed devices |
| Device Compliance Policies | Device compliance policy changes and status |
| Device Configuration Policies | Device configuration policy changes |
| Intune Device Actions | All remote device actions performed in Intune |

---

## 5. File Audit tab

### 5.1 Supported file server types

Windows File Server, Windows File Cluster, NetApp Server (7-Mode and C-Mode), EMC Isilon, Hitachi NAS, Huawei OceanStor, EMC Server, Synology NAS, Amazon FSx, QNAP NAS, Azure File Share, CTERA Edge Filers, Nutanix Files, Qumulo NAS

### 5.2 Standard reports (available per server type and in aggregate)

Column pattern (verified): **SERVER | FILE/FOLDER NAME | LOCATION | TIME ACCESSED | USER | CLIENT MACHINE | CLIENT IP | ACCESS TYPE | OPERATION ID | FILE TYPE | PROCESS NAME | EVENT TYPE**

| Report name | What it shows |
|---|---|
| All File or Folder Changes | Every file and folder change event (create, modify, delete, move, rename, copy) |
| Files Created | Files and folders created, with who created them and where |
| Files Modified | Files modified, with who modified them, when, and from which machine |
| Files Deleted | Files deleted, with who deleted them and when |
| Files Moved | Files moved between locations, with source and destination paths |
| Files Renamed | Files renamed, with old and new names |
| Files Copy-N-Pasted | Files copied and pasted, with source, destination, and who performed the action |
| File Read Access | Successful file read events, with user, machine, and file path |
| Folder Permission Changes | Changes to folder permissions (DACL), with old and new permission values |
| Folder Audit Setting Changes (SACL) | Changes to folder audit policies (SACL) |
| Folder Owner Changes | Changes to folder ownership |
| Failed attempt to Read File | Denied file read attempts, with user, machine, and file |
| Failed attempt to Write File | Denied file write attempts |
| Failed attempt to Delete File | Denied file delete attempts |

### 5.3 Summary views

| Report name | What it shows |
|---|---|
| Summary based on Users | File activity aggregated by user with counts per operation type |
| Summary based on Servers | File activity aggregated by file server |
| Summary based on Process | File activity aggregated by process (columns: Process Name, Total Count, Success, Failure, Files Read, Modified, Created, Deleted, Moved, Renamed, Copy-Pasted, Folder Permission Changes) |
| Changes based on Users | All changes grouped by user |
| Changes based on Servers | All changes grouped by server |
| All File or Folder Changes by Server | Full change log filtered to a single server |
| All File or Folder Changes by User | Full change log filtered to a single user |
| All File or Folder Changes by Share | Full change log filtered to a single share |

---

## 6. Server Audit tab

### 6.1 Windows Server and Workstation logon

| Report name | What it shows |
|---|---|
| Logon Failures | Failed logon attempts on member servers and workstations |
| Logon Activity | All logon events on servers |
| Logon Duration | Session duration per user per server |
| User Work Hours | Time each user was actively logged on |
| Remote Desktop Services Activity | RDP connections to servers |
| Remote Desktop Gateway | RDP connections through RD Gateway |
| RADIUS Logon Failures (NPS) | Failed NPS/RADIUS authentication attempts |
| RADIUS Logon History (NPS) | All NPS authentication events |
| Credential Validation | Credential validation events on servers |
| Recently Detected Replay Attack | Kerberos replay attack events on servers |
| Wifi Logon Activity | Wireless network authentication events |

### 6.2 Local user and group management (servers)

| Report name | What it shows |
|---|---|
| Recently Created Users | Local user accounts created on servers |
| Recently Deleted Users | Local user accounts deleted |
| Recently Modified Users | Local user account attribute changes |
| Recently Enabled/Disabled Users | Local account enable/disable events |
| Recently Locked/Unlocked Users | Local account lockout and unlock events |
| Recently Password Changed/Set Users | Local password change events |
| Recently Created/Deleted Groups | Local group creation and deletion |
| Recently Added/Removed Members | Local group membership changes |

### 6.3 System events

| Report name | What it shows |
|---|---|
| System Events | All Windows system events |
| System Time Changed | Events where the system clock was changed |
| Service Install Attempted | Attempts to install a new Windows service |
| Service Started/Stopped/Failed | Service state change events |
| Startup Type Modified | Changes to service startup configuration |
| User Rights Assigned/Removed | Changes to user right assignments on servers |
| Policy Changed | Local policy changes on servers |
| Computer Startup and Shutdown | Server startup and shutdown events |
| Summary Report | Aggregated system event counts |

### 6.4 Scheduled tasks

| Report name | What it shows |
|---|---|
| Scheduled Task Created | New scheduled tasks created on servers |
| Scheduled Task Deleted | Scheduled tasks deleted |
| Scheduled Task Modified | Scheduled task configuration changes |
| Scheduled Task Disabled/Enabled | Scheduled task state changes |

### 6.5 Process tracking

| Report name | What it shows |
|---|---|
| New Process Created | New processes started on servers |
| New Process Exited | Process exit events |
| Who started the Process | Process creation with user identity |

### 6.6 Netlogon

| Report name | What it shows |
|---|---|
| Denied connection from a machine account | Connection denials for machine accounts |
| Allowed/Denied connection using a trust account | Trust-based connection events |
| Client using RPC Sign/Trust using RPC Sign | RPC signing enforcement events |
| Client Allowed/Denied using RC4 | RC4 encryption enforcement events (relevant for Kerberos hardening) |

### 6.7 User Session Recording

| Report name | What it shows |
|---|---|
| Clipboard changes | Clipboard content events captured during recorded sessions |
| File Operations | File operations captured during recorded sessions |
| Process tracking | Processes launched during recorded sessions |

### 6.8 Sysmon Auditing

| Report name | What it shows |
|---|---|
| Sysmon configuration changes | Changes to Sysmon configuration |
| Sysmon service state changes | Sysmon service start/stop events |
| Sysmon error | Sysmon error events |
| Registry audit | Registry key read and write events |
| DNS Query | DNS queries made by endpoints |
| WMI events activities | WMI-based activity events |
| Pipe activity | Named pipe connection events |
| Remote thread creation | Remote thread injection events (indicator of process injection) |
| Network connections | Network connection events captured by Sysmon |

### 6.9 Replication

| Report name | What it shows |
|---|---|
| Replica Sync History | AD replication sync history between DCs |
| Replica Source NC Changes | Changes to source naming contexts |
| Replica Destination NC Changes | Changes to destination naming contexts |
| AD Object Attributes Replication | Attribute-level replication events |
| Lingering Objects Removed From Replica | Lingering object cleanup events |
| Replication Failures | Failed replication events with error details |
| Replication Failure Details | Detailed replication error information |

### 6.10 AD LDS

| Report name | What it shows |
|---|---|
| Group/OU/GPO/User/Computer/Configuration Mgmt (AD LDS) | Change events in Active Directory Lightweight Directory Services instances |

### 6.11 LDAP

| Report name | What it shows |
|---|---|
| Unsecure LDAP Binds | LDAP binds made without SSL/TLS — a security risk |
| No of Daily Unsecure LDAP Bind | Daily count of unsecured LDAP binds |
| No of LDAP Queries | Total LDAP queries per period |
| Recent LDAP Queries | Most recent LDAP queries |
| Error from LDAP Server | LDAP server error events |
| No of rejected unsecure LDAP Binds | Count of unsecure LDAP binds that were rejected |
| Attempt to make LDAPS connection | LDAPS connection attempts |
| Time-out LDAP Connection | LDAP connection timeout events |

### 6.12 Network Share

| Report name | What it shows |
|---|---|
| Network share read | Network share read access events |
| Network share added | New network shares created |
| Network share modified | Network share configuration changes |
| Network share delete | Network shares deleted |

### 6.13 Print Server

| Report name | What it shows |
|---|---|
| Recent Jobs | Most recent print jobs with user, printer, and document details |
| User Based Reports | Print activity grouped by user |
| Printer Usage | Print job counts and activity per printer |
| Printer Based Reports | Print activity grouped by printer |

### 6.14 File Integrity Monitoring (FIM)

| Report name | What it shows |
|---|---|
| File (or) Folder Created (FIM) | Files created in FIM-monitored locations |
| File (or) Folder deleted (FIM) | Files deleted in FIM-monitored locations |
| Folder Permission Changes (FIM) | Permission changes in FIM-monitored locations |
| Folder Audit Settings (SACL) Changes (FIM) | SACL changes in FIM-monitored locations |
| File (or) Folder Modified (FIM) | File modifications in FIM-monitored locations |
| File (or) Folder Moved (or) Renamed (FIM) | File moves and renames in FIM-monitored locations |
| File (or) Folder Copy-N-Pasted (FIM) | File copy-paste events in FIM-monitored locations |
| File Write Access Failure (FIM) | Denied write attempts in FIM-monitored locations |
| File Delete Access Failure (FIM) | Denied delete attempts in FIM-monitored locations |

### 6.15 Removable Storage

| Report name | What it shows |
|---|---|
| File Read (USB) / File Modified (USB) / File Copy-N-Pasted (USB) | File operations on USB and removable devices |
| Removable Device Plug In events | Detection of removable device connections |
| File Read Access success/failure | Successful and denied file reads on removable devices |

### 6.16 PowerShell

| Report name | What it shows |
|---|---|
| Process Tracking | PowerShell process execution events |
| Script Block Logging | PowerShell script content captured via script block logging |
| Module Logging | PowerShell module load events |

---

## 7. Endpoint tab

| Report name | What it shows |
|---|---|
| Logon Failures | Failed logon attempts on workstations |
| Logon Activity | All logon events on workstations |
| User Work Hours | Active hours each user spent at their workstation |
| Remote Desktop Services Activity | RDP sessions on workstations |
| Wifi Logon Activity | Wireless network authentication on workstations |
| Computer Startup and Shutdown | Workstation startup and shutdown events |
| Computer Last Startup and Shutdown | Most recent startup and shutdown per workstation |
| Computers not Shutdown | Workstations with no recorded shutdown |
| Recently Created/Deleted/Modified Users | Local user account changes on workstations |
| Recently Enabled/Disabled Users | Local account state changes |
| Recently Locked/Unlocked Users | Local account lockout events on workstations |
| Recently Password Changed/Set Users | Local password changes on workstations |
| Recently Created/Deleted Groups | Local group changes on workstations |
| Recently Added/Removed Members | Local group membership changes on workstations |

---

## 8. Analytics tab (UBA)

ADAudit Plus applies machine learning to create a baseline of normal behavior per user, host, and domain. Reports in this tab flag deviations from that baseline.

### 8.1 Unusual Activity reports

| Report name | What it shows |
|---|---|
| Unusual Activities Summary by Type | All anomalies grouped by anomaly type |
| Unusual Activities Summary by User | All anomalies grouped by user |
| Unusual Activities Summary by Server | All anomalies grouped by server or host |
| All Threshold Breach Activity | Events where activity volume exceeded the learned threshold |
| All Unusual Time Activity | Events occurring outside the user's normal working hours |
| All First Time Resource Access | First-ever access to a resource by a user — indicator of lateral movement |

### 8.2 Logon anomalies

| Report name | What it shows |
|---|---|
| Unusual Volume of Logon Failure | Spike in logon failures for a user above their baseline — indicator of brute force |
| Unusual Logon Activity Time | Logon at an unusual time for that specific user |
| First Time Host Accessed by User | A user accessing a host they have never accessed before |
| Unusual Volume of Logon Failure on Host | Logon failure spike on a specific host |
| Unusual Logon Activity Time on Host | Logon to a specific host at an unusual time |
| First Time Remote Access on Host | First-ever RDP or remote session to a host by a user |

### 8.3 User management anomalies

| Report name | What it shows |
|---|---|
| Unusual Volume of User Management Activity | Spike in user management actions by an admin above their baseline |
| Unusual User Activity Time | Admin performing user management actions at an unusual time |

### 8.4 Lockout anomalies

| Report name | What it shows |
|---|---|
| Unusual Volume of Lockout | Spike in account lockout events above the domain baseline |
| Unusual Lockout Activity Time | Account lockouts occurring at an unusual time |

### 8.5 Process anomalies

| Report name | What it shows |
|---|---|
| New process on server | A process running on a server that has not been seen before on that server |

### 8.6 File activity anomalies

| Report name | What it shows |
|---|---|
| Unusual Volume of Failed File Accesses | Spike in denied file access attempts — indicator of unauthorized access attempts |
| Unusual Volume of File Activity | File activity volume exceeding the user's baseline — indicator of data exfiltration or ransomware |
| File Activity performed at Unusual Time | File access at an unusual time for that user |
| Unusual Volume of File Modification | Spike in file modifications — strong indicator of ransomware activity |
| Unusual Volume of File Deletions | Spike in file deletions — indicator of ransomware or deliberate data destruction |

### 8.7 Baseline reports

| Report name | What it shows |
|---|---|
| Usual Activity Volume based on User | The learned normal activity volume for each user |
| Usual Activity Time based on User | The learned normal working hours for each user |
| Usual Activity Volume based on Host | The learned normal activity volume for each host |
| Usual Activity Time based on Host | The learned normal activity time window for each host |
| Usual Lockout Volume Based On Domain | The domain baseline for account lockout frequency |
| Usual Lockout Time Based on Domain | The domain baseline for lockout timing |
| Usual Host Accessed by User | The set of hosts each user normally accesses |
| Usual Remote Access on Host | The set of users who normally remotely access each host |
| Usual Process Running in Host | The baseline set of processes running on each host |

---

## 9. Attack Surface Analyzer

ADAudit Plus detects both indicators of compromise (IoC — active attacks) and indicators of exposure (IoE — risky configurations).

**Verified from:** manageengine.com/products/active-directory-audit/attack-surface-analyzer.html — April 2026

### 9.1 AD attacks detected (IoC) — 25+ attacks

The ASA detects 25+ AD attacks across three named categories:

**Credential access attacks (examples verified from live page):**

| Attack | Description |
|---|---|
| Kerberoasting | Attacker requests service tickets for service accounts to crack offline |
| Golden Ticket attack | Attacker uses a forged Kerberos TGT to impersonate any user |
| DCSync attack | Attacker replicates AD credentials using Domain Controller replication rights |
| Silver Ticket attack | Attacker uses a forged Kerberos service ticket to access specific services |
| Pass-the-hash attack | Attacker uses a stolen NTLM hash to authenticate without knowing the password |
| Pass-the-ticket attack | Attacker uses a stolen Kerberos ticket to authenticate |
| DCShadow attack | Attacker registers a rogue DC to inject malicious changes into AD |
| Skeleton Key attack | Attacker installs a master password on the DC allowing authentication as any user |
| Brute force attacks | Repeated authentication attempts to guess a password |
| AD password spray attacks | Low-and-slow password guessing across many accounts to avoid lockout |

**Lateral movement attacks (examples verified from live page):**

| Attack | Description |
|---|---|
| Ransomware-related techniques | File modification and deletion patterns consistent with ransomware encryption |

**Privilege escalation attacks (examples verified from live page):**

| Attack | Description |
|---|---|
| RID hijacking | Attacker modifies the Relative Identifier of an account to grant it elevated privileges |

**Content writing note:** When referencing the total count, use **25+ AD attacks**. Do not list all attacks individually — the full list is not published by ME. Use category groupings (credential access, lateral movement, privilege escalation) with named examples from the table above.

### 9.2 Network and process attacks — via MITRE ATT&CK®

The ASA also detects threats beyond AD-specific attacks using the MITRE ATT&CK® framework:

- **15+ network attacks** — including techniques where adversaries abuse network protocols
- **20+ process attacks** — including Indirect Command Execution, where an adversary bypasses defense filters that restrict certain executables from running

**Content writing note:** Always include the MITRE ATT&CK® registered trademark on first mention. Use "15+ network attacks" and "20+ process attacks" — do not state specific technique names unless verified from the live demo.

### 9.3 Cloud coverage (IoE — risky configurations)

- Microsoft Azure risky configurations — with step-by-step remediation guidance based on industry benchmarks including NIST
- Amazon Web Services (AWS) risky configurations
- Google Cloud Directory (GCP) risky configurations

### 9.4 How the ASA works

- Uses an exclusive dashboard with threat insights
- Leverages rules derived from industry standards and benchmarks including NIST
- Provides drill-down into when an attack was perpetrated, by whom, from which machine, and its impact
- Shows history of threat actor actions before and after detection
- Sends real-time alerts on ongoing attack attempts
- Supports automated incident response: can shut down a device or auto-generate a ticket in ServiceNow when an alert fires

### 9.5 Licensing

ASA for AD is included in the AD (DC) license. ASA for Cloud Directory (Azure, AWS, GCP) is included in the Azure, AWS, and GCP add-on licenses. ASA is not licensed separately.

---

## 10. Alert profiles (default — verified from demo)

### AD and account alerts
- Account Lockout
- Disabled Users Logon Attempt
- Disabled Users Enabled
- Password Never Expire Enabled
- Group Membership Changes
- Default Domain Policy Modified
- Default Domain Controllers Policy Modified
- User Modifications in OU
- Computer Modifications in OU
- Group Modifications in OU
- Modified Admin Groups
- Deleted Users
- Deleted Security Groups
- Users Created
- GPO deleted
- Domain Policy Changes
- Schema Changes
- Schema Permission Changes
- Configuration Changes
- Configuration Permission Changes
- OU deleted
- System Audit Log cleared
- System Shutdown
- Attributes Changed for Domain DNS Object

### File alerts
- File (or) Folder deleted
- Folder Permission Changes
- Folder Permission Changes in FIM
- File (or) Folder deleted in FIM
- GDPR - File Access on Sensitive Shares
- GDPR - File Modified on Sensitive Shares
- GDPR - File Access Denied on Sensitive Shares
- GDPR - Folder Permission Changes on Sensitive Shares
- GDPR - Logon Access On Executive Servers
- GDPR - PII user attributes changed

### Security and threat alerts
- Possible Ransomware activity detected
- AdminSDHolder Permission Changes
- Unable to log Security log events
- A replay attack was detected
- Detects PowerShell Base64 encoded Shellcode
- Privilege Escalation - First time Utilizing a Privilege

### UBA-driven alerts
- Unusual Activity - File Activity Count (Based on User)
- Unusual Activity - File Failure Count (Based on User)
- Unusual Activity - File Activity Time (Based on User)
- Unusual Logon Activity Time

### ADCS, LDAP, and Azure alerts
- Certificate Service audit filter
- Certificate template modified
- Certificate Authority security or permission settings
- LDAP Authentication
- AzureAD Password Modification Failed
- AzureAD Password Modification in Audit-Only mode

### USB alerts
- Removable Plug In - DiskDrive

---

## 11. Report export formats

All reports can be exported in: **CSV, PDF, HTML, CSVDE, XLSX**

Reports can be scheduled for automatic delivery by email.

---

## 12. Integration capabilities

### SIEM
- Supports SIEM integration for log forwarding

### Ticketing systems (verified from demo UI)
- ServiceNow
- Zendesk
- ManageEngine Service Desk Plus
- Freshservice
- Jira
- Kayako

### Authentication and SSO
- NTLM-based SSO
- SAML-based SSO (Okta, OneLogin, Ping Identity, ADFS, custom identity providers)
- Two-factor authentication: email, SMS, Google Authenticator, RSA SecurID, Duo Security, RADIUS

---

## 13. What NOT to attribute to ADAudit Plus

| Capability | Correct product |
|---|---|
| Data loss prevention (DLP) | DataSecurity Plus |
| Email and Exchange auditing | Exchange Reporter Plus |
| Microsoft 365 management | M365 Manager Plus |
| Self-service password reset / MFA / SSO for end users | ADSelfService Plus |
| Full AD management and provisioning (create/modify/delete users at scale) | ADManager Plus |
| Full SIEM and log management | Log360 / EventLog Analyzer |
| Enterprise backup and recovery (beyond AD objects) | RecoveryManager Plus |
| SharePoint auditing | SharePoint Manager Plus |

---

## 14. Related ManageEngine products

| Product | Purpose |
|---|---|
| ADManager Plus | Active Directory, Microsoft 365, and Exchange management and reporting |
| ADSelfService Plus | Self-service password management, MFA, SSO |
| EventLog Analyzer | Real-time log analysis and reporting |
| DataSecurity Plus | File server auditing and data discovery |
| Exchange Reporter Plus | Exchange Server auditing and reporting |
| M365 Manager Plus | Microsoft 365 management and reporting |
| RecoveryManager Plus | Enterprise backup and recovery |
| Log360 | Comprehensive SIEM and UEBA |
| AD360 | Integrated identity and access management |

---

## 15. Navigation paths — complete report paths

Use these paths when describing how to access a report in content.

### Active Directory tab

| Report | Full navigation path |
|---|---|
| User Logon Activity | Active Directory > Logon Audit > User Logon Reports > User Logon Activity |
| Logon Failures | Active Directory > Logon Audit > User Logon Reports > Logon Failures |
| Logon Failures based on users | Active Directory > Logon Audit > User Logon Reports > Logon Failures based on users |
| Failures due to Bad Password | Active Directory > Logon Audit > User Logon Reports > Failures due to Bad Password |
| Failures due to Bad User Name | Active Directory > Logon Audit > User Logon Reports > Failures due to Bad User Name |
| Domain Controller Logon Activity | Active Directory > Logon Audit > User Logon Reports > Domain Controller Logon Activity |
| Member Server Logon Activity | Active Directory > Logon Audit > User Logon Reports > Member Server Logon Activity |
| Workstation Logon Activity | Active Directory > Logon Audit > User Logon Reports > Workstation Logon Activity |
| Last Logon on Workstations | Active Directory > Logon Audit > User Logon Reports > Last Logon on Workstations |
| User's Last Logon | Active Directory > Logon Audit > User Logon Reports > User's Last Logon |
| Users logged into multiple computers | Active Directory > Logon Audit > User Logon Reports > Users logged into multiple computers |
| Currently Logged On Users | Active Directory > Logon Audit > User Logon Reports > Currently Logged On Users |
| User Work Hours | Active Directory > Logon Audit > User Logon Reports > User Work Hours |
| Remote Desktop Services Activity | Active Directory > Logon Audit > User Logon Reports > Remote Desktop Services Activity |
| RADIUS Logon Failures (NPS) | Active Directory > Logon Audit > User Logon Reports > RADIUS Logon Failures(NPS) |
| Computer Startup and Shutdown | Active Directory > Logon Audit > User Logon Reports > Computer Startup and Shutdown |
| Recently Detected Replay Attack | Active Directory > Logon Audit > User Logon Reports > Recently Detected Replay Attack |
| Account Lockout Analyzer | Active Directory > AD Changes > User Management > Account Lockout Analyzer |
| Logon Failures Summary | Active Directory > Logon Audit > User Logon Reports > Logon Failures Summary |
| Logon Success (ADFS) | Active Directory > Logon Audit > Local Logon-Logoff > Logon Success |
| Extranet Lockout | Active Directory > Logon Audit > Local Logon-Logoff > Extranet Lockout |
| All AD Changes | Active Directory > Logon Audit > Cumulative Reports > All AD Changes |
| All AD Changes By User | Active Directory > Logon Audit > Cumulative Reports > All AD Changes By User |
| All Users Activities | Active Directory > Logon Audit > Cumulative Reports > All Users Activities |
| Recently Created Users | Active Directory > AD Changes > User Management > Recently Created Users |
| Recently Deleted Users | Active Directory > AD Changes > User Management > Recently Deleted Users |
| Recently Enabled Users | Active Directory > AD Changes > User Management > Recently Enabled Users |
| Recently Disabled Users | Active Directory > AD Changes > User Management > Recently Disabled Users |
| Recently Locked Out Users | Active Directory > AD Changes > User Management > Recently Locked Out Users |
| Recently Unlocked Users | Active Directory > AD Changes > User Management > Recently Unlocked Users |
| Recently Password Changed Users | Active Directory > AD Changes > User Management > Recently Password Changed Users |
| Recently Password Set Users | Active Directory > AD Changes > User Management > Recently Password Set Users |
| Recently Modified Users | Active Directory > AD Changes > User Management > Recently Modified Users |
| User Attribute New and Old Value | Active Directory > AD Changes > User Management > User Attribute New and Old Value |
| Recently Undeleted Users | Active Directory > AD Changes > User Management > Recently Undeleted Users |
| Recently Added Members to Security Groups | Active Directory > AD Changes > Group Management > Recently Added Members to Security Groups |
| Recently Removed Members from Security Groups | Active Directory > AD Changes > Group Management > Recently Removed Members from Security Groups |
| Recently Created Groups | Active Directory > AD Changes > Group Management > Recently Created Groups (via Account Management) |
| Recently Created Computers | Active Directory > AD Changes > Computer Management > Recently Created Computers |
| Computer Attribute New and Old Value | Active Directory > AD Changes > Computer Management > Computer Attribute New and Old Value |
| Recently Created OUs | Active Directory > AD Changes > OU Management > Recently Created OUs |
| Recently Created GPOs | Active Directory > GPO Changes > GPO Management > Recently Created GPOs |
| GPO Link changes | Active Directory > GPO Changes > GPO Management > GPO Link changes |
| Group Policy Settings Changes | Active Directory > GPO Changes > GPO Setting Changes > Group Policy Settings Changes |
| Password Policy Changes | Active Directory > GPO Changes > GPO Setting Changes > Password Policy Changes |
| Account Lockout Policy Changes | Active Directory > GPO Changes > GPO Setting Changes > Account Lockout Policy Changes |
| AdminSDHolder Permission Changes | Active Directory > AD Changes > Permission Changes > AdminSDHolder Permission Changes |
| OU Permission Changes | Active Directory > AD Changes > Permission Changes > OU Permission Changes |
| DNS Nodes Added | Active Directory > AD Changes > DNS Changes > DNS Nodes Added |
| Advanced DNS Auditing | Active Directory > AD Changes > DNS Changes > Advanced DNS Auditing |
| LAPS Password Read | Active Directory > AD Changes > LAPS Audit > LAPS Password Read |
| Windows LAPS Password Read | Active Directory > AD Changes > LAPS Audit > Windows LAPS Password Read |
| Certificate Request Status | Active Directory > AD Changes > ADCS Auditing > Certificate Request Status |
| Certificate Template Changes | Active Directory > AD Changes > ADCS Auditing > Certificate Template Changes |
| SOX | Active Directory > Compliance > SOX |
| HIPAA | Active Directory > Compliance > HIPAA |
| PCI-DSS | Active Directory > Compliance > PCI-DSS |
| GLBA | Active Directory > Compliance > GLBA |
| FISMA | Active Directory > Compliance > FISMA |
| GDPR | Active Directory > Compliance > GDPR |
| ISO 27001 | Active Directory > Compliance > ISO 27001 |

### Cloud Directory tab

| Report | Full navigation path |
|---|---|
| Logon Activity | Cloud Directory > User Logon Reports > Logon Activity |
| Logon Failures | Cloud Directory > User Logon Reports > Logon Failures |
| User Last Logon | Cloud Directory > User Logon Reports > User Last Logon |
| Logon Activity by Legacy Authentication | Cloud Directory > User Logon Reports > Logon Activity by Legacy Authentication |
| Risky Logon Activity | Cloud Directory > Risk Detection > Risky Logon Activity |
| Impossible travel to atypical locations | Cloud Directory > Risk Detection > Impossible travel to atypical locations |
| Login with leaked credentials | Cloud Directory > Risk Detection > Login with leaked credentials |
| Login by Anonymized IP Address | Cloud Directory > Risk Detection > Login by Anonymized IP Address |
| Login by PasswordSpray Account | Cloud Directory > Risk Detection > Login by PasswordSpray Account |
| Recently Created Users (Entra ID) | Cloud Directory > User Management > Recently Created Users |
| Recently Added Member to Role | Cloud Directory > Role Management > Recently Added Member to Role |
| Recently Created Groups (Entra ID) | Cloud Directory > Group Management > Recently Created Groups |
| Recently Created Devices | Cloud Directory > Device Management > Recently Created Devices |
| Recently Added Application | Cloud Directory > Application Management > Recently Added Application |
| Recently Added OAuth2.0 Permission | Cloud Directory > Application Management > Recently Added OAuth2.0 Permission |
| Recently Consent to Application | Cloud Directory > Application Management > Recently Consent to Application |
| Logon Activity by MFA | Cloud Directory > Logon Activity By MFA > Logon Activity by MFA |
| Add Conditional Policy | Cloud Directory > Conditional Policy Changes > Add Conditional Policy |
| Intune Device Enrollment | Cloud Directory > Intune Reports > Intune Device Enrollment |
| Device Compliance Policies | Cloud Directory > Intune Reports > Device Compliance Policies |

### File Audit tab

| Report | Full navigation path |
|---|---|
| All File or Folder Changes (Windows) | File Audit > Windows File Server > All File or Folder Changes |
| Files Created | File Audit > [Server Type] > Files Created |
| Files Modified | File Audit > [Server Type] > Files Modified |
| Files Deleted | File Audit > [Server Type] > Files Deleted |
| File Read Access | File Audit > [Server Type] > File Read Access |
| Folder Permission Changes | File Audit > [Server Type] > Folder Permission Changes |
| Failed attempt to Delete File | File Audit > [Server Type] > Failed attempt to Delete File |
| Summary based on Users | File Audit > Windows File Server > Summary based on Users |
| Summary based on Process | File Audit > Windows File Server > Summary based on Process |
| All File or Folder Changes by User | File Audit > Windows File Server > All File or Folder Changes by User |

### Server Audit tab

| Report | Full navigation path |
|---|---|
| Logon Failures (servers) | Server Audit > Member Servers > Logon Failures |
| User Work Hours (servers) | Server Audit > Member Servers > User Work Hours |
| Remote Desktop Services Activity (servers) | Server Audit > Member Servers > Remote Desktop Services Activity |
| Script Block Logging | Server Audit > Member Servers > Script Block Logging |
| Unsecure LDAP Binds | Server Audit > Member Servers > Unsecure LDAP Binds |
| Network share added | Server Audit > Member Servers > Network share added |
| Scheduled Task Created | Server Audit > Member Servers > Scheduled Task Created |
| New Process Created | Server Audit > Member Servers > New Process Created |
| Service Started | Server Audit > Member Servers > Service Started |
| Replication Failures | Server Audit > Member Servers > Replication Failures |
| File (or) Folder Created (FIM) | Server Audit > File Integrity > File (or) Folder Created (FIM) |
| Printer Usage | Server Audit > Print Server > Printer Usage |
| Remote thread creation | Server Audit > Member Servers > Sysmon Auditing > Remote thread creation |
| Registry audit | Server Audit > Member Servers > Sysmon Auditing > Registry audit |
| File Read (USB) | Server Audit > Member Servers > Removable Storage > File Read (USB) |

### Analytics tab

| Report | Full navigation path |
|---|---|
| Unusual Activities Summary by User | Analytics > Unusual Activities Summary by User |
| Unusual Volume of Logon Failure | Analytics > Unusual Volume of Logon Failure |
| Unusual Logon Activity Time | Analytics > Unusual Logon Activity Time |
| First Time Host Accessed by User | Analytics > First Time Host Accessed by User |
| Unusual Volume of File Deletions | Analytics > Unusual Volume of File Deletions |
| Unusual Volume of File Activity | Analytics > Unusual Volume of File Activity |
| Usual Activity Volume based on User | Analytics > Usual Activity Volume based on User |

---

## 16. Event ID to report mapping

The most commonly referenced Windows Event IDs and which ADAudit Plus reports surface them. Source: ManageEngine Event ID library at manageengine.com/products/active-directory-audit/kb/windows-event-log-id-list.html

### Logon and authentication

| Event ID | What it records | ADAudit Plus report(s) |
|---|---|---|
| 4624 | Successful logon | Logon Activity, User Logon Activity, Domain Controller Logon Activity, Workstation Logon Activity, Member Server Logon Activity |
| 4625 | Failed logon | Logon Failures, Failures due to Bad Password, Failures due to Bad User Name, Logon Failures based on users |
| 4634 | Account logged off | Logon Duration, User Work Hours, Local Logon-Logoff |
| 4647 | User initiated logoff | Logon Duration, Local Logon-Logoff |
| 4648 | Logon using explicit credentials | Logon Activity, All AD Changes |
| 4649 | Replay attack detected | Recently Detected Replay Attack |
| 4768 | Kerberos TGT requested | Logon Activity, Attack Surface Analyzer (Golden Ticket detection) |
| 4769 | Kerberos service ticket requested | Attack Surface Analyzer (Kerberoasting detection), Logon Activity |
| 4770 | Kerberos service ticket renewed | Logon Activity |
| 4771 | Kerberos pre-authentication failed | Logon Failures, Attack Surface Analyzer |
| 4776 | Domain controller validated credentials | Logon Failures, Failures due to Bad Password |
| 4778 | Session reconnected to a Window Station | Remote Desktop Services Activity |
| 4779 | Session disconnected from a Window Station | Remote Desktop Services Activity, Terminated Users Session |
| 4800 | Workstation locked | Logon Duration, User Work Hours |
| 4801 | Workstation unlocked | Logon Duration, User Work Hours |

### Account management

| Event ID | What it records | ADAudit Plus report(s) |
|---|---|---|
| 4720 | User account created | Recently Created Users |
| 4722 | User account enabled | Recently Enabled Users |
| 4723 | Password change attempted by user | Recently Password Changed Users |
| 4724 | Password reset by administrator | Recently Password Set Users |
| 4725 | User account disabled | Recently Disabled Users |
| 4726 | User account deleted | Recently Deleted Users |
| 4727 | Security-enabled global group created | Recently Created Groups |
| 4728 | Member added to security-enabled global group | Recently Added Members to Security Groups |
| 4729 | Member removed from security-enabled global group | Recently Removed Members from Security Groups |
| 4730 | Security-enabled global group deleted | Group Management reports |
| 4731 | Security-enabled local group created | Recently Created Groups |
| 4732 | Member added to security-enabled local group | Recently Added Members to Security Groups |
| 4733 | Member removed from security-enabled local group | Recently Removed Members from Security Groups |
| 4735 | Security-enabled local group changed | Security Groups Modified |
| 4737 | Security-enabled global group changed | Security Groups Modified |
| 4738 | User account changed (any attribute) | Recently Modified Users, User Attribute New and Old Value |
| 4739 | Domain Policy changed | Password Policy Changes, Account Lockout Policy Changes |
| 4740 | User account locked out | Recently Locked Out Users, Account Lockout Analyzer |
| 4741 | Computer account created | Recently Created Computers |
| 4742 | Computer account changed | Recently Modified Computers, Computer Attribute New and Old Value |
| 4743 | Computer account deleted | Recently Deleted Computers |
| 4754 | Security-enabled universal group created | Recently Created Groups |
| 4755 | Security-enabled universal group changed | Security Groups Modified |
| 4756 | Member added to security-enabled universal group | Recently Added Members to Security Groups |
| 4757 | Member removed from security-enabled universal group | Recently Removed Members from Security Groups |
| 4767 | User account unlocked | Recently Unlocked Users |
| 4781 | Account name changed | Renamed Users |
| 4798 | User's local group membership enumerated | A user's local group membership was enumerated |
| 4799 | Security-enabled local group membership enumerated | A security-enabled local group membership was enumerated |

### Privilege and policy

| Event ID | What it records | ADAudit Plus report(s) |
|---|---|---|
| 4703 | Token right adjusted | User Rights Assigned/Removed |
| 4704 | User right assigned | User Rights Assigned |
| 4705 | User right removed | User Rights Removed |
| 4706 | New trust created to a domain | Domain Object Changes |
| 4707 | Trust to a domain removed | Domain Object Changes |
| 4713 | Kerberos policy changed | GPO Setting Changes |
| 4715 | Audit policy changed | Security Settings Changes |
| 4716 | Trusted domain information modified | Domain Object Changes |
| 4717 | System security access granted to account | User Rights Assignment Changes |
| 4718 | System security access removed from account | User Rights Assignment Changes |
| 4719 | System audit policy changed | Security Settings Changes, Administrative Template Changes |

### Object access and file events

| Event ID | What it records | ADAudit Plus report(s) |
|---|---|---|
| 4656 | Handle to an object requested | File Read Access, Failed attempt to Read/Write/Delete File |
| 4657 | Registry value modified | Registry audit (Sysmon) |
| 4658 | Handle to an object closed | File Read Access |
| 4660 | Object deleted | Files Deleted |
| 4663 | Access to an object attempted | File Read Access, Failed attempt to Read/Write/Delete File |
| 4670 | Permissions on an object changed | Folder Permission Changes, User/Group/Computer/OU Permission Changes |
| 4698 | Scheduled task created | Scheduled Task Created |
| 4699 | Scheduled task deleted | Scheduled Task Deleted |
| 4700 | Scheduled task enabled | Scheduled Task Enabled |
| 4701 | Scheduled task disabled | Scheduled Task Disabled |
| 4702 | Scheduled task updated | Scheduled Task Modified |

### GPO and directory service

| Event ID | What it records | ADAudit Plus report(s) |
|---|---|---|
| 5136 | Directory service object modified | DNS Nodes Modified, DNS Record Changes, All AD Changes, Recently Modified (users/computers/groups/OUs) |
| 5137 | Directory service object created | DNS Nodes Added, Recently Created (users/computers/groups/OUs/GPOs) |
| 5138 | Directory service object undeleted | Recently Undeleted (users/computers/groups/OUs) |
| 5139 | Directory service object moved | Recently Moved (users/computers/OUs) |
| 5141 | Directory service object deleted | DNS Nodes Removed, Recently Deleted (users/computers/groups/OUs/GPOs) |

### System events

| Event ID | What it records | ADAudit Plus report(s) |
|---|---|---|
| 4608 | Windows starting up | Computer Startup and Shutdown |
| 4609 | Windows shutting down | Computer Startup and Shutdown, System Shutdown |
| 4616 | System time changed | System Time Changed |
| 4688 | New process created | New Process Created, Process Tracking |
| 4689 | Process exited | New Process Exited |

### ADCS (Certificate Services)

| Event ID | What it records | ADAudit Plus report(s) |
|---|---|---|
| 4886 | Certificate request received | Certificate Request Status |
| 4887 | Certificate request approved | Certificate Request Status |
| 4888 | Certificate request denied | Certificate Request Status |
| 4889 | Certificate request status set | Certificate Request Status |
| 4890 | Certificate Services configuration changed | Recently Modified CA Properties |
| 4898 | Certificate Services loaded a template | Certificate Template Changes |

---

## 17. Edition and feature comparison

Source: manageengine.com/products/active-directory-audit/compare-editions.html (verified April 2026)

### Two paid editions: Standard and Professional

| Feature | Standard | Professional |
|---|---|---|
| AD security auditing | Yes | Yes |
| Attack surface analyzer (AD) | Yes | Yes |
| AD user logon monitoring | Yes | Yes |
| Failed logon analysis | Yes | Yes |
| User account management auditing | Yes | Yes |
| Permission change tracking | Yes — but old/new permission values unavailable | Yes — full old/new values |
| GPO settings change auditing | Yes | Yes |
| Account lockout analyzer | Yes | Yes |
| Account lockout auditing | Yes | Yes |
| AD object attribute change auditing | Yes — but old/new attribute values unavailable | Yes — full old/new values |
| AD group change monitoring | Yes | Yes |
| DNS change reporting | Yes — but old/new DNS values unavailable | Yes — full old/new values |
| Microsoft Entra password protection | Yes | Yes |
| AD change email and SMS alerts | Yes | Yes |
| UBA-focused AD threat detector | Yes | Yes |
| FSMO role change auditing | Yes | Yes |
| Sysmon auditing | Yes | Yes |
| Schema, contacts, and configuration auditing | Yes | Yes |
| LAPS auditing | Yes | Yes |
| Compliance reporting (SOX, HIPAA, PCI-DSS, FISMA, GLBA, GDPR, ISO 27001) | Yes | Yes |
| Database support | Yes | Yes |
| ADCS auditing | Yes | Yes |

### Standard vs Professional — the three key differences

1. **Permission changes** — Standard shows that a permission changed but not what the old or new value was. Professional shows both.
2. **AD object attribute changes** — Standard shows that an attribute changed but not the before/after values. Professional shows both.
3. **DNS changes** — Standard shows that a DNS record changed but not the old or new value. Professional shows both.

### Pricing (verify at compare-editions page before use — may change)

| Edition | Starting price |
|---|---|
| Standard | $595 for 2 domain controllers |
| Professional | $945 for 2 domain controllers |
| Free | 25 workstations only; data from evaluation period only |

### Additional capability modules

ADAudit Plus covers the following capability areas, all available with both Standard and Professional editions:

| Capability | What it covers |
|---|---|
| Microsoft Entra ID auditing | Entra ID security auditing + Attack Surface Analyzer for Azure, AWS, GCP |
| File auditing | Windows file servers, Windows File Cluster, NetApp, EMC, Synology, Hitachi, Huawei, QNAP, Amazon FSx, Azure Files, Nutanix, CTERA, Qumulo |
| Windows Server auditing | Member server and workgroup server auditing + ASA CIS benchmark scanning (350+ checks) |
| Workstation auditing | Windows and Mac workstation auditing + ASA CIS benchmark scanning |
| AD Backup and Recovery | Incremental AD backups, point-in-time recovery, domain/schema restoration |
| File Analysis | Storage analysis, permission analysis, file ownership analysis |

**Content writing note — Attack Surface Analyzer scope:**
- The ASA for **AD attacks** (Kerberoasting, Golden Ticket, DCSync, etc.) covers on-premises AD and is available in the base product.
- The ASA for **cloud configurations** (Azure, AWS, GCP) is part of the Microsoft Entra ID capability module.

---

## 18. Update log and maintenance instructions

| Date | Change |
|---|---|
| April 2026 | Initial build — report names and descriptions from live demo at demo.adauditplus.com |
| April 2026 | Added verified column headers and one-line descriptions for all reports |
| April 2026 | Added Section 16 (navigation paths), Section 17 (Event ID mapping), Section 18 (edition comparison) |
| April 2026 | Report count corrected from 200+ to 300+ based on ME's own published product page |
| April 2026 | Section 9 (Attack Surface Analyzer) updated — corrected IoC count from 10 named attacks to 25+; added network attack category (15+) and process attack category (20+) via MITRE ATT&CK®; added RID hijacking and ransomware as named attack examples; added IoE remediation detail; added ASA licensing section. Source: manageengine.com/products/active-directory-audit/attack-surface-analyzer.html |

**When to update this file:**
- New ADAudit Plus version released — check: manageengine.com/products/active-directory-audit/help/intro/release-notes.html
- New data source added — update Sections 5 and 11
- Report renamed or removed — update Sections 3–8 and Section 16
- New attack type in Attack Surface Analyzer — update Section 9
- Edition or pricing changes — update Section 18; always re-verify at compare-editions page

**How to verify a specific report:**
1. Go to demo.adauditplus.com → Administrator Login
2. Navigate to the report
3. Run in browser console: `Array.from(document.querySelectorAll('th')).map(c=>c.innerText.trim()).filter(t=>t.length>1).join(' | ')`
4. Update the description and columns in this file

**How to verify editions:**
Always check: manageengine.com/products/active-directory-audit/compare-editions.html

**Do not update from:** blog posts, third-party reviews, or training data memory. Always use the live demo or official ManageEngine pages as the source.