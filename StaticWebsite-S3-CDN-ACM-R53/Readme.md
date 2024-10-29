# Static Website with Amazon S3, CloudFront, ACM SSL, and Route 53
## Introduction
In this project we are going to host a static website using amazon S3. S3 serves as the origin for the website's static files. 
Amazon CloudFront is used for CDN (Content Delivery Network) to enhance website performance by reducing latency and ensure secure HTTPS delivery.AWS Certificate Manager (ACM) issues an SSL certificate for HTTPS access. Route 53 manages the custom domain.
## Architecture
![Diagram explaining the architecture of this project](Images/Architecture-diagram.png)
* When an user tries to access a domain(ex:www.pranavswaroop.com), the domain hosted on route53 which has an `Alias record` configured for your domain that points to the cloudFront distribution. 
* CloudFront first checks if the requested content is available in its `cache` at an `edge location` near the user. If the content is cached, CF serves the files immediately, reducing latency and improving load times.
* Cloudfront uses SSL certificate issued by `AWS certificate manager(ACM)` to establish a secure HTTP connection ensuring that the data b/w the user and CF is encrypted.
* If the requested file isn't in the CF cache, CF forwards the request to `origin(S3 bucket)` where the website's static files are stored. S3 serves the file back to CloudFront. This initial fetch happens only if CloudFront’s cache doesn’t already contain the requested content.
* Once the file is fetched from S3, CloudFront caches it at the edge location that handled the request. This cached content will serve future requests from users in the same or nearby locations without needing to retrieve it from S3 again, optimizing performance.
* The requested file will be sent from CF to user's browser over HTTPS. 
