# Monitoring Memory utilization of EC2 using cloudwatch
## Objective of this project
This project demonstrates how to monitor the `memory utilization` of an Amazon EC2 instance using Amazon CloudWatch. By default, CloudWatch monitors metrics like CPU usage, disk I/O, and network, but it does not monitor memory usage. This project shows how to set up the `CloudWatch` agent to send custom memory utilization metrics from an EC2 instance to CloudWatch.
   The CloudWatch agent extends the built-in monitoring capabilities of CloudWatch, allowing you to collect additional system-level metrics such as:
   * Memory Utilization
   * Disk space usage
   * Disk Swap usage
   This enhanced monitoring is essential for gaining deeper insight into instance performance, helping to optimize resource usage and troubleshoot performance issues efficiently.

## Steps to implement this project
**Step 1 - Create an IAM role and attach `CloudWatchFullAccess` and `AmazonSSMFullAccess`**
* Go to IAM->`Create Role`-> select `Trusted entity type` as `AWS service` and `Use case` as `EC2`.
* Attach `CloudWatchFullAccess` and `AmazonSSMFullAccess` permission policy to the role. We need to attach
  `CloudWatchFullAccess` inorder to allow EC2 instance to send the memory utilization data to cloudwatch. We need to attach
  `AmazonSSMFullAccess` because, we are going to store a parameter(JSON file) in `AWS systems manager parameter store`.
  The parameter specifies cloudwatch agent the metrics to collect and the frequency of data reporting. The CloudWatch agent
  installed on the instance will fetch the JSON configuration file from the parameter store. This set-up allows CW agent to
  dynamically obtain apply the desired configuration, enabling seamless updates and centralized control over metric collection.

**Step 2 - Create a parameter in Systems manager parameter store**
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


