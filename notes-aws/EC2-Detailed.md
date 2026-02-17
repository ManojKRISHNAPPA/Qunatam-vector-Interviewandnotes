# Amazon EC2 (Elastic Compute Cloud) - Complete Guide

## Table of Contents
1. [What is EC2](#what-is-ec2)
2. [Why We Need EC2](#why-we-need-ec2)
3. [Key Concepts](#key-concepts)
4. [Use Cases](#use-cases)
5. [Advantages](#advantages)
6. [Disadvantages](#disadvantages)
7. [Practical Demonstration](#practical-demonstration)
8. [Scenario-Based Interview Questions](#scenario-based-interview-questions)

---

## What is EC2?

**Amazon EC2 (Elastic Compute Cloud)** is a web service that provides secure, resizable compute capacity in the cloud. It's essentially a virtual server that runs in AWS data centers.

**Simple Analogy:** Think of EC2 as renting a computer in Amazon's data center. Instead of buying physical hardware, you rent virtual servers that you can configure, start, stop, and terminate as needed.

**Technical Definition:** EC2 provides Infrastructure as a Service (IaaS), allowing you to launch virtual machines (instances) with various configurations of CPU, memory, storage, and networking capacity.

---

## Why We Need EC2?

### Problem Statement
Traditional on-premises infrastructure has several challenges:
- **High upfront costs:** Purchase servers, storage, networking equipment
- **Long procurement time:** Weeks or months to acquire and setup hardware
- **Capacity planning difficulties:** Over-provisioning (wasted money) or under-provisioning (performance issues)
- **Maintenance overhead:** Hardware failures, upgrades, patching
- **Physical space requirements:** Data center space, cooling, power
- **Scalability limitations:** Can't quickly scale up/down based on demand

### EC2 Solution
EC2 solves these problems by providing:
- **On-demand computing:** Launch servers in minutes
- **Pay-as-you-go:** Only pay for what you use
- **Elastic scalability:** Scale up/down automatically
- **No hardware management:** AWS handles physical infrastructure
- **Global availability:** Deploy worldwide in minutes

---

## Key Concepts

### 1. Instance
A virtual server running in the AWS cloud. Each instance is a complete computing environment with:
- Operating system (Linux, Windows, etc.)
- CPU (vCPU)
- Memory (RAM)
- Storage (EBS or Instance Store)
- Network interface

### 2. Instance Types
AWS offers different instance families optimized for specific workloads:

| Family | Purpose | Use Case | Example |
|--------|---------|----------|---------|
| **General Purpose** | Balanced compute, memory, networking | Web servers, dev environments | t3.micro, t3.medium, m5.large |
| **Compute Optimized** | High-performance processors | Batch processing, gaming servers | c5.large, c6i.xlarge |
| **Memory Optimized** | Fast performance for large datasets | Databases, in-memory caches | r5.large, x1e.xlarge |
| **Storage Optimized** | High sequential read/write | Data warehouses, log processing | i3.large, d2.xlarge |
| **Accelerated Computing** | Hardware accelerators (GPU) | ML training, video rendering | p3.2xlarge, g4dn.xlarge |

### 3. Instance States
- **Pending:** Instance is launching
- **Running:** Instance is running and ready
- **Stopping:** Instance is shutting down
- **Stopped:** Instance is stopped (EBS-backed only)
- **Shutting-down:** Instance is terminating
- **Terminated:** Instance is permanently deleted

### 4. Pricing Models

#### a) On-Demand Instances
- Pay by the hour or second
- No long-term commitment
- Best for: Short-term, unpredictable workloads

#### b) Reserved Instances (RI)
- 1 or 3-year commitment
- Up to 75% discount compared to On-Demand
- Best for: Steady-state applications

#### c) Spot Instances
- Bid on unused EC2 capacity
- Up to 90% discount
- Can be interrupted with 2-minute warning
- Best for: Fault-tolerant, flexible workloads

#### d) Savings Plans
- Flexible pricing model
- 1 or 3-year commitment
- Up to 72% savings

#### e) Dedicated Hosts
- Physical server dedicated to your use
- Best for: Compliance requirements, licensing

---

## Use Cases

### 1. Web Application Hosting
**Scenario:** Host a dynamic e-commerce website
- Use Auto Scaling to handle traffic spikes
- Load balancer distributes traffic
- Multiple instances for high availability

### 2. Development and Testing
**Scenario:** Developers need environments for testing
- Spin up instances on-demand
- Terminate when not needed
- Cost-effective for temporary needs

### 3. Big Data Processing
**Scenario:** Process large datasets
- Launch compute-optimized instances
- Process data and terminate
- Pay only for processing time

### 4. Disaster Recovery
**Scenario:** Backup site for on-premises infrastructure
- Keep AMIs and data in AWS
- Launch instances when primary site fails
- Minimal standby costs

### 5. Batch Processing
**Scenario:** Nightly batch jobs
- Use Spot Instances for cost savings
- Schedule jobs during off-peak hours
- Automatic termination after completion

### 6. High-Performance Computing (HPC)
**Scenario:** Scientific simulations, financial modeling
- Use cluster placement groups
- High-performance instance types
- Low-latency networking

---

## Advantages

### 1. **Elasticity**
- Scale up/down based on demand
- Auto Scaling groups automate this process
- Handle traffic spikes without over-provisioning

### 2. **Cost-Effective**
- No upfront hardware costs
- Pay-as-you-go pricing
- Multiple pricing models to optimize costs
- Only pay for what you use

### 3. **Reliability**
- 99.99% SLA (with proper architecture)
- Multiple Availability Zones
- Automatic health checks
- Easy to replace failed instances

### 4. **Security**
- Security Groups (firewall)
- Network ACLs
- IAM for access control
- Encryption options
- VPC isolation

### 5. **Global Infrastructure**
- Deploy in multiple regions worldwide
- Low latency for global users
- Data residency compliance

### 6. **Flexibility**
- Wide variety of instance types
- Multiple operating systems
- Custom configurations
- Easy to change instance types

### 7. **Integration**
- Seamless integration with other AWS services
- S3, RDS, CloudWatch, Lambda, etc.
- Rich ecosystem of tools

### 8. **Speed**
- Launch instances in minutes
- Rapid prototyping and deployment
- Fast time-to-market

---

## Disadvantages

### 1. **Complexity**
- Steep learning curve for beginners
- Many options and configurations
- Requires understanding of networking, security
- **Mitigation:** Start with AWS tutorials, use AWS Well-Architected Framework

### 2. **Costs Can Escalate**
- Easy to lose track of running instances
- Data transfer costs can be high
- Costs accumulate over time
- **Mitigation:** Use Cost Explorer, set billing alarms, implement tagging

### 3. **Vendor Lock-in**
- Difficult to migrate to another cloud provider
- AWS-specific configurations
- **Mitigation:** Use containerization, Infrastructure as Code

### 4. **Performance Variability**
- Shared infrastructure (noisy neighbor)
- Network latency variations
- **Mitigation:** Use dedicated instances or hosts

### 5. **Limited Control**
- No access to physical hardware
- Dependent on AWS for infrastructure management
- **Mitigation:** Accept this trade-off for convenience

### 6. **Data Transfer Costs**
- Outbound data transfer fees
- Inter-region transfer costs
- **Mitigation:** Use CloudFront, optimize data transfer

### 7. **Security Responsibility**
- Shared responsibility model
- You manage OS and application security
- **Mitigation:** Follow AWS security best practices

### 8. **Temporary Storage Limitations**
- Instance Store is ephemeral
- Data lost on instance stop/terminate
- **Mitigation:** Use EBS for persistent storage

---

## Practical Demonstration

### Demo 1: Launching Your First EC2 Instance

#### Step 1: Access EC2 Console
```
1. Log in to AWS Management Console
2. Navigate to EC2 Dashboard
3. Click "Launch Instance"
```

#### Step 2: Choose AMI
```
1. Select "Amazon Linux 2 AMI" (Free Tier eligible)
2. This is a pre-configured template with OS and software
```

#### Step 3: Choose Instance Type
```
1. Select "t2.micro" (Free Tier: 750 hours/month)
   - 1 vCPU
   - 1 GB RAM
   - Low to moderate network performance
```

#### Step 4: Configure Instance Details
```
Number of instances: 1
Network: Default VPC
Subnet: No preference (default)
Auto-assign Public IP: Enable
IAM Role: None (for now)
Shutdown behavior: Stop
Enable termination protection: No
Monitoring: Enable CloudWatch detailed monitoring (optional)
Tenancy: Shared
```

#### Step 5: Add Storage
```
Volume Type: Root (General Purpose SSD - gp2)
Size: 8 GB (default)
Delete on Termination: Yes (default)
```

#### Step 6: Add Tags
```
Key: Name
Value: MyFirstEC2Instance

Key: Environment
Value: Development
```

#### Step 7: Configure Security Group
```
Create a new security group:
Name: web-server-sg
Description: Allow SSH and HTTP

Rule 1:
Type: SSH
Protocol: TCP
Port: 22
Source: My IP (your current IP)

Rule 2:
Type: HTTP
Protocol: TCP
Port: 80
Source: Anywhere (0.0.0.0/0)
```

#### Step 8: Review and Launch
```
1. Review all configurations
2. Click "Launch"
3. Create or select a key pair:
   - Create new key pair
   - Name: my-ec2-keypair
   - Download .pem file (KEEP IT SAFE!)
```

#### Step 9: Connect to Instance

**For Linux/Mac:**
```bash
# Change permissions of key file
chmod 400 my-ec2-keypair.pem

# Connect via SSH
ssh -i "my-ec2-keypair.pem" ec2-user@<PUBLIC_IP>
```

**For Windows:**
Use PuTTY or PowerShell:
```powershell
ssh -i "my-ec2-keypair.pem" ec2-user@<PUBLIC_IP>
```

---

### Demo 2: Installing and Running a Web Server

#### Once connected to your EC2 instance:

```bash
# Update system packages
sudo yum update -y

# Install Apache web server
sudo yum install httpd -y

# Start Apache service
sudo systemctl start httpd

# Enable Apache to start on boot
sudo systemctl enable httpd

# Check status
sudo systemctl status httpd

# Create a simple HTML page
echo "<h1>Hello from EC2!</h1>" | sudo tee /var/www/html/index.html

# Verify: Open browser and navigate to http://<PUBLIC_IP>
```

---

### Demo 3: Creating a Custom AMI

```bash
# After configuring your instance with software and settings:

1. In EC2 Console, select your instance
2. Actions → Image and templates → Create image
3. Image name: my-web-server-ami
4. Image description: Web server with Apache pre-installed
5. No reboot: Unchecked (for data consistency)
6. Click "Create Image"

# Your AMI can now be used to launch identical instances
```

---

### Demo 4: Monitoring with CloudWatch

```bash
# CloudWatch automatically monitors:
- CPU Utilization
- Network In/Out
- Disk Read/Write (if CloudWatch agent installed)
- Status Checks

# View metrics in EC2 Console:
1. Select your instance
2. Click "Monitoring" tab
3. View graphs for CPU, Network, etc.

# Set up an alarm:
1. Go to CloudWatch
2. Create Alarm
3. Select Metric: EC2 → Per-Instance Metrics → CPUUtilization
4. Conditions: Greater than 80% for 2 consecutive periods
5. Actions: Send notification to SNS topic
```

---

### Demo 5: Stopping, Starting, and Terminating

```bash
# Stopping an Instance (EBS-backed only):
1. Select instance
2. Instance state → Stop instance
3. You're charged for EBS storage, not compute
4. Public IP is released (use Elastic IP to keep it)

# Starting a Stopped Instance:
1. Select instance
2. Instance state → Start instance
3. New public IP assigned (unless using Elastic IP)

# Terminating an Instance:
1. Select instance
2. Instance state → Terminate instance
3. Warning: This is permanent!
4. EBS volumes deleted if "Delete on Termination" is Yes
```

---

## Scenario-Based Interview Questions

### Question 1: High Availability Web Application

**Scenario:** You need to deploy a web application that must be highly available and handle variable traffic. The application runs on EC2 instances. How would you design this?

**Answer:**
```
Architecture:
1. Multi-AZ Deployment:
   - Launch EC2 instances in at least 2 Availability Zones
   - Ensures availability if one AZ fails

2. Auto Scaling Group (ASG):
   - Define min: 2, desired: 2, max: 10 instances
   - Automatically scales based on CPU or custom metrics
   - Replaces unhealthy instances automatically

3. Elastic Load Balancer (ELB):
   - Application Load Balancer distributes traffic
   - Health checks ensure traffic goes to healthy instances
   - Cross-zone load balancing enabled

4. Security:
   - Instances in private subnets (no direct internet access)
   - ELB in public subnet
   - Security groups restrict access

5. Monitoring:
   - CloudWatch alarms for CPU, memory, requests
   - SNS notifications for critical issues

Diagram:
Internet → ELB (Public Subnet) →
  → EC2 Instance (AZ-1, Private Subnet)
  → EC2 Instance (AZ-2, Private Subnet)
```

---

### Question 2: Cost Optimization

**Scenario:** Your company runs a data processing application on EC2 that processes data every night from 2 AM to 6 AM. During the day, instances are idle. How would you optimize costs?

**Answer:**
```
Solutions:

1. Scheduled Scaling:
   - Use AWS Instance Scheduler or EventBridge
   - Stop instances at 6 AM, start at 1:45 AM
   - Save ~20 hours/day of compute costs

2. Use Spot Instances:
   - Data processing is fault-tolerant
   - Spot instances offer up to 90% discount
   - Use Spot Fleet for mix of instance types
   - Handle spot interruptions gracefully

3. Right-sizing:
   - Analyze actual resource usage
   - Use compute-optimized instances (c5.large instead of m5.xlarge)
   - Test with smaller instance types

4. Reserved Instances (if baseline needed):
   - Purchase RI for minimum baseline capacity
   - Use Spot/On-Demand for additional capacity

5. Lambda Alternative:
   - If processing can be broken into tasks
   - Use Lambda for event-driven processing
   - Pay only for execution time

Cost Comparison:
- Current: m5.xlarge On-Demand 24/7 = $140/month
- Optimized: c5.large Spot 4 hours/day = $8-10/month
- Savings: ~93%
```

---

### Question 3: Security Breach Response

**Scenario:** You suspect an EC2 instance has been compromised. What immediate steps would you take?

**Answer:**
```
Immediate Actions:

1. Isolate the Instance:
   - Change Security Group to deny all inbound/outbound traffic
   - Or attach a "quarantine" security group
   - Do NOT terminate yet (preserve evidence)

2. Snapshot for Forensics:
   - Create snapshots of all EBS volumes
   - These snapshots preserve state for investigation
   - Tag with "Forensic-Investigation" and timestamp

3. Capture Memory (if possible):
   - Use SSM or tools to dump memory before stopping
   - Memory contains running processes, connections

4. Revoke Credentials:
   - Rotate any IAM credentials that were on the instance
   - Revoke any temporary credentials
   - Check CloudTrail for unauthorized API calls

5. Investigation:
   - Review CloudTrail logs for unusual API calls
   - Check VPC Flow Logs for unusual network patterns
   - Review CloudWatch Logs for application logs
   - Look for unauthorized changes in Config

6. Launch Replacement:
   - Launch new instance from trusted AMI
   - Apply latest security patches
   - Implement stricter security controls

7. Post-Incident:
   - Identify root cause (exposed credentials, vulnerable software, etc.)
   - Implement preventive measures
   - Update incident response playbook

Prevention Measures:
- Use Systems Manager Session Manager (no SSH keys)
- Implement IMDSv2 (prevent SSRF attacks)
- Use GuardDuty for threat detection
- Regular security patching
- Principle of least privilege for IAM
```

---

### Question 4: Instance Performance Issues

**Scenario:** Users report that your EC2-based application is slow. How would you troubleshoot and resolve this?

**Answer:**
```
Troubleshooting Steps:

1. Check CloudWatch Metrics:
   a) CPU Utilization:
      - If >80%: CPU-bound, need more compute
      - Solution: Upgrade to larger instance or scale out

   b) Network In/Out:
      - If hitting instance network limits
      - Solution: Use network-optimized instance (ena enabled)

   c) Disk I/O:
      - EBS volumes have IOPS limits
      - Solution: Use io2 volumes or increase gp3 IOPS

   d) Memory (needs CloudWatch agent):
      - If memory is full, leads to swapping
      - Solution: Upgrade to memory-optimized instance

2. Application-Level Issues:
   a) Check application logs:
      - Database connection timeouts
      - External API slowness
      - Memory leaks

   b) Use APM tools:
      - AWS X-Ray for tracing
      - New Relic, DataDog, etc.

3. Network Issues:
   a) Security Group rules:
      - Check if throttling connections

   b) VPC configuration:
      - NAT Gateway throttling
      - Internet Gateway limits

   c) External dependencies:
      - RDS database performance
      - S3 throttling

4. Instance-Level Issues:
   a) Instance type mismatch:
      - General purpose vs. compute-optimized

   b) Placement group:
      - Use cluster placement for low latency

   c) EBS optimization:
      - Ensure EBS-optimized instance type

   d) Instance age:
      - Older generation instances slower
      - Migrate to newer generation (m5 vs m4)

5. Quick Wins:
   - Enable Enhanced Networking (SR-IOV)
   - Use Elastic Load Balancer for distribution
   - Implement caching (ElastiCache)
   - Use CloudFront for static content
   - Enable Auto Scaling for horizontal scaling

Real Example:
Problem: Application slow during peak hours
Investigation: CloudWatch showed CPU at 100%
Root Cause: Single t3.medium instance
Solution:
  - Implemented Auto Scaling (2-5 instances)
  - Added Application Load Balancer
  - Changed to c5.large (compute-optimized)
Result: Response time improved from 3s to 300ms
```

---

### Question 5: Instance Store vs EBS

**Scenario:** You're deploying a high-performance database that requires very low latency storage. Should you use Instance Store or EBS? Explain your reasoning.

**Answer:**
```
Comparison:

Instance Store:
Pros:
- Very high IOPS (millions)
- Included in instance cost
- No network latency (directly attached)
- Ideal for temporary data, caches

Cons:
- Ephemeral (data lost on stop/terminate)
- No snapshots
- Can't detach and attach to another instance
- Data lost on hardware failure

EBS:
Pros:
- Persistent storage
- Snapshots for backup
- Can detach/attach to instances
- Multiple volume types (gp3, io2)
- Encryption at rest

Cons:
- Network-attached (some latency)
- Additional cost
- IOPS limits (though very high with io2)

Recommendation for High-Performance Database:

Option 1: Instance Store (i3/i4i instances)
Best for:
- Replicated databases (Cassandra, MongoDB)
- Data can be restored from replica
- Need millions of IOPS
- Cost-sensitive

Architecture:
- Use i3.large or higher
- Implement database replication (minimum 3 nodes)
- Regular backups to S3
- Automate restoration process
- Accept that individual nodes are ephemeral

Option 2: EBS io2 Volumes
Best for:
- Single-instance databases
- Need data persistence
- Can tolerate slightly higher latency
- Need point-in-time recovery

Architecture:
- Use io2 Block Express volumes (up to 256,000 IOPS)
- EBS-optimized instance type
- Automated EBS snapshots
- Can stop/start instance without data loss

Hybrid Approach (Best of Both):
1. Use i3 instance with Instance Store
2. Database primary storage on Instance Store
3. Write-Ahead Logs (WAL) on EBS
4. Automated backups to S3
5. Benefits:
   - Ultra-low latency for reads/writes
   - WAL on EBS provides durability
   - S3 backups for disaster recovery

Real-World Example:
Netflix uses:
- Cassandra on i3 instances with Instance Store
- Multi-region replication
- Automated backup to S3
- Can lose individual nodes without impact
- Achieves microsecond latencies
```

---

### Question 6: Multi-Region Deployment

**Scenario:** Your application serves users globally. You need to deploy EC2 instances in multiple AWS regions for low latency. How would you design this?

**Answer:**
```
Architecture:

1. DNS Layer (Route 53):
   - Geolocation routing: Direct users to nearest region
   - Or Latency-based routing: Route to lowest latency region
   - Health checks: Failover to healthy regions

2. Per-Region Architecture:
   Each region has:
   - VPC with public/private subnets across 2+ AZs
   - Application Load Balancer (public subnet)
   - EC2 instances in Auto Scaling Group (private subnet)
   - Regional RDS database (or DynamoDB Global Tables)
   - ElastiCache for regional caching

3. Data Synchronization:

   Option A: Database Replication
   - Primary region: us-east-1
   - Replica regions: eu-west-1, ap-south-1
   - Read replicas in each region
   - Writes go to primary, reads from local replica
   - RDS Cross-Region Read Replicas or DynamoDB Global Tables

   Option B: Active-Active
   - DynamoDB Global Tables (multi-region writes)
   - Conflict resolution automatically handled
   - All regions can write

4. Shared Resources:
   - S3 with Cross-Region Replication
   - CloudFront for static content (global CDN)
   - Centralized logging (CloudWatch Logs)

5. Deployment Strategy:
   - Infrastructure as Code (Terraform/CloudFormation)
   - Deploy same stack to multiple regions
   - CI/CD pipeline (CodePipeline/Jenkins)
   - Blue/Green deployments per region

6. Monitoring:
   - CloudWatch dashboards per region
   - Aggregated metrics in primary region
   - Route 53 health checks
   - SNS notifications for failures

Example Configuration:

Route 53:
- api.example.com
  - Geolocation: North America → us-east-1
  - Geolocation: Europe → eu-west-1
  - Geolocation: Asia → ap-south-1
  - Default: us-east-1

Region: us-east-1 (Primary)
├── VPC (10.0.0.0/16)
├── Public Subnet AZ1 (10.0.1.0/24): ALB
├── Public Subnet AZ2 (10.0.2.0/24): ALB
├── Private Subnet AZ1 (10.0.11.0/24): EC2 ASG
├── Private Subnet AZ2 (10.0.12.0/24): EC2 ASG
├── RDS Primary
└── ElastiCache

Region: eu-west-1 (Secondary)
├── VPC (10.1.0.0/16)
├── [Same structure]
├── RDS Read Replica (from us-east-1)
└── ElastiCache

Challenges & Solutions:

1. Data Consistency:
   Challenge: Eventual consistency with replication lag
   Solution:
   - Use DynamoDB Global Tables for strong consistency
   - Or accept eventual consistency and design accordingly
   - Critical writes to primary region only

2. Increased Costs:
   Challenge: Running resources in multiple regions
   Solution:
   - Use Auto Scaling to minimize instances
   - Reserved Instances for baseline capacity
   - CloudFront reduces origin requests

3. Complexity:
   Challenge: Managing multiple regions
   Solution:
   - Automate everything with IaC
   - Centralized monitoring and alerting
   - Standardize configurations

4. Cross-Region Data Transfer:
   Challenge: Data transfer costs
   Solution:
   - Use CloudFront for static content
   - Minimize cross-region traffic
   - Compress data before transfer
```

---

### Question 7: Auto Scaling Strategy

**Scenario:** Design an Auto Scaling strategy for an e-commerce website that experiences predictable traffic spikes during sales events (Black Friday) and regular daily patterns.

**Answer:**
```
Auto Scaling Strategy:

1. Base Configuration:
   - Launch Configuration/Template with:
     - AMI: Pre-configured with application
     - Instance Type: m5.large (compute + memory balanced)
     - Security Groups, IAM Role
     - User Data for bootstrapping

2. Auto Scaling Group Configuration:

   A. Capacity Settings:
      - Minimum: 2 (always maintain 2 for HA)
      - Desired: 4 (normal traffic baseline)
      - Maximum: 50 (handle extreme spikes)

   B. Multi-AZ Deployment:
      - Distribute across 3 AZs
      - Even distribution for balanced load

3. Scaling Policies:

   A. Target Tracking Scaling (Primary):
      - Target Metric: Average CPU Utilization
      - Target Value: 60%
      - Warm-up time: 180 seconds (3 minutes)
      - Rationale: Keeps CPU under control, allows for bursts

   B. Step Scaling (For rapid spikes):
      - Trigger: CPUUtilization > 80% for 2 minutes
      - Add instances:
        - 80-90%: Add 2 instances
        - 90-100%: Add 5 instances

      - Trigger: CPUUtilization < 30% for 10 minutes
      - Remove instances:
        - Decrease by 1 instance (gradual scale-in)

   C. Scheduled Scaling (For predictable patterns):

      Daily Pattern:
      - 8:00 AM: Increase to 6 instances (business hours start)
      - 10:00 PM: Decrease to 3 instances (low traffic)

      Weekly Pattern:
      - Monday 7:00 AM: Increase to 8 instances (week start)
      - Friday 6:00 PM: Decrease to 4 instances (weekend)

      Black Friday Event:
      - November 24, 11:00 PM: Pre-scale to 30 instances
      - November 25, 12:00 AM: Scale to 50 instances
      - November 25, 6:00 AM: Reduce to 25 instances
      - November 25, 12:00 PM: Return to normal (dynamic scaling)

4. Advanced Configurations:

   A. Instance Warmup:
      - Default instance warmup: 180 seconds
      - Prevents premature scaling decisions
      - Allows application to fully start

   B. Health Checks:
      - ELB health check: 30-second interval
      - Grace period: 300 seconds (5 minutes)
      - Unhealthy threshold: 2 consecutive failures

   C. Termination Policy:
      - OldestInstance (for rolling updates)
      - Or ClosestToNextInstanceHour (cost optimization)

   D. Instance Protection:
      - Protect instances during critical operations
      - Prevent scale-in during deployments

5. Cost Optimization:

   A. Mix Instance Types (If possible):
      - On-Demand: 2 instances (baseline)
      - Reserved: 2 instances (1-year term)
      - Spot: Up to 46 instances (handle spikes)

   B. Spot Instance Strategy:
      - Use multiple instance types (m5.large, m5.xlarge)
      - Diversified across AZs
      - Spot allocation strategy: capacity-optimized
      - Handle spot interruptions gracefully

   C. Savings Plans:
      - Commit to $X/hour for compute
      - Covers baseline usage

6. Monitoring and Alarms:

   A. CloudWatch Alarms:
      - CPU > 80% for 5 minutes → Alert operations
      - Instances < 2 → Critical alarm (below minimum)
      - Failed status checks → Replace instance

   B. Custom Metrics:
      - Application-specific metrics (requests/second)
      - Database connection pool usage
      - Memory utilization (CloudWatch agent)

   C. Scaling Activity Logs:
      - Track all scaling events
      - Analyze patterns for optimization

7. Testing Strategy:

   A. Load Testing:
      - Use tools like Apache JMeter, Locust
      - Simulate Black Friday traffic
      - Validate scaling behavior

   B. Chaos Engineering:
      - Randomly terminate instances
      - Ensure Auto Scaling recovers
      - Test resilience

Example Timeline (Black Friday):

Nov 24, 11:00 PM:
- Scheduled scaling: 30 instances launched
- Load balanced across 3 AZs

Nov 25, 12:00 AM (Black Friday starts):
- Scheduled scaling: 50 instances
- Traffic spike: 10,000 requests/second
- All instances healthy, CPU avg 65%

Nov 25, 12:30 AM:
- Unexpected spike: CPU jumps to 85%
- Step scaling triggers: Add 5 instances
- Total: 55 instances (exceeded max, capped at 50)
- Alarm sent to operations team

Nov 25, 1:00 AM:
- Traffic normalizes: CPU drops to 60%
- Instances remain at 50 (no scale-in yet)

Nov 25, 6:00 AM:
- Scheduled scaling: Reduce to 25 instances
- Gradual scale-in over 30 minutes

Nov 25, 12:00 PM:
- Return to dynamic scaling
- Target tracking adjusts based on actual traffic

Key Learnings:
- Scheduled scaling for predictable patterns
- Dynamic scaling for unexpected spikes
- Gradual scale-in to prevent flapping
- Pre-warming for major events
- Monitor and adjust thresholds based on data
```

---

### Question 8: Placement Groups

**Scenario:** Explain when and why you would use different types of EC2 placement groups. Provide real-world examples.

**Answer:**
```
EC2 Placement Groups: Types and Use Cases

1. Cluster Placement Group:

What:
- Instances placed close together in single AZ
- Low-latency, high-throughput network
- 10 Gbps or 25 Gbps network speed between instances

When to Use:
- High-Performance Computing (HPC)
- Distributed databases requiring low latency
- Big data analytics
- Applications requiring high network throughput

Advantages:
- Lowest possible network latency
- Highest network throughput
- Full bisection bandwidth

Disadvantages:
- Single AZ (no fault tolerance)
- Limited to one AZ
- Capacity limitations (launch all at once)

Real-World Example:
Company: Financial services firm
Use Case: High-frequency trading platform
- Cluster placement group in us-east-1a
- c5n.18xlarge instances (100 Gbps network)
- Co-located database and application servers
- Sub-millisecond latencies critical
- Trades executed in microseconds

Configuration:
aws ec2 create-placement-group \
  --group-name hft-cluster \
  --strategy cluster

aws ec2 run-instances \
  --placement "GroupName=hft-cluster" \
  --instance-type c5n.18xlarge \
  --count 10

---

2. Spread Placement Group:

What:
- Instances spread across different hardware
- Maximum 7 instances per AZ per group
- Each instance on distinct rack

When to Use:
- Critical applications requiring HA
- Each instance must be isolated from failures
- Small number of critical instances
- Reduce correlated failures

Advantages:
- Minimizes risk of simultaneous failures
- Instances on different physical hardware
- Can span multiple AZs

Disadvantages:
- Limited to 7 instances per AZ
- Not suitable for large deployments

Real-World Example:
Company: Healthcare SaaS provider
Use Case: HIPAA-compliant medical record system
- Spread placement group across 3 AZs
- 7 instances per AZ = 21 total
- Each instance handles different patient data
- Hardware failure affects only 1 instance
- Meets compliance requirements

Configuration:
aws ec2 create-placement-group \
  --group-name medical-spread \
  --strategy spread

aws ec2 run-instances \
  --placement "GroupName=medical-spread" \
  --instance-type m5.xlarge \
  --count 21 \
  --subnet-ids subnet-1a subnet-1b subnet-1c

---

3. Partition Placement Group:

What:
- Divides instances into logical partitions
- Each partition on separate racks
- Up to 7 partitions per AZ
- Hundreds of instances supported

When to Use:
- Large distributed systems
- Hadoop, Cassandra, Kafka clusters
- Fault-tolerant applications
- Need more than 7 instances per AZ with isolation

Advantages:
- Supports large deployments
- Partition-level fault isolation
- Visibility into partition placement
- Spans multiple AZs

Disadvantages:
- More complex than spread
- Partition-level failure impacts multiple instances

Real-World Example:
Company: Social media analytics startup
Use Case: Kafka cluster for real-time data processing
- 3 AZs, 7 partitions per AZ = 21 partitions
- 10 Kafka brokers per partition = 210 brokers
- Topic replication across partitions
- Partition failure loses max 10 brokers
- Kafka replication ensures no data loss

Configuration:
aws ec2 create-placement-group \
  --group-name kafka-partition \
  --strategy partition

aws ec2 run-instances \
  --placement "GroupName=kafka-partition,PartitionNumber=1" \
  --instance-type m5.2xlarge \
  --count 10

---

Comparison Table:

| Feature | Cluster | Spread | Partition |
|---------|---------|--------|-----------|
| Max instances | Hundreds | 7 per AZ | Hundreds |
| Isolation level | None | Instance | Partition |
| Network performance | Highest | Normal | Normal |
| Multi-AZ | No | Yes | Yes |
| Use case | HPC, low latency | HA, critical apps | Large distributed systems |

---

Interview Follow-up Questions:

Q: Can you mix instance types in a placement group?
A:
- Cluster: Recommended to use same instance type and launch simultaneously
- Spread: Can mix, but consider capacity constraints
- Partition: Can mix freely

Q: What happens if placement group capacity is insufficient?
A:
- Cluster: Launch fails if insufficient capacity
- Solution: Stop all instances, then restart (gets new hardware allocation)
- Or launch all instances at once initially

Q: Can you move an existing instance to a placement group?
A:
- No, can't move running instances
- Must stop instance → change placement group → start
- Applies only to stopped instances

Q: How do you monitor placement group health?
A:
- CloudWatch metrics per instance
- Status checks (system + instance)
- VPC Flow Logs for network issues
- Custom health check scripts

Q: Cost implications?
A:
- No additional cost for placement groups
- Enhanced networking (SR-IOV) included
- Pay only for instance types used
```

This completes the comprehensive EC2 guide. Would you like me to continue with the other topics (EBS, Snapshots, AMI, Security Groups, and User Data)?

