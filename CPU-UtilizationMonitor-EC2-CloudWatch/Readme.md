# Monitoring CPU Utilization of EC2 using CloudWatch
## Project Overview
This project involves setting up a CloudWatch alarm to monitor the CPU utilization of an EC2 instance on AWS. The alarm is configured to trigger when the CPU utilization exceeds a specific threshold. To simulate high CPU usage, a stress application is installed on the instance.
## Architecture
1. EC2 Instance: A compute instance where application(s) run and are monitored.
2. CloudWatch: AWS service to monitor metrics and set alarms.
3. CloudWatch Alarm: Configured to alert when CPU utilization exceeds a predefined threshold.
4. EC2 nstance Connect: Used to access the EC2 instance and apply the stress test.
## Step 1 - Launch an EC2 instance
* Go to EC2 dashboard in AWS Console
* Click `Launch instance`. Select `Amazon Linux 2023` AMI.
* Select the instance type as `t2.micro`. Create a `Key pair` if you want to connect to the EC2 instance using SSH via local terminal. If you are using `EC2 instance` connect, you don't need to create a Key pair.
* For EC2 Instance Connect to work, the security group associated with the instance must allow inbound SSH (TCP) traffic on port 22 from your IP address or a range of IPs. Without this rule, you won’t be able to access the instance, as the security group acts as a firewall controlling network access.
  Under `Network settings` select `Create security group`. Add an `Inbound rule`.
  `Type:SSH`, `Protocol: TCP`, `Port Range: 22`, `Source: Your IP (or a specific range if needed)`
* Under `Advanced details` enable `Detailed CloudWatch monitoring`(required for more granular data).
* Leave all other settings as default and click on `Launch instance`.
## Step 2 - Configure a CloudWatch Alarm
* Go to CloudWatch dashboard in the AWS console.
* Navigate to `Alarms` and click `Create Alarm` then click `Select metric`.
* Select the metric as `EC2`. Then select `Per instance metric`. In the search bar enter the instanceID that you launched before and select the instance ID with the metric name `CPUUtilization`. ('CPUUtilization` comes under 'Namespaces' of Cloudwatch Alarm)
* Under `Specify metric and conditions` select `statistic` as `Average` and `Period` as 5 minutes.
* Under conditions, select `Threshold type` as `Static` which lets you use a value as a threshold. Define the alarm condition
  to trigger the alarm when CPUUtilization is `Greater/Equal>= 15%`.
* You can also configure the alarm to take actions(Such as sending notifications) when the alarm is triggerd to notify the user about exceeded CPUUtilization.
* After setting up everythin, click `Next` and create the Alarm.

 The instance CPU utilization data will take sometime to get transferred to cloudwatch, in this situation it shows the `state` as `Insufficient data`. 
 Once the instance CPU utilization data is transferred to CW, it shows the `state` as `OK`.

## Step 3 - Connect to the EC2 instance using 'instance connect'
* In the EC2 dashboard, select the instance.
* Right click on the instance, click `connect` and select `Instance connect` and access the terminal.

## Step 4 - Install and run a stress application on the EC2 instance
* Let's increase the CPU utilization by installing a stress application to stimulate high CPU usage.
1. Update the package on the Ec2 instance to install all the dependencies we want
  ```
  sudo yum update -y  # For Amazon Linux
  ```
2. Install `stress` application (For testing CPU Utilization)
  ```
  sudo yum install stress -y
  ```
3. Run the stress test to increase CPU utilization
  ```
   stress --cpu 1 --timeout 60
  ```
   `--cpu 1` starts one CPU workers, stimulating load on one CPU cores.
   `--timeout 60` sets the duration for which the stress test runs.(In this case, 60 seconds)
This allows you to simulate CPU load for a specific period without manually stopping it. You can adjust this value to increase or decrease the duration of the stress test.

## Results and Monitoring
* Go to cloudwatch console, click on `Dashboard` to view real-time metrics for CPU utilization.
* Monitor the Alarm state (OK, ALARM) to confirm if the alarm triggers when CPU utilization exceeds the defined threshold.
  Since you have set the threshold value as 15%, alarm's state changes to `InAlarm` state if the CPU utilization is more than 15%.

