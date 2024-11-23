# Using DynamoDB Streams with Lambda Triggers
## 📘Project Overview
In this project we will look at how to capture DynamoDB stream data using a lambda function. We can enable dynamoDB stream in any table and the moment you enable it, any application/user that INSERTS, MODIFIES or DELETES the data in the table, the modifications will be automatically streamed and this information will be available for 24H. The data is time-ordered and you can set what exactly needs to be streamed( Stream view types). We can set Stream view types such as:
  1. KEYS ONLY
  2. NEW IMAGE
  3. OLD IMAGE
  4. NEW AND OLD IMAGES
* You can attach a lambda function to the stream. Push will be invoked synchronously and you can do whatever post processing you want to do with this lambda function.
## Architecture
![Diagram explaining the architecture of this project](Images/Architecture-diagram.svg)
## Steps to build this project
### Step 1 - Create a dynamoDB table
* Enter the table name as `books`
* Partition key as `author`
* Sort key as `bookTitle`
* Under tables's capacity settings, choose `On-demand` mode.
### Step 2 - Configure DynamoDB streams
* Under tables's **exports and streams** section you'll find an option to enable **DynamoDB streams**
* You have to select the view type. View type is the data that will be sent to your streams. Select `New and old images`
* Once the stream is enabled you can add a trigger to invoke a lambda function
### Step 3 - Create a Lambda function
* Name the function and select the runtime as python.
* Under **Change default execution role**, allow it to create a new IAM role for Lambda function to assume so that it can access the dynamoDB streams and CloudWatch logs.
* You need to make some changes to the policy attached to the IAM role. Add permissions by selecting the sevice as dynamoDB.
  It requires four different actions. Those ase `GetRecords`,`GetShardIterator`,`DescribeStream`,`ListStreams`.
* Also add the **dynamoDb stream ARN** to the policy. After that review the changes and save.
* The code of the lambda function will be
```python
import json

def lambda_handler(event, context):
    print(event)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```
### Step 4 - Create a trigger to invoke the Lambda function
* Under tables's **exports and streams** section you'll find an option to create a trigger.
* Select the Lambda function that you created. Select the **batch size** as `1`. Batch size how long dynamoDb has to wait before it streams the data into the lambda function. By setting `1`, for every single change in the table, your lambda function will get invoked. If the **batch size** is set to `10`, for every 10 changes in the table, your lambda function will get invoked.
## 🔎Testing
1. **INSERT** record event: Lets create an entry in the table. Add the Value as `Dan Brown` to **author** and `The DaVinci code` to **bookTitle**.
   If we go to lambda-> Monitor-> view CloudWatchlogs for the function, you should be able to see the event being printed.
   You can verify the `NewImage` event with the item details you created.
2. **MODIFY** record event: Edit the existing record. Add a new attribute to the item. Add the attribute name as `subTitle`and value as `Volume-1`.
   If you check the CW logs, you can verify the `MODIFY` event with `NewImage` and `OldImage`.
3. **REMOVE** record event: Delete the item from the table. You can verify `REMOVE` event with `OldImage`
## ✅Conclusion
At the end of this project we achieve the following:
   1. **Event-Driven Architecture**: Real-time processing of DynamoDB changes using Lambda.
   2. **Stream Data Access**: Demonstrates how to retrieve INSERT, MODIFY, and DELETE events.
   3. **Practical Insights**: Teaches how to set up triggers and access stream records programmatically.
