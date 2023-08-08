# REFERENCE: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs-example-long-polling.html
import boto3
sqs = boto3.client('sqs')
# Create a SQS queue with long polling enabled
response = sqs.create_queue(QueueName='SQS_QUEUE_NAME', Attributes={'ReceiveMessageWaitTimeSeconds': '20'})
print(response['QueueUrl'])


# Example 2
sqs = boto3.client('sqs')
queue_url = 'SQS_QUEUE_URL'
# Enable long polling on an existing SQS queue
sqs.set_queue_attributes(QueueUrl=queue_url, Attributes={'ReceiveMessageWaitTimeSeconds': '20'})


# Example 3
sqs = boto3.client('sqs')
queue_url = 'SQS_QUEUE_URL'
# Long poll for message on provided SQS queue
response = sqs.receive_message(QueueUrl=queue_url, AttributeNames=['SentTimestamp'], MaxNumberOfMessages=1, MessageAttributeNames=['All'], WaitTimeSeconds=20)
print(response)


# Example 4
sqs = boto3.client('sqs')
# List SQS queues
response = sqs.list_queues()
print(response['QueueUrls'])






#
