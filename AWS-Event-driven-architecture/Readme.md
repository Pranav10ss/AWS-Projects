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

### Architecture Overview
The system performs the following tasks:
1. Detects specific events on an S3 bucket.
2. Publishes notifications about these events to an SNS topic.
3. SNS Distributes the notifications to two SQS queues based on filter policies('Put' and 'Copy').
4. Triggers Lambda functions for processing messages from the respective SQS queues.
## Steps to Build the Project
### Step 1 - Set Up the S3 Bucket
* Create a S3 bucket with default settings.
### Step 1 - Create a SNS Topic
* Name the SNS topic as event-driven-project
