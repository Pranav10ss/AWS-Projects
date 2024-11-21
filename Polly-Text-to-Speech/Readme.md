# Building a Text to Speech/Audio converter using Amazon Polly
## 📘Project Overview
The primary objective of this project is to create an automated system that converts text files uploaded to an Amazon S3 bucket into audio files using Amazon Polly. This project demonstrates the integration of multiple AWS services—S3, Lambda, Polly, and IAM—to build a scalable, serverless application. It addresses the need for text-to-speech functionality, which can be utilized in accessibility tools, voice-based applications, or content creation workflows.
## Architecture diagram
![Diagram explaining the architecture of this project](Images/TextToSpeech.svg)
## Steps to build the project:
### Step 1 - Create a source S3 bucket
* Create a Source S3 bucket to store the text files.
* Go to S3 console, create a bucket with default settings.
*Now we have two EC2 instances in two different AZs, ready to share files from EFS.*
### Step 2 - Create a destination S3 bucket
* Create a destination S3 bucket to store the audio files.
* Go to S3 console, create a bucket with default settings.
### Step 3 - Create an IAM policy
* In order to allow Lambda function to access S3 bucket, Amazon Polly and execute basic functions attach an IAM role to the
  function.
* Create a IAM policy and paste the following JSON code:
  ```
  {
  "Version": "2012-10-17",
  "Statement": [
      {
          "Effect": "Allow",
          "Action": [
              "s3:GetObject",
              "s3:PutObject"
          ],
          "Resource": [
              "arn:aws:s3:::amc-polly-source-bucket/*",
              "arn:aws:s3:::amc-polly-destination-bucket/*"
          ]
      },
      {
          "Effect": "Allow",
          "Action": [
              "polly:SynthesizeSpeech"
          ],
          "Resource": "*"
      }
  ]
}
  ```
* Create a role in the IAM console and attach the above inline policy. Also attach `AWSLambdaBasicExecutionRole`
* Make sure that the role has `trust relationship policy` attached so that Lambda service has permission to assume the role
  and act on behalf of the function.
### Step 4 - Create a Lambda function
* Go to lambda console -> create function -> select Python 3.X as the runtime.
* Under **Change default execution role** , choose the execution role that you created in the last step. 
## ✅Conclusion
`
