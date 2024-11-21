# Building a Text to Speech/Audio converter using Amazon Polly
## 📘Project Overview
The primary objective of this project is to create an automated system that converts text files uploaded to an Amazon S3 bucket into audio files using Amazon Polly. This project demonstrates the integration of multiple AWS services—S3, Lambda, Polly, and IAM—to build a scalable, serverless application. It addresses the need for text-to-speech functionality, which can be utilized in accessibility tools, voice-based applications, or content creation workflows.
## Architecture diagram
![Diagram explaining the architecture of this project](Images/TextToSpeech.svg)
## Steps to build the project:
### Step 1 - Create a source S3 bucket
* Create a Source S3 bucket to store the text files.
* Go to S3 console, create a bucket with default settings.
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
* After configuring the Lambda function, go to **configuration** and add environment variables. Enter the key as
  `SOURCE_BUCKET` and under **value** enter the name of your source bucket. Similarly Enter the key as 
  `DESTINATION_BUCKET`and under **value** enter the name of your destination bucket.
### Step 5 - Add a Lambda trigger
* Set up a trigger to notify the lambda function on new object creation events in the source S3 bucket with `.txt` as 
  **suffix**.
* Go to the lambda function click on `Add trigger`, select the source as `S3` and select the **source bucket**. Under
  **Event types**, select `All object create events`.
* Add the suffix as `.txt`.
### Step 6 - Write a Lambda function code
* Write a Lambda function to process the text file.
* Go through the *Amazon Polly documentation* to know about different **VoiceIds**.
* Paste the code and deploy the code.
## Testing
 Create a text file. Add the text file to the source bucket. Once uploaded, the lambda function is triggered. Lambda will
read the text file, Processes the text with **Amazon Polly** to generate an audio stream and uploads the audio file to the
destination bucket.
 You can also check `cloudwatchLogs` under **Monitor** section of the Lambda function to analyze the event flow.
## ✅Conclusion
   This project successfully demonstrates a serverless application for converting text to speech using AWS services. The integration of S3 for file storage, Lambda for compute, and Polly for speech synthesis showcases the flexibility and power of AWS's cloud-native tools. The application is scalable, cost-effective, and adaptable for various real-world scenarios, such as e-learning, audiobook creation, and accessibility solutions.
