# Static Website Hosting on AWS S3 with CI/CD using GitHub Actions
## Description
#### This project demonstrates how to host a static website on AWS S3, using a custom domain registered in AWS Route 53. The website files are managed in a GitHub repository, and GitHub Actions are configured to provide CI/CD, syncing changes to S3 automatically when updates are made to the code.
## Project Architecture
![Diagram explaining the architecture of this project](image.png)
## Stage 1 - Create the S3 Bucket
#### Create a S3 bucket to store the static website files. The name of the S3 bucket should be same as the custom domain name.
* disable 'block all public access' inorder to allow public access to the buckeet.
* select 'ACLs enabled' option. Since the website files will be owned by github repository and not by S3, we need to enable ACL(Access control list) inorder to allow github repository to access the S3 bucket and its objects. Create the bucket after configuring these settings.
* Go to 'properties' in the S3 tab and enable 'Static website hosting'. Specify the name of the html file as index.html
## Stage 2 - Setting up a Github repository
* create github repository to store the website files. Upload the files in a specific folder called 'Website'
* create a github workflow directory and add a workflow file to run a job which deploys the website files to S3 bucket. It also triggers the workflow file whenever there's change in code. This how CI/CD in github action works.
The workflow file is a Yaml file which uses 'S3-sync-action'. This action is readily available on github marketplace.
The code requires parameters like **AWS_S3_BUCKET** which will be the name of the S3 bucket where the website files are going to get deployed. **AWS_ACCESS_KEY_ID** & **AWS_SECRET_ACCESS_KEY** parameters are basically provided by IAM inorder for the github to access S3 bucket.
      IAM:
   * Create an **'IAM user'** for github action and attach a **'AmazonS3FullAccess'** permissions policy.
   * Under 'Security credentials' create an Access key and Secret access key.



