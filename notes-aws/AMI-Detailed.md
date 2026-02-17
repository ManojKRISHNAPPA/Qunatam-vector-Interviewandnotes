# Amazon Machine Images (AMI) - Complete Guide

## Table of Contents
1. [What is an AMI](#what-is-an-ami)
2. [Why We Need AMIs](#why-we-need-amis)
3. [Key Concepts](#key-concepts)
4. [AMI Types](#ami-types)
5. [Use Cases](#use-cases)
6. [Advantages](#advantages)
7. [Disadvantages](#disadvantages)
8. [Practical Demonstration](#practical-demonstration)
9. [Scenario-Based Interview Questions](#scenario-based-interview-questions)

---

## What is an AMI?

**Amazon Machine Image (AMI)** is a template that contains the software configuration (operating system, application server, applications) required to launch an EC2 instance. It's essentially a pre-configured snapshot of a complete server environment.

**Simple Analogy:** An AMI is like a photograph of a fully configured computer. When you want an identical computer, you use the photograph (AMI) to recreate it exactly as it was - same operating system, same software, same settings.

**Technical Definition:** An AMI is a packaged environment that includes:
- Root volume template (operating system, application software)
- Launch permissions (which AWS accounts can use it)
- Block device mapping (specifies volumes to attach)

### AMI Components:
1. **Root Volume Template:** EBS snapshot or instance store template
2. **Launch Permissions:** Public, private, or specific AWS accounts
3. **Block Device Mapping:** Defines volumes (EBS or instance store)

---

## Why We Need AMIs?

### Problems Without AMIs:
1. **Time-Consuming Setup:** Configure each instance from scratch
2. **Inconsistency:** Manual configuration leads to variations
3. **No Repeatability:** Can't easily replicate environments
4. **Slow Scaling:** Takes time to launch and configure new instances
5. **Complex Deployments:** Error-prone manual deployments

### AMI Solutions:
1. **Rapid Deployment:** Launch pre-configured instances in minutes
2. **Consistency:** Identical configuration across all instances
3. **Automation:** Auto Scaling uses AMIs for automatic instance creation
4. **Version Control:** Different AMIs for different software versions
5. **Disaster Recovery:** Quick recovery with pre-configured AMIs
6. **Multi-Region Deployment:** Copy AMIs to other regions

### Real-World Scenario:
**Problem:** Need to launch 100 web servers for Black Friday sale
- **Without AMI:** Install OS, web server, app code on each = 100 hours
- **With AMI:** Launch 100 instances from AMI = 10 minutes

---

## Key Concepts

### 1. AMI Lifecycle

```
┌─────────────────┐
│  Source Instance│
│  - OS installed │
│  - Apps config  │
│  - Code deployed│
└────────┬────────┘
         │
         │ Create Image
         ▼
┌─────────────────┐
│   AMI Created   │
│  - EBS Snapshot │
│  - Configuration│
└────────┬────────┘
         │
         │ Launch Instance
         ▼
┌─────────────────┐
│  New Instances  │
│  (Identical to  │
│   source)       │
└─────────────────┘
```

### 2. AMI ID

Format: `ami-0123456789abcdef0`
- Region-specific (different ID in different regions)
- Unique within a region
- Never changes (immutable)

### 3. AMI State

- **Pending:** AMI being created
- **Available:** Ready to launch instances
- **Failed:** Creation failed
- **Deregistered:** AMI deleted (snapshots remain)

### 4. Root Device Type

#### a) EBS-Backed AMI (Most Common)
- Root volume is EBS snapshot
- Instance can be stopped and started
- Data persists when instance stopped
- Faster boot time (typically)

#### b) Instance Store-Backed AMI
- Root volume is instance store template
- Instance cannot be stopped (only running or terminated)
- Data lost when instance stops
- Used for temporary/ephemeral workloads

### 5. Virtualization Type

#### a) Hardware Virtual Machine (HVM)
- Full virtualization
- Better performance
- Required for modern instance types (m5, c5, etc.)
- **Recommended**

#### b) Paravirtual (PV)
- Legacy virtualization
- Older instance types only
- Not recommended for new deployments

### 6. AMI Permissions

**Private (Default):**
- Only your AWS account can use it
- Most secure

**Public:**
- Anyone can launch instances from it
- Use for sharing open-source configurations

**Explicit:**
- Specific AWS accounts granted permission
- Controlled sharing with partners/customers

---

## AMI Types

### 1. Amazon-Provided AMIs

**What:** Pre-built AMIs maintained by AWS

**Examples:**
- Amazon Linux 2 (Free Tier eligible)
- Ubuntu Server
- Windows Server
- Red Hat Enterprise Linux (RHEL)
- SUSE Linux
- Deep Learning AMIs (pre-installed ML frameworks)

**Use Cases:**
- Starting point for new projects
- Standard operating systems
- Quick proof-of-concepts

**Advantages:**
- Maintained and patched by AWS
- Free (except Windows/RHEL license costs)
- Well-tested and reliable

### 2. AWS Marketplace AMIs

**What:** Commercial AMIs from third-party vendors

**Examples:**
- WordPress (pre-configured LAMP stack)
- GitLab (complete CI/CD platform)
- Fortinet firewall
- Splunk (log analysis)
- Cisco network appliances

**Use Cases:**
- Enterprise software with support
- Pre-configured complex applications
- Compliance-certified images

**Costs:**
- Software licensing fees (hourly or annual)
- EC2 instance costs (separate)

### 3. Community AMIs

**What:** AMIs shared by other AWS users

**Examples:**
- Custom Linux distributions
- Pre-configured development environments
- Open-source application stacks

**Caution:**
- Not verified by AWS
- Security risk (may contain malware)
- Use only from trusted sources
- Scan before use

### 4. Custom/Private AMIs

**What:** AMIs you create from your configured instances

**Use Cases:**
- Your application deployments
- Company-standard configurations
- Golden images for compliance

**Benefits:**
- Full control over configuration
- Proprietary software installations
- Optimized for your workload

---

## Use Cases

### 1. Application Deployment and Scaling

**Scenario:** E-commerce website with variable traffic

**Setup:**
```
1. Configure "golden instance":
   - Install NGINX
   - Deploy application code
   - Install dependencies
   - Configure settings
   - Security hardening

2. Create AMI from golden instance

3. Configure Auto Scaling:
   - Launch Configuration uses custom AMI
   - Auto Scaling launches instances from AMI
   - All instances identical (consistency)

4. Deployment:
   - New version ready → Update golden instance
   - Create new AMI (v2.0)
   - Update Auto Scaling launch configuration
   - Replace instances gradually (rolling deployment)
```

**Benefits:**
- Instant deployment of pre-configured instances
- Consistent environment
- Easy rollback (use previous AMI)

---

### 2. Disaster Recovery

**Scenario:** Production database in us-east-1, need DR in us-west-2

**Setup:**
```
1. Create AMI of production database instance
2. Copy AMI to us-west-2
3. In case of disaster:
   - Launch instance from AMI in us-west-2
   - Attach latest EBS snapshot
   - Update DNS to new region
   - Resume operations

RTO (Recovery Time Objective): 15-20 minutes
RPO (Recovery Point Objective): Depends on snapshot frequency
```

---

### 3. Development/Testing Environments

**Scenario:** Developers need identical staging environments

**Setup:**
```
1. Create production-like AMI:
   - Same OS, software versions
   - Database with sample data
   - Application configurations

2. Developers launch instances from AMI:
   - Instant environment setup
   - Consistent across team
   - No configuration drift

3. Destroy when done (save costs)
```

---

### 4. Compliance and Standardization

**Scenario:** Company requires CIS-compliant hardened OS

**Setup:**
```
1. Build hardened "golden AMI":
   - CIS benchmark configurations
   - Security patches applied
   - Monitoring agents installed
   - Logging configured
   - Unnecessary services disabled

2. Mandate use of golden AMI:
   - All instances must launch from approved AMI
   - Enforce via AWS Config rules
   - Audit compliance

3. Regular updates:
   - Monthly patch cycle
   - New AMI version created
   - Old versions deprecated
```

---

### 5. Software Licensing and Bring Your Own License (BYOL)

**Scenario:** Use existing Windows Server licenses on AWS

**Setup:**
```
1. Create AMI with your licensed software
2. Launch instances from AMI
3. License tracking:
   - AMI tied to your license
   - Track instance count
   - Compliance with vendor terms

Examples:
- Windows Server (Dedicated Hosts for BYOL)
- Oracle Database
- SAP HANA
```

---

### 6. Multi-Tier Application Deployment

**Scenario:** 3-tier web application

**Setup:**
```
Tier 1: Web Server AMI
- NGINX
- SSL certificates
- Static content
- AMI ID: ami-web-v1.0

Tier 2: Application Server AMI
- Node.js runtime
- Application code
- Environment configs
- AMI ID: ami-app-v1.0

Tier 3: Database AMI
- PostgreSQL 14
- Database extensions
- Backup scripts
- AMI ID: ami-db-v1.0

Deployment:
- Launch instances from respective AMIs
- Auto Scaling groups for each tier
- Version-controlled AMI IDs
```

---

## Advantages

### 1. **Fast Deployment**
- Launch instances in minutes (vs hours of manual setup)
- Pre-configured and ready to use
- Enables rapid scaling

### 2. **Consistency and Standardization**
- All instances identical
- Eliminates configuration drift
- Reduces human error

### 3. **Version Control**
- Different AMI versions for different software versions
- Easy rollback to previous versions
- Track changes over time

### 4. **Automation Enabler**
- Auto Scaling uses AMIs
- Infrastructure as Code (CloudFormation, Terraform)
- CI/CD pipeline integration

### 5. **Disaster Recovery**
- Pre-configured recovery environments
- Copy AMIs to other regions
- Fast recovery from failures

### 6. **Cost Savings**
- Faster deployment = less labor cost
- Consistent environments = fewer bugs
- Can delete instances and recreate from AMI

### 7. **Reusability**
- One AMI, many instances
- Share across teams/accounts
- Marketplace monetization opportunity

### 8. **Security**
- Hardened images
- Pre-configured security tools
- Reduced attack surface

---

## Disadvantages

### 1. **Storage Costs**
- AMIs are backed by EBS snapshots
- Snapshots cost $0.05/GB-month
- Multiple AMI versions accumulate costs
- **Mitigation:** Delete old AMIs and deregister unused snapshots

### 2. **Maintenance Overhead**
- Must keep AMIs updated with security patches
- Version management complexity
- Testing new AMI versions
- **Mitigation:** Automated build pipelines (Packer, CodeBuild)

### 3. **Region-Specific**
- AMI in us-east-1 not available in eu-west-1
- Must copy to each region needed
- Cross-region copy costs money
- **Mitigation:** Automate cross-region copying for DR

### 4. **Size Limitations**
- Large AMIs slow to create and copy
- Large snapshots expensive
- **Mitigation:** Minimize AMI size, download large files at launch

### 5. **Immutability Challenges**
- Can't modify AMI once created
- Need new AMI for any changes
- Version proliferation
- **Mitigation:** Use User Data for dynamic configuration

### 6. **Data Sensitivity**
- AMIs may contain sensitive data (passwords, keys)
- Shared AMIs can leak secrets
- **Mitigation:** Use secrets management (Secrets Manager, Parameter Store)

### 7. **Stale AMIs**
- Old AMIs become outdated
- Security vulnerabilities in old OS/software
- Confusion about which AMI to use
- **Mitigation:** Lifecycle policies, deregister old AMIs

### 8. **Limited Configuration Flexibility**
- AMI is static snapshot
- Environment-specific configs require User Data or config management
- **Mitigation:** Hybrid approach (AMI + User Data + Ansible/Chef)

---

## Practical Demonstration

### Demo 1: Creating a Custom AMI from an Instance

#### Step 1: Prepare the Instance

```bash
# SSH into your instance
ssh -i key.pem ec2-user@<instance-ip>

# Update packages
sudo yum update -y

# Install web server
sudo yum install httpd -y

# Create a custom web page
echo "<h1>Custom AMI Demo - Version 1.0</h1>" | sudo tee /var/www/html/index.html

# Start and enable Apache
sudo systemctl start httpd
sudo systemctl enable httpd

# Install application dependencies
sudo yum install -y nodejs npm git

# Clean up to reduce AMI size
sudo yum clean all
sudo rm -rf /var/cache/yum
sudo rm -rf /tmp/*

# (Optional) Clear history for security
history -c
```

#### Step 2: Create AMI via Console

```
1. In EC2 Console, select your instance
2. Actions → Image and templates → Create image

Configuration:
- Image name: web-server-ami-v1.0
- Image description: Web server with Apache and Node.js v1.0
- No reboot: Unchecked (recommended for data consistency)
- Instance volumes: (auto-populated)
  - /dev/xvda (Root): 8 GB, Delete on termination: Yes
  - Add volumes if needed

Tags:
- Name: web-server-ami-v1.0
- Version: 1.0
- Environment: Production
- Application: WebServer

3. Click "Create image"

4. Monitor progress:
   - Navigate to AMIs
   - Status: pending → available (5-15 minutes)
```

#### Step 3: Create AMI via CLI

```bash
# Create AMI
aws ec2 create-image \
    --instance-id i-0123456789abcdef0 \
    --name "web-server-ami-v1.0" \
    --description "Web server with Apache and Node.js v1.0" \
    --tag-specifications 'ResourceType=image,Tags=[{Key=Name,Value=web-server-ami-v1.0},{Key=Version,Value=1.0}]' \
    --no-reboot  # Use --reboot for data consistency

# Output:
{
    "ImageId": "ami-0abcd1234efgh5678"
}

# Monitor creation
aws ec2 describe-images \
    --image-ids ami-0abcd1234efgh5678 \
    --query 'Images[0].[State,ImageId,Name]' \
    --output table

# Wait for completion
aws ec2 wait image-available \
    --image-ids ami-0abcd1234efgh5678
```

#### Step 4: Launch Instance from Custom AMI

**Via Console:**
```
1. Navigate to AMIs
2. Select your AMI
3. Click "Launch instance from AMI"
4. Configure instance (t2.micro)
5. Launch
6. SSH into new instance and verify configuration is identical
```

**Via CLI:**
```bash
aws ec2 run-instances \
    --image-id ami-0abcd1234efgh5678 \
    --instance-type t2.micro \
    --key-name my-key \
    --security-group-ids sg-0123456789abcdef0 \
    --subnet-id subnet-12345 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=from-custom-ami}]'
```

---

### Demo 2: Copying AMI to Another Region

#### Use Case: Disaster Recovery or Multi-Region Deployment

```bash
# Source region: us-east-1
# Destination region: us-west-2

# Copy AMI to us-west-2
aws ec2 copy-image \
    --source-region us-east-1 \
    --source-image-id ami-0abcd1234efgh5678 \
    --region us-west-2 \
    --name "web-server-ami-v1.0-dr" \
    --description "DR copy from us-east-1" \
    --encrypted  # Optionally encrypt the copy

# Output:
{
    "ImageId": "ami-west-2-copy-id"
}

# Monitor copy progress (in us-west-2)
aws ec2 describe-images \
    --region us-west-2 \
    --image-ids ami-west-2-copy-id \
    --query 'Images[0].[State,ImageId]'

# Copy progress can take 10-30 minutes depending on size

# Launch instance in us-west-2 from copied AMI
aws ec2 run-instances \
    --region us-west-2 \
    --image-id ami-west-2-copy-id \
    --instance-type t2.micro \
    --key-name my-west-2-key \
    --security-group-ids sg-west-2-sg
```

**Cost:**
- Cross-region data transfer: $0.02/GB (one-time)
- Snapshot storage in destination region: $0.05/GB-month

---

### Demo 3: Sharing AMI with Another AWS Account

#### Scenario: Partner needs access to your AMI

```bash
# Grant permission to specific AWS account
aws ec2 modify-image-attribute \
    --image-id ami-0abcd1234efgh5678 \
    --launch-permission "Add=[{UserId=123456789012}]"

# Verify permissions
aws ec2 describe-image-attribute \
    --image-id ami-0abcd1234efgh5678 \
    --attribute launchPermission

# Output:
{
    "LaunchPermissions": [
        {
            "UserId": "123456789012"
        }
    ]
}

# Partner account (123456789012) can now see the AMI
# In partner account:
aws ec2 describe-images \
    --image-ids ami-0abcd1234efgh5678 \
    --owners 999988887777  # Your account ID

# Partner launches instance
aws ec2 run-instances \
    --image-id ami-0abcd1234efgh5678 \
    --instance-type t2.micro \
    ...

# Revoke access when no longer needed
aws ec2 modify-image-attribute \
    --image-id ami-0abcd1234efgh5678 \
    --launch-permission "Remove=[{UserId=123456789012}]"
```

**Important:**
- Sharing encrypted AMIs requires sharing KMS key as well
- Shared AMIs can't be modified by recipient
- Recipient pays for instances they launch

---

### Demo 4: Making AMI Public (Open Source)

```bash
# Make AMI public (anyone can use)
aws ec2 modify-image-attribute \
    --image-id ami-0abcd1234efgh5678 \
    --launch-permission "Add=[{Group=all}]"

# Verify
aws ec2 describe-image-attribute \
    --image-id ami-0abcd1234efgh5678 \
    --attribute launchPermission

# Output:
{
    "LaunchPermissions": [
        {
            "Group": "all"
        }
    ]
}

# Anyone can now find and use this AMI
# Example: Public community AMI for open-source project

# Make private again
aws ec2 modify-image-attribute \
    --image-id ami-0abcd1234efgh5678 \
    --launch-permission "Remove=[{Group=all}]"
```

**Caution:**
- Ensure no sensitive data in AMI
- Check for hardcoded credentials
- Review security configurations
- Understand you're distributing software publicly

---

### Demo 5: Deregistering AMI and Deleting Snapshots

#### When: AMI no longer needed, save costs

```bash
# Step 1: Identify AMI and its snapshots
aws ec2 describe-images \
    --image-ids ami-0abcd1234efgh5678 \
    --query 'Images[0].BlockDeviceMappings[*].Ebs.SnapshotId' \
    --output text

# Output: snap-111111 snap-222222

# Step 2: Deregister AMI
aws ec2 deregister-image \
    --image-id ami-0abcd1234efgh5678

# AMI is now deregistered, but snapshots still exist (still costing money!)

# Step 3: Delete associated snapshots
aws ec2 delete-snapshot --snapshot-id snap-111111
aws ec2 delete-snapshot --snapshot-id snap-222222

# Complete cleanup, stop incurring costs
```

**Automated Script:**
```bash
#!/bin/bash
# deregister-ami.sh

AMI_ID=$1

# Get snapshot IDs
SNAPSHOTS=$(aws ec2 describe-images \
    --image-ids $AMI_ID \
    --query 'Images[0].BlockDeviceMappings[*].Ebs.SnapshotId' \
    --output text)

# Deregister AMI
echo "Deregistering AMI: $AMI_ID"
aws ec2 deregister-image --image-id $AMI_ID

# Delete snapshots
for snap in $SNAPSHOTS; do
    echo "Deleting snapshot: $snap"
    aws ec2 delete-snapshot --snapshot-id $snap
done

echo "Cleanup complete"
```

---

### Demo 6: Automated AMI Creation with Packer

#### Use Case: Build AMIs automatically in CI/CD pipeline

**Install Packer:**
```bash
# Install Packer
curl -O https://releases.hashicorp.com/packer/1.9.4/packer_1.9.4_linux_amd64.zip
unzip packer_1.9.4_linux_amd64.zip
sudo mv packer /usr/local/bin/
```

**Packer Template (web-server.pkr.hcl):**
```hcl
packer {
  required_plugins {
    amazon = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "web_server" {
  ami_name      = "web-server-{{timestamp}}"
  instance_type = "t2.micro"
  region        = "us-east-1"
  source_ami_filter {
    filters = {
      name                = "amzn2-ami-hvm-*-x86_64-gp2"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["amazon"]
  }
  ssh_username = "ec2-user"
  tags = {
    Name        = "web-server-ami"
    Environment = "Production"
    Version     = "{{timestamp}}"
  }
}

build {
  sources = ["source.amazon-ebs.web_server"]

  provisioner "shell" {
    inline = [
      "sudo yum update -y",
      "sudo yum install -y httpd nodejs npm",
      "sudo systemctl enable httpd",
      "echo '<h1>Automated AMI</h1>' | sudo tee /var/www/html/index.html",
      "sudo yum clean all"
    ]
  }
}
```

**Build AMI:**
```bash
# Validate template
packer validate web-server.pkr.hcl

# Build AMI
packer build web-server.pkr.hcl

# Output:
# ...
# ==> amazon-ebs.web_server: Creating AMI: web-server-1708182000
# ==> amazon-ebs.web_server: AMI: ami-0newami123456789
```

**Benefits:**
- Automated, repeatable builds
- Version control for AMI configurations
- Integration with CI/CD (GitHub Actions, Jenkins)
- Consistent across environments

---

### Demo 7: AMI Lifecycle Management (Automated Cleanup)

#### Lambda Function to Delete Old AMIs

```python
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Get all AMIs owned by this account
    images = ec2.describe_images(Owners=['self'])

    # Define retention period (e.g., 30 days)
    retention_days = 30
    cutoff_date = datetime.now() - timedelta(days=retention_days)

    for image in images['Images']:
        # Parse creation date
        creation_date = datetime.strptime(
            image['CreationDate'],
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )

        # Check if AMI is older than retention period
        if creation_date < cutoff_date:
            ami_id = image['ImageId']
            ami_name = image.get('Name', 'Unknown')

            # Skip if AMI has "keep" tag
            tags = {tag['Key']: tag['Value'] for tag in image.get('Tags', [])}
            if tags.get('Keep') == 'true':
                print(f"Skipping {ami_id} ({ami_name}) - Keep tag set")
                continue

            print(f"Deleting old AMI: {ami_id} ({ami_name})")

            # Get snapshot IDs
            snapshot_ids = [
                bdm['Ebs']['SnapshotId']
                for bdm in image['BlockDeviceMappings']
                if 'Ebs' in bdm
            ]

            # Deregister AMI
            ec2.deregister_image(ImageId=ami_id)

            # Delete snapshots
            for snap_id in snapshot_ids:
                print(f"Deleting snapshot: {snap_id}")
                ec2.delete_snapshot(SnapshotId=snap_id)

    return {
        'statusCode': 200,
        'body': 'AMI cleanup complete'
    }
```

**Schedule with EventBridge:**
```bash
# Create Lambda function (upload above code as zip)
aws lambda create-function \
    --function-name AMI-Cleanup \
    --runtime python3.9 \
    --role arn:aws:iam::123456789012:role/lambda-execution-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip

# Create EventBridge rule (run monthly)
aws events put-rule \
    --name MonthlyAMICleanup \
    --schedule-expression "cron(0 2 1 * ? *)"  # 1st of month at 2 AM

# Add Lambda as target
aws events put-targets \
    --rule MonthlyAMICleanup \
    --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:123456789012:function:AMI-Cleanup"
```

---

## Scenario-Based Interview Questions

### Question 1: Golden AMI Strategy

**Scenario:** Your company wants to implement a "Golden AMI" strategy to standardize all EC2 deployments. How would you design and implement this?

**Answer:**
```
Golden AMI Strategy Design:

1. Requirements Gathering:

Categories of Golden AMIs:
- Base OS AMIs (Linux, Windows)
- Application-specific AMIs (Web, Database, Cache)
- Environment-specific (Dev, Staging, Production)

Example AMI Structure:
- base-amazon-linux-2-hardened-v1.0
  ├─ web-server-ami-v1.0 (Apache + security tools)
  ├─ app-server-ami-v1.0 (Node.js + monitoring)
  └─ db-server-ami-v1.0 (PostgreSQL + backup scripts)

2. Golden AMI Build Process:

Step 1: Base AMI Creation
```bash
# Packer template for base AMI
source "amazon-ebs" "base_ami" {
  ami_name = "base-amazon-linux-2-{{timestamp}}"
  source_ami_filter {
    filters = {
      name = "amzn2-ami-hvm-*"
    }
    owners = ["amazon"]
    most_recent = true
  }
}

build {
  sources = ["source.amazon-ebs.base_ami"]

  # Hardening
  provisioner "shell" {
    scripts = [
      "scripts/disable-unused-services.sh",
      "scripts/configure-firewall.sh",
      "scripts/install-security-tools.sh",
      "scripts/cis-benchmark.sh"
    ]
  }

  # Monitoring agents
  provisioner "shell" {
    inline = [
      "sudo yum install -y amazon-cloudwatch-agent",
      "sudo yum install -y amazon-ssm-agent"
    ]
  }

  # Compliance scanning
  provisioner "shell" {
    script = "scripts/compliance-scan.sh"
  }
}
```

Step 2: Application AMI (Built from Base AMI)
```hcl
source "amazon-ebs" "web_ami" {
  ami_name = "web-server-ami-{{timestamp}}"
  source_ami = var.base_ami_id  # Reference base AMI
}

build {
  sources = ["source.amazon-ebs.web_ami"]

  provisioner "shell" {
    inline = [
      "sudo yum install -y httpd mod_ssl",
      "sudo systemctl enable httpd"
    ]
  }

  # Deploy application code from S3
  provisioner "shell" {
    inline = [
      "aws s3 cp s3://my-app-bucket/latest.tar.gz /tmp/",
      "sudo tar -xzf /tmp/latest.tar.gz -C /var/www/html/"
    ]
  }
}
```

3. Automated Build Pipeline (CI/CD):

GitHub/GitLab Pipeline:
```yaml
# .gitlab-ci.yml
stages:
  - validate
  - build
  - test
  - promote

validate_packer:
  stage: validate
  script:
    - packer validate base-ami.pkr.hcl

build_base_ami:
  stage: build
  script:
    - packer build base-ami.pkr.hcl
    - echo $AMI_ID > base_ami_id.txt
  artifacts:
    paths:
      - base_ami_id.txt

build_app_amis:
  stage: build
  dependencies:
    - build_base_ami
  script:
    - BASE_AMI=$(cat base_ami_id.txt)
    - packer build -var "base_ami_id=$BASE_AMI" web-ami.pkr.hcl
    - packer build -var "base_ami_id=$BASE_AMI" app-ami.pkr.hcl

test_ami:
  stage: test
  script:
    - ./scripts/launch-test-instance.sh
    - ./scripts/run-integration-tests.sh
    - ./scripts/security-scan.sh
    - ./scripts/cleanup-test-instance.sh

promote_to_production:
  stage: promote
  when: manual
  script:
    - aws ec2 create-tags --resources $AMI_ID --tags Key=Environment,Value=Production
    - aws ec2 copy-image --source-region us-east-1 --region us-west-2 --source-image-id $AMI_ID
```

4. Governance and Compliance:

AWS Config Rules:
```json
{
  "ConfigRuleName": "approved-amis-only",
  "Source": {
    "Owner": "CUSTOM_LAMBDA",
    "SourceIdentifier": "arn:aws:lambda:us-east-1:123456789012:function:CheckApprovedAMI"
  },
  "Scope": {
    "ComplianceResourceTypes": [
      "AWS::EC2::Instance"
    ]
  }
}
```

Lambda Function:
```python
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    config = boto3.client('config')

    instance_id = event['configurationItem']['configuration']['instanceId']
    ami_id = event['configurationItem']['configuration']['imageId']

    # List of approved AMI prefixes
    approved_prefixes = [
        'ami-base-',
        'ami-web-',
        'ami-app-'
    ]

    # Check AMI name
    ami = ec2.describe_images(ImageIds=[ami_id])['Images'][0]
    ami_name = ami.get('Name', '')

    compliant = any(ami_name.startswith(prefix) for prefix in approved_prefixes)

    if not compliant:
        # Report non-compliance
        config.put_evaluations(
            Evaluations=[{
                'ComplianceResourceType': 'AWS::EC2::Instance',
                'ComplianceResourceId': instance_id,
                'ComplianceType': 'NON_COMPLIANT',
                'Annotation': f'Instance using non-approved AMI: {ami_name}',
                'OrderingTimestamp': datetime.now()
            }]
        )
```

5. AMI Versioning and Lifecycle:

Versioning Scheme:
```
{application}-{version}-{timestamp}
Example: web-server-v2.5.1-20250217-103045

Tags:
- Name: web-server-v2.5.1
- Version: 2.5.1
- BuildDate: 2025-02-17
- GitCommit: abc123def
- Environment: Production
- ApprovedBy: Jane Doe
```

Lifecycle Policy (DLM for AMIs):
```bash
# Keep last 5 versions of each AMI type
# Delete AMIs older than 90 days (except tagged as "LongTerm")

aws dlm create-lifecycle-policy \
    --policy-details file://ami-lifecycle-policy.json
```

6. Documentation and Training:

AMI Catalog (Internal Wiki):
```
AMI Catalog:

Base AMIs:
- base-amazon-linux-2-v1.5 (ami-0abc123)
  - Last updated: 2025-02-17
  - Security: CIS Level 1 compliant
  - Includes: CloudWatch agent, SSM agent
  - Use for: All Linux deployments

Application AMIs:
- web-server-ami-v2.1 (ami-0def456)
  - Based on: base-amazon-linux-2-v1.5
  - Includes: Apache 2.4, mod_ssl, Let's Encrypt
  - Use for: Public-facing web servers
  - Last updated: 2025-02-15
```

7. Multi-Region Strategy:

Automated Cross-Region Copying:
```bash
# After AMI build, copy to all regions
REGIONS=("us-west-2" "eu-west-1" "ap-southeast-1")

for region in "${REGIONS[@]}"; do
    aws ec2 copy-image \
        --source-region us-east-1 \
        --source-image-id $AMI_ID \
        --region $region \
        --name $AMI_NAME \
        --description "$AMI_DESCRIPTION"
done
```

8. Testing and Validation:

Automated AMI Testing:
```bash
#!/bin/bash
# test-ami.sh

AMI_ID=$1

# Launch test instance
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type t2.micro \
    --security-group-ids sg-test \
    --subnet-id subnet-test \
    --query 'Instances[0].InstanceId' \
    --output text)

# Wait for instance to be running
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Run tests
ssh ec2-user@$INSTANCE_IP <<'EOF'
# Check services
systemctl is-active httpd || exit 1
systemctl is-active amazon-cloudwatch-agent || exit 1

# Check security hardening
grep "PermitRootLogin no" /etc/ssh/sshd_config || exit 1

# Check installed packages
rpm -q httpd mod_ssl || exit 1

echo "All tests passed"
EOF

# Terminate test instance
aws ec2 terminate-instances --instance-ids $INSTANCE_ID
```

9. Monitoring and Alerting:

CloudWatch Dashboard:
- AMI build success/failure rate
- AMI age (alert if >60 days)
- Non-compliant instances (using unapproved AMIs)
- AMI storage costs

10. Cost Management:

AMI Cleanup:
```bash
# Monthly cleanup of old AMIs
# Keep:
# - Last 5 versions of each application
# - Any AMI tagged "LongTerm"
# - AMIs less than 30 days old

# Script automatically deregisters and deletes snapshots
```

Benefits of Golden AMI Strategy:
- Consistency across all deployments
- Faster instance launches
- Security compliance
- Simplified patch management
- Auditability
- Cost savings (fewer configuration errors)

Challenges:
- Initial setup effort
- Ongoing maintenance
- Training required
- Storage costs (mitigated by lifecycle policies)
```

This completes the comprehensive AMI guide! Let me continue with Security Groups and User Data to finish all your requested topics.

