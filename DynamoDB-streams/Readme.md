# Using DynamoDB Streams with Lambda Triggers
## Project Overview
In this project we will look at how to build capture stream data using lambda functions. We can enable dynamoDB in any table and the moment you enable it, any application/user that INSERTS, MODIFIES or DELETES the data in the table
, the modifications will be automatically streamed and this information will be available for 24H. The data is time-ordered and you can set what exactly needs to be streamed( Stream view types). We can Stream view types such as:
  1. KEYS ONLY
  2. NEW IMAGE
  3. OLD IMAGE
  4. NEW AND OLD IMAGES
You can attach a lambda function to the stream. Push will be invoked synchronously and you can do whatever post processing you want to do with this lambda function.
## Architecture
## Steps to build this project
### Step 1 - Create a dynamoDB table
* Enter the table namme as 
