# Stream AWS DynamoDB data to AWS OpenSearch Index using DynamoDB Lambda Triggers
## 📘 Introduction
   The purpose of this project is to create a real-time data pipeline that streams data from an Amazon DynamoDB table to an Amazon OpenSearch domain. This allows you to efficiently index and search data stored in DynamoDB for analytical and operational use cases, such as Log analytics, Full-text search on DynamoDB data, Dashboards and visualizations using OpenSearch Dashboards.
* In this project we will enable a dynamoDB stream and attach a lambda trigger to it, which processes the DDB streams and then sends the data to opensearch domain for indexing. We will create a Proxy API using API gateway and integrate it with the same lambda function. The lambda function will process incoming HTTP requests from API gateway and interact with the Opensearch domain.
## Architecture
![Diagram explaining the architecture of this project](Images/Architecture-diagram.svg)

## Step 1 - Create a VPC
* Go to AWS Console->VPC-> Configure two AZs in `us-east-1`. The AZs will be `us-east-1a` and `us-east-1b`.
* Create two private subnets and two public subnets.
* Attach a NAT gateway to one of the AZ.
* The VPC structure will be as follows:
  1. **us-east-1a**                                  
    * `private1-us-east-1a`:Lambda         
    * `public1-us-east-1a` :NAT Gateway              
  2. **us-east-1b**
    * `private2-us-east-1b`: Opensearch
    * `public2-us-east-1b`: Empty (for redundancy if needed later)
* Internet gateway will be attached to the VPC, Route tables will be created for subnets and an elastic IP will be attached to the NAT gateway(NAT Gateway requires an Elastic IP to provide outbound internet access for the Lambda function in the `private1-us-east-1a` subnet). Make sure all these are created once the VPC is configured.
* The NAT Gateway in `public1-us-east-1a` relies on the Internet Gateway to provide internet access.
### Subnet Configuration(Route table):
  1. **Lambda's Subnet (private1-us-east-1a):**
    * Destination : `0.0.0.0/0`
    * Target : NAT Gateway in `public1-us-east-1a`
  2. **OpenSearch's Subnet (private2-us-east-1b):**
    * No direct route to the internet is needed, as OpenSearch does not require outbound internet access. OpenSearch communicates directly with Lambda using private IPs.
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
* Once the domain is created, under **security configuration** add an `access policy` so that the lambda function's role can access the opensearch domain.
## Step 3 - Create a Lambda function
* Before creating a lambda function, create a lambda execution role. Attch the JSON policy. This allows the lambda function to access opensearch index, write the logs to cloudwatch, execute API gateway request and permission to dynamoDB stream.
* Next, Create a lambda function, select the runtime as python 3.8, attach the execution role that you created in the last step.
* Under Advanced settings, choose the VPC, `private1-us-east-1a` subnet and the security group associated with lambda.
* Upload the Lambda function code once the function is created. The Lambda function will process incoming HTTP request from the API gateway and interact with the opensearch domain. The Lambda function code also proesses DynamoDB streams and send the data to opensearch.
* Go to **Configuration**->  **general configuration** -> Update the timeout from 3 sec(default) to 1 minute because there will be multiple API calls happening to opensearch domain.
## Step 4 - Create a API gateway
* Create a REST API.
* Create a resource within the API gateway. This resource will redirect your request to the lambda. Enter the Resource name as `{proxy+}` so that all the request will be redirected to the single lambda.
* Create a method. Select the method as `ANY`. And select the lambda function that you have created. Now this integration will add the permission to invoke the lambda function.
* Deploy the API to a new stage called `dev`. Once deployed you'll get a API gateway invoke URL.
## Step 5 - Configure DynamoDB Streams
### Create a dynamoDB table
* Enter the table name as `books`, Partition key as `author`, Sort key as `bookTitle`
* Under tables's capacity settings, choose `On-demand mode`.
### Configure DynamoDB streams
* Under tables's exports and streams section you'll find an option to enable DynamoDB streams
* You have to select the view type. View type is the data that will be sent to your streams. Select New and old images.
### Create a trigger to invoke the Lambda function
* Under tables's exports and streams section you'll find an option to create a trigger.
* Select the Lambda function that you created. Select the batch size as 1. Batch size is how long dynamoDb has to wait before it streams the data into the lambda function. By setting 1, for every single change in the table, your lambda function will get invoked. If the batch size is set to 10, for every 10 changes in the table, your lambda function will get invoked.
## Step 6 - Add Environment variables to Lambda function
* Under **configuration**, click on edit environment variables. Add the following variables.
 1. Add `HOST` as *Key* and under *value*, add the opensearch domain endpoint.
 2. Add `API_STAGE' as *Key* and under *Value* add `dev`.
 3. Add `ES_INDEX` as *key* and under *Value* add `books`.
 4. Add `DB_HASH_KEY` as *Key* and under *Value* add `author`.
 5. Add `DB_SORT_KEY` as *Key* and under *Value* add `bookTitle`.
## 🔎Testing
1. Try accesing the Opensearch domain through API gateway endpoint and you'll be able to see opensearch dashboard. The following is the URL to access opensearch dashboard. 
`https://<host>/<api-stage-name>/_dashboards/app/dev_tools#/console`
Replace `https://<host>/<api-stage-name>` with your `API invoke URL`.
2. Once you open the opensearch domain you get to see the default index. Create a new index. You can get an example index from *opensearch documentation*. You can find example index by searching `**Create index**` in the search bar.
Paste the index in the opensearch domain console.
   Change the *index* name as `books`(Name of the dynamoDB table).
   In *Mappings*, add the dynamoDB table attributes. In our case its `bookTitle` and `author`. Give your index an alias name.
   Once all the changes are done you can run the command and that will create your first index. Below is the sample template.
```
GET /books/_search
{
  "query": {
    "match_all": {}
  }
}

GET /books

PUT /books
{
  "settings": {
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  },
  "mappings": {
    "properties": {
      "bookTitle": {
        "type": "text"
      },
      "author": {
        "type": "text"
      }
    }
  },
  "aliases": {
    "book1": {}
  }
}
```
3. * **INSERT item**: Lets create an entry in the table. Add the Value as 'Dan Brown' to *author* and 'The DaVinci code' to *bookTitle*. If we go to OpenSearch dashboard you should be able to see the item/data that you created. You can verify the New data the item details you created.
   * **MODIFY item**: Edit the existing record. Add a new attribute to the item. Add the attribute name as *subTitle* and *value* as 'Volume-1'. If you check the Opensearch dashboard, you can verify the modified item.
   * **REMOVE item**: Delete an item from the table. You can verify opensearch dashboard to see that the item is deleted or not.
## ✅ Conclusion
This project demonstrates a scalable, serverless architecture for real-time data streaming and indexing. By leveraging AWS services such as DynamoDB, Lambda, and OpenSearch, it provides a cost-effective solution for integrating NoSQL data with full-text search and analytics capabilities.
 

