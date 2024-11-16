# Notify Subscribers about missing EC2 tags
## 📌Project Overview
The purpose of this project is to ensure that all EC2 instances in your AWS environment have the necessary tags, specifically the `Environment` tag. Proper tagging of resources is crucial for effective cost management, resource organization, and compliance. This solution automatically checks all running EC2 instances and sends an email notification to subscribed users if any instance is missing the required tag.
### Why is tagging important?
* **Cost Allocation**: Helps in identifying and managing costs associated with specific projects or environments.
* **Resource Organization**: Makes it easier to filter and manage resources in a large-scale environment.
* **Automation and Compliance**: Ensures that instances adhere to tagging policies, enabling automation and compliance checks.
## Architecture
![Diagram explaining the architecture of this project](Images/Architecture-diagram.png)
### Services used"
1. **Amazon EC2** - Compute service where instances are monitored for missing tags.
2. **Amazon EventBridge(CW Events)** - Triggers the Lambda function on a schedule to check for missing tags.
3. **AWS Lambda** - Executes a Python script to verify the presence of the `Environment` tag on EC2 instances.
4. **Amazon SNS (Simple Notification Service)** - Sends email notifications to subscribers about missing tags.
5. **Email Subscription** - Receives alerts from SNS notifications.
## Steps in building the project
### **Step 1 - Create an SNS Topic for Email Notifications**
* Go to AWS console->SNS->Topics->Click on 
