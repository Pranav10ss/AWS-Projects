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
          `private1-us-east-1a`:Lambda                   `private1-us-east-1b`: Opensearch
          `public1-us-east-1a` :NAT Gateway              `public1-us-east-1b`: Empty (for redundancy if needed later)
* Internet gateway will be attached to the VPC, Route tables will be created for subnets and an elastic IP will be attached to the NAT gateway(NAT Gateway requires an Elastic IP to provide outbound internet access for the Lambda function in the `private1-us-east-1a` subnet) by default. Make sure all these are created once the VPC is configured.
* The NAT Gateway in `public1-us-east-1a` relies on the Internet Gateway to provide internet access.
### Subnet Configuration(Route table):
**Lambda's Subnet (private1-us-east-1a):**
    * Destination : `0.0.0.0/0`
    * Target : NAT Gateway in `public1-us-east-1a`
**OpenSearch's Subnet (private1-us-east-1b):**
    * No direct route to the internet is needed, as OpenSearch does not require outbound internet access.
      OpenSearch communicates directly with Lambda using private IPs.
### Security Group Configuration:
**Lambda's Security Group:**(To allow outbound HTTPS access)
    * Select VPC that you created.
    * Under Outbound rule, Select the type as `HTTPS` and select the destination as `Anywhere IPv4`.
    * Inbound Rules Are Not Needed for Lambda because, Lambda is invoked by AWS internally (e.g., API Gateway or DynamoDB 
      Streams), so no direct inbound traffic from the network is required.
**OpenSearch's Security Group:**
    * Select the VPC that you created. 
    * Inbound Rule: Allow HTTPS (port 443) from Lambda’s Security Group. This ensures that only Lambda can communicate with 
      OpenSearch securely.
### VPC Workflow

## ✅ Conclusion

 

