# AWS Event-Driven Architecture
## Purpose of the Project
  The purpose of this project is to demonstrate an event-driven architecture using AWS services that leverage Amazon S3, SNS, SQS, and Lambda to build a decoupled, scalable, and resilient system. The project highlights the use of Amazon SQS for decoupling message producers and consumers, enabling asynchronous processing and high availability of event handling.
  This project uses events to decouple an application's components.
  This project mainly has four components:
1. Event producers(S3) - These are the ones that causes the change in state and produces the event
2. Event ingestion(SNS) - Its like an event router that filters and pushes the event to the next componenet
3. Event stream(SQS) - Serve as buffers and ensure reliable, decoupled delivery of events to consumers
4. Event consumers - Processes the events received from queues. These are the ones that actually take action on the events
   like performing some workflow or updating the database.
  
## Architecture
![Diagram explaining the architecture of this project](Images/Architecture-diagram.png)

### Architecture Overview
The system performs the following tasks:
1. Detects specific events on an S3 bucket.
2. Publishes notifications about these events to an SNS topic.
3. SNS Distributes the notifications to two SQS queues based on filter policies('Put' and 'Copy').
4. Triggers Lambda functions for processing messages from the respective SQS queues.
## Steps to Build the Project
### Step 1 - Set Up the S3 Bucket
* Create a S3 bucket with default settings.
### Step 2 - Create a SNS Topic
* Name the SNS topic as `event-driven-project` and select the Type as `Standard`
* Attach an **access policy** to allow S3 to send messages to SNS and to allow SQS to subscribe to SNS Topic. Under **access
  policy**, choose the method as `Advanced` and paste the JSON policy.
### Step 3 - Create SQS Queues
* We need to create two queues. Name the first queue as `queue1` and second queue as `queue2`.
* Select the queue type as `standard`.
* Attach an **access policy** to allow SNS to send messages to SQS queue and to allow Lambda to access/receive the messages.
  Under **access policy**, choose the method as `Advanced` and paste the JSON policy.
* We need to point `queue1` to the first Lambda function i.e, `event-driven-function1` and `queue2` to the second Lambda
  function i.e, `event-driven-function2`. So make sure that in the access policy of the queues you specify the respective 
  Lambda function's name.
### Step 4 - Create Lambda function
* We need to create two Lambda functions. Before creating the Lambda functions we need to create an IAM role for bot the
  functions.
* Create two roles and attach the inline policy. Use `Lambda-policy.json` as the JSON code. This policy allows Lambda to 
  access SQS queue and cloudwatchlogs.
* In the access policy, mark `queue1` to the first Lambda function i.e, `event-driven-function1` and `queue2` to the second 
  Lambda function i.e, `event-driven-function2`.
* After creating the IAM roles, create the lambda functions `event-driven-function1` and `event-driven-function2` with
  respective roles attached. Select the runtime as `python 3.8`.
* Below is the Lambda function code which is same for both the functions.
  
  ```python
    import json
  
  def lambda_handler(event, context):
      print(json.dumps(event))
      return {
          'statusCode': 200,
          'body': json.dumps('Hello from Lambda!')
      }
  ```
### Step 5 - connect all the components
1. Connect S3 to SNS:
   * Create an S3 Event. Go to **Event Notifications** and name the event as `NewObjectNotifier`. Select event type as `All
     object create events`.
   * Select the **destination** as `SNS Topic` and choose the topic that you've created.
2. Connect SNS Topic to SQS queues:
   * Create two **Subscriptions** one for `queue1` and another for `queue2`.
   * We need to attach **Subscription filter policy** which allows SNS to filter messages/events and forward only the
     specific event to specific SQS queue.
   * Attach the following policy to queue1's subscription. Only the `PUT` related events will be forwarded to this stream.
  ```json 
  {
  "Records": {
    "eventName": [
      "ObjectCreated:Put"
    ]
  }
}
```
   