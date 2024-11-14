# Building a Scalable Storage Solution with AWS EFS and EC2
## Project Overview
In this project, we design and implement a Scalable Storage Solution using AWS Elastic File System (EFS) and EC2 instances. The project demonstrates a solution that requires a centralized, scalable, and highly available storage solution for managing large volumes of files. By leveraging EFS, we can achieve a fully managed, elastic, and high-performance shared file system that can be accessed by multiple EC2 instances deployed across different Availability Zones (AZs).
 EFS offers a fully managed, elastic, and highly available shared file system, which multiple EC2 instances can access simultaneously. This allows different teams to collaborate seamlessly and work on shared assets without storage bottlenecks.
## Architecture diagram
![Diagram explaining the architecture of this project](Images/Architecture-diagram.png)
### Key components:
   * EC2 instances: EC2 instances serve as the clients that access and utilize the shared storage provided by Amazon EFS. EC2 
     instances are deployed in multiple Availability Zones (AZs) to access the shared file system (EFS) concurrently. This setup
     allows production teams to work on the same set of media files from different servers without needing to copy or transfer
     files between instances.
     The EC2 instances use NFS to mount the EFS file system. The secure data transfer between EC2 and EFS is encrypted in 
     transit using TLS, ensuring that sensitive files are protected.
   * VPC with Subnets: The infrastructure is set up within a Virtual Private Cloud (VPC) with subnets in different AZs.
   * Security Groups: Control inbound and outbound traffic for the EC2 instances and EFS mount targets.
   * Amazon Elastic File System (EFS): Provides scalable, high-performance, and highly available shared storage for multiple
     EC2 instances.
