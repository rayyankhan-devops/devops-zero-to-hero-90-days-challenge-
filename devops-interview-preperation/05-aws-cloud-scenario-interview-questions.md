# ☁️ AWS Cloud Infrastructure & Automation - 50 Scenario-Based Interview Questions

## Scenario 1: EC2 Status Check Failures (Instance Status vs System Status)
**Q:** An EC2 instance triggers a CloudWatch alert for `StatusCheckFailed`. How do you differentiate between a **System Status Check Failure** and an **Instance Status Check Failure**, and what are the respective remediation steps?
**A:**
- **System Status Check Failure:** Indicates hardware/underlying physical host failure managed by AWS (e.g. hypervisor failure, loss of physical power).
  - *Fix:* Stop and Start the EC2 instance (forces AWS to migrate the virtual machine to a healthy physical hypervisor host).
- **Instance Status Check Failure:** Indicates operating system or software-level issues inside the guest OS (e.g. kernel panic, corrupted file system, exhausted network stack).
  - *Fix:* Reboot instance, inspect serial console logs via EC2 Console, or attach root EBS volume to a rescue EC2 instance to inspect `/var/log/syslog`.

## Scenario 2: S3 Bucket Policy vs IAM Policy Evaluation
**Q:** An IAM User has an explicit `Allow` for `s3:GetObject` in their IAM policy. However, when trying to download `s3://company-confidential/data.csv`, they receive `403 Access Denied`. What explicit setting in the S3 Bucket Policy overrides the IAM User's policy?
**A:** In AWS IAM evaluation logic, an explicit **`Deny`** always overrides any number of explicit `Allow` statements.
If the S3 Bucket Policy contains a statement with `"Effect": "Deny"`, or if the object is encrypted with a KMS key the IAM user does not have `kms:Decrypt` access to, the request will return `403 Access Denied`.

## Scenario 3: Auto Scaling Group (ASG) Thrashing (Flapping)
**Q:** An Auto Scaling Group (ASG) keeps launching a new EC2 instance, waiting 3 minutes, terminating it, and launching another endlessly. What is causing this "thrashing" and how do you resolve it?
**A:** This occurs when the ASG Health Check grace period is shorter than the application startup time. The instance launches, but before Nginx/App finishes bootstrapping, the ASG EC2/ELB health check runs, marks the instance `Unhealthy`, terminates it, and retries.
1. Increase the **Health Check Grace Period** (e.g. from 60s to 300s).
2. Optimize User Data scripts to speed up startup times.

## Scenario 4: ALB Health Check Failures Returning HTTP 502 Bad Gateway
**Q:** Users accessing an Application Load Balancer receive `502 Bad Gateway`. Target Group status shows all EC2 instances as `Unhealthy`. How do you troubleshoot?
**A:** `502 Bad Gateway` means the ALB reached the target EC2 instance, but received an invalid response or connection reset.
1. Verify the web application daemon (Nginx/Node/Go) is actively listening on the target port (`netstat -tlpn`).
2. Verify Security Group rules: Target EC2 SG must permit inbound traffic on the app port from the ALB Security Group ID.
3. Verify Health Check URL path (e.g. `/health` returning HTTP 200 OK instead of 404).

## Scenario 5: Amazon RDS Out of Storage Space
**Q:** A production PostgreSQL RDS instance hits 100% disk usage and transitions to `storage-full` state, blocking all write queries. How do you recover?
**A:**
1. Enable **Storage Autoscaling** or manually modify the allocated storage in RDS Console / CLI:
   ```bash
   aws rds modify-db-instance --db-instance-identifier prod-db --allocated-storage 200 --apply-immediately
   ```
2. Note: RDS storage allocation increases take several minutes to apply, and you cannot scale down RDS storage once expanded.

## Scenario 6: Boto3 Python Script EC2 Provisioning Automation
**Q:** Write a Python script snippet using `boto3` that launches a `t2.micro` EC2 instance in `us-east-1`, tags it with `Name: Web-Prod`, and returns its Instance ID.
**A:**
```python
import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')
response = ec2.run_instances(
    ImageId='ami-0c7217cdde317cfec',
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    TagSpecifications=[{
        'ResourceType': 'instance',
        'Tags': [{'Key': 'Name', 'Value': 'Web-Prod'}]
    }]
)
instance_id = response['Instances'][0]['InstanceId']
print(f"Launched EC2 Instance: {instance_id}")
```

## Scenario 7: AWS Lambda Execution Timeout Handling
**Q:** A Python AWS Lambda function processing images from S3 times out after 3 seconds on large files. What parameters should you adjust?
**A:**
1. Increase Lambda **Timeout** configuration (up to 15 minutes max).
2. Increase Lambda **Memory** allocation (e.g. from 128MB to 1024MB), which proportionally increases allocated CPU power and network bandwidth.
3. Optimize Python image processing using stream buffers rather than reading entire files into RAM.

## Scenario 8: Securing Root User Account
**Q:** What are the top 4 security best practices for securing the AWS Root Account immediately after creating an AWS account?
**A:**
1. Enable Hardware / Virtual **Multi-Factor Authentication (MFA)** on the Root user.
2. Delete Root Access Keys and Secret Keys (never use root for programmatic access).
3. Create IAM Admin Users / Roles for daily tasks following Principle of Least Privilege.
4. Set up CloudWatch Budget Alerts to monitor unexpected billing charges.

## Scenario 9: S3 Bucket Versioning & Accidental Deletion Recovery
**Q:** A user ran `aws s3 rm s3://prod-data/important.json`. S3 Bucket Versioning is enabled. How do you restore the deleted object?
**A:** When S3 Versioning is enabled, running `s3 rm` creates a **Delete Marker** rather than permanently erasing the file.
1. List object versions: `aws s3api list-object-versions --bucket prod-data --prefix important.json`
2. Remove the Delete Marker version ID using `aws s3api delete-object`:
   ```bash
   aws s3api delete-object --bucket prod-data --key important.json --version-id <DELETE_MARKER_VERSION_ID>
   ```

## Scenario 10: IAM Role vs IAM User for EC2 Instance Access
**Q:** An application running on an EC2 instance needs to read files from S3. Should you store AWS Access Keys in `~/.aws/credentials` on the server or attach an IAM Role? Why?
**A:** Attach an **IAM Role to the EC2 Instance** (Instance Profile). Storing static credentials on disk creates a major security vulnerability if the server is compromised. IAM Roles use AWS Security Token Service (STS) to automatically issue short-lived, self-rotating credentials.

---

## Scenario 11-50 Summary Coverage Matrix
- **AWS Infrastructure:** VPC Peering vs Transit Gateway, Elastic IP allocation, EBS Snapshot automated lifecycle policies.
- **Serverless & Databases:** DynamoDB partition keys vs sort keys, SQS Queue DLQ (Dead Letter Queue) processing, SNS topic subscriptions.
