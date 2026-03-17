# AWS Projects for Students

## Project 1: Host a Static Website using EC2

**Objective:** Students will launch a server using Amazon EC2 and host a simple website.

**Architecture:**
```
User -> Internet -> EC2 Instance -> Apache Web Server -> Website
```

**Steps:**

*   Login to AWS console.
*   Launch EC2 instance:
    *   AMI: Ubuntu
    *   Instance type: t2.micro
*   Create security group:
    *   Allow HTTP (80) and SSH (22)
*   Connect to EC2 via SSH
*   Install Apache:
    ```bash
    sudo apt update
    sudo apt install apache2 -y
    ```
*   Create HTML page:
    ```bash
    sudo nano /var/www/html/index.html
    ```
*   Example content:
    ```html
    <h1>Welcome to Manoj DevOps Lab</h1>
    ```
*   Open browser: `http://EC2-Public-IP`

**Required Screenshots:**

*   EC2 instance running
*   Security group inbound rule
*   SSH connection terminal
*   Apache installation output
*   Website running in browser

---

## Project 2: Build Custom Network using VPC

**Objective:** Create isolated network using Amazon VPC and deploy EC2 inside it.

**Architecture:**
```
Internet
↓
Internet Gateway
↓
Public Subnet
↓
EC2 Instance
```

**Steps:**

*   Create VPC:
    *   CIDR: 10.0.0.0/16
*   Create Subnet:
    *   Public subnet: 10.0.1.0/24
*   Create Internet Gateway
*   Attach gateway to VPC
*   Create Route Table:
    *   0.0.0.0/0 → Internet Gateway
*   Launch EC2 instance inside subnet
*   Connect via SSH

**Required Screenshots:**

*   VPC created
*   Subnet configuration
*   Internet gateway attached
*   Route table configuration
*   EC2 instance inside VPC

---

## Project 3: Serverless Image Processor

**Objective:** Use AWS Lambda to process files uploaded to Amazon S3.

**Architecture:**
```
User uploads image
↓
S3 Bucket
↓
Lambda Trigger
↓
Image processing
```

**Steps:**

*   Create S3 bucket:
    *   `student-image-upload`
*   Create Lambda function:
    *   Runtime: Python 3.11
    *   Example code:
        ```python
        import json

        def lambda_handler(event, context):
            print("File uploaded")
            return {
                'statusCode': 200,
                'body': json.dumps('Success')
            }
        ```
*   Configure trigger:
    *   S3 → Lambda
    *   Event: ObjectCreated
*   Upload image to S3
*   Check logs in CloudWatch

**Required Screenshots:**

*   S3 bucket created
*   Lambda function created
*   Trigger configuration
*   Upload file to S3
*   CloudWatch logs

---

## Project 4: Secure AWS Access using IAM

**Objective:** Implement access control using AWS Identity and Access Management.

**Architecture:**
```
Admin → IAM Policies → IAM Users → AWS Resources
```

**Steps:**

*   Create IAM user:
    *   `student-user`
*   Create policy:
    *   Example policy:
        ```json
        {
         "Version": "2012-10-17",
         "Statement": [
          {
           "Effect": "Allow",
           "Action": "ec2:DescribeInstances",
           "Resource": "*"
          }
         ]
        }
        ```
*   Attach policy to user
*   Login using IAM credentials
*   Verify limited access

**Required Screenshots:**

*   IAM user creation
*   Policy creation
*   Policy attachment
*   Login with IAM user
*   Access denied example

---

## Project 5: Build File Upload System using S3 + EC2

**Objective:** Create simple application where EC2 uploads files to S3.

**Uses:**

*   Amazon EC2
*   Amazon S3
*   AWS Identity and Access Management

**Architecture:**
```
User → EC2 App → S3 Storage
```

**Steps:**

*   Launch EC2 instance
*   Install AWS CLI:
    ```bash
    sudo apt install awscli
    ```
*   Configure credentials:
    ```bash
    aws configure
    ```
*   Create S3 bucket:
    *   `student-file-storage`
*   Upload file:
    ```bash
    aws s3 cp test.txt s3://student-file-storage
    ```
