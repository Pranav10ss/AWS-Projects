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
* Go to AWS console-> S3-> create bucket -> Name the bucket and click on `create bucket`
### Step 2 - Create an SNS Topic
* Go to SNS -> Topics -> Create topic -> Select the 'type' of topic as `standard`.
  *(Note that SNS `FIFO` topics have restrictions on the types of endpoints they can deliver messages to. They are designed to work primarily with Amazon SQS queues to maintain strict message ordering and deduplication.
  SNS FIFO topics do not support delivery to endpoints like SMS, email, Lambda functions, or HTTP/HTTPS endpoints directly. This is because these endpoint types cannot guarantee the preservation of strict message ordering, which is a key feature of FIFO topics.)*
* Name the topic as `ImageUploadNotification` and click on `create topic`.
### Step 3 - Create a subscription for the SNS topic
* Go to SNS -> Subscriptions -> Create subscription -> Enter the 'ARN' of the SNS topic under `Topic ARN`. Select the 
  protocol as `Email`. Enter the Email address in the `Endpoint` field. At last click on `create subscription`.
* Once the subscription is created you'll receive a mail from AWS to confirm the subscription. Click on the link provided in
  the mail to confirm the SNS subscription. Once you confirm the subscription the status of the subscription changes from `pending confirmation` to `confirmed`.
### Step 4 - Create a Lambda function
* Go to `Lambda`-> `ceeate function`-> select `Author from scratch`. Give the name of the function as `ImageUploadProcessor`.
  Select the latest python runtime. Under 'Change default execution role' select `create a new role with basic lambda 
  permissions` which lets Lambda create an execution role named `ImageUploadProcessor-Role`. Then click on `Create function`.
* You need to attach permissions policy to this lambda role in order to allow lambda function to access S3 events and to be 
  able to send messages to SNS topic after processing the event. So attach `S3FullAccess` and `SNSFullAccess`.
### Step 5 - Add a S3 trigger to the Lambda function
* Go to Lambda function -> Click on `+ Add trigger` -> 'Select a source' as `S3`-> Select the name of the bucket which you
  have created for this project. Under 'Event types' select `All object create events`. Which means Lambda will get
  triggered whenever an object is created/uploaded to the S3 bucket. At last click on `Add` to add the trigger.
### Step 6 - Write the Lambda function code
* Using AWS SDK for python (Boto3) write a lambda function. Since Lambda function will interact with SNS topic the `Client` will be SNS. Attach the ARN of the SNS topic in place of `topic_arn`.
```python
  import json
  import boto3

  def lambda_handler(event, context):
    sns_client = boto3.client('sns')
    topic_arn = 'arn:aws:sns:your-region:your-account-id:ImageUploadNotification'
    
    # Parse the S3 event
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        message = f'Image uploaded to bucket {bucket} with key {key}'
        
        # Publish message to SNS
        sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject='Image Upload Notification'
        )
        
    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent successfully!')
    }
#Replace your-region, your-account-id, and ImageUploadNotification with appropriate values from your SNS topic.
```
  

