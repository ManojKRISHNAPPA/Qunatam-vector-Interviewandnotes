# AWS Interview Questions and Answers

## Cloud Basics

**Q1: What is the difference between IaaS, PaaS, and SaaS?**

*   **IaaS (Infrastructure as a Service):** Provides virtualized computing resources over the internet. You manage the OS, middleware, and applications. Examples: AWS EC2, Google Compute Engine.
*   **PaaS (Platform as a Service):** Provides a platform for developing, running, and managing applications without the complexity of infrastructure management. You manage the application and data. Examples: AWS Elastic Beanstalk, Heroku.
*   **SaaS (Software as a Service):** Provides ready-to-use software applications over the internet. The provider manages everything. Examples: Google Workspace, Salesforce.

**Q2: What are the benefits of cloud computing?**

*   **Cost Savings:** Pay-as-you-go model reduces capital expenditure.
*   **Scalability and Elasticity:** Easily scale resources up or down based on demand.
*   **Flexibility and Agility:** Quickly deploy new applications and services.
*   **High Availability and Reliability:** Cloud providers offer robust infrastructure with built-in redundancy.
*   **Global Reach:** Deploy applications in multiple regions around the world.

## Amazon EC2

**Q3: What is an Amazon Machine Image (AMI)?**

An AMI is a pre-configured template for your instances that includes the operating system, application server, and applications. It provides the information required to launch an instance.

**Q4: What are the different pricing models for EC2?**

*   **On-Demand:** Pay for compute capacity by the hour or second with no long-term commitments.
*   **Reserved Instances:** Purchase instances for a 1 or 3-year term for a significant discount.
*   **Spot Instances:** Bid on spare EC2 computing capacity for up to 90% off the On-Demand price.
*   **Dedicated Hosts:** A physical server dedicated for your use.

**Q5: What is the difference between Amazon EBS and Instance Store?**

*   **Amazon EBS (Elastic Block Store):** A persistent block storage service. The data is independent of the instance lifecycle.
*   **Instance Store:** Temporary block-level storage for an instance. The data is deleted when the instance is terminated.

**Q6: What is a Security Group?**

A security group acts as a virtual firewall for your instance to control inbound and outbound traffic. You can specify rules that allow or deny traffic from certain IP addresses or other security groups.
