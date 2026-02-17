# Amazon EBS Snapshots - Complete Guide

## Table of Contents
1. [What are EBS Snapshots](#what-are-ebs-snapshots)
2. [Why We Need Snapshots](#why-we-need-snapshots)
3. [Key Concepts](#key-concepts)
4. [How Snapshots Work](#how-snapshots-work)
5. [Use Cases](#use-cases)
6. [Advantages](#advantages)
7. [Disadvantages](#disadvantages)
8. [Practical Demonstration](#practical-demonstration)
9. [Scenario-Based Interview Questions](#scenario-based-interview-questions)

---

## What are EBS Snapshots?

**Amazon EBS Snapshots** are point-in-time copies of EBS volumes that are stored in Amazon S3. They capture the entire state of a volume at a specific moment.

**Simple Analogy:** Think of a snapshot like taking a photograph of your hard drive. The photo captures everything at that moment. If your hard drive crashes later, you can recreate it from the photo.

**Technical Definition:** Snapshots are incremental backups stored in S3, replicated across multiple Availability Zones within a region. Each snapshot contains only the blocks that have changed since the last snapshot.

### Key Characteristics:
- **Incremental:** Only changed blocks are saved after the first snapshot
- **Point-in-time:** Captures volume state at creation moment
- **Durable:** Stored in S3 with 99.999999999% (11 nines) durability
- **Regional:** Available throughout the region
- **Restorable:** Create new volumes from snapshots
- **Shareable:** Can be shared with other AWS accounts
- **Portable:** Can be copied to other regions

---

## Why We Need Snapshots?

### Problems Without Snapshots:
1. **Data Loss Risk:** Hardware failure, accidental deletion, corruption
2. **No Disaster Recovery:** Can't recover from regional failures
3. **Difficult Migrations:** Can't easily move data across AZs/regions
4. **No Point-in-Time Recovery:** Can't restore to previous state
5. **Manual Backup Complexity:** Error-prone, time-consuming

### Snapshot Solutions:
1. **Backup & Recovery:** Protect against data loss
2. **Disaster Recovery:** Copy snapshots to another region
3. **Data Migration:** Move volumes across AZs or regions
4. **Environment Cloning:** Create dev/test from production data
5. **Cost Savings:** Archive old data in snapshot form (delete volume)
6. **Compliance:** Meet backup retention requirements

### Real-World Scenario:
**Problem:** Ransomware encrypts your database server
- **Without Snapshots:** Pay ransom or lose all data
- **With Snapshots:** Restore from yesterday's snapshot, lose only 1 day of data (or less with frequent snapshots)

---

## Key Concepts

### 1. Incremental Backups

**First Snapshot (Full):**
```
Volume: 100 GB (50 GB used)
Snapshot 1: Copies all 50 GB of used data
Storage cost: 50 GB
```

**Second Snapshot (Incremental):**
```
Volume: 100 GB (55 GB used, 5 GB changed)
Snapshot 2: Copies only the 5 GB of changed blocks
Storage cost: 55 GB total (50 GB + 5 GB)
```

**Benefits:**
- Faster snapshot creation (only delta copied)
- Lower storage costs (no duplication)
- Automatic deduplication by AWS

### 2. Snapshot Lifecycle

**States:**
- **Pending:** Snapshot being created (0-100%)
- **Completed:** Fully created and available
- **Error:** Creation failed

**Progress:**
- Can use snapshot once it reaches "completed"
- Large volumes take longer (TB-sized can take hours)

### 3. Lazy Loading (Fast Snapshot Restore)

**Normal Behavior:**
- Create volume from snapshot
- Volume available immediately
- Data loaded on-demand (first access is slow)

**Fast Snapshot Restore (FSR):**
- Pre-warms data into volume
- Full performance immediately
- Costs extra ($0.75 per AZ per hour)

### 4. Snapshot Retention

**Options:**
- Manual: Keep snapshots until manually deleted
- Automated: Data Lifecycle Manager (DLM) policies
- Retention rules: Keep daily for 7 days, weekly for 4 weeks, etc.

### 5. Snapshot Pricing

**Cost:** $0.05 per GB-month (us-east-1)

**Example:**
```
Snapshot 1: 50 GB (full backup)
Snapshot 2: +5 GB (incremental)
Snapshot 3: +10 GB (incremental)
Total stored: 65 GB
Monthly cost: 65 GB × $0.05 = $3.25/month
```

**Note:** You pay for total unique data, not number of snapshots

### 6. Snapshot Lifecycle Manager (DLM)

**What:** Automated snapshot creation and deletion

**Features:**
- Schedule snapshots (hourly, daily, weekly, monthly)
- Automatic retention policy
- Cross-account snapshot copying
- Tagging for organization

---

## How Snapshots Work

### Architecture

```
┌─────────────────────┐
│   EC2 Instance      │
│                     │
│   ┌─────────────┐   │
│   │ EBS Volume  │   │──────┐
│   │   100 GB    │   │      │
│   └─────────────┘   │      │ Create Snapshot
└─────────────────────┘      │
                             ▼
                   ┌─────────────────────┐
                   │   Amazon S3         │
                   │  (Behind the scenes)│
                   │                     │
                   │  ┌───────────────┐  │
                   │  │  Snapshot 1   │  │ ◄── Replicated across
                   │  │   50 GB       │  │     multiple AZs
                   │  └───────────────┘  │
                   │  ┌───────────────┐  │
                   │  │  Snapshot 2   │  │
                   │  │   +5 GB       │  │
                   │  └───────────────┘  │
                   └─────────────────────┘
```

### Block-Level Incremental Process

**Initial State (Volume has 10 blocks):**
```
Volume Blocks: [A][B][C][D][E][F][G][H][I][J]
```

**Snapshot 1 (Full backup):**
```
Snapshot 1: [A][B][C][D][E][F][G][H][I][J]
Copied: All blocks
```

**Change 1: Blocks C and F modified:**
```
Volume Blocks: [A][B][C'][D][E][F'][G][H][I][J]
                      ↑           ↑
                    Changed    Changed
```

**Snapshot 2 (Incremental):**
```
Snapshot 2: [C'][F']
Copied: Only changed blocks
References: Snapshot 1 for unchanged blocks
```

**Change 2: Block A deleted, Block K added:**
```
Volume Blocks: [B][C'][D][E][F'][G][H][I][J][K]
```

**Snapshot 3 (Incremental):**
```
Snapshot 3: [K]
Copied: Only new block
References: Snapshot 2 for C' and F', Snapshot 1 for others
```

### Snapshot Deletion

**Important:** Deleting a snapshot only removes unique data

**Scenario:**
```
Snapshot 1: [A][B][C][D]
Snapshot 2: [A][B][C'][E]  (C changed, D deleted, E added)
Snapshot 3: [A][B'][C'][E]  (B changed)

Delete Snapshot 2:
- Blocks C' and E are still in Snapshot 3 (kept)
- No unique data lost
- Storage reclaimed: ~0 GB

Delete Snapshot 1:
- Blocks A and D are unique to Snapshot 1
- Check if needed by later snapshots (not needed)
- Storage reclaimed: Size of A and D blocks
```

**AWS automatically manages this!**

---

## Use Cases

### 1. Disaster Recovery (DR)

**Scenario:** Protect against regional failures

**Architecture:**
```
Primary Region (us-east-1):
- Production database on EBS
- Daily snapshots created
- Snapshots automatically copied to us-west-2

DR Region (us-west-2):
- Snapshot copies received
- In case of disaster:
  1. Create volume from latest snapshot
  2. Attach to EC2 instance
  3. Resume operations

Recovery Time Objective (RTO): 30 minutes
Recovery Point Objective (RPO): 24 hours (daily snapshots)
```

**Implementation:**
```bash
# Automated DR with DLM
1. Create DLM policy in us-east-1
2. Enable cross-region copy to us-west-2
3. Retention: 7 days in primary, 30 days in DR
4. In disaster, launch instance in us-west-2 from snapshot
```

---

### 2. Development/Test Environment Cloning

**Scenario:** Developers need production-like data for testing

**Process:**
```
1. Production Volume (us-east-1a): 500 GB database
2. Create snapshot (once per week)
3. Create 5 volumes from snapshot (us-east-1b)
4. Attach to 5 dev/test instances
5. Developers have realistic data
6. Destroy dev volumes after testing (save costs)

Cost Savings:
- Production volume: $40/month
- Snapshot: $25/month
- 5 dev volumes (only during work hours): $20/month
- Total: $85/month
- vs 5 full-time volumes: $200/month
- Savings: $115/month (57%)
```

---

### 3. Data Migration Across AZs

**Scenario:** Move database from us-east-1a to us-east-1b

**Steps:**
```bash
# 1. Create snapshot of volume in us-east-1a
aws ec2 create-snapshot \
    --volume-id vol-in-az1a \
    --description "Migration to AZ 1b"

# 2. Wait for completion
aws ec2 wait snapshot-completed \
    --snapshot-ids snap-xxxxx

# 3. Create volume in us-east-1b from snapshot
aws ec2 create-volume \
    --snapshot-id snap-xxxxx \
    --availability-zone us-east-1b \
    --volume-type gp3

# 4. Attach to instance in us-east-1b
# 5. Minimal downtime (only during cutover)
```

---

### 4. Compliance and Auditing

**Scenario:** Financial company must retain data for 7 years

**Strategy:**
```
Daily Snapshots: Retain for 30 days
Monthly Snapshots: Retain for 7 years

Storage calculation:
- Daily: 30 snapshots × 10 GB incremental = 300 GB
- Monthly: 84 snapshots × 50 GB incremental = 4,200 GB
- Total: 4,500 GB = ~$225/month

vs keeping 84 full volumes:
- 84 volumes × 500 GB × $0.08/GB = $3,360/month
- Savings: $3,135/month (93%)
```

---

### 5. Pre-Production Testing (Blue/Green Deployments)

**Scenario:** Test application upgrade without affecting production

**Process:**
```
1. Production (Blue): Running on volume-A
2. Create snapshot of volume-A
3. Create volume-B from snapshot
4. Attach volume-B to staging instance
5. Test application upgrade on volume-B
6. If successful: Cut over production to volume-B (Green)
7. If failed: Discard volume-B, production unaffected
```

---

### 6. Data Archiving

**Scenario:** Old project data not actively used

**Strategy:**
```
1. Project completed, data rarely needed
2. Volume: 1 TB at $80/month
3. Create snapshot: $50/month
4. Delete volume
5. Savings: $30/month ($360/year)
6. If needed later: Create volume from snapshot (takes minutes)
```

---

## Advantages

### 1. **Data Protection**
- Point-in-time recovery
- Protection against:
  - Accidental deletion
  - Corruption
  - Ransomware
  - Application errors
- Retain multiple versions (hourly, daily, weekly)

### 2. **Durability**
- Stored in S3 (99.999999999% durability)
- Automatically replicated across multiple AZs
- Much more durable than single EBS volume

### 3. **Cost-Effective**
- Incremental backups (only pay for changed blocks)
- Cheaper than keeping duplicate volumes
- Can delete volumes and keep snapshots

### 4. **Disaster Recovery**
- Cross-region copy for geographic redundancy
- Quick recovery in case of regional failure
- Automated with DLM policies

### 5. **Flexibility**
- Create volumes of different sizes from snapshots
- Change volume type (gp2 → gp3, gp3 → io2)
- Create volumes in any AZ within region

### 6. **Sharing and Collaboration**
- Share snapshots with other AWS accounts
- Public snapshots (for open-source AMIs)
- Cross-account disaster recovery

### 7. **No Performance Impact**
- Snapshot creation happens in background
- Minimal impact on volume performance
- No downtime required

### 8. **Automation**
- Data Lifecycle Manager (DLM) automates:
  - Snapshot creation
  - Retention policies
  - Cross-region copying
  - Deletion of old snapshots

---

## Disadvantages

### 1. **Initial Snapshot Slowness**
- First snapshot copies all used data
- Large volumes (TB-sized) take hours
- **Mitigation:** Create first snapshot during off-peak hours

### 2. **Cost Accumulation**
- Snapshots accumulate over time
- Forgotten snapshots = wasted money
- $0.05/GB-month adds up
- **Mitigation:** Use DLM policies with retention limits, regular audits

### 3. **Lazy Loading Performance**
- Volumes created from snapshots load data on-demand
- First access to blocks is slower
- **Mitigation:** Use Fast Snapshot Restore (FSR) for critical volumes

### 4. **Region-Specific**
- Snapshots stored in one region
- Cross-region copy required for DR
- Additional costs for cross-region transfer
- **Mitigation:** Automate cross-region copy with DLM

### 5. **Deletion Complexity**
- Can't see exactly what data is in each snapshot
- Deleting snapshots in wrong order doesn't save space
- **Mitigation:** Let AWS manage via DLM, trust incremental system

### 6. **Snapshot Limits**
- 10,000 snapshots per region (soft limit, can be increased)
- 5 concurrent snapshot copies per destination region
- **Mitigation:** Implement retention policies

### 7. **Cross-Region Transfer Costs**
- Data transfer out of region: $0.02/GB (us-east-1)
- 500 GB snapshot to another region = $10
- **Mitigation:** Only copy critical snapshots cross-region

### 8. **No Application Consistency (by default)**
- Snapshot captures volume at block level
- Application may have in-flight writes
- Database may be in inconsistent state
- **Mitigation:** Use application-level quiescing, freeze filesystems, or use AWS Backup for application-consistent snapshots

---

## Practical Demonstration

### Demo 1: Creating a Manual Snapshot

#### Via Console:
```
1. Navigate to EC2 → Volumes
2. Select volume
3. Actions → Create Snapshot

Configuration:
- Description: "Production DB backup 2025-02-17"
- Tags:
  - Name: prod-db-backup-20250217
  - Environment: Production
  - RetentionDays: 30

4. Click "Create Snapshot"

5. View progress:
   - Navigate to Snapshots
   - Watch status: pending (0%) → pending (75%) → completed
```

#### Via CLI:
```bash
# Create snapshot
aws ec2 create-snapshot \
    --volume-id vol-0123456789abcdef0 \
    --description "Production DB backup $(date +%Y-%m-%d)" \
    --tag-specifications 'ResourceType=snapshot,Tags=[{Key=Name,Value=prod-db-backup},{Key=Environment,Value=Production}]'

# Output:
{
    "SnapshotId": "snap-0123456789abcdef0",
    "VolumeId": "vol-0123456789abcdef0",
    "State": "pending",
    "StartTime": "2025-02-17T10:30:00.000Z",
    "Progress": "0%",
    ...
}

# Monitor progress
aws ec2 describe-snapshots \
    --snapshot-ids snap-0123456789abcdef0 \
    --query 'Snapshots[0].[State,Progress]' \
    --output text

# Wait for completion
aws ec2 wait snapshot-completed \
    --snapshot-ids snap-0123456789abcdef0
```

---

### Demo 2: Creating a Volume from Snapshot

```bash
# Create volume from snapshot
aws ec2 create-volume \
    --snapshot-id snap-0123456789abcdef0 \
    --availability-zone us-east-1b \
    --volume-type gp3 \
    --iops 5000 \
    --throughput 250 \
    --encrypted \
    --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=restored-from-snapshot}]'

# Output: volume-id

# Attach to instance
aws ec2 attach-volume \
    --volume-id vol-new-volume-id \
    --instance-id i-instance-in-us-east-1b \
    --device /dev/sdf

# Mount on instance
sudo mkdir /restored-data
sudo mount /dev/xvdf /restored-data

# Verify data is intact
ls -la /restored-data
```

**Key Points:**
- Can create volume in different AZ (us-east-1a → us-east-1b)
- Can change volume type (original was gp2, new is gp3)
- Can increase size (original 100 GB, new 200 GB)
- Data is lazy-loaded (first access slower)

---

### Demo 3: Cross-Region Snapshot Copy

#### Use Case: Disaster Recovery

```bash
# Step 1: Copy snapshot from us-east-1 to us-west-2
aws ec2 copy-snapshot \
    --source-region us-east-1 \
    --source-snapshot-id snap-0123456789abcdef0 \
    --destination-region us-west-2 \
    --description "DR copy from us-east-1" \
    --encrypted \
    --kms-key-id arn:aws:kms:us-west-2:123456789012:key/xxxx-xxxx

# Output:
{
    "SnapshotId": "snap-west-2-copy-id"
}

# Step 2: Monitor copy progress (in us-west-2)
aws ec2 describe-snapshots \
    --region us-west-2 \
    --snapshot-ids snap-west-2-copy-id \
    --query 'Snapshots[0].[State,Progress]'

# Step 3: In case of disaster in us-east-1
# Create volume in us-west-2 from DR snapshot
aws ec2 create-volume \
    --region us-west-2 \
    --snapshot-id snap-west-2-copy-id \
    --availability-zone us-west-2a \
    --volume-type gp3

# Attach to DR instance and resume operations
```

**Costs:**
- Snapshot storage in us-west-2: $0.05/GB-month
- Data transfer (one-time): $0.02/GB
- Example: 500 GB snapshot
  - Transfer: $10 (one-time)
  - Storage: $25/month

---

### Demo 4: Automating Snapshots with Data Lifecycle Manager (DLM)

#### Scenario: Daily backups, keep for 7 days

**Via Console:**
```
1. Navigate to EC2 → Lifecycle Manager
2. Click "Create Lifecycle Policy"

Configuration:
- Policy type: EBS snapshot policy
- Resource type: Volume
- Target with these tags:
  - Key: Backup
  - Value: Daily

Schedule:
- Schedule name: DailyBackup
- Frequency: Daily
- Time: 03:00 UTC (off-peak)
- Retention type: Count
- Retain: 7 snapshots

Copy tags from volume: Yes
Enable cross-region copy: No (or Yes for DR)

Advanced:
- Enable fast snapshot restore: No (save costs)
- Cross-account sharing: No

IAM role: Default (or create custom)

3. Click "Create Policy"
```

**Via CLI:**
```bash
# Create DLM policy (JSON)
cat > dlm-policy.json <<'EOF'
{
  "ExecutionRoleArn": "arn:aws:iam::123456789012:role/AWSDataLifecycleManagerDefaultRole",
  "Description": "Daily backups, 7-day retention",
  "State": "ENABLED",
  "PolicyDetails": {
    "ResourceTypes": ["VOLUME"],
    "TargetTags": [
      {
        "Key": "Backup",
        "Value": "Daily"
      }
    ],
    "Schedules": [
      {
        "Name": "DailyBackup",
        "CopyTags": true,
        "CreateRule": {
          "Interval": 24,
          "IntervalUnit": "HOURS",
          "Times": ["03:00"]
        },
        "RetainRule": {
          "Count": 7
        }
      }
    ]
  }
}
EOF

# Create the policy
aws dlm create-lifecycle-policy \
    --cli-input-json file://dlm-policy.json

# Tag your volumes to enable automated snapshots
aws ec2 create-tags \
    --resources vol-0123456789abcdef0 \
    --tags Key=Backup,Value=Daily
```

**Result:**
- DLM creates snapshot daily at 3 AM UTC
- Keeps 7 most recent snapshots
- Automatically deletes snapshots older than 7 days
- No manual intervention required

---

### Demo 5: Fast Snapshot Restore (FSR)

#### Problem: Volume created from snapshot has slow initial performance

**Without FSR:**
```
1. Create volume from snapshot
2. Attach to instance
3. First read of each block is slow (lazy loading)
4. Application startup takes 10 minutes (reading all data)
```

**With FSR:**
```bash
# Enable FSR on snapshot
aws ec2 enable-fast-snapshot-restores \
    --availability-zones us-east-1a us-east-1b \
    --source-snapshot-ids snap-0123456789abcdef0

# Create volume from FSR-enabled snapshot
aws ec2 create-volume \
    --snapshot-id snap-0123456789abcdef0 \
    --availability-zone us-east-1a \
    --volume-type gp3

# Result: Volume has full performance immediately
# Application startup: 10 minutes → 1 minute
```

**Cost:**
```
FSR cost: $0.75 per hour per AZ per snapshot
Example:
- 1 snapshot
- 2 AZs (us-east-1a, us-east-1b)
- 24 hours
- Cost: $0.75 × 2 × 24 = $36/day

Use Case: Critical production restores, DR drills
```

**Disable when not needed:**
```bash
aws ec2 disable-fast-snapshot-restores \
    --availability-zones us-east-1a us-east-1b \
    --source-snapshot-ids snap-0123456789abcdef0
```

---

### Demo 6: Sharing Snapshots with Another AWS Account

#### Scenario: Share snapshot with partner account for collaboration

```bash
# Step 1: Modify snapshot permissions (in account A)
aws ec2 modify-snapshot-attribute \
    --snapshot-id snap-0123456789abcdef0 \
    --attribute createVolumePermission \
    --operation-type add \
    --user-ids 999988887777

# Step 2: Partner (account 999988887777) can now see snapshot
# In account B:
aws ec2 describe-snapshots \
    --owner-ids 123456789012 \
    --snapshot-ids snap-0123456789abcdef0

# Step 3: Create volume from shared snapshot (in account B)
aws ec2 create-volume \
    --snapshot-id snap-0123456789abcdef0 \
    --availability-zone us-east-1a \
    --volume-type gp3

# Note: Encrypted snapshots require KMS key sharing
```

**Important Security Notes:**
- Shared snapshots are read-only
- Recipient can create volumes but cannot modify original snapshot
- Recipient is charged for volumes they create
- Can revoke access anytime

**Revoke Access:**
```bash
aws ec2 modify-snapshot-attribute \
    --snapshot-id snap-0123456789abcdef0 \
    --attribute createVolumePermission \
    --operation-type remove \
    --user-ids 999988887777
```

---

### Demo 7: Application-Consistent Snapshots (Database)

#### Problem: Snapshot captures volume while database has uncommitted transactions

**Solution: Freeze filesystem and flush database**

**For MySQL:**
```bash
# SSH into EC2 instance

# Step 1: Connect to MySQL
mysql -u root -p

# Step 2: Flush tables and lock
mysql> FLUSH TABLES WITH READ LOCK;

# Step 3: In another terminal, create snapshot
aws ec2 create-snapshot \
    --volume-id vol-database \
    --description "Application-consistent MySQL backup"

# Wait for snapshot to start (not complete)
aws ec2 describe-snapshots \
    --snapshot-ids snap-xxxxx \
    --query 'Snapshots[0].State'
# Output: "pending" (snapshot initiated)

# Step 4: Back in MySQL, unlock tables
mysql> UNLOCK TABLES;
mysql> EXIT;

# Snapshot continues in background
# Database is locked for only ~30 seconds
```

**For PostgreSQL:**
```bash
# Use pg_start_backup and pg_stop_backup
psql -U postgres -c "SELECT pg_start_backup('snapshot-backup');"

# Create snapshot
aws ec2 create-snapshot --volume-id vol-database --description "PG backup"

# End backup mode
psql -U postgres -c "SELECT pg_stop_backup();"
```

**Best Practice: Use AWS Backup**
```bash
# AWS Backup handles application consistency automatically
aws backup start-backup-job \
    --backup-vault-name Default \
    --resource-arn arn:aws:ec2:us-east-1:123456789012:volume/vol-xxxxx \
    --iam-role-arn arn:aws:iam::123456789012:role/AWSBackupDefaultRole
```

---

## Scenario-Based Interview Questions

### Question 1: Snapshot Strategy for Production Database

**Scenario:** Design a snapshot strategy for a production PostgreSQL database that meets the following requirements:
- RPO (Recovery Point Objective): 1 hour
- RTO (Recovery Time Objective): 15 minutes
- Must retain backups for 30 days
- Must have off-site backup for disaster recovery
- Minimize costs

**Answer:**
```
Solution Design:

1. Snapshot Schedule:

A. Hourly Snapshots (RPO: 1 hour):
   - Frequency: Every hour
   - Retention: 24 hours (24 snapshots)
   - Automated via DLM

B. Daily Snapshots (Long-term retention):
   - Frequency: Once per day at 2 AM
   - Retention: 30 days (30 snapshots)
   - Automated via DLM

C. Weekly Snapshots (Compliance):
   - Frequency: Sunday at 2 AM
   - Retention: 12 weeks (3 months)
   - Automated via DLM

2. Disaster Recovery (Off-site):
   - Daily snapshots copied to secondary region (us-west-2)
   - Automated via DLM cross-region copy
   - Retention: 7 days in DR region

3. Fast Snapshot Restore (RTO: 15 minutes):
   - Enable FSR on latest 2 snapshots
   - Pre-warms data for immediate performance
   - Disable FSR on older snapshots (cost control)

4. Implementation:

DLM Policy Configuration:
```
Policy 1: Hourly Backups
- Target tags: Backup=Hourly
- Schedule: Every 1 hour
- Retention: 24 snapshots
- Fast Snapshot Restore: Latest 2 snapshots
- Copy tags: Yes

Policy 2: Daily Backups
- Target tags: Backup=Daily
- Schedule: Daily at 02:00 UTC
- Retention: 30 days
- Cross-region copy: us-west-2 (retain 7 days)
- Fast Snapshot Restore: No (cost savings)

Policy 3: Weekly Backups
- Target tags: Backup=Weekly
- Schedule: Weekly on Sunday at 02:00 UTC
- Retention: 12 weeks
- Cross-region copy: No (daily copies cover DR)
```

5. Cost Calculation:

Database Volume: 500 GB

Hourly Snapshots:
- First snapshot: 500 GB
- Subsequent 23 snapshots: ~10 GB each (incremental)
- Total: 500 + (23 × 10) = 730 GB
- Cost: 730 GB × $0.05 = $36.50/month

Daily Snapshots:
- 30 snapshots × 50 GB incremental = 1,500 GB
- Cost: 1,500 GB × $0.05 = $75/month

Weekly Snapshots:
- 12 snapshots × 100 GB incremental = 1,200 GB
- Cost: 1,200 GB × $0.05 = $60/month

Cross-Region Copies (DR):
- 7 daily snapshots × 500 GB = 3,500 GB
- Cost: 3,500 GB × $0.05 = $175/month
- Transfer cost (one-time per day): 500 GB × $0.02 = $10/day = $300/month

Fast Snapshot Restore:
- 2 snapshots × 1 AZ × $0.75/hour × 720 hours/month = $1,080/month

Total Monthly Cost: $1,726.50/month

Cost Optimization (Alternative):
- Reduce FSR to 1 snapshot: Save $540/month
- Reduce cross-region retention to 3 days: Save ~$100/month
- Optimized total: ~$1,086.50/month

6. Recovery Procedures:

Scenario A: Accidental table drop (1 hour ago)
Recovery Steps:
1. Identify hourly snapshot from 1 hour ago (RTO starts)
2. Create volume from FSR-enabled snapshot (2 minutes)
3. Attach to standby instance (1 minute)
4. Mount volume (1 minute)
5. Restore table using pg_restore (10 minutes)
6. Verify data (1 minute)
Total: 15 minutes (meets RTO)

Scenario B: Regional disaster (us-east-1 fails)
Recovery Steps:
1. Failover to us-west-2 (RTO starts)
2. Create volume from latest DR snapshot (2 minutes with FSR)
3. Launch EC2 instance in us-west-2 (3 minutes)
4. Attach volume (1 minute)
5. Start PostgreSQL service (2 minutes)
6. Update DNS to point to new instance (5 minutes)
7. Verify application connectivity (2 minutes)
Total: 15 minutes
Data Loss: Up to 24 hours (last cross-region copy)

Improvement for Better DR RPO:
- Copy snapshots every 4 hours instead of daily
- RPO improves to 4 hours
- Additional cost: ~$100/month

7. Monitoring and Alerts:

CloudWatch Alarms:
- DLM policy failed to create snapshot → Alert operations
- Snapshot age > 2 hours → Alert (hourly snapshots may be failing)
- Cross-region copy failed → Critical alert
- FSR credits exhausted → Alert

8. Testing and Validation:

Monthly DR Drill:
- Create volume from DR snapshot in us-west-2
- Launch test instance
- Verify database integrity
- Measure actual RTO/RPO
- Document any issues

9. Application-Consistent Backups:

Before each snapshot creation:
```bash
# Use pg_start_backup for consistency
psql -U postgres -c "SELECT pg_start_backup('dlm-backup');"
# DLM creates snapshot
# Webhook/Lambda triggers:
psql -U postgres -c "SELECT pg_stop_backup();"
```

Or use AWS Backup for automatic application consistency.

10. Tags for Organization:

Volume tags:
- Backup: Hourly
- Environment: Production
- Application: PostgreSQL
- CostCenter: Engineering

Snapshot tags (inherited):
- Same as volume +
- SnapshotType: Hourly/Daily/Weekly
- RetentionDays: 1/30/90

Summary:
- RPO: 1 hour (hourly snapshots)
- RTO: 15 minutes (FSR enabled)
- Retention: 30 days (daily) + 90 days (weekly)
- DR: Cross-region copies
- Cost: ~$1,100-1,700/month (depending on FSR usage)
- Automated: Full DLM automation, no manual intervention
```

---

### Question 2: Snapshot Cost Optimization

**Scenario:** Your company has 1,000 EBS volumes with daily snapshots. Snapshot costs have reached $10,000/month. How would you optimize costs without compromising data protection?

**Answer:**
```
Analysis and Optimization Strategy:

1. Current State Assessment:

Assumptions:
- 1,000 volumes
- Daily snapshots
- Average volume size: 100 GB
- Average incremental: 10 GB/day
- Retention: Not clear (problem!)

Current Cost Breakdown:
```bash
# Calculate total snapshot storage
aws ec2 describe-snapshots \
    --owner-ids self \
    --query 'Snapshots[*].[SnapshotId,VolumeSize,StartTime]' \
    --output json | \
    jq 'group_by(.[1]) | map({size: .[0][1], count: length})'

# Identify old snapshots
aws ec2 describe-snapshots \
    --owner-ids self \
    --query 'Snapshots[?StartTime<=`2024-01-01`].[SnapshotId,StartTime,VolumeSize]' \
    --output table

# Total storage (calculation)
# Assume 30-day retention:
# 1,000 volumes × 30 days × 10 GB incremental = 300,000 GB
# Cost: 300,000 GB × $0.05 = $15,000/month
```

2. Optimization Strategies:

Strategy 1: Implement Retention Policies
```
Problem: Snapshots never deleted, accumulate indefinitely

Solution:
- Define retention based on business needs:
  - Development volumes: 7 days
  - Production volumes: 30 days
  - Critical databases: 90 days

Implementation:
1. Tag volumes by criticality
2. Create DLM policies with appropriate retention
3. Delete old snapshots

Impact:
- Remove snapshots older than retention policy
- Estimated savings: 40-60%
```

Strategy 2: Reduce Snapshot Frequency for Non-Critical Volumes
```
Problem: All volumes backed up daily, regardless of importance

Solution:
- Development/Test: Weekly snapshots (not daily)
- Non-production: Every 3 days
- Production: Daily (keep as is)

Segmentation:
- 700 dev/test volumes → Weekly (reduce by 85%)
- 200 non-critical prod → Every 3 days (reduce by 66%)
- 100 critical prod → Daily (no change)

Impact:
- Dev/test: 700 × 30 snapshots → 700 × 4 snapshots = 93% fewer snapshots
- Non-critical: 200 × 30 → 200 × 10 = 67% fewer
- Estimated savings: 40%
```

Strategy 3: Consolidate Snapshots (Archive and Delete Volumes)
```
Problem: Old project volumes still running, backed up daily

Solution:
- Identify unused volumes (last attached > 90 days ago)
- Create final snapshot
- Delete unused volumes

Script:
```bash
# Find unused volumes
aws ec2 describe-volumes \
    --filters "Name=status,Values=available" \
    --query 'Volumes[?AttachTime<=`2024-01-01`].[VolumeId,Size,CreateTime]'

# Create final snapshot and delete
for vol in $(aws ec2 describe-volumes --filters "Name=status,Values=available" --query 'Volumes[].VolumeId' --output text); do
    aws ec2 create-snapshot --volume-id $vol --description "Final snapshot before deletion"
    aws ec2 delete-volume --volume-id $vol
done
```

Impact:
- Estimated 200 unused volumes
- Save: 200 volumes × $8/month = $1,600/month
- One-time snapshot: 200 × 100 GB × $0.05 = $1,000/month (still cheaper)
```

Strategy 4: Use Tiered Backup Strategy
```
Problem: All snapshots treated equally, excessive retention

Solution: GFS (Grandfather-Father-Son) backup scheme
- Daily snapshots: Retain 7 days
- Weekly snapshots: Retain 4 weeks
- Monthly snapshots: Retain 12 months

DLM Configuration:
Policy 1 (Daily):
  Frequency: Daily
  Retention: 7 days

Policy 2 (Weekly):
  Frequency: Weekly (Sunday)
  Retention: 4 weeks

Policy 3 (Monthly):
  Frequency: Monthly (1st of month)
  Retention: 12 months

Impact:
- Reduce total snapshots by 60-70%
- Maintain long-term point-in-time recovery
- Estimated savings: 50%
```

Strategy 5: Identify and Delete Orphaned Snapshots
```
Problem: Snapshots from deleted volumes/instances still exist

Script to find orphans:
```bash
# Get all snapshot volume IDs
snapshot_volumes=$(aws ec2 describe-snapshots --owner-ids self --query 'Snapshots[].VolumeId' --output text)

# Get all existing volume IDs
existing_volumes=$(aws ec2 describe-volumes --query 'Volumes[].VolumeId' --output text)

# Find orphans (volumes that no longer exist)
for vol in $snapshot_volumes; do
    if ! echo $existing_volumes | grep -q $vol; then
        echo "Orphaned snapshots for deleted volume: $vol"
        aws ec2 describe-snapshots --filters "Name=volume-id,Values=$vol" --query 'Snapshots[].SnapshotId' --output text
    fi
done

# Decide: Delete if truly orphaned, or keep if archival purpose
```

Impact:
- Estimated 20% of snapshots are orphaned
- Savings: $2,000/month
```

Strategy 6: Enable EBS Archive (for Long-Term Retention)
```
Problem: Keeping infrequently accessed snapshots in standard storage

Solution: Archive snapshots to EBS Snapshot Archive
- Cost: $0.0125/GB-month (75% cheaper than standard $0.05/GB)
- Trade-off: Restore takes 24-72 hours

Use Cases:
- Compliance snapshots (7-year retention)
- Monthly/yearly snapshots
- Rarely accessed backups

```bash
# Archive snapshot
aws ebs put-snapshot-archive \
    --snapshot-id snap-old-snapshot

# Restore when needed (24-72 hours)
aws ebs restore-snapshot-archive \
    --snapshot-id snap-old-snapshot
```

Impact:
- Archive 50% of snapshots (older than 90 days)
- 150,000 GB × ($0.05 - $0.0125) = $5,625/month savings
```

3. Implementation Plan:

Phase 1 (Week 1): Quick Wins
```
1. Identify and delete orphaned snapshots (20% reduction)
2. Delete snapshots older than 1 year (unless compliance)
3. Set up DLM policies with retention rules
Estimated Savings: $3,000/month
```

Phase 2 (Week 2-3): Optimization
```
1. Categorize volumes by criticality
2. Implement tiered backup strategy (GFS)
3. Reduce frequency for dev/test environments
Estimated Savings: $4,000/month
```

Phase 3 (Week 4): Long-Term
```
1. Archive old snapshots to EBS Snapshot Archive
2. Automate monthly orphan snapshot cleanup
3. Set up cost monitoring and alerts
Estimated Savings: $3,000/month
```

4. Cost Comparison:

Before Optimization:
- Snapshot storage: 300,000 GB
- Cost: $15,000/month

After Optimization:
- Active snapshots: 100,000 GB @ $0.05 = $5,000/month
- Archived snapshots: 100,000 GB @ $0.0125 = $1,250/month
- Total: $6,250/month

Savings: $8,750/month (58% reduction)

5. Monitoring and Governance:

Implement Cost Controls:
```bash
# Monthly cost report
aws ce get-cost-and-usage \
    --time-period Start=2025-02-01,End=2025-03-01 \
    --granularity MONTHLY \
    --metrics UnblendedCost \
    --filter file://snapshot-filter.json

# Set budget alert
aws budgets create-budget \
    --account-id 123456789012 \
    --budget file://snapshot-budget.json \
    --notifications-with-subscribers file://notifications.json
```

Automated Cleanup Lambda:
```python
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Get all snapshots older than 30 days
    threshold = datetime.now() - timedelta(days=30)

    snapshots = ec2.describe_snapshots(OwnerIds=['self'])

    for snapshot in snapshots['Snapshots']:
        if 'RetentionDays' not in snapshot.get('Tags', {}):
            # No retention tag, evaluate for deletion
            start_time = snapshot['StartTime'].replace(tzinfo=None)
            if start_time < threshold:
                print(f"Candidate for deletion: {snapshot['SnapshotId']}")
                # Optional: Auto-delete or send notification
```

6. Best Practices Going Forward:

1. Tag All Volumes and Snapshots:
   - Environment (Production/Dev/Test)
   - Backup Frequency (Daily/Weekly/Monthly)
   - Retention Days
   - Cost Center

2. Implement DLM Policies:
   - Automate snapshot creation and deletion
   - Prevent manual snapshot accumulation

3. Regular Audits:
   - Monthly review of snapshot costs
   - Identify anomalies (sudden increase)
   - Clean up orphaned snapshots

4. Training:
   - Educate teams on snapshot costs
   - Require approval for long-retention snapshots

5. Chargeback:
   - Allocate costs to teams/projects via tags
   - Encourages responsible snapshot usage

Summary:
- Current Cost: $15,000/month
- Optimized Cost: $6,250/month
- Savings: $8,750/month (58%)
- Methods: Retention policies, tiered backups, archiving, cleanup
- Risk: Low (maintains data protection for critical systems)
```

This completes the comprehensive Snapshots guide! Let me continue with the remaining topics.

