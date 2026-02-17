# Amazon EBS (Elastic Block Store) - Complete Guide

## Table of Contents
1. [What is EBS](#what-is-ebs)
2. [Why We Need EBS](#why-we-need-ebs)
3. [Key Concepts](#key-concepts)
4. [Volume Types](#volume-types)
5. [Use Cases](#use-cases)
6. [Advantages](#advantages)
7. [Disadvantages](#disadvantages)
8. [Practical Demonstration](#practical-demonstration)
9. [Scenario-Based Interview Questions](#scenario-based-interview-questions)

---

## What is EBS?

**Amazon EBS (Elastic Block Store)** is a high-performance block storage service designed for use with Amazon EC2 instances. It provides persistent, network-attached storage that can be attached to EC2 instances.

**Simple Analogy:** Think of EBS as an external hard drive that you can plug into your EC2 instance (computer). Unlike the computer's internal storage, you can unplug it and move it to another computer.

**Technical Definition:** EBS provides block-level storage volumes that persist independently from the life of an EC2 instance. Volumes are automatically replicated within their Availability Zone to protect from component failure.

### Key Characteristics:
- **Persistent:** Data remains even when instance is stopped or terminated
- **Network-attached:** Connected via AWS network (not physically attached)
- **Replicated:** Automatically replicated within an AZ
- **Resizable:** Can increase size, IOPS, and throughput
- **Encrypted:** Optional encryption at rest and in transit

---

## Why We Need EBS?

### Problems with Instance Store (Ephemeral Storage):
1. **Data Loss:** Data lost when instance stops or terminates
2. **No Snapshots:** Can't backup easily
3. **Fixed Size:** Can't resize
4. **Not Detachable:** Can't move to another instance

### EBS Solutions:
1. **Data Persistence:** Data survives instance lifecycle
2. **Backup & Recovery:** Create snapshots stored in S3
3. **Flexibility:** Resize volumes, change types
4. **Portability:** Detach and attach to different instances
5. **Performance:** Provisioned IOPS for consistent performance
6. **Security:** Encryption with AWS KMS

### Real-World Scenario:
**Problem:** You run a database on EC2. Instance hardware fails.
- **Without EBS:** All data lost, business stops
- **With EBS:** Detach volume, attach to new instance, resume operations

---

## Key Concepts

### 1. Volume
- A virtual disk that you attach to an EC2 instance
- Size: 1 GB to 64 TB (depending on type)
- One volume attached to one instance at a time (except io2 multi-attach)
- Exists independently of instance lifecycle

### 2. Availability Zone (AZ) Bound
- EBS volume exists in one specific AZ
- Can only attach to instances in the same AZ
- To move across AZs: Create snapshot → Create volume in target AZ

### 3. IOPS (Input/Output Operations Per Second)
- Measure of storage performance
- Higher IOPS = faster read/write operations
- Different volume types have different IOPS limits

### 4. Throughput
- Amount of data transferred per second (MB/s)
- Important for sequential read/write operations
- Large file processing, log analysis

### 5. Volume State
- **Creating:** Volume being created
- **Available:** Ready to be attached
- **In-use:** Attached to an instance
- **Deleting:** Being deleted
- **Error:** Creation failed

### 6. Attachment State
- **Attaching:** Volume being attached
- **Attached:** Successfully attached
- **Detaching:** Being detached
- **Detached:** Removed from instance

---

## Volume Types

### Overview Table

| Type | Use Case | Size | Max IOPS | Max Throughput | Price |
|------|----------|------|----------|----------------|-------|
| **gp3** | General purpose SSD | 1 GB - 16 TB | 16,000 | 1,000 MB/s | $0.08/GB-month |
| **gp2** | General purpose SSD | 1 GB - 16 TB | 16,000 | 250 MB/s | $0.10/GB-month |
| **io2 Block Express** | Highest performance SSD | 4 GB - 64 TB | 256,000 | 4,000 MB/s | $0.125/GB-month |
| **io2** | High performance SSD | 4 GB - 16 TB | 64,000 | 1,000 MB/s | $0.125/GB-month |
| **io1** | High performance SSD | 4 GB - 16 TB | 64,000 | 1,000 MB/s | $0.125/GB-month |
| **st1** | Throughput optimized HDD | 125 GB - 16 TB | 500 | 500 MB/s | $0.045/GB-month |
| **sc1** | Cold HDD | 125 GB - 16 TB | 250 | 250 MB/s | $0.015/GB-month |

---

### 1. General Purpose SSD (gp3) - RECOMMENDED

**What:** Balance of price and performance for most workloads

**Technical Specs:**
- Size: 1 GB - 16 TB
- Baseline: 3,000 IOPS (regardless of size)
- Baseline: 125 MB/s throughput
- Can provision up to 16,000 IOPS
- Can provision up to 1,000 MB/s throughput
- Independent IOPS and throughput scaling

**Use Cases:**
- Boot volumes
- Virtual desktops
- Development and test environments
- Low-latency interactive applications
- Medium-sized databases

**Advantages:**
- Predictable performance regardless of size
- Cost-effective
- Independent IOPS/throughput configuration
- 20% cheaper than gp2

**Example:**
```
Volume: 100 GB gp3
Default: 3,000 IOPS, 125 MB/s
Cost: $8/month

Add 10,000 IOPS: +$6.50/month
Add 500 MB/s throughput: +$3.75/month
Total: $18.25/month
```

---

### 2. General Purpose SSD (gp2) - LEGACY

**What:** Previous generation general purpose SSD

**Technical Specs:**
- Size: 1 GB - 16 TB
- IOPS scales with size: 3 IOPS per GB
- Minimum: 100 IOPS (volumes < 33.33 GB)
- Maximum: 16,000 IOPS (at 5,334 GB and above)
- Throughput: 250 MB/s max
- Burst capability: Smaller volumes can burst to 3,000 IOPS

**Use Cases:**
- Legacy applications
- When you already have gp2 volumes

**Disadvantages vs gp3:**
- More expensive
- IOPS tied to volume size
- Lower throughput (250 MB/s vs 1,000 MB/s)

**Migration Tip:** Convert gp2 → gp3 with no downtime

---

### 3. Provisioned IOPS SSD (io2 Block Express)

**What:** Highest performance SSD for mission-critical workloads

**Technical Specs:**
- Size: 4 GB - 64 TB
- IOPS: Up to 256,000
- Throughput: Up to 4,000 MB/s
- IOPS:GB ratio: 1000:1 (max)
- Sub-millisecond latency
- 99.999% durability (5 nines)

**Use Cases:**
- Large databases (SAP HANA, Oracle, SQL Server)
- Mission-critical applications
- Applications requiring sustained IOPS
- Sub-millisecond latency requirements

**Example:**
```
Database server requirements:
- 100,000 IOPS
- 2,000 MB/s throughput
- 1 TB storage

Solution: io2 Block Express
- Size: 1 TB
- IOPS: 100,000
- Throughput: 2,000 MB/s
- Cost: ~$125/month + ~$6,500/month for IOPS = $6,625/month
```

---

### 4. Provisioned IOPS SSD (io2 / io1)

**What:** High-performance SSD for I/O intensive workloads

**Technical Specs:**
- Size: 4 GB - 16 TB
- IOPS: Up to 64,000
- Throughput: Up to 1,000 MB/s
- IOPS:GB ratio: 50:1 (io2), 500:1 (io2 for smaller volumes)
- 99.999% durability (io2), 99.9% (io1)

**Use Cases:**
- Large relational databases
- NoSQL databases
- I/O intensive applications
- Multi-Attach use cases (share volume across instances)

**Multi-Attach Feature (io2 only):**
- Attach single volume to up to 16 instances
- All instances in same AZ
- Use case: Clustered applications (Oracle RAC)
- Requires cluster-aware file system

---

### 5. Throughput Optimized HDD (st1)

**What:** Low-cost HDD for frequently accessed, throughput-intensive workloads

**Technical Specs:**
- Size: 125 GB - 16 TB
- Max IOPS: 500
- Max Throughput: 500 MB/s
- Baseline: 40 MB/s per TB
- Burst: 250 MB/s per TB
- Cannot be boot volume

**Use Cases:**
- Big data analytics
- Data warehouses
- Log processing
- Streaming workloads
- Sequential I/O patterns

**Example:**
```
Use Case: Apache Kafka logs
- Need: High throughput for sequential writes
- Data: 1 TB
- st1: 40 MB/s baseline, 250 MB/s burst
- Cost: $45/month (vs $80 for gp3)
```

---

### 6. Cold HDD (sc1)

**What:** Lowest cost HDD for infrequently accessed data

**Technical Specs:**
- Size: 125 GB - 16 TB
- Max IOPS: 250
- Max Throughput: 250 MB/s
- Baseline: 12 MB/s per TB
- Burst: 80 MB/s per TB
- Cannot be boot volume

**Use Cases:**
- File servers
- Infrequently accessed data
- Archival storage (when S3 Glacier not suitable)
- Cold data requiring occasional access

**Example:**
```
Use Case: File server with archived files
- Accessed once per month
- 5 TB storage
- sc1: $75/month (vs $400 for gp3)
- Acceptable slow performance for rare access
```

---

## Use Cases

### 1. Database Storage
**Scenario:** MySQL database with 10,000 transactions/second
```
Requirements:
- Consistent high IOPS
- Low latency
- High durability

Solution: io2 volume
- Size: 500 GB
- IOPS: 20,000
- Throughput: 500 MB/s
- Latency: < 1ms
```

### 2. Boot Volumes
**Scenario:** EC2 instance boot drive
```
Requirements:
- Fast boot time
- General purpose performance
- Cost-effective

Solution: gp3 volume
- Size: 30 GB
- IOPS: 3,000 (default)
- Throughput: 125 MB/s
- Cost: $2.40/month
```

### 3. Big Data Processing
**Scenario:** Hadoop cluster with large sequential reads/writes
```
Requirements:
- High throughput
- Large storage
- Cost-effective

Solution: st1 volume
- Size: 5 TB
- Throughput: 500 MB/s
- Cost: $225/month
```

### 4. Development/Test Environments
**Scenario:** Temporary dev environment
```
Requirements:
- Moderate performance
- Low cost
- Temporary

Solution: gp3 volume (small)
- Size: 50 GB
- Default IOPS: 3,000
- Cost: $4/month
```

### 5. Backup/Archive Storage
**Scenario:** Long-term file storage, rarely accessed
```
Requirements:
- Large capacity
- Lowest cost
- Rare access acceptable

Solution: sc1 volume
- Size: 10 TB
- Cost: $150/month
```

---

## Advantages

### 1. **Data Persistence**
- Data survives instance stop, start, terminate
- Independent lifecycle from EC2 instance
- Can detach and reattach

### 2. **High Availability**
- Automatically replicated within AZ
- Protects against hardware failures
- 99.999% availability SLA (io2)

### 3. **Backup and Recovery**
- Create point-in-time snapshots
- Snapshots stored in S3 (durable, replicated)
- Restore volumes from snapshots
- Cross-region snapshot copy

### 4. **Flexible Performance**
- Multiple volume types for different needs
- Can change volume type (gp2 → gp3)
- Increase size without downtime
- Increase IOPS/throughput on-the-fly

### 5. **Security**
- Encryption at rest (AWS KMS)
- Encryption in transit (instance to volume)
- IAM policies for access control
- Snapshot encryption

### 6. **Scalability**
- Resize volumes from 1 GB to 64 TB
- Increase performance characteristics
- No downtime for modifications

### 7. **Cost-Effective**
- Pay only for provisioned storage
- Different types for different budgets
- gp3 offers best price/performance

### 8. **Integration**
- Seamless with EC2
- Works with CloudWatch monitoring
- Automated snapshots with DLM
- Multi-attach for clustered apps (io2)

---

## Disadvantages

### 1. **AZ-Locked**
- Volume exists in one AZ only
- Can't directly attach to instance in different AZ
- Migration requires snapshot + new volume creation
- **Mitigation:** Use snapshots for cross-AZ/region replication

### 2. **Network Latency**
- Network-attached storage (vs local Instance Store)
- Some latency compared to directly attached storage
- **Mitigation:** Use io2 Block Express for lowest latency

### 3. **Cost Accumulation**
- Charges for provisioned storage even if not used
- IOPS charges for io1/io2
- Snapshot storage costs
- **Mitigation:** Delete unused volumes, use lifecycle policies

### 4. **IOPS Limits**
- Each instance type has IOPS limits
- Example: t3.micro limited to 2,880 IOPS even with high-IOPS volume
- **Mitigation:** Choose EBS-optimized instance types

### 5. **Single Attachment (Except io2)**
- One volume → one instance (typically)
- Can't share volume across instances
- **Mitigation:** Use io2 multi-attach or EFS for shared storage

### 6. **Performance Variability**
- gp2/gp3 burst performance can be exhausted
- st1/sc1 baseline performance low
- **Mitigation:** Provision adequate IOPS, use io2 for consistency

### 7. **Management Overhead**
- Need to manage volumes separately from instances
- Monitor volume health and performance
- Snapshot management
- **Mitigation:** Use automation (CloudWatch, Lambda, DLM)

### 8. **Data Transfer Costs**
- Snapshots to S3 incur charges
- Cross-region snapshot copy expensive
- **Mitigation:** Plan snapshot strategy, use lifecycle rules

---

## Practical Demonstration

### Demo 1: Creating and Attaching an EBS Volume

#### Step 1: Create EBS Volume via Console

```
1. Navigate to EC2 → Volumes
2. Click "Create Volume"

Configuration:
- Volume Type: gp3
- Size: 10 GB
- IOPS: 3000 (default)
- Throughput: 125 MB/s (default)
- Availability Zone: us-east-1a (match your instance!)
- Snapshot: None
- Encryption: Enable
- KMS Key: aws/ebs (default)

Tags:
- Name: my-data-volume
- Environment: Development

3. Click "Create Volume"
```

#### Step 2: Create Volume via AWS CLI

```bash
aws ec2 create-volume \
    --volume-type gp3 \
    --size 10 \
    --availability-zone us-east-1a \
    --encrypted \
    --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=my-data-volume}]'

# Output: volume-id (e.g., vol-0123456789abcdef0)
```

#### Step 3: Attach Volume to EC2 Instance

**Via Console:**
```
1. Select the volume
2. Actions → Attach Volume
3. Instance: Select your EC2 instance
4. Device name: /dev/sdf (Linux) or xvdf
5. Click "Attach"
```

**Via CLI:**
```bash
aws ec2 attach-volume \
    --volume-id vol-0123456789abcdef0 \
    --instance-id i-1234567890abcdef0 \
    --device /dev/sdf
```

#### Step 4: Format and Mount Volume (SSH into instance)

```bash
# List block devices
lsblk

# Output:
# NAME    MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
# xvda    202:0    0   8G  0 disk
# └─xvda1 202:1    0   8G  0 part /
# xvdf    202:80   0  10G  0 disk          <-- New volume

# Check if volume has file system
sudo file -s /dev/xvdf
# Output: /dev/xvdf: data (means no file system)

# Create ext4 file system
sudo mkfs -t ext4 /dev/xvdf

# Create mount point
sudo mkdir /data

# Mount the volume
sudo mount /dev/xvdf /data

# Verify mount
df -h
# /dev/xvdf       9.8G   37M  9.3G   1% /data

# Create test file
echo "Hello from EBS!" | sudo tee /data/test.txt

# Read back
cat /data/test.txt
```

#### Step 5: Auto-Mount on Reboot

```bash
# Get UUID of volume
sudo blkid /dev/xvdf
# /dev/xvdf: UUID="12345678-1234-1234-1234-123456789abc" TYPE="ext4"

# Edit fstab
sudo nano /etc/fstab

# Add line (replace UUID with your actual UUID):
UUID=12345678-1234-1234-1234-123456789abc  /data  ext4  defaults,nofail  0  2

# Test the fstab entry
sudo umount /data
sudo mount -a

# Verify
df -h | grep /data
```

---

### Demo 2: Resizing an EBS Volume (Increase Size)

#### Step 1: Modify Volume (No Downtime)

**Via Console:**
```
1. Select volume
2. Actions → Modify Volume
3. Change size: 10 GB → 20 GB
4. Click "Modify"
5. Confirm
```

**Via CLI:**
```bash
aws ec2 modify-volume \
    --volume-id vol-0123456789abcdef0 \
    --size 20

# Monitor progress
aws ec2 describe-volumes-modifications \
    --volume-id vol-0123456789abcdef0
```

#### Step 2: Extend the File System (SSH into instance)

```bash
# View current size
df -h /data
# /dev/xvdf       9.8G   37M  9.3G   1% /data

# Check partition
lsblk
# xvdf    202:80   0  20G  0 disk  /data  <-- Now shows 20G

# Extend file system (ext4)
sudo resize2fs /dev/xvdf

# Verify
df -h /data
# /dev/xvdf        20G   45M   19G   1% /data

# For XFS file system, use instead:
# sudo xfs_growfs /data
```

**No Reboot Required!**

---

### Demo 3: Creating a Snapshot

#### Step 1: Create Snapshot

**Via Console:**
```
1. Select volume
2. Actions → Create Snapshot
3. Description: "Backup before upgrade"
4. Tags:
   - Name: my-data-volume-snapshot-2025-02-17
   - Purpose: Backup
5. Click "Create Snapshot"
```

**Via CLI:**
```bash
aws ec2 create-snapshot \
    --volume-id vol-0123456789abcdef0 \
    --description "Backup before upgrade" \
    --tag-specifications 'ResourceType=snapshot,Tags=[{Key=Name,Value=backup-snapshot}]'

# Output: snapshot-id (e.g., snap-0123456789abcdef0)
```

#### Step 2: Monitor Snapshot Progress

```bash
aws ec2 describe-snapshots \
    --snapshot-ids snap-0123456789abcdef0

# Status: pending → completed (takes minutes for first snapshot)
```

#### Step 3: Create Volume from Snapshot

```bash
aws ec2 create-volume \
    --snapshot-id snap-0123456789abcdef0 \
    --availability-zone us-east-1b \
    --volume-type gp3 \
    --size 20

# This creates a new volume in a different AZ!
```

---

### Demo 4: Changing Volume Type (gp2 to gp3)

```bash
# No downtime required!

# Via CLI:
aws ec2 modify-volume \
    --volume-id vol-0123456789abcdef0 \
    --volume-type gp3 \
    --iops 4000 \
    --throughput 250

# Monitor progress
aws ec2 describe-volumes-modifications \
    --volume-id vol-0123456789abcdef0

# Status: modifying → optimizing → completed
# Instance continues running during this process
```

---

### Demo 5: Detaching and Reattaching Volume

```bash
# Step 1: Unmount (SSH into instance)
sudo umount /data

# Step 2: Detach via CLI
aws ec2 detach-volume \
    --volume-id vol-0123456789abcdef0

# Step 3: Attach to different instance
aws ec2 attach-volume \
    --volume-id vol-0123456789abcdef0 \
    --instance-id i-0987654321fedcba0 \
    --device /dev/sdf

# Step 4: Mount on new instance
sudo mkdir /data
sudo mount /dev/xvdf /data

# Data is intact!
cat /data/test.txt
# Output: Hello from EBS!
```

---

### Demo 6: Encryption of Existing Unencrypted Volume

**You cannot directly encrypt an existing unencrypted volume. Use this workaround:**

```bash
# Step 1: Create snapshot of unencrypted volume
aws ec2 create-snapshot \
    --volume-id vol-unencrypted \
    --description "Snapshot for encryption"

# Step 2: Copy snapshot with encryption
aws ec2 copy-snapshot \
    --source-region us-east-1 \
    --source-snapshot-id snap-unencrypted \
    --destination-region us-east-1 \
    --encrypted \
    --kms-key-id arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012 \
    --description "Encrypted snapshot"

# Step 3: Create encrypted volume from encrypted snapshot
aws ec2 create-volume \
    --snapshot-id snap-encrypted \
    --availability-zone us-east-1a \
    --volume-type gp3

# Step 4: Detach old volume, attach new encrypted volume
# Step 5: Update /etc/fstab with new UUID
```

---

### Demo 7: Monitoring EBS Performance

```bash
# Via CloudWatch (automatic metrics)
# View in Console: CloudWatch → Metrics → EBS

# Key metrics:
# - VolumeReadOps / VolumeWriteOps (IOPS)
# - VolumeReadBytes / VolumeWriteBytes (throughput)
# - VolumeThroughputPercentage (burst credit usage)
# - VolumeQueueLength (I/O queue depth)

# Set CloudWatch Alarm for high queue length
aws cloudwatch put-metric-alarm \
    --alarm-name high-volume-queue \
    --alarm-description "EBS volume queue too high" \
    --metric-name VolumeQueueLength \
    --namespace AWS/EBS \
    --statistic Average \
    --period 300 \
    --threshold 10 \
    --comparison-operator GreaterThanThreshold \
    --dimensions Name=VolumeId,Value=vol-0123456789abcdef0 \
    --evaluation-periods 2

# On instance, use iostat to monitor
sudo yum install sysstat -y
iostat -x 1

# Output shows per-device metrics:
# Device  r/s   w/s   rMB/s   wMB/s   %util
# xvdf    100   50    12.5    6.3     45%
```

---

## Scenario-Based Interview Questions

### Question 1: Volume Size and IOPS Planning

**Scenario:** You're migrating an on-premises SQL Server database to AWS EC2. The database is 500 GB and requires 10,000 sustained IOPS with low latency. What EBS volume configuration would you recommend?

**Answer:**
```
Analysis:

Requirements:
- Size: 500 GB
- IOPS: 10,000 (sustained, not burst)
- Latency: Low (database workload)
- Consistency: High (SQL Server is I/O intensive)

Volume Type Evaluation:

1. gp3:
   - Max IOPS: 16,000 ✓
   - Default: 3,000 IOPS (need to provision more)
   - Cost: $40/month (storage) + $39/month (7,000 extra IOPS) = $79/month
   - Latency: Single-digit millisecond
   - Verdict: Good option, cost-effective

2. gp2:
   - IOPS: 3 IOPS/GB = 500 GB × 3 = 1,500 IOPS ✗
   - Would need 3,334 GB to get 10,000 IOPS
   - Cost: $333/month (storage)
   - Verdict: Not recommended, expensive

3. io2:
   - Max IOPS: 64,000 ✓
   - Can provision exactly 10,000 IOPS
   - Cost: $62.50/month (storage) + $650/month (IOPS) = $712.50/month
   - Latency: Sub-millisecond
   - Durability: 99.999% (higher than gp3)
   - Verdict: Best for production databases, but expensive

Recommendation:

Development/Test Environment:
- Volume Type: gp3
- Size: 500 GB
- IOPS: 10,000
- Throughput: 250 MB/s (default is 125, increase for SQL Server)
- Cost: ~$88/month
- Rationale: Cost-effective, sufficient performance

Production Environment:
- Volume Type: io2
- Size: 500 GB
- IOPS: 10,000
- Throughput: 500 MB/s
- Cost: ~$712/month
- Rationale: Mission-critical, needs consistent performance, higher durability

Additional Considerations:

1. Instance Type:
   - Must support 10,000 IOPS
   - Use EBS-optimized instance (m5.xlarge or higher)
   - Check EBS bandwidth limits

2. Multi-AZ Setup (Production):
   - Primary database: io2 volume in AZ-1
   - Standby database: io2 volume in AZ-2
   - Use SQL Server Always On or RDS for failover

3. Backup Strategy:
   - Daily EBS snapshots
   - Cross-region snapshot copy for DR
   - Test restore procedures

4. Monitoring:
   - CloudWatch alarms:
     - VolumeQueueLength > 5 (I/O bottleneck)
     - BurstBalance < 20% (for gp3 burst credits)
   - Database performance monitoring

Cost Optimization (If Approved):
- Start with gp3 for 30 days
- Monitor actual IOPS usage with CloudWatch
- If consistently hitting limits, migrate to io2
- Most databases don't actually use 10,000 IOPS constantly

Final Configuration:
aws ec2 create-volume \
    --volume-type gp3 \
    --size 500 \
    --iops 10000 \
    --throughput 250 \
    --availability-zone us-east-1a \
    --encrypted \
    --kms-key-id <key-id> \
    --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=sql-server-data}]'
```

---

### Question 2: EBS vs Instance Store

**Scenario:** You're deploying a Cassandra cluster that requires high-performance storage. Would you use EBS or Instance Store? Explain your reasoning and architecture.

**Answer:**
```
Comparison:

Instance Store:
Pros:
- Included in instance cost (no extra charge)
- Very high IOPS (millions)
- Ultra-low latency (physically attached)
- Best for temporary data

Cons:
- Ephemeral (data lost on stop/terminate)
- Data lost on hardware failure
- Can't create snapshots
- Can't detach/reattach

EBS:
Pros:
- Persistent storage
- Snapshots for backup
- Can detach/reattach
- Flexible (resize, change type)

Cons:
- Network latency
- Additional cost
- IOPS limits (max 256,000 for Block Express)

Cassandra Characteristics:
- Distributed database (data replicated across nodes)
- Fault-tolerant (designed for node failures)
- Write-heavy workload
- Requires high IOPS and low latency

Recommendation: Instance Store

Architecture:

1. Instance Type:
   - i3.2xlarge or i4i.2xlarge
   - Instance Store: 1.9 TB NVMe SSD
   - IOPS: ~400,000 4KB random reads
   - Latency: Microseconds

2. Cluster Configuration:
   - Minimum 3 nodes across 3 AZs
   - Replication Factor (RF): 3
   - Each piece of data on 3 different nodes
   - Can tolerate 1-2 node failures

3. Data Protection Strategy:

   a) Replication (Primary):
      - RF=3 means data on 3 nodes
      - If one node fails, data still on 2 others
      - Cassandra automatically repairs

   b) Backup to S3 (Secondary):
      - Daily snapshots of Cassandra data
      - Use Cassandra's nodetool snapshot
      - Upload to S3 via cron job
      ```bash
      nodetool snapshot -t daily-backup
      aws s3 sync /var/lib/cassandra/data/snapshots/ s3://backups/cassandra/
      ```

   c) Bootstrap New Nodes:
      - When node fails, launch new instance
      - Cassandra automatically streams data from replicas
      - No manual intervention needed

4. Cost Analysis:

   Option A: Instance Store (i3.2xlarge)
   - Cost: $0.624/hour = ~$450/month
   - Storage: 1.9 TB (included)
   - IOPS: ~400,000
   - Total per node: $450/month
   - 3 nodes: $1,350/month

   Option B: EBS (m5.2xlarge + io2 volumes)
   - Instance: $0.384/hour = ~$280/month
   - Volume: 1.9 TB io2 = $237/month
   - IOPS: 50,000 @ $0.065/IOPS/month = $3,250/month
   - Total per node: ~$3,767/month
   - 3 nodes: $11,301/month

   Savings with Instance Store: 88%

5. Handling Node Failure:

   Scenario: i3 instance hardware fails

   Steps:
   1. Cassandra cluster detects node down
   2. Continues operating (2/3 nodes healthy)
   3. Launch new i3 instance via Auto Scaling
   4. Install Cassandra, join cluster
   5. Cassandra streams data from replicas
   6. Node fully rebuilt in 1-2 hours
   7. No data loss (RF=3 protected us)

6. Production Setup:

   - Nodes: 6 instances (2 per AZ, not just 3)
   - Auto Scaling Group: Maintains count
   - Health checks: Cassandra-specific
   - Monitoring: nodetool status, CloudWatch

Exception - When to Use EBS:

Use EBS if:
1. Compliance requires persistent storage
2. Cannot tolerate data rebuild time
3. Replication factor must be 1 (not recommended)
4. Need frequent backups via snapshots

Hybrid Approach:

Some companies use both:
- Commitlog (WAL) on EBS (durability)
- Data files on Instance Store (performance)
- Best of both worlds

Configuration:
# In cassandra.yaml
commitlog_directory: /ebs/commitlog
data_file_directories:
    - /instance-store/data

Final Recommendation:
For Cassandra: Use Instance Store (i3/i4i instances)
- Better performance
- Much lower cost
- Cassandra's replication provides durability
- Industry standard practice
```

---

### Question 3: Multi-Attach Use Case

**Scenario:** Explain a real-world use case for EBS Multi-Attach. What are the requirements and limitations?

**Answer:**
```
EBS Multi-Attach Feature:

What:
- Attach single io2 volume to multiple EC2 instances
- Up to 16 instances simultaneously
- All instances in same AZ
- Concurrent read/write access

Requirements:

1. Volume Type: io2 or io2 Block Express only
2. Availability Zone: All instances in same AZ
3. Instance Type: Nitro-based instances only
   - Examples: m5, c5, r5, t3 (not t2)
4. File System: Cluster-aware file system required
   - XFS, ext4 NOT supported (data corruption risk)
   - Must use: GFS2, OCFS2, or application-level locking

Real-World Use Case: Oracle RAC (Real Application Clusters)

Scenario:
Company runs Oracle database requiring high availability and horizontal scalability.

Architecture:

1. Setup:
   - 3 EC2 instances (m5.4xlarge)
   - 1 io2 volume (2 TB, 20,000 IOPS) with multi-attach
   - Oracle RAC software installed
   - All in us-east-1a

2. Configuration:
```bash
# Create io2 volume with multi-attach
aws ec2 create-volume \
    --volume-type io2 \
    --size 2048 \
    --iops 20000 \
    --availability-zone us-east-1a \
    --multi-attach-enabled \
    --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=oracle-rac-shared}]'

# Attach to first instance
aws ec2 attach-volume \
    --volume-id vol-xxxxx \
    --instance-id i-rac-node1 \
    --device /dev/sdf

# Attach to second instance
aws ec2 attach-volume \
    --volume-id vol-xxxxx \
    --instance-id i-rac-node2 \
    --device /dev/sdf

# Attach to third instance
aws ec2 attach-volume \
    --volume-id vol-xxxxx \
    --instance-id i-rac-node3 \
    --device /dev/sdf
```

3. Oracle RAC Configuration:
   - Oracle Clusterware manages locks
   - ASM (Automatic Storage Management) for volume management
   - All nodes can read/write simultaneously
   - Oracle handles data consistency

4. Benefits:
   - High Availability: If one node fails, others continue
   - Scalability: Add nodes to increase capacity
   - Performance: Distribute load across nodes
   - Shared Storage: Single source of truth

5. How It Works:
```
User Request 1 → Load Balancer → RAC Node 1 ┐
User Request 2 → Load Balancer → RAC Node 2 ├→ Multi-Attach io2 Volume → Oracle Database
User Request 3 → Load Balancer → RAC Node 3 ┘

- All nodes access same data files
- Oracle's Cache Fusion coordinates changes
- Lock management prevents conflicts
```

Other Use Cases:

1. Microsoft SQL Server Failover Cluster:
   - Active-Passive setup
   - Shared storage for database files
   - Fast failover (seconds)

2. SAP HANA Scale-Out:
   - Multiple nodes sharing data volumes
   - High-performance analytics

3. Media Rendering Farm:
   - Multiple render nodes accessing same project files
   - Collaborative editing workflows

Limitations and Considerations:

1. Same AZ Only:
   - Cannot attach across AZs
   - Single point of failure (AZ outage)
   - Mitigation: Use snapshots to replicate to other AZs

2. File System Constraints:
   - Standard file systems not safe (ext4, xfs)
   - Must use cluster-aware FS or application locking
   - Complexity increases

3. Performance Impact:
   - More instances sharing = potential contention
   - Must design for concurrent access patterns
   - Monitor VolumeQueueLength metric

4. Instance Type Restrictions:
   - Nitro-based only
   - Older instance types not supported

5. Detachment Behavior:
   - Must detach from all instances before deleting
   - Cannot modify volume while attached to multiple instances

6. Cost:
   - io2 volumes more expensive
   - Need provisioned IOPS
   - Example: 2 TB, 20,000 IOPS = ~$1,550/month

When NOT to Use Multi-Attach:

1. Simple File Sharing:
   - Use EFS (Elastic File System) instead
   - Easier, no cluster-aware FS needed

2. Cross-AZ Redundancy:
   - Use multiple volumes with replication
   - Or use managed services (RDS, EFS)

3. High-Concurrency Writes:
   - Risk of contention
   - Consider distributed storage (S3, DynamoDB)

Monitoring Multi-Attach Volume:

```bash
# CloudWatch Metrics
- VolumeReadOps / VolumeWriteOps (per instance)
- VolumeQueueLength (shared queue depth)
- BurstBalance (if using burst credits)

# Set alarm for high contention
aws cloudwatch put-metric-alarm \
    --alarm-name multi-attach-high-queue \
    --metric-name VolumeQueueLength \
    --namespace AWS/EBS \
    --statistic Average \
    --period 60 \
    --threshold 32 \
    --comparison-operator GreaterThanThreshold \
    --dimensions Name=VolumeId,Value=vol-xxxxx
```

Best Practices:

1. Design for Concurrent Access:
   - Application-level locking if possible
   - Minimize write conflicts
   - Oracle RAC, SQL Server FCI handle this

2. Test Failover:
   - Simulate node failures
   - Verify other nodes continue operating
   - Practice disaster recovery

3. Monitor Performance:
   - Watch for I/O bottlenecks
   - May need higher IOPS if contention occurs

4. Backup Strategy:
   - Regular snapshots
   - Test restoration process
   - Can't snapshot while multiple attachments (detach first)

Summary:
Multi-attach is specialized feature for:
- Clustered databases (Oracle RAC, SQL Server FCI)
- Applications designed for shared storage
- High availability within single AZ

For most use cases, use:
- EFS for shared file storage
- Multiple EBS volumes with replication
- Managed services (RDS, Aurora)
```

---

### Question 4: Performance Troubleshooting

**Scenario:** Your application is experiencing slow EBS performance. CloudWatch shows high VolumeQueueLength and low throughput. How would you troubleshoot and resolve this?

**Answer:**
```
Troubleshooting Steps:

1. Analyze CloudWatch Metrics:

Key Metrics to Check:

a) VolumeQueueLength:
   - Current: 50 (high!)
   - Normal: < 10
   - Indicates: More I/O requests than volume can handle

b) VolumeReadOps + VolumeWriteOps:
   - Check against volume's IOPS limit
   - Example: 5,000 IOPS but volume is gp3 with 3,000 IOPS limit

c) VolumeThroughputPercentage (gp2/gp3):
   - If consistently 100%: Exhausting burst credits or hitting limits
   - Indicates: Need higher baseline performance

d) VolumeReadBytes / VolumeWriteBytes:
   - Check throughput (MB/s)
   - Compare against volume's throughput limit

e) BurstBalance (gp2 only):
   - If < 20%: Running out of burst credits
   - Indicates: Sustained high I/O

2. Check Instance-Level Limits:

Instance types have EBS performance limits:

Example: t3.medium
- EBS Bandwidth: 2,085 Mbps (260 MB/s)
- Max IOPS: 11,800

Even if volume supports 16,000 IOPS, t3.medium caps at 11,800!

```bash
# Check instance type limits
aws ec2 describe-instance-types \
    --instance-types t3.medium \
    --query 'InstanceTypes[0].EbsInfo'

# Output:
{
    "EbsOptimizedSupport": "default",
    "EncryptionSupport": "supported",
    "EbsOptimizedInfo": {
        "BaselineBandwidthInMbps": 347,
        "BaselineThroughputInMBps": 43.38,
        "BaselineIops": 2085,
        "MaximumBandwidthInMbps": 2085,
        "MaximumThroughputInMBps": 260.62,
        "MaximumIops": 11800
    }
}
```

3. Check Volume Configuration:

```bash
aws ec2 describe-volumes --volume-ids vol-xxxxx

# Check:
# - VolumeType: gp2? gp3? io2?
# - Size: Impacts IOPS for gp2
# - Iops: Provisioned IOPS
# - Throughput: Provisioned throughput (gp3)
```

4. Application-Level Investigation:

```bash
# On the instance, install iostat
sudo yum install sysstat -y

# Monitor real-time I/O
iostat -x 1

# Output:
Device  r/s    w/s   rkB/s   wkB/s  %util
xvdf    800   1200   32000   48000   98%
#                                    ^^ Near 100% = bottleneck

# Check I/O wait
top
# Look for high %wa (I/O wait) in CPU line
# Cpu(s):  10.0%us,  5.0%sy,  0.0%ni, 50.0%id, 35.0%wa
#                                                ^^ High I/O wait

# Find processes causing high I/O
sudo iotop
```

5. Common Root Causes and Solutions:

Issue 1: Volume Type Insufficient
Symptom: gp3 with default 3,000 IOPS, app needs 10,000
Solution:
```bash
# Increase IOPS (no downtime!)
aws ec2 modify-volume \
    --volume-id vol-xxxxx \
    --iops 10000

# Wait for modification to complete
aws ec2 describe-volumes-modifications --volume-id vol-xxxxx
```

Issue 2: Instance Type Too Small
Symptom: t3.medium can't deliver volume's 16,000 IOPS
Solution:
```bash
# Upgrade to larger instance
# t3.medium (11,800 IOPS) → m5.xlarge (26,250 IOPS)

# Stop instance
aws ec2 stop-instances --instance-ids i-xxxxx

# Change instance type
aws ec2 modify-instance-attribute \
    --instance-id i-xxxxx \
    --instance-type m5.xlarge

# Start instance
aws ec2 start-instances --instance-ids i-xxxxx
```

Issue 3: gp2 Burst Credits Exhausted
Symptom: BurstBalance near 0%, performance degraded to baseline
Solution:
```bash
# Check burst balance
aws cloudwatch get-metric-statistics \
    --namespace AWS/EBS \
    --metric-name BurstBalance \
    --dimensions Name=VolumeId,Value=vol-xxxxx \
    --start-time 2025-02-17T00:00:00Z \
    --end-time 2025-02-17T23:59:59Z \
    --period 3600 \
    --statistics Average

# If consistently low, migrate gp2 → gp3
aws ec2 modify-volume \
    --volume-id vol-xxxxx \
    --volume-type gp3 \
    --iops 3000

# gp3 has consistent 3,000 IOPS baseline (no burst needed)
```

Issue 4: Throughput Bottleneck
Symptom: High MB/s workload, but volume limited to 125 MB/s (gp3 default)
Solution:
```bash
# Increase throughput
aws ec2 modify-volume \
    --volume-id vol-xxxxx \
    --throughput 500

# Cost: Additional $2.25/month per 125 MB/s
```

Issue 5: EBS Not Optimized (Older instances)
Symptom: Shared bandwidth with network traffic
Solution:
```bash
# Enable EBS optimization
aws ec2 modify-instance-attribute \
    --instance-id i-xxxxx \
    --ebs-optimized

# Note: Modern instances (m5, c5, etc.) are always EBS-optimized
```

Issue 6: Application Inefficiency
Symptom: Small random I/O (4 KB), causing high IOPS usage
Example: Database with 1000 operations/sec, each 4 KB
- IOPS required: 1000
- Throughput: 4 MB/s (minimal)

Solution:
```
- Optimize queries (reduce I/O)
- Implement caching (Redis, Memcached)
- Use larger block sizes if possible
- Consider read replicas
```

6. Migration to Higher Performance Volume:

Scenario: Current gp3 insufficient, need io2

Step-by-Step:
```bash
# 1. Create snapshot (for rollback)
aws ec2 create-snapshot \
    --volume-id vol-xxxxx \
    --description "Before migration to io2"

# 2. Modify volume type (no downtime!)
aws ec2 modify-volume \
    --volume-id vol-xxxxx \
    --volume-type io2 \
    --iops 20000

# 3. Monitor modification
watch aws ec2 describe-volumes-modifications --volume-id vol-xxxxx

# Status: modifying → optimizing (can take hours) → completed

# 4. Verify performance improvement
# Watch CloudWatch metrics: VolumeQueueLength should decrease
```

7. Implement Monitoring and Alarms:

```bash
# Alarm 1: High Queue Length
aws cloudwatch put-metric-alarm \
    --alarm-name ebs-high-queue \
    --alarm-description "EBS volume queue too high" \
    --metric-name VolumeQueueLength \
    --namespace AWS/EBS \
    --statistic Average \
    --period 60 \
    --threshold 10 \
    --comparison-operator GreaterThanThreshold \
    --dimensions Name=VolumeId,Value=vol-xxxxx \
    --evaluation-periods 2

# Alarm 2: Low Burst Balance (gp2)
aws cloudwatch put-metric-alarm \
    --alarm-name ebs-low-burst \
    --metric-name BurstBalance \
    --namespace AWS/EBS \
    --statistic Average \
    --period 300 \
    --threshold 20 \
    --comparison-operator LessThanThreshold \
    --dimensions Name=VolumeId,Value=vol-xxxxx

# Alarm 3: High I/O Wait (via CloudWatch Agent)
aws cloudwatch put-metric-alarm \
    --alarm-name high-io-wait \
    --metric-name iowait \
    --namespace CWAgent \
    --statistic Average \
    --period 60 \
    --threshold 25 \
    --comparison-operator GreaterThanThreshold
```

8. Best Practices Going Forward:

1. Right-Size Initially:
   - Estimate IOPS and throughput requirements
   - Choose appropriate volume type
   - Use gp3 for most workloads (better value)

2. Monitor Proactively:
   - Set CloudWatch alarms before issues occur
   - Review performance trends weekly

3. Use Application-Level Caching:
   - ElastiCache (Redis/Memcached)
   - Reduces EBS I/O requirements

4. Optimize Application:
   - Batch writes
   - Use connection pooling (databases)
   - Implement read replicas

5. Test Before Production:
   - Load test with expected workload
   - Validate performance meets requirements

Real-World Example:

Problem:
- E-commerce site slow during checkout
- CloudWatch: VolumeQueueLength = 40, High I/O wait

Investigation:
- Volume: gp3, 100 GB, 3,000 IOPS, 125 MB/s
- Instance: t3.large (4,750 max IOPS)
- Database: PostgreSQL with many small transactions
- Actual IOPS demand: ~6,000 (exceeded both limits)

Solution:
1. Upgraded instance: t3.large → m5.xlarge (26,250 IOPS)
2. Increased volume IOPS: 3,000 → 8,000
3. Increased throughput: 125 → 250 MB/s
4. Implemented Redis cache for frequent queries

Result:
- VolumeQueueLength: 40 → 3
- Response time: 3 seconds → 300 ms
- Cost increase: $50/month (acceptable)

Cost Analysis:
- Old: t3.large ($60/month) + gp3 100GB ($8/month) = $68/month
- New: m5.xlarge ($140/month) + gp3 100GB ($8 + $33 IOPS + $1 throughput) = $182/month
- Increase: $114/month
- Value: Happy customers, increased sales
```

This completes the comprehensive EBS guide. Would you like me to continue with Snapshots, AMI, Security Groups, and User Data?

