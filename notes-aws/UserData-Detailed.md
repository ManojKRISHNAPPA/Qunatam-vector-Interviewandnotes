# EC2 User Data - Complete Guide

## Table of Contents
1. [What is User Data](#what-is-user-data)
2. [Why We Need User Data](#why-we-need-user-data)
3. [Key Concepts](#key-concepts)
4. [How User Data Works](#how-user-data-works)
5. [Use Cases](#use-cases)
6. [Advantages](#advantages)
7. [Disadvantages](#disadvantages)
8. [Practical Demonstration](#practical-demonstration)
9. [Scenario-Based Interview Questions](#scenario-based-interview-questions)

---

## What is User Data?

**EC2 User Data** is a feature that allows you to pass configuration scripts or commands to an EC2 instance at launch time. These scripts run automatically when the instance boots for the first time (or every time, if configured).

**Simple Analogy:** Think of User Data as a "setup checklist" you give to a new employee on their first day. When they arrive (instance launches), they follow the checklist to set up their workspace (install software, configure settings, etc.).

**Technical Definition:** User Data is a bootstrap script that executes during the instance initialization phase. It can be a shell script (Linux) or PowerShell/batch script (Windows) that runs as the root/administrator user.

### Key Characteristics:
- **Runs at boot:** Executes during instance launch
- **Root/Admin privileges:** Runs with highest permissions
- **Text or file-based:** Can be inline script or reference to S3
- **Max size:** 16 KB (plain text)
- **Base64 encoded:** Automatically encoded by AWS
- **Visible in metadata:** Can be accessed via instance metadata service

---

## Why We Need User Data?

### Problems Without User Data:
1. **Manual Configuration:** SSH into each instance and run commands
2. **Time-Consuming:** Repeat setup for every new instance
3. **Inconsistency:** Human errors lead to different configurations
4. **Not Scalable:** Auto Scaling requires manual intervention
5. **Slow Deployment:** Can't launch instances ready-to-use

### User Data Solutions:
1. **Automation:** Scripts run automatically at launch
2. **Consistency:** Same script ensures identical configuration
3. **Speed:** Instances become operational without manual steps
4. **Scalability:** Auto Scaling groups use User Data for new instances
5. **Dynamic Configuration:** Can fetch configs from S3, Parameter Store, etc.
6. **Cost Savings:** Reduce need for custom AMIs (use base AMI + User Data)

### Real-World Scenario:
**Problem:** Launch 100 web servers for Black Friday, each needs Apache installed
- **Without User Data:** SSH into 100 instances × 5 minutes each = 500 minutes
- **With User Data:** Launch all 100 with script = Apache installed automatically = 5 minutes total

---

## Key Concepts

### 1. Execution Timing

**First Boot Only (Default - cloud-init):**
```
Instance launches → User Data runs → Instance available
Instance stops → Instance starts → User Data does NOT run
```

**Every Boot (Configure with cloud-init):**
```
Add this to the top of your script:
#cloud-config
cloud_final_modules:
  - scripts-user

Or:
#!/bin/bash
# Force run on every boot by placing in /var/lib/cloud/scripts/per-boot/
```

### 2. Execution User

**Linux:**
- Runs as `root` user
- No need for `sudo` in commands

**Windows:**
- Runs as `Administrator`
- PowerShell scripts with admin privileges

### 3. User Data Format

**Bash Script (Linux):**
```bash
#!/bin/bash
# Must start with shebang
yum update -y
yum install httpd -y
systemctl start httpd
```

**Cloud-Config (Linux):**
```yaml
#cloud-config
packages:
  - httpd
  - git
runcmd:
  - systemctl start httpd
```

**PowerShell (Windows):**
```powershell
<powershell>
Install-WindowsFeature -Name Web-Server
</powershell>
```

### 4. User Data Logging

**Linux:**
- Output logged to: `/var/log/cloud-init-output.log`
- Errors logged to: `/var/log/cloud-init.log`

**Windows:**
- Output in: `C:\ProgramData\Amazon\EC2-Windows\Launch\Log\UserdataExecution.log`

### 5. Accessing User Data from Instance

**Via Instance Metadata (from inside instance):**
```bash
# Linux
curl http://169.254.169.254/latest/user-data

# Windows PowerShell
Invoke-RestMethod -Uri http://169.254.169.254/latest/user-data
```

### 6. User Data Size Limit

**Limits:**
- Maximum: 16 KB (raw, before base64 encoding)
- After encoding: ~21.3 KB

**Workaround for Large Scripts:**
```bash
#!/bin/bash
# Download larger script from S3
aws s3 cp s3://my-bucket/large-setup-script.sh /tmp/setup.sh
chmod +x /tmp/setup.sh
/tmp/setup.sh
```

### 7. Modifying User Data

**Can Modify When:**
- Instance is stopped (EBS-backed instances)

**Cannot Modify When:**
- Instance is running
- Instance store-backed instances (can't stop)

**Modification Effect:**
- Changes only apply to next launch
- Existing instance not affected (unless configured to run on every boot)

---

## How User Data Works

### Execution Flow

```
┌────────────────────────────────────┐
│  Launch EC2 Instance               │
│  - AMI: Amazon Linux 2             │
│  - Instance Type: t2.micro         │
│  - User Data: #!/bin/bash...       │
└──────────────┬─────────────────────┘
               │
               ▼
┌────────────────────────────────────┐
│  Instance Boot Process             │
│  1. Hardware initialization        │
│  2. OS kernel loads                │
│  3. cloud-init starts              │
└──────────────┬─────────────────────┘
               │
               ▼
┌────────────────────────────────────┐
│  cloud-init Retrieves User Data    │
│  - From instance metadata          │
│  - URL: http://169.254.169.254/... │
└──────────────┬─────────────────────┘
               │
               ▼
┌────────────────────────────────────┐
│  User Data Execution               │
│  - Runs as root                    │
│  - Output → /var/log/cloud-init... │
│  - Blocks until completion         │
└──────────────┬─────────────────────┘
               │
               ▼
┌────────────────────────────────────┐
│  Instance Ready                    │
│  - Status checks: 2/2 passed       │
│  - Services running                │
│  - Ready for connections           │
└────────────────────────────────────┘
```

### Behind the Scenes (Linux)

**cloud-init Process:**
```
1. cloud-init runs on first boot
2. Checks for User Data at http://169.254.169.254/latest/user-data
3. Determines script type:
   - Starts with #!/bin/bash → Shell script
   - Starts with #cloud-config → Cloud-config YAML
   - Starts with <powershell> → PowerShell (Windows)
4. Executes script as root
5. Logs output to /var/log/cloud-init-output.log
6. Sets /var/lib/cloud/instance/boot-finished (marks complete)
7. Instance status checks pass
```

**File Locations:**
```
/var/lib/cloud/instance/user-data.txt      # Copy of User Data
/var/log/cloud-init-output.log             # Script output
/var/log/cloud-init.log                    # cloud-init process log
/var/lib/cloud/instance/boot-finished      # Completion marker
```

---

## Use Cases

### 1. Installing Software on Launch

**Scenario:** Launch web servers with Apache pre-installed

**User Data Script:**
```bash
#!/bin/bash
# Update system
yum update -y

# Install Apache
yum install -y httpd

# Start and enable Apache
systemctl start httpd
systemctl enable httpd

# Create a simple web page
cat > /var/www/html/index.html <<EOF
<html>
<head><title>Web Server</title></head>
<body>
<h1>Hello from $(hostname -f)</h1>
<p>Instance ID: $(ec2-metadata --instance-id | cut -d' ' -f2)</p>
</body>
</html>
EOF

# Set permissions
chmod 644 /var/www/html/index.html
```

---

### 2. Dynamic Configuration with Parameter Store

**Scenario:** Fetch database credentials from AWS Systems Manager Parameter Store

**User Data Script:**
```bash
#!/bin/bash
# Install AWS CLI (if not already installed)
yum install -y aws-cli

# Fetch database credentials from Parameter Store
DB_HOST=$(aws ssm get-parameter --name "/myapp/db/host" --query "Parameter.Value" --output text --region us-east-1)
DB_USER=$(aws ssm get-parameter --name "/myapp/db/username" --query "Parameter.Value" --output text --region us-east-1)
DB_PASS=$(aws ssm get-parameter --name "/myapp/db/password" --with-decryption --query "Parameter.Value" --output text --region us-east-1)

# Create application config file
cat > /opt/myapp/config.json <<EOF
{
  "database": {
    "host": "$DB_HOST",
    "username": "$DB_USER",
    "password": "$DB_PASS"
  }
}
EOF

# Secure the config file
chmod 600 /opt/myapp/config.json
chown myapp:myapp /opt/myapp/config.json

# Start application
systemctl start myapp
```

**Benefit:**
- No hardcoded credentials in User Data
- Centralized secret management
- Can rotate secrets without changing User Data

---

### 3. Downloading Application Code from S3

**Scenario:** Deploy latest application version from S3 bucket

**User Data Script:**
```bash
#!/bin/bash
# Install dependencies
yum install -y nodejs npm

# Create app directory
mkdir -p /var/www/myapp

# Download application code from S3
aws s3 cp s3://my-app-bucket/releases/latest.tar.gz /tmp/app.tar.gz

# Extract code
tar -xzf /tmp/app.tar.gz -C /var/www/myapp

# Install Node.js dependencies
cd /var/www/myapp
npm install --production

# Create systemd service
cat > /etc/systemd/system/myapp.service <<EOF
[Unit]
Description=My Node.js Application
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/var/www/myapp
ExecStart=/usr/bin/node /var/www/myapp/server.js
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start service
systemctl daemon-reload
systemctl enable myapp
systemctl start myapp
```

---

### 4. Joining a Domain (Active Directory)

**Scenario:** Windows instance joins corporate AD domain

**User Data Script (Windows PowerShell):**
```powershell
<powershell>
# Set DNS to domain controllers
$adapter = Get-NetAdapter | Where-Object {$_.Status -eq "Up"}
Set-DnsClientServerAddress -InterfaceIndex $adapter.ifIndex -ServerAddresses ("10.0.1.10","10.0.1.11")

# Fetch domain join credentials from Secrets Manager
$secret = Get-SECSecretValue -SecretId "prod/ad/domain-join"
$secretJson = $secret.SecretString | ConvertFrom-Json
$username = $secretJson.username
$password = $secretJson.password | ConvertTo-SecureString -AsPlainText -Force

# Create credential object
$credential = New-Object System.Management.Automation.PSCredential($username, $password)

# Join domain
Add-Computer -DomainName "corp.example.com" -Credential $credential -Restart -Force
</powershell>
```

---

### 5. Auto Scaling with Configuration Management

**Scenario:** New instances register with Chef/Puppet/Ansible

**User Data Script:**
```bash
#!/bin/bash
# Install Chef client
curl -L https://www.chef.io/chef/install.sh | bash

# Configure Chef client
mkdir -p /etc/chef

# Fetch Chef configuration from S3
aws s3 cp s3://my-chef-config/client.rb /etc/chef/client.rb
aws s3 cp s3://my-chef-config/validation.pem /etc/chef/validation.pem

# Set node name
NODE_NAME="web-$(ec2-metadata --instance-id | cut -d' ' -f2)"
echo "node_name '$NODE_NAME'" >> /etc/chef/client.rb

# Run Chef client (registers with Chef server and applies runlist)
chef-client

# Enable Chef client as a service
systemctl enable chef-client
systemctl start chef-client
```

---

### 6. Sending Launch Notification

**Scenario:** Notify Slack when instance launches

**User Data Script:**
```bash
#!/bin/bash
# Get instance details
INSTANCE_ID=$(ec2-metadata --instance-id | cut -d' ' -f2)
INSTANCE_IP=$(ec2-metadata --local-ipv4 | cut -d' ' -f2)
AZ=$(ec2-metadata --availability-zone | cut -d' ' -f2)

# Send notification to Slack
SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

curl -X POST $SLACK_WEBHOOK \
    -H 'Content-Type: application/json' \
    -d "{
        \"text\": \"🚀 New EC2 Instance Launched\",
        \"attachments\": [{
            \"color\": \"good\",
            \"fields\": [
                {\"title\": \"Instance ID\", \"value\": \"$INSTANCE_ID\", \"short\": true},
                {\"title\": \"IP Address\", \"value\": \"$INSTANCE_IP\", \"short\": true},
                {\"title\": \"Availability Zone\", \"value\": \"$AZ\", \"short\": true}
            ]
        }]
    }"

# Continue with regular setup
yum update -y
yum install -y httpd
systemctl start httpd
```

---

### 7. Environment-Specific Configuration

**Scenario:** Configure instance differently based on environment tag

**User Data Script:**
```bash
#!/bin/bash
# Install AWS CLI
yum install -y aws-cli jq

# Get instance ID
INSTANCE_ID=$(ec2-metadata --instance-id | cut -d' ' -f2)
REGION=$(ec2-metadata --availability-zone | cut -d' ' -f2 | sed 's/[a-z]$//')

# Get environment tag
ENVIRONMENT=$(aws ec2 describe-tags \
    --region $REGION \
    --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=Environment" \
    --query "Tags[0].Value" \
    --output text)

# Configure based on environment
case $ENVIRONMENT in
    "production")
        # Production configuration
        LOG_LEVEL="INFO"
        MEMORY_LIMIT="2048M"
        ;;
    "staging")
        # Staging configuration
        LOG_LEVEL="DEBUG"
        MEMORY_LIMIT="1024M"
        ;;
    "development")
        # Development configuration
        LOG_LEVEL="DEBUG"
        MEMORY_LIMIT="512M"
        ;;
esac

# Apply configuration
echo "LOG_LEVEL=$LOG_LEVEL" >> /opt/myapp/.env
echo "MEMORY_LIMIT=$MEMORY_LIMIT" >> /opt/myapp/.env

# Start application
systemctl start myapp
```

---

## Advantages

### 1. **Automation**
- No manual SSH and command execution
- Scripts run automatically at launch
- Eliminates human error

### 2. **Scalability**
- Auto Scaling groups launch instances automatically
- User Data ensures new instances configured identically
- Handle sudden traffic spikes

### 3. **Consistency**
- Same script = identical configuration
- No configuration drift
- Reproducible environments

### 4. **Speed**
- Instances operational faster
- No waiting for manual configuration
- Rapid deployment in emergencies

### 5. **Cost-Effective**
- Reduce need for multiple custom AMIs
- Base AMI + User Data = flexibility
- Save on AMI storage costs

### 6. **Dynamic Configuration**
- Fetch latest configs from Parameter Store/Secrets Manager
- Download latest code from S3/CodeDeploy
- Environment-specific setup

### 7. **Integration**
- Works with Auto Scaling, Launch Templates, CloudFormation
- Part of Infrastructure as Code
- Version control your bootstrap scripts

### 8. **No Additional Cost**
- Free feature, no charges
- Included with EC2

---

## Disadvantages

### 1. **Size Limitation**
- Max 16 KB (plain text)
- Large scripts require workarounds (download from S3)
- **Mitigation:** Use User Data to download larger scripts

### 2. **Runs Only at Launch (Default)**
- Changes to User Data don't affect running instances
- Must terminate and launch new instance
- **Mitigation:** Configure cloud-init to run on every boot

### 3. **Debugging Difficulty**
- Scripts run before you can SSH
- If script fails, instance may not function
- Must check logs to diagnose
- **Mitigation:** Add logging, error handling, notifications

### 4. **Security Risks**
- User Data visible via metadata service (from inside instance)
- Never put secrets in User Data (plain text!)
- **Mitigation:** Use Parameter Store, Secrets Manager, IAM roles

### 5. **Longer Boot Time**
- Instance takes longer to become ready
- User Data execution blocks completion
- **Mitigation:** Optimize scripts, use AMIs for heavy installations

### 6. **No Rollback**
- If script fails halfway, instance in unknown state
- Must terminate and relaunch
- **Mitigation:** Idempotent scripts, use configuration management tools

### 7. **Testing Challenges**
- Must launch instances to test
- Time-consuming to iterate
- **Mitigation:** Use Packer to test scripts before deployment

### 8. **Visibility**
- User Data can be viewed by anyone with access to EC2 metadata
- Including other processes on the instance
- **Mitigation:** Never store sensitive data, use IAM roles

---

## Practical Demonstration

### Demo 1: Basic Web Server Setup

**Scenario:** Launch EC2 with Apache installed and custom page

**Via Console:**
```
1. EC2 → Launch Instance
2. Choose AMI: Amazon Linux 2
3. Instance Type: t2.micro
4. Configure Instance Details → Advanced Details

User Data (text):
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Hello from $(hostname -f)</h1>" > /var/www/html/index.html

5. Add Storage (default)
6. Add Tags: Name=web-server-userdata
7. Configure Security Group:
   - HTTP (80) from 0.0.0.0/0
   - SSH (22) from My IP
8. Launch
```

**Via CLI:**
```bash
# Create User Data file
cat > userdata.sh <<'EOF'
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Hello from $(hostname -f)</h1>" > /var/www/html/index.html
EOF

# Launch instance with User Data
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --key-name my-key \
    --security-group-ids sg-web \
    --user-data file://userdata.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=web-server-userdata}]'

# Wait for instance to be running
aws ec2 wait instance-running --instance-ids i-xxxxx

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids i-xxxxx \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

# Wait for User Data to complete (check logs)
# SSH into instance
ssh ec2-user@$PUBLIC_IP

# Check User Data execution log
sudo tail -f /var/log/cloud-init-output.log

# Test web server
curl http://$PUBLIC_IP
# Output: <h1>Hello from ip-10-0-1-50.ec2.internal</h1>
```

---

### Demo 2: Error Handling and Logging

**Robust User Data Script:**
```bash
#!/bin/bash
# Redirect all output to log file
exec > >(tee /var/log/user-data.log)
exec 2>&1

# Enable error handling
set -e  # Exit on error
set -x  # Print commands

# Function for error notification
error_exit() {
    echo "ERROR: $1" >&2
    # Send SNS notification
    aws sns publish \
        --topic-arn arn:aws:sns:us-east-1:123456789012:instance-launch-failures \
        --message "User Data script failed: $1. Instance: $(ec2-metadata --instance-id)" \
        --region us-east-1
    exit 1
}

# Start script
echo "User Data script started at $(date)"

# Update system
echo "Updating system packages..."
yum update -y || error_exit "Failed to update system packages"

# Install Apache
echo "Installing Apache..."
yum install -y httpd || error_exit "Failed to install Apache"

# Start Apache
echo "Starting Apache..."
systemctl start httpd || error_exit "Failed to start Apache"
systemctl enable httpd || error_exit "Failed to enable Apache"

# Create test page
echo "Creating test page..."
echo "<h1>Success! Instance ready.</h1>" > /var/www/html/index.html || error_exit "Failed to create test page"

# Success notification
aws sns publish \
    --topic-arn arn:aws:sns:us-east-1:123456789012:instance-launch-success \
    --message "Instance $(ec2-metadata --instance-id) launched successfully" \
    --region us-east-1

echo "User Data script completed successfully at $(date)"
```

**Check Logs After Launch:**
```bash
# SSH into instance
ssh ec2-user@<instance-ip>

# View full User Data output
sudo cat /var/log/user-data.log

# View cloud-init log
sudo cat /var/log/cloud-init-output.log
```

---

### Demo 3: Fetching Secrets from AWS Secrets Manager

**User Data Script:**
```bash
#!/bin/bash
# Install jq for JSON parsing
yum install -y jq

# Fetch database credentials from Secrets Manager
SECRET_ARN="arn:aws:secretsmanager:us-east-1:123456789012:secret:prod/db/credentials"
SECRET=$(aws secretsmanager get-secret-value --secret-id $SECRET_ARN --region us-east-1 --query SecretString --output text)

# Parse JSON secret
DB_HOST=$(echo $SECRET | jq -r '.host')
DB_USER=$(echo $SECRET | jq -r '.username')
DB_PASS=$(echo $SECRET | jq -r '.password')
DB_NAME=$(echo $SECRET | jq -r '.database')

# Create application config file (NOT in User Data!)
cat > /opt/myapp/config.env <<EOF
DB_HOST=$DB_HOST
DB_USER=$DB_USER
DB_PASS=$DB_PASS
DB_NAME=$DB_NAME
EOF

# Secure the file
chmod 600 /opt/myapp/config.env
chown myapp:myapp /opt/myapp/config.env

# Start application
systemctl start myapp

echo "Application configured with secrets from Secrets Manager"
```

**IAM Role Required:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:prod/db/credentials*"
    }
  ]
}
```

---

### Demo 4: Running User Data on Every Boot

**Scenario:** Want to refresh configuration on each boot

**User Data Script:**
```bash
#!/bin/bash
# Write script to run on every boot
cat > /var/lib/cloud/scripts/per-boot/my-boot-script.sh <<'BOOT_SCRIPT'
#!/bin/bash
echo "Running on every boot at $(date)" >> /var/log/every-boot.log

# Refresh application config from Parameter Store
APP_CONFIG=$(aws ssm get-parameter --name "/myapp/config" --query "Parameter.Value" --output text)
echo "$APP_CONFIG" > /opt/myapp/config.json

# Restart application to pick up new config
systemctl restart myapp

echo "Config refreshed and app restarted" >> /var/log/every-boot.log
BOOT_SCRIPT

chmod +x /var/lib/cloud/scripts/per-boot/my-boot-script.sh

echo "Per-boot script configured"
```

**Or use cloud-config:**
```yaml
#cloud-config
bootcmd:
  - echo "Running on every boot" >> /var/log/bootcmd.log
  - systemctl restart myapp
```

**Testing:**
```bash
# Stop instance
aws ec2 stop-instances --instance-ids i-xxxxx

# Start instance
aws ec2 start-instances --instance-ids i-xxxxx

# SSH and check log
ssh ec2-user@<instance-ip>
sudo cat /var/log/every-boot.log
# Should show multiple entries (each boot)
```

---

### Demo 5: CloudFormation with User Data

**CloudFormation Template:**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'EC2 instance with User Data'

Parameters:
  KeyName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: EC2 Key Pair for SSH access

Resources:
  WebServerInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0c55b159cbfafe1f0
      InstanceType: t2.micro
      KeyName: !Ref KeyName
      SecurityGroups:
        - !Ref WebServerSecurityGroup
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          yum update -y
          yum install -y httpd
          systemctl start httpd
          systemctl enable httpd

          # Use CloudFormation variables
          cat > /var/www/html/index.html <<EOF
          <h1>Web Server</h1>
          <p>Stack Name: ${AWS::StackName}</p>
          <p>Region: ${AWS::Region}</p>
          <p>Instance ID: $(ec2-metadata --instance-id | cut -d' ' -f2)</p>
          EOF

          # Signal CloudFormation when complete
          /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource WebServerInstance --region ${AWS::Region}
      Tags:
        - Key: Name
          Value: !Sub '${AWS::StackName}-web-server'

  WebServerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow HTTP and SSH
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0

Outputs:
  WebServerURL:
    Description: URL of the web server
    Value: !Sub 'http://${WebServerInstance.PublicDnsName}'
```

**Deploy:**
```bash
aws cloudformation create-stack \
    --stack-name my-web-server \
    --template-body file://template.yaml \
    --parameters ParameterKey=KeyName,ParameterValue=my-key
```

---

### Demo 6: Viewing and Modifying User Data

**View User Data (from outside instance):**
```bash
# Describe instance attribute
aws ec2 describe-instance-attribute \
    --instance-id i-xxxxx \
    --attribute userData \
    --query "UserData.Value" \
    --output text | base64 --decode

# Output: Your User Data script (decoded)
```

**View User Data (from inside instance):**
```bash
# SSH into instance
ssh ec2-user@<instance-ip>

# View User Data via metadata service
curl http://169.254.169.254/latest/user-data

# Or from cached file
cat /var/lib/cloud/instance/user-data.txt
```

**Modify User Data (instance must be stopped):**
```bash
# Stop instance
aws ec2 stop-instances --instance-ids i-xxxxx
aws ec2 wait instance-stopped --instance-ids i-xxxxx

# Create new User Data file
cat > new-userdata.sh <<'EOF'
#!/bin/bash
echo "Updated User Data" > /var/log/updated.log
yum install -y nginx
systemctl start nginx
EOF

# Modify User Data
aws ec2 modify-instance-attribute \
    --instance-id i-xxxxx \
    --user-data file://new-userdata.sh

# Start instance (new User Data will NOT run unless configured to run on every boot)
aws ec2 start-instances --instance-ids i-xxxxx

# To make it run, configure cloud-init or manually run:
# sudo /var/lib/cloud/instance/scripts/part-001
```

---

## Scenario-Based Interview Questions

### Question 1: Auto Scaling with Dynamic Configuration

**Scenario:** You have an Auto Scaling group that launches EC2 instances for a web application. The application needs to:
1. Download latest code from S3
2. Fetch database credentials from Secrets Manager
3. Register with a monitoring system (DataDog)
4. Join the application cluster

Design a User Data script to accomplish this.

**Answer:**
```bash
#!/bin/bash
# Enable error handling and logging
exec > >(tee /var/log/user-data.log)
exec 2>&1
set -e
set -x

echo "=== Starting User Data script at $(date) ==="

# Variables
REGION="us-east-1"
S3_BUCKET="my-app-bucket"
APP_VERSION=$(aws ec2 describe-tags \
    --region $REGION \
    --filters "Name=resource-id,Values=$(ec2-metadata --instance-id | cut -d' ' -f2)" \
              "Name=key,Values=AppVersion" \
    --query "Tags[0].Value" \
    --output text)

echo "Deploying application version: $APP_VERSION"

# Install dependencies
yum install -y aws-cli jq docker

# Start Docker
systemctl start docker
systemctl enable docker

# 1. Download application code from S3
echo "Downloading application code..."
aws s3 cp s3://$S3_BUCKET/releases/$APP_VERSION/app.tar.gz /tmp/app.tar.gz
mkdir -p /opt/myapp
tar -xzf /tmp/app.tar.gz -C /opt/myapp

# 2. Fetch database credentials from Secrets Manager
echo "Fetching database credentials..."
SECRET_ARN="arn:aws:secretsmanager:$REGION:123456789012:secret:prod/db/credentials"
SECRET=$(aws secretsmanager get-secret-value \
    --secret-id $SECRET_ARN \
    --region $REGION \
    --query SecretString \
    --output text)

DB_HOST=$(echo $SECRET | jq -r '.host')
DB_USER=$(echo $SECRET | jq -r '.username')
DB_PASS=$(echo $SECRET | jq -r '.password')
DB_NAME=$(echo $SECRET | jq -r '.database')

# Create environment file for application
cat > /opt/myapp/.env <<ENV
DB_HOST=$DB_HOST
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASS
DB_NAME=$DB_NAME
APP_VERSION=$APP_VERSION
NODE_ENV=production
ENV

chmod 600 /opt/myapp/.env

# 3. Register with DataDog monitoring
echo "Installing DataDog agent..."
DD_API_KEY=$(aws ssm get-parameter \
    --name "/prod/datadog/api-key" \
    --with-decryption \
    --region $REGION \
    --query "Parameter.Value" \
    --output text)

DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=$DD_API_KEY DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"

# Configure DataDog tags
cat >> /etc/datadog-agent/datadog.yaml <<DD_CONFIG
tags:
  - env:production
  - app:myapp
  - version:$APP_VERSION
  - az:$(ec2-metadata --availability-zone | cut -d' ' -f2)
DD_CONFIG

systemctl restart datadog-agent

# 4. Join application cluster
echo "Registering with application cluster..."
CLUSTER_ENDPOINT=$(aws ssm get-parameter \
    --name "/prod/cluster/endpoint" \
    --region $REGION \
    --query "Parameter.Value" \
    --output text)

INSTANCE_ID=$(ec2-metadata --instance-id | cut -d' ' -f2)
INSTANCE_IP=$(ec2-metadata --local-ipv4 | cut -d' ' -f2)

# Register with cluster using API
curl -X POST https://$CLUSTER_ENDPOINT/api/v1/nodes/register \
    -H "Content-Type: application/json" \
    -d "{
        \"nodeId\": \"$INSTANCE_ID\",
        \"ipAddress\": \"$INSTANCE_IP\",
        \"version\": \"$APP_VERSION\",
        \"capacity\": 100
    }"

# 5. Start application using Docker
echo "Starting application..."
docker run -d \
    --name myapp \
    --restart always \
    -p 8080:8080 \
    --env-file /opt/myapp/.env \
    -v /opt/myapp:/app \
    myapp:$APP_VERSION

# Wait for application to be healthy
echo "Waiting for application health check..."
for i in {1..30}; do
    if curl -f http://localhost:8080/health; then
        echo "Application is healthy!"
        break
    fi
    echo "Waiting for application to start... ($i/30)"
    sleep 2
done

# 6. Send success notification
aws sns publish \
    --topic-arn arn:aws:sns:$REGION:123456789012:instance-launch-success \
    --subject "Instance $INSTANCE_ID launched successfully" \
    --message "Application version $APP_VERSION is running on $INSTANCE_ID at $INSTANCE_IP" \
    --region $REGION

echo "=== User Data script completed successfully at $(date) ==="
```

**IAM Role Permissions Required:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::my-app-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:prod/db/credentials*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter"
      ],
      "Resource": [
        "arn:aws:ssm:us-east-1:123456789012:parameter/prod/datadog/api-key",
        "arn:aws:ssm:us-east-1:123456789012:parameter/prod/cluster/endpoint"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeTags"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "arn:aws:sns:us-east-1:123456789012:instance-launch-success"
    }
  ]
}
```

**Testing Checklist:**
```
✓ Application code downloaded from S3
✓ Database credentials fetched and secured
✓ DataDog agent installed and reporting
✓ Instance registered with cluster
✓ Docker container running
✓ Health check passing
✓ SNS notification sent
✓ Logs in /var/log/user-data.log
```

**Benefits of This Approach:**
- Fully automated deployment
- No secrets in User Data (uses Secrets Manager)
- Version-controlled application deployments
- Monitoring from first boot
- Auto Scaling works seamlessly
- Idempotent and repeatable

---

I've now completed ALL comprehensive guides for your requested AWS topics:

1. **EC2-Detailed.md** - Complete EC2 guide with scenarios
2. **EBS-Detailed.md** - Complete EBS guide with scenarios
3. **Snapshots-Detailed.md** - Complete Snapshots guide with scenarios
4. **AMI-Detailed.md** - Complete AMI guide with scenarios
5. **SecurityGroups-Detailed.md** - Complete Security Groups guide with scenarios
6. **UserData-Detailed.md** - Complete User Data guide with scenarios

Each guide includes:
- **What it is** - Clear definitions and analogies
- **Why we need it** - Problem statements and solutions
- **Key concepts** - Important technical details
- **Use cases** - Real-world scenarios
- **Advantages** - Benefits and strengths
- **Disadvantages** - Limitations and mitigation strategies
- **Practical demonstrations** - Step-by-step hands-on examples
- **Scenario-based interview questions** - In-depth questions with detailed answers

All files have been created in your `notes-aws/` directory and are ready for your interview preparation!

