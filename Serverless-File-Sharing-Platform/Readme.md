# Serverless File Sharing Platform on AWS
## Purpose of the project
The Serverless File Sharing Platform was designed to create a simple, cost-effective, and scalable solution for securely uploading and downloading files via a RESTful HTTP API. Utilizing AWS services like Lambda for compute, API Gateway for API management, and S3 for object storage, this project aims to provide a serverless, fully managed, and highly available solution for file sharing. Users can interact with the platform using any HTTP client (like Postman), making it versatile for various use cases that involve file sharing and storage. The main goal is to avoid the complexity of managing traditional server infrastructure, while ensuring secure and efficient file handling.
## Architecture
![Diagram explaining the architecture of this project](Images/Architecture-diagram.svg)

## Steps to Build the Project
The project was implemented with the following AWS services:
### Step 1 - Amazon S3 Bucket Setup
* Bucket Name: `my-file-sharing-bucket-pranav`
* **Purpose**: The S3 bucket serves as the storage layer for the file-sharing platform, enabling object storage and retrieval.
### Step 2 - Create an IAM Role for Lambda function
* An IAM role is needed with permissions to allow the Lambda functions to interact with the S3 bucket.
* We need to attach an **inline policy** to the IAM role.
### Step 3 - Create a Lambda function for Uploading files
* Function Name: `Upload-function`
* **Purpose**: This Lambda function handles file uploads to the S3 bucket. The function receives file content directly from the HTTP request body and saves it to S3 with a specified file name.
* The function receives the `fileName` as a query string parameter and the file content in the request body.
### Step 4 - Create a Lambda function for downloading files
* Function Name: `Download-function`
* **Purpose**: This Lambda function retrieves files from the S3 bucket and returns the file content in a Base64-encoded format.
* The function retrieves the `fileName` as a query string parameter.
* The retrieved file content is Base64-encoded to handle binary data in HTTP responses.
### Step 5 - API Gateway Configuration
* **Purpose**: API Gateway provides a RESTful API interface for the upload and download operations.
* Create a REST API.
* Create resource: `/files` will be the Resource path. Also we should enable CORS(Cross Origin Resource Sharing).
* Create method: Create `POST` method and `GET` method and select the integration type as `Lambda function` and associate them with `Upload-function` and `Download-function` respectively.
* **GET Method Configuration (Download)**:
  * We have added **query string parameter** as `filename` in the Lambda **upload-function**. This parameter will be used to
    identify the name of the file being uploaded.
  * Go to Method request-> Edit-> Select the **Request Validator** as `Validate query string parameters and headers`.
  * Under **Request body**-> Enter the **content type** as `text/plain`
  * The **Mapping Template** transforms the incoming HTTP request into a format that the Lambda function can process.
  * The **content type** header in an HTTP request indicates the media type of the resource being sent. It helps the server
    understand how to interpret the data in the body of the request.
  * For instance:
    * If the **Content-Type**: `text/plain`: The request body is plain text.
    * If the **Content-Type**: `application/json`: The request body is JSON-formatted data.
  * Go to integration request-> Edit-> Enter the **content type** as `application/json`. By specifying `application/json`, the API Gateway ensures that the incoming request data is processed as JSON. This consistency makes it easier to extract query parameters or other structured information in the Lambda function. Under **Mapping templates** paste
    the following:
```
  {
  "queryStringParameters": {
      "fileName": "$input.params('fileName')"
  }
}
```
* **POST Method Configuration (Upload)**:
  * Go to **integration request**-> Select integration type as `Lambda Function`. Under **Mapping templates**-> Enter the **Content type** as `text/plain`. By specifying `text/plain`, you inform API Gateway and the Lambda function that the request body is simple, unformatted text.Under template body paste the following:
```
{
  "body" : "$input.body",
  "queryStringParameters" : {
      "fileName" : "$input.params('fileName')"
  }
}
```
* Deployed the API to a stage (e.g., dev) via API Gateway's deployment feature.
* Once deployed, a API invoke URL will be created.
## Testing the Platform
### Upload a File: 
```
curl --location "https://lnbdggd6oe.execute-api.us-east-1.amazonaws.com/dev/files?fileName=test.txt" \
--header "Content-Type: text/plain" \
--data "Hello from pranav!"
```
* Response: `File uploaded successfully!`
### Download a File:
```
curl --location "https://lnbdggd6oe.execute-api.us-east-1.amazonaws.com/dev/files?fileName=test.txt"

```
* Response: Base64-encoded content of `test.txt`, which can be decoded to retrieve the original file content.
## Conclusion
The Serverless File Sharing Platform successfully demonstrates a cost-efficient and scalable solution using AWS serverless services. By leveraging Lambda, S3, and API Gateway, the system avoids traditional server management and provides a flexible file-sharing API that can handle a variety of file types and sizes. The implementation showcases how to build a fully managed backend that can scale automatically based on demand, ensuring high availability and reliability for file operations.
