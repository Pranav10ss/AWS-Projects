# Stream AWS DynamoDB data to AWS OpenSearch Index using DynamoDB Lambda Triggers
## 📘 Introduction

## Architecture
![Diagram explaining the architecture of this project](Images/Architecture-diagram.png)

## Step 1 - Create a VPC
* Go to AWS Console->VPC-> Configure two AZs in `us-east-1`. The AZs will be `us-east-1a` and `us-east-1b`.
* Create two private subnets and two public subnets.
* Attach a NAT gateway to one of the AZ.
* The VPC structure will be as follows:
            **us-east-1a**                                   **us-east-1b**
          `private1-us-east-1a`:Lambda                   `private2-us-east-1b`: Opensearch
          `public1-us-east-1a` :NAT Gateway              `public2-us-east-1b`: Empty (for redundancy if needed later)
* Internet gateway will be attached to the VPC, Route tables will be created for subnets and an elastic IP will be attached to the NAT gateway(NAT Gateway requires an Elastic IP to provide outbound internet access for the Lambda function in the `private1-us-east-1a` subnet) by default. Make sure all these are created once the VPC is configured.
* The NAT Gateway in `public1-us-east-1a` relies on the Internet Gateway to provide internet access.
### Subnet Configuration(Route table):
**Lambda's Subnet (private1-us-east-1a):**
* Destination : `0.0.0.0/0`
* Target : NAT Gateway in `public1-us-east-1a`
**OpenSearch's Subnet (private2-us-east-1b):**
* No direct route to the internet is needed, as OpenSearch does not require outbound internet access.OpenSearch communicates directly with Lambda using private IPs.
### Security Group Configuration:
**Lambda's Security Group:**(To allow outbound HTTPS access)
* Select VPC that you created.
* Under Outbound rule, Select the type as `HTTPS` and select the destination as `Anywhere IPv4`.
* Inbound Rules Are Not Needed for Lambda because, Lambda is invoked by AWS internally (e.g., API Gateway or DynamoDB Streams), so no direct inbound traffic from the network is required.
**OpenSearch's Security Group:**
* Select the VPC that you created. 
* Inbound Rule: Allow HTTPS (port 443) from Lambda’s Security Group. This ensures that only Lambda can communicate with OpenSearch securely.
### VPC Workflow
1. Lambda in `private1-us-east-1a`:
   * Sends outbound HTTPS requests to OpenSearch in `private2-us-east-1b` via private IP.
   * Uses NAT Gateway in `public1-us-east-1a` for internet access.
2. OpenSearch in `private1-us-east-1b`:
   * Accepts HTTPS traffic from Lambda (restricted by security group).
3. NAT Gateway:
   * Provides Lambda with outbound internet connectivity (e.g., for AWS APIs, DynamoDB, etc.).
4. Internet Gateway:
   * Required for the NAT Gateway to provide internet access.
## Step 2 - Create an Opensearch domain
* Go to opensearch domain-> Give a domain name-> Select the **Deployment type** as `Development and testing`.
* Select the `latest version` of opensearch.
* Select the number of Availability zones as 1. AWS is place opensearch's node(primary node) across 1AZ.
  (**NOTE**: If you select 2 AZs,  the OpenSearch domain will distribute its nodes(replica and primary) across two Availability Zones (`us-east-1a` and `us-east-1b`).
* Choose the number of nodes as 1.
* Under **Network** configuration, choose the VPC. Select the `private2-us-east-1b` subnet and select the security group that you created for the opensearch.
## Step 2 - Create a Lambda function
* Before creating a lambda function, create a lambda execution role. Attch the JSON policy.

## ✅ Conclusion

 

