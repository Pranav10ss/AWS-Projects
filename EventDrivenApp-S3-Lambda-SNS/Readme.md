# Building an Event-driven-application on AWS using S3, Lambda and SNS
## Project description
Building a simple event driven application in AWS. We will learn how to set-up a S3 bucket to trigger a lambda function whenever a new image is uploaded to the S3 bucket. This function processes the event and sends a notification to the subscribers/apps through Simple notification service(SNS).
## Project Architecture
## Project Workflow
1. S3: Client/application uploads an image to S3 bucket. S3 is used to store the images uploaded by the user.
2. Lambda: Lambda is a serverless compute service that lets you run code in response to an event. The S3 bucket is configured to trigger a Lambda function when an object is created. The Lambda function, written in Python, processes the S3 event to extract details such as the bucket name, object key etc., and publishes a message to an SNS topic.
3. SNS: SNS is a fully managed messaging service for both application to application and application to person communication.
   The **SNS topic** receives the message from the lambda function and then sends a notification to its subscribers through E-Mail.
## Steps to build this project
### Step 1 - Create a S3 bucket
* hu
