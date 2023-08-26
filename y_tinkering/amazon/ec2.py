import boto3
import json
import base64
from urllib.parse import unquote_plus


BUCKET_NAME = "YOUR_S3_BUCKET_NAME"
CONFIG_FILE_KEY = "config/ec2-launch-config.json"
USER_DATA_FILE_KEY = "config/user-data"
BUCKET_INPUT_DIR = "inputs"
BUCKET_OUTPUT_DIR = "outputs"


def launch_instance(EC2, config, user_data):
    tag_specs = [{}]
    tag_specs[0]['ResourceType'] = 'instance'
    tag_specs[0]['Tags'] = config['set_new_instance_tags']

    ec2_response = EC2.run_instances(
        ImageId=config['ami'],  # ami-0123b531fc646552f
        InstanceType=config['instance_type'],   # t2.nano
        KeyName=config['ssh_key_name'],  # ambar-default
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=config['security_group_ids'],  # sg-08b6b31110601e924
        TagSpecifications=tag_specs,
        # UserData=base64.b64encode(user_data).decode("ascii")
        UserData=user_data
    )

    new_instance_resp = ec2_response['Instances'][0]
    instance_id = new_instance_resp['InstanceId']
    # print(f"[DEBUG] Full ec2 instance response data for '{instance_id}': {new_instance_resp}")

    return (instance_id, new_instance_resp)



def lambda_handler(raw_event, context):
    print(f"Received raw event: {raw_event}")
    # event = raw_event['Records']

    for record in raw_event['Records']:
        bucket = record['s3']['bucket']['name']
        print(f"Triggering S3 Bucket: {bucket}")
        key = unquote_plus(record['s3']['object']['key'])
        print(f"Triggering key in S3: {key}")

        # get config from config file stored in S3
        S3 = boto3.client('s3')
        result = S3.get_object(Bucket=BUCKET_NAME, Key=CONFIG_FILE_KEY)
        ec2_config = json.loads(result["Body"].read().decode())
        print(f"Config from S3: {ec2_config}")

        ec2_filters = [
            {
                'Name': f"tag:{ec2_config['filter_tag_key']}",
                'Values':[ ec2_config['filter_tag_value'] ]
            }
        ]

        EC2 = boto3.client('ec2', region_name=ec2_config['region'])

        # launch new EC2 instance if necessary
        if bucket == BUCKET_NAME and key.startswith(f"{BUCKET_INPUT_DIR}/"):
            print("[INFO] Describing EC2 instances with target tags...")
            resp = EC2.describe_instances(Filters=ec2_filters)
            # print(f"[DEBUG] describe_instances response: {resp}")

            if resp["Reservations"] is not []:    # at least one instance with target tags was found
                for reservation in resp["Reservations"] :
                    for instance in reservation["Instances"]:
                        print(f"[INFO] Found '{instance['State']['Name']}' instance '{ instance['InstanceId'] }'"
                            f" having target tags: {instance['Tags']} ")

                        if instance['State']['Code'] == 16: # instance has target tags AND also is in running state
                            print(f"[INFO] instance '{ instance['InstanceId'] }' is already running: so not launching any more instances")
                            return {
                                "newInstanceLaunched": False,
                                "old-instanceId": instance['InstanceId'],
                                "new-instanceId": ""
                            }

            print("[INFO] Could not find even a single running instance matching the desired tag, launching a new one")

            # retrieve EC2 user-data for launch
            result = S3.get_object(Bucket=BUCKET_NAME, Key=USER_DATA_FILE_KEY)
            user_data = result["Body"].read()
            print(f"UserData from S3: {user_data}")

            result = launch_instance(EC2, ec2_config, user_data)
            print(f"[INFO] LAUNCHED EC2 instance-id '{result[0]}'")
            # print(f"[DEBUG] EC2 launch_resp:\n {result[1]}")
            return {
                "newInstanceLaunched": True,
                "old-instanceId": "",
                "new-instanceId": result[0]
            }

        # terminate all tagged EC2 instances
        if bucket == BUCKET_NAME and key.startswith(f"{BUCKET_OUTPUT_DIR}/"):
            print("[INFO] Describing EC2 instances with target tags...")
            resp = EC2.describe_instances(Filters=ec2_filters)
            # print(f"[DEBUG] describe_instances response: {resp}")
            terminated_instance_ids = []

            if resp["Reservations"] is not []:    # at least one instance with target tags was found
                for reservation in resp["Reservations"] :
                    for instance in reservation["Instances"]:
                        print(f"[INFO] Found '{instance['State']['Name']}' instance '{ instance['InstanceId'] }'"
                            f" having target tags: {instance['Tags']} ")

                        if instance['State']['Code'] == 16: # instance has target tags AND also is in running state
                            print(f"[INFO] instance '{ instance['InstanceId'] }' is running: terminating it")
                            terminated_instance_ids.append(instance['InstanceId'])
                            boto3.resource('ec2').Instance(instance['InstanceId']).terminate()

            return {
                "terminated-instance-ids:": terminated_instance_ids
            }
