# Building a HTTP CRUD API with AWS Lambda, API Gateway, and DynamoDB
## 📜Project Overview
The purpose of this project is to demonstrate how to build a serverless CRUD(Create, Read, Update, Delete) API using AWS services. This application leverages AWS Lambda for backend logic, API Gateway for HTTP API management, and DynamoDB as a NoSQL database for data storage. 
## Architecture
## 🎯Goal of this project
The goal of this project is to create a simple, scalable, and cost-effective HTTP API that allows users to perform basic CRUD operations on an item list. This project helps to understand:
* How to use AWS Lambda for serverless functions.
* How to integrate Lambda with API Gateway.
* How to interact with DynamoDB for data storage using AWS SDK (Boto3).
## Step 1 - Create a DynamoDB table
* Create a dynamoDB table with name `http-crud-tutorial-items`
* Enter the Primary key as `id`
## Step 2 - Create an IAM Role for the Lambda funtion
* Create an IAM role to allow Lambda function to allow access to dynamoDB. Attach `AmazonDynamoDBFullAccess` permissions policy.
## Step 3 - Create the Lambda function
* Enter the function name as `http-crud-tutorial-function`. Select the runtime as `Python 3.9`
* Under `Change default execution role` select the role that you created in the last step and attach it to the function.
* Click on `Create function`.
## Step 3 - Create a HTTP API using API Gateway
* Go to API Gateway'and choose `HTTP API` type and click on `build`.
* Enter the name as `http-crud-tutorial-api`. Keep all other things as default and click on `create`.
## Step 4 - Create routes 
* Define routes and integrate them with the Lambda function.
* To create 'Routes', Go to `Routes`->`Create`-> Select the method and enter the path.
```
GET /items/{id}                  #Retrieve an item by its ID
GET /items                       #Retrieve all items
PUT /items                       #Create or update an item
DELETE /items/{id}               #Delete an item by its ID
```
* To integrate the routes with lambda function, go to `Integrations` and select each route at a time and attach the lambda
  function.
