# ref https://stackoverflow.com/questions/55456337/consume-sqs-messages-from-celery

@app.task(name='listen_to_sqs_telemetry')
def listen_to_sqs_telemetry():
    s3  = boto3.client('s3')
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-2.amazonaws.com/xxx'

    keep_going = True
    num = 0
    while keep_going:
        keep_going = False
        try:
            response = sqs.receive_message(QueueUrl=queue_url, AttributeNames=['SentTimestamp',], MaxNumberOfMessages=5, MessageAttributeNames=['All'], WaitTimeSeconds=20)
            if 'Messages' in response:
                keep_going = True
                for rec in response['Messages']:

                # for msg in response.get("Messages", []):
                #     s3.download_file("yourBucket", msg["key"], "local/file/path")

                    # Process message
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=rec['ReceiptHandle'])
                    num = num + 1
            else:
                pass
                # logger.info(response)
        except Exception as e:
            logger.error(str(e))
    logger.info('done with listen_to_sqs_telemetry')
    return "Processed {} message(s)".format(num)
