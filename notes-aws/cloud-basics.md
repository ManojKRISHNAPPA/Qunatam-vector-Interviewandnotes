# Cloud Computing Basics

Cloud computing is the delivery of computing services—including servers, storage, databases, networking, software, analytics, and intelligence—over the Internet ("the cloud") to offer faster innovation, flexible resources, and economies of scale.

## Service Models

### Infrastructure as a Service (IaaS)

IaaS provides virtualized computing resources over the internet. It's the most basic category of cloud computing services. With IaaS, you rent IT infrastructure—servers and virtual machines (VMs), storage, networks, operating systems—from a cloud provider on a pay-as-you-go basis.

**Analogy:** It's like leasing a plot of land. You can build whatever you want on it, but you're responsible for maintaining the structure.

### Platform as a Service (PaaS)

PaaS provides a platform allowing customers to develop, run, and manage applications without the complexity of building and maintaining the infrastructure typically associated with developing and launching an app.

**Analogy:** It's like renting a workshop. The tools and equipment are provided, but you bring your own materials and build your own things.

### Software as a Service (SaaS)

SaaS is a method for delivering software applications over the Internet, on demand and typically on a subscription basis. With SaaS, cloud providers host and manage the software application and underlying infrastructure and handle any maintenance, like software upgrades and security patching.

**Analogy:** It's like renting a fully furnished and serviced apartment. You just move in and use it.

## Amazon EC2 (Elastic Compute Cloud)

Amazon Elastic Compute Cloud (Amazon EC2) is a web service that provides secure, resizable compute capacity in the cloud. It is designed to make web-scale cloud computing easier for developers.

### Key Features of EC2

*   **Instances:** Virtual servers that can be configured with various CPU, memory, storage, and networking capacities.
*   **Amazon Machine Images (AMIs):** Pre-configured templates for your instances that package the bits you need for your server (including the operating system and additional software).
*   **Instance Types:** Various families of instance types are optimized to fit different use cases. Instance types comprise varying combinations of CPU, memory, storage, and networking capacity and give you the flexibility to choose the appropriate mix of resources for your applications.
*   **Key Pairs:** Secure login information for your instances. AWS stores the public key, and you store the private key in a secure place.
*   **Storage:**
    *   **Amazon EBS (Elastic Block Store):** Persistent block storage volumes for use with Amazon EC2 instances.
    *   **Instance Store:** Provides temporary block-level storage for your instance. This storage is located on disks that are physically attached to the host computer.
*   **Networking and Security:**
    *   **Virtual Private Cloud (VPC):** A logically isolated section of the AWS Cloud where you can launch AWS resources in a virtual network that you define.
    *   **Security Groups:** A virtual firewall for your instance to control inbound and outbound traffic.
*   **Pricing Models:**
    *   **On-Demand:** Pay for compute capacity by the hour or the second with no long-term commitments.
    *   **Reserved Instances:** Provide you with a significant discount (up to 75%) compared to On-Demand instance pricing.
    *   **Spot Instances:** Allow you to request spare Amazon EC2 computing capacity for up to 90% off the On-Demand price.
    *   **Dedicated Hosts:** A physical EC2 server dedicated for your use.

## Why Choose Amazon Web Services (AWS)?

*   **Market Leader:** AWS is the oldest and most dominant player in the cloud computing market. It has a vast and mature offering.
*   **Comprehensive Services:** AWS offers a wide range of services, from basic compute and storage to advanced services like machine learning, AI, and IoT.
*   **Global Reach:** AWS has a massive global infrastructure, allowing you to deploy applications and serve users worldwide with low latency.
*   **Security and Reliability:** AWS provides a highly secure and reliable infrastructure with extensive compliance certifications.
*   **Innovation:** AWS is constantly innovating and releasing new services and features.
*   **Large Community and Partner Ecosystem:** A vast community of users and partners means extensive documentation, tutorials, and third-party tools are available.