*   Verify file in S3 console

**Required Screenshots:**

*   EC2 instance running
*   S3 bucket created
*   AWS CLI configured
*   File upload command
*   File visible in S3 bucket

---

## Project 6: Deploy a Docker Container to a new EC2 Instance and host a simple website.

**Objective:** Students will deploy a docker container to a new EC2 instance and host a simple website.

**Architecture:**
```
User → Internet → EC2 Instance → Docker Container → Nginx Web Server → Website
```

**Steps:**

*   Login to AWS console.
*   Launch EC2 instance:
    *   AMI: Ubuntu
    *   Instance type: t2.micro
*   Create security group:
    *   Allow HTTP (80) and SSH (22)
*   Connect to EC2 via SSH
*   Install Docker:
    ```bash
    sudo apt update
    sudo apt install docker.io -y
    ```
*   Create a simple html file in a folder
*   Create a Dockerfile in the same folder:
    ```dockerfile
    FROM nginx:alpine
    COPY . /usr/share/nginx/html
    ```
*   Build the docker image:
    ```bash
    sudo docker build -t my-nginx .
    ```
*   Run the docker container:
    ```bash
    sudo docker run -d -p 80:80 my-nginx
    ```
*   Open browser: `http://EC2-Public-IP`

**Required Screenshots:**

*   EC2 instance running
*   Security group inbound rule
*   SSH connection terminal
*   Docker installation output
*   Website running in browser

---

## Project 7: Create a CI/CD Pipeline using AWS CodePipeline.

**Objective:** Students will create a CI/CD pipeline using AWS CodePipeline.

**Architecture:**
```
User → GitHub → CodePipeline → CodeBuild → S3
```

**Steps:**

*   Create a GitHub repository
*   Create a simple index.html file in the repository
*   Create a S3 bucket to host the website
*   Create a CodeBuild project
*   Create a CodePipeline:
    *   Source: GitHub
    *   Build: CodeBuild
    *   Deploy: S3
*   Make a change to the index.html file in the GitHub repository
*   Verify the change in the S3 bucket

**Required Screenshots:**

*   GitHub repository created
*   S3 bucket created
*   CodeBuild project created
*   CodePipeline created
*   Website updated after a git push

---

## Project 8: Create a serverless API using API Gateway and Lambda.

**Objective:** Students will create a serverless API using API Gateway and Lambda.

**Architecture:**
```
User → API Gateway → Lambda
```

**Steps:**

*   Create a Lambda function:
    *   Runtime: Python 3.11
    *   Example code:
        ```python
        import json

        def lambda_handler(event, context):
            return {
                'statusCode': 200,
                'body': json.dumps('Hello from Lambda!')
            }
        ```
*   Create an API Gateway
*   Create a resource
*   Create a method
*   Deploy the API
*   Test the API

**Required Screenshots:**

*   Lambda function created
*   API Gateway created
*   Resource and method created
*   API deployed
*   API tested

---

## Project 9: Create a highly available and scalable web application using Elastic Load Balancing and Auto Scaling.

**Objective:** Students will create a highly available and scalable web application using Elastic Load Balancing and Auto Scaling.

**Architecture:**
```
User → Route 53 → Elastic Load Balancer → Auto Scaling Group → EC2 Instances
```

**Steps:**

*   Create a launch template
*   Create an Auto Scaling group
*   Create an Elastic Load Balancer
*   Create a Route 53 record
*   Test the application

**Required Screenshots:**

*   Launch template created
*   Auto Scaling group created
*   Elastic Load Balancer created
*   Route 53 record created
*   Application tested

---

## Project 10: Monitor an EC2 instance using CloudWatch.

**Objective:** Students will monitor an EC2 instance using CloudWatch.

**Architecture:**
```
User → EC2 Instance → CloudWatch
```

**Steps:**

*   Launch an EC2 instance
*   Enable detailed monitoring
*   Create a CloudWatch alarm
*   Stop the EC2 instance
*   Verify the alarm

**Required Screenshots:**

*   EC2 instance launched
*   Detailed monitoring enabled
*   CloudWatch alarm created
*   EC2 instance stopped
*   Alarm verified
