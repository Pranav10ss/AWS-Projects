# Monitoring Memory utilization of EC2 using cloudwatch
## Objective of this project
This project demonstrates how to monitor the `memory utilization` of an Amazon EC2 instance using Amazon CloudWatch. By default, CloudWatch monitors metrics like CPU usage, disk I/O, and network, but it does not monitor memory usage. This project shows how to set up the `CloudWatch agent` to send custom memory utilization metrics from an EC2 instance to CloudWatch.
   The CloudWatch agent extends the built-in monitoring capabilities of CloudWatch, allowing you to collect additional system-level metrics such as:
   * Memory Utilization
   * Disk space usage
   * Disk Swap usage

This enhanced monitoring is essential for gaining deeper insight into instance performance, helping to optimize resource usage and troubleshoot performance issues efficiently.

## Steps to implement this project
## **Step 1 - Create an IAM role and attach `CloudWatchFullAccess` and `AmazonSSMFullAccess`**
* Go to IAM->`Create Role`-> select `Trusted entity type` as `AWS service` and `Use case` as `EC2`.
* Attach `CloudWatchFullAccess` and `AmazonSSMFullAccess` permission policy to the role. We need to attach
`CloudWatchFullAccess` in order to allow EC2 instance to send the memory utilization data to cloudwatch. We need to attach
`AmazonSSMFullAccess` because, we are going to store a parameter(JSON file) in `AWS systems manager parameter store`.
The parameter specifies cloudwatch agent the metrics to collect and the frequency of data reporting. The CloudWatch agent
installed on the instance will fetch the JSON configuration file from the parameter store. This set-up allows CW agent to
dynamically obtain apply the desired configuration, enabling seamless updates and centralized control over metric collection.

## **Step 2 - Create a parameter in Systems manager parameter store**
* Go to `Systems Manager`-> `Application Management` -> `Parameter Store`-> `Create Parameter`. Specify the 'Name' of the
  parameter as `/alarm/AWS-CWAgentConfig`, select 'Tier' as `Standard`, 'Type' as `String`, 'Data Type' as `text` and under
  'Value' copy the following JSON code. After Everything click on `Create parameter`.
  ```JSON
  {
	"metrics": {
		"append_dimensions": {
			"InstanceId": "${aws:InstanceId}"
		},
		"metrics_collected": {
			"mem": {
				"measurement": [
					"mem_used_percent"
				],
				"metrics_collection_interval": 60
			}
		}
	}
  }
  ```
## **Step 3 - Create an EC2 instance and install a CloudWatch agent on the instance by adding the userdata**
* Go to EC2 console-> `Launch instance`-> Under `Advanced details`-> `IAM instance profile` attach the IAM role that you
  created.
* Under `Userdata` paste the following command to install the `CloudWatch` agent on the EC2 instance. This script sets up the Amazon CloudWatch Agent on the EC2 instance, retrieves a pre-defined configuration from the SSM
  Parameter Store, and starts the agent. This allows the instance to send custom metrics, such as memory utilization and other system-level data, to Amazon CloudWatch.
  ```
  #!/bin/bash
   wget https://s3.amazonaws.com/amazoncloudwatch-agent/linux/amd64/latest/AmazonCloudWatchAgent.zip
   unzip AmazonCloudWatchAgent.zip
   sudo ./install.sh
   sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c ssm:/alarm/AWS-CWAgentConfig -s
  ```
* Once the instance is in `Running` state and the `2/2 checks passed` status check is met, connect to the instance using 
  `EC2 instance connect`. Once connected you can check whether the CW agent is installed or not. Use the following command 
  to check the same:
  ```
  sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a status
  ```
* If the `status` is in `running state` then the CloudWatch Agent is successfully installed on the EC2 instance. 
## **Step 4 - Verify Metrics in CloudWatch**
* Go to Cloudwatch dashboard and navigate to `metrics`->`All metrics`, there you can see a metric called `CWAgent`. This
    can only be seen after installing the cloud watch agent on the EC2 instance.
* Click on `CWAgent`-> `InstanceId`->Now it will show you all the instances with CloudWatch agent installed. Search for the
    specific instance using the isntance's id.
* Once you click on the instance id, you can check the memory utilization of the EC2 instance in percentage. Based on this
    you can create alarms.
* Go to alarms-> Create alarm-> Select metric-> select the metric as `CWAgent`-> `Instance id`-> Select the instance with
    the cloudwatch agent installed for which you would like to check the memory utilization. Under `Specify metrics and
    conditions`->Set the 'statistic' as `average` and 'Period' as `5 minutes`.
    Set the 'Threshold type' as `Static`, define the desired 'alarm condition'(ex; Greater/equal>= threshold)
* Then define the `threshold value` in %. If the memory utilization is exceeding the `threshold value` you can configure
    actions to send notifications to specified userd when the alarm triggers.
    
## Conclusion
  Monitoring memory utilization using the CloudWatch agent helps you capture vital performance data not available by
  default, providing comprehensive insights for optimizing and managing EC2 instances effectively.

