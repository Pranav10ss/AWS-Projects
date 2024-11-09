# Serverless Registration form
## Project Overview
The **serverless registration form** is serverless web application built using AWS services: API Gateway, Lambda, and DynamoDB. The main goal of this project is to provide a scalable and cost-effective solution for collecting user registration data without maintaining a traditional server.
## Project Architecture
## Step 1 - Create a dynamoDB table
* Go to DynamoDB console-> `Create table`-> Enter the table name as `registration-table` and Partition Key as `email`(String).
  (Primary key should be unique for each item in the table. In this table we will use `email` as the primary key since it is
  unique for each user). Then click on `Create table`.
## Step 2 - Create a IAM role for Lambda function
* We need to create an IAM Role with certain permissions that will allow Lambda function to access dynamoDB. Go to IAM console->
  Roles->Select trusted entity types as `AWS service`. Select the use case as `Lambda`.
* Assign `AmazonDynamoDBFullAccess` permission policy to the role.
* In order to look for the logs, we need to assign `CloudwatchFullAccess` permission policy as well. All the logs will be 
  written to CloudWatch.
* Give the role a name and Click on `Create Role`.
## Step 3 - Create a Lambda function
* In this step we will create a Lambda function that will handle form submission and store the data to dynamoDB table. We
  will python as our Lambda function's programming language. 
* Go to Lambda console-> `Create function`-> Enter the function name as `registration-form-function`. Select the latest
  python runtime. Under 'Change default execution role' select `Use an existing role` and choose the IAM role that you
  created in the last step. Then click on `Create function`.
* Write a lambda function. Write the code for the Lambda function. We will define the Lambda function that recieves the 
  registration form data, creates a new item in the dynamoDB table and returns a response to the user. We will also add CORS 
  headers to the response to enable cross domain request from the frontend. 
