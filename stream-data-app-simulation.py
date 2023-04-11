import boto3
import csv
import json
from time import sleep
from datetime import datetime

# AWS Settings
s3 = boto3.client('s3', region_name='eu-west-1')
s3_resource = boto3.resource('s3', region_name='eu-west-1')
kinesis_client = boto3.client('kinesis', region_name='eu-west-1')

# Env. variables; i.e. can be OS variables in Lambda
kinesis_stream_name = 'ecommerce-raw-user-activity-stream-1'
streaming_partition_key = 'category_id'


# Function can be converted to Lambda;
#   i.e. by iterating the S3-put events records; e.g. record['s3']['bucket']['name']
def stream_data_simulator(input_s3_bucket, input_s3_key):
    s3_bucket = input_s3_bucket
    s3_key = input_s3_key

    # Read CSV Lines and split the file into lines
    csv_file = s3_resource.Object(s3_bucket, s3_key)
    s3_response = csv_file.get()
    lines = s3_response['Body'].read().decode('utf-8').split('\n')

    for row in csv.DictReader(lines):
        try:
            # Convert to JSON, to make it easier to work in Kinesis Analytics
            line_json = json.dumps(row)
            json_load = json.loads(line_json)

            # Adding fake txn ts:
            json_load['txn_timestamp'] = datetime.now().isoformat()
            # print(json_load)

            # Write to Kinesis Streams:
            response = kinesis_client.put_record(StreamName=kinesis_stream_name, Data=json.dumps(json_load, indent=4),
                                                 PartitionKey=str(json_load[streaming_partition_key]))
            # response['category_code'] = json_load['category_code']
            print('HttpStatusCode:', response['ResponseMetadata']['HTTPStatusCode'], ', ', json_load['category_code'])

            # Adding a temporary pause, for demo-purposes:
            sleep(0.250)

        except Exception as e:
            print('Error: {}'.format(e))


# Run stream:
for i in range(0, 5):
    stream_data_simulator(input_s3_bucket="ecommerce-raw-euwest1-14317-dev",
                          input_s3_key="ecomm_user_activity_sample/2019-Nov-sample.csv")
