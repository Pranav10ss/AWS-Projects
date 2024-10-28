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



