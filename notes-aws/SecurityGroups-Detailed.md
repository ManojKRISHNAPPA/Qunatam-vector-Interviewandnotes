# AWS Security Groups - Complete Guide

## Table of Contents
1. [What is a Security Group](#what-is-a-security-group)
2. [Why We Need Security Groups](#why-we-need-security-groups)
3. [Key Concepts](#key-concepts)
4. [How Security Groups Work](#how-security-groups-work)
5. [Use Cases](#use-cases)
6. [Advantages](#advantages)
7. [Disadvantages](#disadvantages)
8. [Practical Demonstration](#practical-demonstration)
9. [Scenario-Based Interview Questions](#scenario-based-interview-questions)

---

## What is a Security Group?

**Security Group** is a virtual firewall that controls inbound and outbound traffic for EC2 instances and other AWS resources. It acts at the instance level to allow or deny traffic based on rules you define.

**Simple Analogy:** Think of a security group as a bouncer at a club. The bouncer (security group) has a list of who's allowed in (inbound rules) and who's allowed out (outbound rules). Only people on the list get through.

**Technical Definition:** A security group is a stateful virtual firewall that controls network traffic to and from AWS resources. It operates at the instance network interface level and uses allow rules only (no deny rules).

###Key Characteristics:
- **Stateful:** Return traffic automatically allowed
- **Allow rules only:** Cannot create deny rules
- **Instance-level:** Attached to ENI (Elastic Network Interface)
- **Default deny:** All traffic denied unless explicitly allowed
- **Multiple instances:** One security group can be applied to many instances
- **Multiple security groups:** One instance can have multiple security groups

---

## Why We Need Security Groups?

### Problems Without Security Groups:
1. **No Network Protection:** All ports open to the internet
2. **Security Risks:** Vulnerable to attacks (SSH brute force, port scanning)
3. **No Access Control:** Can't restrict who accesses your instances
4. **Compliance Issues:** Unable to meet security standards
5. **Manual Firewall Management:** Tedious iptables configuration on each instance

### Security Group Solutions:
1. **Centralized Security:** Manage firewall rules from AWS Console/API
2. **Defense in Depth:** Layer of protection before traffic reaches instance
3. **Granular Control:** Specify exactly which traffic is allowed
4. **Easy Management:** Change rules instantly, apply to multiple instances
5. **Compliance Ready:** Meet security requirements with auditable rules
6. **Zero Configuration on Instance:** No iptables or Windows Firewall setup needed

### Real-World Scenario:
**Problem:** Web server hacked via open SSH port (port 22) accessible from entire internet
- **Without Security Group:** SSH open to 0.0.0.0/0, attackers brute force password
- **With Security Group:** SSH allowed only from office IP (203.0.113.0/24), attack blocked

---

## Key Concepts

### 1. Inbound Rules

**What:** Control incoming traffic TO your instance

**Rule Components:**
- **Type:** Protocol (SSH, HTTP, HTTPS, Custom TCP, etc.)
- **Protocol:** TCP, UDP, ICMP
- **Port Range:** Which port(s) to allow
- **Source:** Where traffic can come from

**Source Types:**
```
CIDR Block:
- 0.0.0.0/0 (anywhere - entire internet)
- 203.0.113.0/24 (specific IP range)
- 203.0.113.10/32 (single IP address)

Security Group ID:
- sg-0123456789abcdef0 (another security group)
- Allows traffic from instances in that security group

Prefix List ID:
- pl-xxxxx (managed IP address list, e.g., S3, CloudFront)
```

**Example Inbound Rules:**
```
Rule 1: Allow SSH from office
- Type: SSH
- Protocol: TCP
- Port: 22
- Source: 203.0.113.0/24 (office IP range)

Rule 2: Allow HTTP from anywhere
- Type: HTTP
- Protocol: TCP
- Port: 80
- Source: 0.0.0.0/0 (internet)

Rule 3: Allow MySQL from app servers
- Type: MySQL/Aurora
- Protocol: TCP
- Port: 3306
- Source: sg-app-servers (security group ID)
```

### 2. Outbound Rules

**What:** Control outgoing traffic FROM your instance

**Default Behavior:**
- Default outbound rule: Allow ALL traffic to anywhere (0.0.0.0/0)
- Most common: Keep default (allow all outbound)

**Custom Outbound Rules (Advanced):**
```
Scenario: Highly restricted environment

Remove default (allow all) and add:
- Allow HTTPS to internet (443 to 0.0.0.0/0) - for updates
- Allow MySQL to database (3306 to sg-database)
- Allow DNS (53 to VPC DNS)
```

### 3. Stateful Nature

**Critical Concept:** If inbound traffic is allowed, response is automatically allowed outbound (and vice versa)

**Example:**
```
Scenario: Web server

Inbound Rule:
- Allow HTTP (port 80) from 0.0.0.0/0

Traffic Flow:
1. User (203.0.113.50) → Web server:80 (allowed by inbound rule)
2. Web server:80 → User (203.0.113.50) (automatically allowed - stateful!)

You do NOT need to create outbound rule for response traffic!

vs Non-Stateful Firewall (Network ACL):
- Must explicitly allow both inbound and outbound
```

### 4. Default Security Group

**Every VPC has a default security group:**

**Default Rules:**
```
Inbound:
- Allow ALL traffic from instances in same security group
- Purpose: Instances can communicate with each other

Outbound:
- Allow ALL traffic to anywhere (0.0.0.0/0)
```

**Recommendation:** Don't use default SG, create custom SGs with specific rules

### 5. Security Group Limits

**Per Region Limits (Soft limits, can be increased):**
- Security Groups per VPC: 500 (can request 5,000+)
- Inbound/Outbound rules per SG: 60 each
- Security Groups per ENI: 5 (can request 16)

**Best Practice:**
- Use security group references instead of CIDR blocks (saves rules)
- Request limit increase if needed

### 6. Security Group Changes

**Propagation:**
- Changes apply immediately
- No instance reboot required
- Affects all instances using the SG instantly

**Example:**
```
1. 100 web servers use sg-web
2. You add rule: Allow port 8080 from 0.0.0.0/0
3. Change propagates in seconds to all 100 instances
4. All instances now accept traffic on port 8080
```

---

## How Security Groups Work

### Architecture

```
┌─────────────────────────────────────┐
│         Internet/VPC                │
└──────────────┬──────────────────────┘
               │
               │ Incoming Traffic
               ▼
┌──────────────────────────────────────┐
│      Security Group (sg-web)         │
│                                      │
│  Inbound Rules:                      │
│  - Port 22 from 203.0.113.0/24  ✓    │
│  - Port 80 from 0.0.0.0/0       ✓    │
│  - Port 443 from 0.0.0.0/0      ✓    │
│  - Port 3389 from anywhere      ✗    │ ← Blocked (not in rules)
│                                      │
│  Stateful: Return traffic allowed    │
└──────────────┬───────────────────────┘
               │ Allowed Traffic
               ▼
┌──────────────────────────────────────┐
│         EC2 Instance                 │
│  - Private IP: 10.0.1.50             │
│  - Public IP: 54.123.45.67           │
│  - ENI with sg-web attached          │
└──────────────────────────────────────┘
```

### Traffic Flow Example

**Scenario: User accesses website**

```
1. User (IP: 203.0.113.100) → HTTP request → EC2 Instance:80

2. Security Group Evaluation (Inbound):
   - Check: Does any rule allow 203.0.113.100 → Instance:80?
   - Rule: Allow port 80 from 0.0.0.0/0
   - Decision: ✓ ALLOW

3. Request reaches EC2 instance

4. Instance processes request, sends response

5. Security Group Evaluation (Outbound):
   - Check: Does any rule allow Instance → 203.0.113.100?
   - Stateful Decision: Inbound was allowed, so outbound automatically allowed
   - Decision: ✓ ALLOW (no outbound rule needed)

6. Response reaches user

7. Session established, subsequent packets use same stateful connection
```

**Scenario: Attacker tries SSH from unknown IP**

```
1. Attacker (IP: 198.51.100.50) → SSH request → EC2 Instance:22

2. Security Group Evaluation (Inbound):
   - Check: Does any rule allow 198.51.100.50 → Instance:22?
   - Rule: Allow port 22 from 203.0.113.0/24 only
   - 198.51.100.50 NOT in 203.0.113.0/24
   - Decision: ✗ DENY (implicit deny)

3. Packet dropped silently (no response to attacker)

4. Attacker sees connection timeout (no "connection refused")
```

### Multiple Security Groups on One Instance

**Behavior:** Rules are aggregated (OR logic)

**Example:**
```
Instance has TWO security groups:

SG-1 (sg-ssh):
- Allow port 22 from 203.0.113.0/24

SG-2 (sg-web):
- Allow port 80 from 0.0.0.0/0
- Allow port 443 from 0.0.0.0/0

Effective Rules (Combined):
- Port 22 from 203.0.113.0/24 ✓
- Port 80 from 0.0.0.0/0 ✓
- Port 443 from 0.0.0.0/0 ✓

All other traffic: ✗ DENIED
```

### Security Group Chaining

**Concept:** Reference security groups in rules instead of IP addresses

**Example:**
```
Architecture: Web Servers → App Servers → Database

SG-Web (sg-1111):
- Allow port 80/443 from 0.0.0.0/0 (internet)
- Allow outbound to sg-2222 (app servers)

SG-App (sg-2222):
- Allow port 8080 from sg-1111 (web servers only!)
- Allow outbound to sg-3333 (database)

SG-Database (sg-3333):
- Allow port 3306 from sg-2222 (app servers only!)

Benefits:
- Web servers can reach app servers ✓
- App servers can reach database ✓
- Internet CANNOT directly reach database ✗
- No need to update rules when IPs change
```

---

## Use Cases

### 1. Public Web Server

**Scenario:** Host a website accessible from internet

**Security Group Configuration:**
```
Name: sg-web-server
Description: Public web server security group

Inbound Rules:
┌──────┬──────────┬──────┬─────────────────┬─────────────────┐
│ Type │ Protocol │ Port │ Source          │ Description     │
├──────┼──────────┼──────┼─────────────────┼─────────────────┤
│ HTTP │ TCP      │ 80   │ 0.0.0.0/0       │ Web traffic     │
│ HTTPS│ TCP      │ 443  │ 0.0.0.0/0       │ Secure web      │
│ SSH  │ TCP      │ 22   │ 203.0.113.0/24  │ Admin access    │
└──────┴──────────┴──────┴─────────────────┴─────────────────┘

Outbound Rules:
- Allow ALL (default)

Why:
- HTTP/HTTPS open to world (public website)
- SSH restricted to office IP (security)
- Outbound unrestricted (can download updates)
```

### 2. Private Database Server

**Scenario:** Database accessed only by application servers

**Security Group Configuration:**
```
Name: sg-database
Description: Private database security group

Inbound Rules:
┌───────────┬──────────┬──────┬─────────────────┬────────────────┐
│ Type      │ Protocol │ Port │ Source          │ Description    │
├───────────┼──────────┼──────┼─────────────────┼────────────────┤
│ PostgreSQL│ TCP      │ 5432 │ sg-app-servers  │ App server     │
│ SSH       │ TCP      │ 22   │ sg-bastion      │ Admin via jump │
└───────────┴──────────┴──────┴─────────────────┴────────────────┘

Outbound Rules:
- Allow HTTPS to 0.0.0.0/0 (software updates)
- Allow PostgreSQL replication to sg-database-replica

Why:
- Database accessible only from app servers (security)
- SSH only via bastion host (defense in depth)
- No direct internet access (private subnet)
```

### 3. Bastion Host (Jump Server)

**Scenario:** Secure access point to private instances

**Security Group Configuration:**
```
Name: sg-bastion
Description: Bastion host for SSH access

Inbound Rules:
┌──────┬──────────┬──────┬─────────────────┬────────────────────┐
│ Type │ Protocol │ Port │ Source          │ Description        │
├──────┼──────────┼──────┼─────────────────┼────────────────────┤
│ SSH  │ TCP      │ 22   │ 203.0.113.0/24  │ Office IP only     │
└──────┴──────────┴──────┴─────────────────┴────────────────────┘

Outbound Rules:
- Allow SSH (22) to sg-private-instances

Private Instance SG:
Inbound Rules:
┌──────┬──────────┬──────┬─────────────┬──────────────────────┐
│ Type │ Protocol │ Port │ Source      │ Description          │
├──────┼──────────┼──────┼─────────────┼──────────────────────┤
│ SSH  │ TCP      │ 22   │ sg-bastion  │ Access via bastion   │
└──────┴──────────┴──────┴─────────────┴──────────────────────┘

Access Flow:
Your Office → Bastion (public subnet) → Private Instance (private subnet)
```

### 4. Load Balancer + Auto Scaling

**Scenario:** Application behind ALB with Auto Scaling

**Security Group Configuration:**
```
SG-ALB (sg-alb):
Inbound:
- HTTP (80) from 0.0.0.0/0
- HTTPS (443) from 0.0.0.0/0

Outbound:
- HTTP (80) to sg-web-servers
- HTTPS (443) to sg-web-servers

SG-Web-Servers (sg-web-servers):
Inbound:
- HTTP (80) from sg-alb
- HTTPS (443) from sg-alb
- SSH (22) from sg-bastion

Outbound:
- PostgreSQL (5432) to sg-database
- HTTPS (443) to 0.0.0.0/0 (for external APIs)

Flow:
Internet → ALB → Web Servers → Database
- Web servers ONLY accessible via ALB
- Database ONLY accessible from web servers
- No direct SSH from internet
```

### 5. Multi-Tier Application

**Scenario:** Web → App → Database architecture

**Security Groups:**
```
SG-Web (sg-web):
Inbound:
- HTTP/HTTPS from 0.0.0.0/0

Outbound:
- Port 8080 to sg-app

SG-App (sg-app):
Inbound:
- Port 8080 from sg-web

Outbound:
- Port 3306 to sg-db

SG-DB (sg-db):
Inbound:
- Port 3306 from sg-app

Result:
- Tier isolation (web can't directly access database)
- Principle of least privilege
- Defense in depth
```

---

## Advantages

### 1. **Ease of Management**
- Centralized control from AWS Console/CLI
- No need to configure iptables on each instance
- Changes apply instantly
- Can be managed via Infrastructure as Code

### 2. **Stateful Firewall**
- Return traffic automatically allowed
- Simpler rule management
- No need for complex bidirectional rules

### 3. **Scalability**
- One security group applies to unlimited instances
- Changes propagate to all instances simultaneously
- Ideal for Auto Scaling groups

### 4. **Flexibility**
- Multiple security groups per instance
- Rules aggregate (OR logic)
- Reference other security groups (dynamic)

### 5. **Security**
- Default deny (implicit deny all)
- Allow rules only (can't accidentally allow then deny)
- Instance-level protection
- No traffic bypasses security group

### 6. **Cost**
- Free! No additional charge
- No separate firewall appliances needed

### 7. **Integration**
- Works with all VPC resources (EC2, RDS, ELB, Lambda, etc.)
- CloudFormation and Terraform support
- AWS Config for compliance monitoring

### 8. **Auditability**
- All changes logged in CloudTrail
- Track who changed what and when
- Compliance reporting

---

## Disadvantages

### 1. **No Deny Rules**
- Can only allow traffic, not explicitly deny
- Can't block specific IP if broader allow rule exists
- **Workaround:** Use Network ACLs for deny rules

**Example:**
```
Problem:
- Allow SSH from 203.0.113.0/24
- Want to block specific IP 203.0.113.50 (compromised)
- Security Group: Can't deny 203.0.113.50 while allowing /24

Solution:
- Network ACL: Add explicit deny for 203.0.113.50
- Security Group + NACL = layered security
```

### 2. **Limited Logging**
- Security groups don't log traffic by default
- Can't see blocked attempts
- **Workaround:** Enable VPC Flow Logs

**Example:**
```
# VPC Flow Logs capture accepted/rejected traffic
Accepted: 203.0.113.50 → 10.0.1.100:80 (allowed by SG)
Rejected: 198.51.100.25 → 10.0.1.100:22 (blocked by SG)
```

### 3. **Not Application-Aware**
- Layer 4 firewall (TCP/UDP/ICMP)
- Can't inspect application-layer traffic
- Can't block based on HTTP URLs, SQL injection, etc.
- **Workaround:** Use WAF (Web Application Firewall) for Layer 7

### 4. **Rule Limit Per Security Group**
- Max 60 inbound + 60 outbound rules
- Can be limiting for complex environments
- **Workaround:** Use security group references, prefix lists, or multiple SGs

### 5. **Stateful Can Be Limitation**
- Can't have asymmetric routing easily
- Complex for some networking scenarios
- **Workaround:** Use Network ACLs (stateless) if needed

### 6. **No Geographic Blocking**
- Can't block traffic from specific countries
- CIDR blocks only
- **Workaround:** Use AWS WAF with geographic rules

### 7. **Propagation Delay (Rare)**
- Changes usually instant, but can take up to 60 seconds in rare cases
- Affects thousands of instances
- **Mitigation:** Test in non-production first

### 8. **Complexity with Many Security Groups**
- Troubleshooting traffic issues becomes harder
- Need to check multiple SGs
- **Mitigation:** Good naming conventions, documentation, VPC Reachability Analyzer

---

## Practical Demonstration

### Demo 1: Creating a Security Group

#### Via AWS Console:

```
1. Navigate to EC2 → Security Groups
2. Click "Create security group"

Basic Details:
- Security group name: web-server-sg
- Description: Security group for public web servers
- VPC: Select your VPC (vpc-0123456789abcdef0)

Inbound Rules:
Click "Add rule":

Rule 1:
- Type: HTTP
- Protocol: TCP (auto-filled)
- Port range: 80 (auto-filled)
- Source: Custom - 0.0.0.0/0
- Description: Allow HTTP from internet

Rule 2:
- Type: HTTPS
- Protocol: TCP
- Port range: 443
- Source: Custom - 0.0.0.0/0
- Description: Allow HTTPS from internet

Rule 3:
- Type: SSH
- Protocol: TCP
- Port range: 22
- Source: My IP (auto-detects your IP)
- Description: SSH access from my office

Outbound Rules:
- Leave default: All traffic to 0.0.0.0/0

Tags:
- Name: web-server-sg
- Environment: Production

3. Click "Create security group"
```

#### Via AWS CLI:

```bash
# Create security group
aws ec2 create-security-group \
    --group-name web-server-sg \
    --description "Security group for public web servers" \
    --vpc-id vpc-0123456789abcdef0 \
    --tag-specifications 'ResourceType=security-group,Tags=[{Key=Name,Value=web-server-sg}]'

# Output: Security Group ID (e.g., sg-0123456789abcdef0)
SG_ID="sg-0123456789abcdef0"

# Add inbound rules
# HTTP from anywhere
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0 \
    --group-rule-description "Allow HTTP from internet"

# HTTPS from anywhere
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0 \
    --group-rule-description "Allow HTTPS from internet"

# SSH from specific IP
MY_IP="203.0.113.50/32"
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr $MY_IP \
    --group-rule-description "SSH from office"

# View security group
aws ec2 describe-security-groups --group-ids $SG_ID
```

---

### Demo 2: Attaching Security Group to EC2 Instance

```bash
# Launch instance with security group
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --key-name my-key \
    --security-group-ids sg-0123456789abcdef0 \
    --subnet-id subnet-12345 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=web-server-1}]'

# Modify security group of running instance
aws ec2 modify-instance-attribute \
    --instance-id i-1234567890abcdef0 \
    --groups sg-0123456789abcdef0 sg-additional-sg

# Note: This REPLACES all security groups, not adds to them
```

---

### Demo 3: Security Group Chaining (App → Database)

```bash
# Create database security group
aws ec2 create-security-group \
    --group-name database-sg \
    --description "Database servers" \
    --vpc-id vpc-0123456789abcdef0

DB_SG="sg-database-id"

# Create application server security group
aws ec2 create-security-group \
    --group-name app-server-sg \
    --description "Application servers" \
    --vpc-id vpc-0123456789abcdef0

APP_SG="sg-app-id"

# Database SG: Allow PostgreSQL from app servers
aws ec2 authorize-security-group-ingress \
    --group-id $DB_SG \
    --protocol tcp \
    --port 5432 \
    --source-group $APP_SG \
    --group-rule-description "PostgreSQL from app servers"

# Now any instance with APP_SG can access databases with DB_SG
# Even if app server IPs change (Auto Scaling), rule still works!
```

---

### Demo 4: Modifying Existing Rules

```bash
# Remove a rule (revoke ingress)
aws ec2 revoke-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr 203.0.113.50/32

# Add updated rule
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr 203.0.113.0/24  # Changed from single IP to subnet

# Changes apply immediately to all instances
```

---

### Demo 5: Troubleshooting Connectivity

#### Scenario: Can't connect to instance on port 80

**Step 1: Check Security Group Rules**

```bash
# Describe security group
aws ec2 describe-security-groups --group-ids sg-xxxxxxxx

# Check inbound rules
# Look for: Port 80, TCP, Source 0.0.0.0/0 (or your IP)

# Common issues:
# - Port 80 not allowed
# - Wrong source IP (e.g., allowed 10.0.0.0/8 but you're 203.0.113.50)
# - Instance has different security group than you think
```

**Step 2: Verify Instance Security Groups**

```bash
# Check which SGs are attached to instance
aws ec2 describe-instances \
    --instance-ids i-xxxxxxxx \
    --query 'Reservations[0].Instances[0].SecurityGroups'

# Output shows all attached SGs
```

**Step 3: Use VPC Reachability Analyzer**

```bash
# Create path analysis
aws ec2 create-network-insights-path \
    --source i-instance-id \
    --destination i-instance-id \
    --destination-port 80 \
    --protocol tcp

# Run analysis
aws ec2 start-network-insights-analysis \
    --network-insights-path-id nip-xxxxxxxx

# View results
aws ec2 describe-network-insights-analyses \
    --network-insights-analysis-ids nia-xxxxxxxx

# Tells you exactly why traffic is blocked
```

**Step 4: Enable VPC Flow Logs**

```bash
# Create Flow Log for troubleshooting
aws ec2 create-flow-logs \
    --resource-type NetworkInterface \
    --resource-ids eni-xxxxxxxx \
    --traffic-type ALL \
    --log-destination-type cloud-watch-logs \
    --log-group-name /aws/vpc/flowlogs

# View logs to see if traffic is ACCEPT or REJECT
# REJECT indicates security group or NACL blocking
```

---

### Demo 6: Compliance Scanning with AWS Config

**Check if any instance has port 22 open to 0.0.0.0/0 (insecure)**

```bash
# AWS Config Rule (Managed Rule)
aws configservice put-config-rule \
    --config-rule file://ssh-restricted-rule.json

# ssh-restricted-rule.json:
{
  "ConfigRuleName": "restricted-ssh",
  "Description": "Checks if security groups allow SSH from 0.0.0.0/0",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "INCOMING_SSH_DISABLED"
  },
  "Scope": {
    "ComplianceResourceTypes": [
      "AWS::EC2::SecurityGroup"
    ]
  }
}

# Config will alert if any SG violates this rule
# Automated compliance monitoring
```

---

### Demo 7: Automated Security Group Cleanup

**Lambda function to remove unused security groups**

```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Get all security groups
    sgs = ec2.describe_security_groups()['SecurityGroups']

    # Get all network interfaces
    enis = ec2.describe_network_interfaces()['NetworkInterfaces']

    # Get attached SG IDs
    attached_sgs = set()
    for eni in enis:
        for group in eni['Groups']:
            attached_sgs.add(group['GroupId'])

    # Find unused security groups
    unused_sgs = []
    for sg in sgs:
        if sg['GroupName'] == 'default':
            continue  # Never delete default SG

        if sg['GroupId'] not in attached_sgs:
            unused_sgs.append(sg['GroupId'])
            print(f"Unused SG: {sg['GroupId']} - {sg['GroupName']}")

    # Optional: Delete unused SGs (be careful!)
    # for sg_id in unused_sgs:
    #     ec2.delete_security_group(GroupId=sg_id)

    return {
        'statusCode': 200,
        'body': f"Found {len(unused_sgs)} unused security groups"
    }
```

---

## Scenario-Based Interview Questions

### Question 1: Web Application Architecture

**Scenario:** Design security groups for a 3-tier web application:
- Web tier: Public-facing web servers (NGINX)
- Application tier: Application servers (Node.js)
- Database tier: PostgreSQL database

Requirements:
- Users access website via HTTPS
- Only web tier accessible from internet
- SSH access for administrators from office (203.0.113.0/24)
- Deploy in VPC 10.0.0.0/16

**Answer:**
```
Security Group Design:

1. SG-Web-Tier (sg-web):

Inbound Rules:
┌───────┬──────────┬──────┬────────────────┬─────────────────────┐
│ Type  │ Protocol │ Port │ Source         │ Description         │
├───────┼──────────┼──────┼────────────────┼─────────────────────┤
│ HTTPS │ TCP      │ 443  │ 0.0.0.0/0      │ Internet users      │
│ HTTP  │ TCP      │ 80   │ 0.0.0.0/0      │ Redirect to HTTPS   │
│ SSH   │ TCP      │ 22   │ 203.0.113.0/24 │ Admin access        │
└───────┴──────────┴──────┴────────────────┴─────────────────────┘

Outbound Rules:
┌──────────┬──────────┬──────┬──────────┬──────────────────────┐
│ Type     │ Protocol │ Port │ Dest     │ Description          │
├──────────┼──────────┼──────┼──────────┼──────────────────────┤
│ Custom   │ TCP      │ 8080 │ sg-app   │ Forward to app tier  │
│ HTTPS    │ TCP      │ 443  │ 0.0.0.0/0│ External APIs        │
└──────────┴──────────┴──────┴──────────┴──────────────────────┘

2. SG-App-Tier (sg-app):

Inbound Rules:
┌──────────┬──────────┬──────┬─────────┬───────────────────────┐
│ Type     │ Protocol │ Port │ Source  │ Description           │
├──────────┼──────────┼──────┼─────────┼───────────────────────┤
│ Custom   │ TCP      │ 8080 │ sg-web  │ From web tier only    │
│ SSH      │ TCP      │ 22   │ sg-web  │ Admin via web tier    │
└──────────┴──────────┴──────┴─────────┴───────────────────────┘

Outbound Rules:
┌───────────┬──────────┬──────┬─────────┬──────────────────────┐
│ Type      │ Protocol │ Port │ Dest    │ Description          │
├───────────┼──────────┼──────┼─────────┼──────────────────────┤
│ PostgreSQL│ TCP      │ 5432 │ sg-db   │ Database access      │
│ HTTPS     │ TCP      │ 443  │0.0.0.0/0│ External APIs/updates│
└───────────┴──────────┴──────┴─────────┴──────────────────────┘

3. SG-Database-Tier (sg-db):

Inbound Rules:
┌───────────┬──────────┬──────┬─────────┬──────────────────────┐
│ Type      │ Protocol │ Port │ Source  │ Description          │
├───────────┼──────────┼──────┼─────────┼──────────────────────┤
│ PostgreSQL│ TCP      │ 5432 │ sg-app  │ From app tier only   │
│ PostgreSQL│ TCP      │ 5432 │ sg-db   │ Replication (self)   │
│ SSH       │ TCP      │ 22   │ sg-web  │ Admin via web tier   │
└───────────┴──────────┴──────┴─────────┴──────────────────────┘

Outbound Rules:
┌───────────┬──────────┬──────┬─────────┬──────────────────────┐
│ Type      │ Protocol │ Port │ Dest    │ Description          │
├───────────┼──────────┼──────┼─────────┼──────────────────────┤
│ PostgreSQL│ TCP      │ 5432 │ sg-db   │ Replication          │
│ HTTPS     │ TCP      │ 443  │0.0.0.0/0│ OS/software updates  │
└───────────┴──────────┴──────┴─────────┴──────────────────────┘

Implementation:

```bash
# Create VPC and subnets (assumed already exists)
VPC_ID="vpc-0123456789abcdef0"

# Create Web Tier SG
WEB_SG=$(aws ec2 create-security-group \
    --group-name web-tier-sg \
    --description "Web tier security group" \
    --vpc-id $VPC_ID \
    --query 'GroupId' --output text)

aws ec2 authorize-security-group-ingress \
    --group-id $WEB_SG \
    --ip-permissions \
    IpProtocol=tcp,FromPort=443,ToPort=443,IpRanges='[{CidrIp=0.0.0.0/0,Description="HTTPS"}]' \
    IpProtocol=tcp,FromPort=80,ToPort=80,IpRanges='[{CidrIp=0.0.0.0/0,Description="HTTP"}]' \
    IpProtocol=tcp,FromPort=22,ToPort=22,IpRanges='[{CidrIp=203.0.113.0/24,Description="SSH from office"}]'

# Create App Tier SG
APP_SG=$(aws ec2 create-security-group \
    --group-name app-tier-sg \
    --description "Application tier security group" \
    --vpc-id $VPC_ID \
    --query 'GroupId' --output text)

aws ec2 authorize-security-group-ingress \
    --group-id $APP_SG \
    --protocol tcp \
    --port 8080 \
    --source-group $WEB_SG \
    --group-rule-description "App traffic from web tier"

aws ec2 authorize-security-group-ingress \
    --group-id $APP_SG \
    --protocol tcp \
    --port 22 \
    --source-group $WEB_SG \
    --group-rule-description "SSH from web tier"

# Create Database SG
DB_SG=$(aws ec2 create-security-group \
    --group-name database-tier-sg \
    --description "Database tier security group" \
    --vpc-id $VPC_ID \
    --query 'GroupId' --output text)

aws ec2 authorize-security-group-ingress \
    --group-id $DB_SG \
    --protocol tcp \
    --port 5432 \
    --source-group $APP_SG \
    --group-rule-description "PostgreSQL from app tier"

aws ec2 authorize-security-group-ingress \
    --group-id $DB_SG \
    --protocol tcp \
    --port 5432 \
    --source-group $DB_SG \
    --group-rule-description "PostgreSQL replication"

# Configure outbound rules for web tier
aws ec2 authorize-security-group-egress \
    --group-id $WEB_SG \
    --protocol tcp \
    --port 8080 \
    --destination-group $APP_SG

# Remove default allow all outbound (more restrictive)
aws ec2 revoke-security-group-egress \
    --group-id $WEB_SG \
    --protocol -1 \
    --cidr 0.0.0.0/0
```

Traffic Flow:

```
Internet → [SG-Web: 443] → Web Servers
Web Servers → [SG-App: 8080] → App Servers
App Servers → [SG-DB: 5432] → Database

Block Examples:
Internet → [SG-App: 8080] → ✗ BLOCKED (not in SG-App inbound rules)
Internet → [SG-DB: 5432] → ✗ BLOCKED (database not exposed)
Web → [SG-DB: 5432] → ✗ BLOCKED (web can't bypass app tier)
```

This completes the comprehensive Security Groups guide! Let me now create the final topic: User Data.

