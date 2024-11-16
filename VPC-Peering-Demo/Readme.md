# VPC Peering Connection demo
## Project Overview
The goal of this project is to establish connectivity between two distinct AWS Virtual Private Clouds (VPCs) using VPC Peering. This setup allows instances in different VPCs to communicate with each other privately without using an internet gateway, VPN, or other AWS networking services. VPC Peering provides a secure, low-latency, and scalable method of communication between VPCs across the same or different AWS accounts and regions.
## Architecture of the Project
![Diagram explaining the architecture of this project](Images/Architecture-diagram.svg)
### **Components Used:**
1. VPCs:
   * **VPC A** with CIDR `10.16.0.0/16`
   * **VPC B** with CIDR `10.17.0.0/16`
2. Subnets:
   * **Subnet A** in VPC A with CIDR `10.16.0.0/20`
   * **Subnet B** in VPC B with CIDR `10.17.0.0/20`
3. EC2 Instances:
   * EC2 instance in Subnet A (VPC A)
   * EC2 instance in Subnet B (VPC B)
4. IAM Role:
   * IAM Role for CloudFormation to provision EC2 instances with required SSM (AWS Systems Manager) permissions.
5. VPC Peering:
   * Peering connection between **VPC A** and **VPC B**.
## Steps to build this project
### Step 1 - Create a CloudFormation Stack
* Create a CloudFormation template (YAML) to automate the creation of VPCs, subnets, EC2 instances, security groups, IAM
  roles, and VPC endpoints.
* The stack will deploy the following resources:
  * **VPC A** and **VPC B**: Each with its own subnets.
  * Security Groups: Allow SSH (port 22) access to instances from any IP address.
  * EC2 Instances: Two instances launched, one in each VPC's subnet.
### Step 2 - Establish VPC Peering
* Go to VPC console-> Peering Connections-> Create peering connects-> Name it as `VPC A - VPC B`.
* Select the local VPC as `VPC-A`. Select the Acceptor VPC(the one which you are trying to connect to) as `VPC-B`. You can
  verify the CIDR of both VPCs.
* After creating the peering you'll have to accept the peering connection. Click on `Actions` and you'll find an option as
  `Accept request`. Click on it to accept the peering connection between two VPCs.
### Step 3 - Security group configuration
