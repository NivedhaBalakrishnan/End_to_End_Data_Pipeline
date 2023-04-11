# Fabricating-Batch-and-Stream-Data-Pipelines

## Problem Statement

Our eCommerce company has received requests from the marketing team and Datascience team to build a real-time data pipeline that can analyze the shopping journey and behavior of users as well as detect any anomalies or intrusions on the website.

-Marketing team wants to analyze user shopping journey in real-time.
-Data Science team wants to detect anomalies on the website in real-time.
-The pipeline must involve ingesting, processing, and visualizing data simultaneously & must be capable of detecting anomalies or intrusions on website.
-The pipeline will be deployed to a production environment where Regular monitoring and maintenance are required.

## Goals

- We will be analyzing the realtime stream data for making realtime decisions
- Detecting the intusions on the website and sending an alarm or Notifications
## Business Overview :
Ecommerce analytics is the process which involves gathering data from various sources to analyze customer behavior and shopping patterns across the entire customer journey. In this project, an eCommerce dataset will be used to create two analytical pipelines using various Amazon services to draw insights such as 

- unique visitors per day 
- identifying when users add products to carts but don't buy 
- top categories per hour/weekday for promotions, and identifying brands that need more marketing. 

On the other hand, the Real-time channel focuses on detecting Distributed Denial of Service (DDoS) and Bot attacks using AWS Lambda, DynamoDB, CloudWatch, and AWS SNS.
     
## Dataset Description :

This dataset contains user behavioral information from a large multi-category online store along with fields such as event_time, event_type, product_id, price, user_id. Each row in the file represents one of the following event types such as View,Cart,Removed from Cart,Purchase. the data is extracted from the following link https://rees46.com/en/open-cdp

## Tech Stack:
#### Languages : 
     Python
     SQL
#### AWS Services :
     AWS S3
     AWS Glue
     AWS Athena
     AWS Cloud9
     Apache Flink
     Amazon Kinesis
     Amazon SNS
     AWS Lambda
     Amazon CloudWatch
     QuickSight
     Apache Zepplin
     Amazon DynamoDB
     
## System Architecture 

Below is the lucid chart diagram of system architecture. after we downloaded the data in CSV format, we have stored this data in s3 bucket which is a data lake service. 

later we lauched a cloud 9 in EC2 instance to run boto3 to connect python simulator to AWS services.

Now we had to create a Kinesis streams which could handle our continous streaming data, this will be our stream 1.

the python simulator is created in such a way it connects to s3 bucket to pull the static data which is in CSV and simulates it into a continous stream with partitions based on Category Id, here we will shard the data in Kinesis streams with category id.

The glue service is used now to crawl the data from Stream 1


  
![image](https://user-images.githubusercontent.com/83365184/222992271-4c3f3f06-fb32-4664-9968-b52d5ba93a34.png)

## Implementation

## S3 

The data which is in CSV format is moved to Amazon Simple Storage Service Bucket, since most of the this project is associated with aws services, also it is a cheap cloud storage provider.

Amazon S3 (Simple Storage Service) is a cloud-based object storage service provided by Amazon Web Services (AWS). S3 enables users to store and retrieve any amount of data, at any time, from anywhere on the web. It provides a highly scalable, reliable, and cost-effective storage infrastructure that can be used for a wide range of use cases, such as backup and restore, disaster recovery, archiving, data lakes, and big data analytics.

S3 stores objects (files) in buckets, which are containers for objects that can be accessed using a unique URL. S3 supports multiple storage classes, including Standard, Standard-Infrequent Access (IA), One Zone-Infrequent Access (One Zone-IA), Intelligent Tiering, Glacier, and Glacier Deep Archive. Each storage class has different features, performance characteristics, and costs, allowing users to choose the appropriate storage class for their specific use case and data access requirements.

![image](https://user-images.githubusercontent.com/83365184/222992656-74222c6d-496b-4e43-8fc7-2114bde0bbee.png)

## Cloud9 

To run our python script which has been created to mimic the real time data, we will be using cloud9.

Cloud9 is an integrated development environment (IDE) that allows developers to write, run, and debug code in the cloud. It is a web-based platform that is fully managed by AWS and provides a range of features, such as code editing, debugging, collaboration, and more.

To use Cloud9 in AWS, you will need an AWS account. Once you have an AWS account, you can create a Cloud9 environment by following these steps:

Go to the AWS Management Console and select the Cloud9 service.
Click on the "Create environment" button.
Give your environment a name and select the type of environment you want to create (for example, a Python in our case).
Choose the settings for your environment, such as the instance type, network settings, and permissions.
Click on the "Create environment" button to create your environment.
Once your environment is created, you can start writing and running code in the cloud using the Cloud9 IDE. You can also collaborate with other developers by sharing your environment with them.

Cloud9 in AWS provides a powerful and flexible development environment that can help you streamline your development workflows and accelerate your development process

![image](https://user-images.githubusercontent.com/83365184/222992678-2b29bb90-2c90-4578-92f2-6d0da154ee0f.png)

## Boto3

Boto3 needs to be installed in cloud9 to connect our python script to aws services.

Boto3 is a Python software development kit (SDK) for AWS (Amazon Web Services) that enables developers to create Python scripts or applications to interact with AWS services. Boto3 provides an easy-to-use, Pythonic interface to AWS services, making it simple to integrate AWS into your Python applications.

Using Boto3, developers can create, configure, and manage AWS resources like EC2 instances, S3 buckets, RDS instances, and more programmatically. Boto3 provides Pythonic methods for interacting with AWS resources, making it easy to integrate AWS services with Python applications.

Boto3 also supports automatic credential management, allowing you to authenticate and authorize access to AWS services using AWS Identity and Access Management (IAM) roles, profiles, or environment variables.

With Boto3, developers can easily build serverless applications using AWS Lambda functions, which can be triggered by events from various AWS services like S3, Kinesis, DynamoDB, and more. Boto3 also supports AWS Step Functions, enabling developers to create and manage state machines that coordinate AWS services.

## Kinesis 

we need to create a stream which could collect the data from our CSV file which is in S3 and shard the data based on category id and replicate it into different zones for zero tolerance.

A Kinesis stream is a managed service provided by AWS that allows you to collect and process large streams of data records in real time. The stream is made up of shards, and the partition key determines which shard a data record belongs to. In your case, it seems that the partition key is set to the category_id field, meaning that records with the same category_id will be sent to the same shard for processing.

It's worth noting that when designing a Kinesis stream, it's important to choose an appropriate partition key that evenly distributes data records across shards to ensure optimal performance and scalability. Additionally, you'll need to configure one or more consumers to read data from the stream and process it in real time.

!![image](https://user-images.githubusercontent.com/83365184/226069598-07c0d01c-37d6-495c-a876-be4236271afd.png)


## Python Script

### Importing Libraries

In this step we are importing essential libraries which are required.

![image](https://user-images.githubusercontent.com/83365184/226068960-6ff395dc-e416-4bcb-817e-2f3f420128f0.png)

### creating AWS settings

1. The first line creates an S3 client object by calling the boto3.client() function with 's3' as the service name and 'us-west-1' as the region name. This client object provides an interface to interact with S3 service in the US West 1 region, such as uploading or downloading files to/from S3 buckets, creating and deleting S3 buckets, and more..
2. The second line creates an S3 resource object by calling the boto3.resource() function with 's3' as the service name and 'us-west-1' as the region name. This resource object provides a higher-level interface to interact with S3 service in the US West 1 region, such as creating S3 buckets, listing objects in S3 buckets, copying objects from one bucket to another, and more.
3. The third line creates a Kinesis client object by calling the boto3.client() function with 'kinesis' as the service name and 'us-west-1' as the region name. This client object provides an interface to interact with Kinesis service in the US West 1 region, such as creating and managing Kinesis streams, putting and getting records from Kinesis streams, and more.

![image](https://user-images.githubusercontent.com/83365184/226069049-ea77f808-4984-47ae-9c49-c3c2cc79c725.png)

### Environmnent Variables 

we have defined a Kinesis stream with the name ecommerce-raw-user-activity-stream-1 and a streaming partition key of category_id

![image](https://user-images.githubusercontent.com/83365184/226070678-43becc06-365b-4952-93e3-25faa6572bd1.png)

### Creating a function to split file to n number of JSON files 

This Python code defines a function called stream_data_simulator that reads a CSV file from an Amazon S3 bucket, converts each row to a JSON object, adds a fake timestamp, writes the JSON object to an Amazon Kinesis stream, and prints some information about the process. The function takes two arguments: input_s3_bucket, which is the name of the S3 bucket containing the CSV file, and input_s3_key, which is the key for the CSV file within the S3 bucket.

The function first reads the CSV file using the S3 resource s3_resource and csv_file.get(), which returns a response object. It then decodes the response body using utf-8 encoding and splits the resulting string into individual lines using the split method.

For each line in the CSV file, the function uses json.dumps and json.loads to convert the row to a JSON object. It then adds a fake timestamp to the JSON object using datetime.now().isoformat(). The function then writes the JSON object to a Kinesis stream using kinesis_client.put_record, which takes three arguments: StreamName, which is the name of the Kinesis stream to write to, Data, which is the JSON object to write, and PartitionKey, which is a string used to determine which shard the data is written to. The function also prints the HTTP status code and the category_code field from the JSON object.

Finally, the function adds a pause of 250 milliseconds using sleep(0.250) to simulate a slow data stream for demonstration purposes.



![image](https://user-images.githubusercontent.com/83365184/226071262-2cc1c31c-580d-465f-af15-6db667bf2bdc.png)


### Kinesis Stream 1

Now the data is consumed by the kinesis stream 1 and partioned based on category id, this is considered as a raw data and we can use Glue crawler.The crawler can then use this metadata to create a data catalog, which can be used to keep track of the data and make it available for analysis.

! 












   
                                      

