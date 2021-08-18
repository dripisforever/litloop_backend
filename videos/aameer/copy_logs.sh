#!/bin/bash
source ./aws_credentials.sh
# help text displayed at various times to guide user how to invoke the bash script
helptext="$(basename "$0") [-h] [-f p v] -- program to get burned in watermark hls videos with master list with ffmpeg logs
e.g mutliple word argument processor:
time bash copy_logs.sh --projectid=3631 --mothervideoid="3799" --videoid="3798" -server="your_bucket_name"
e.g with log files:
(time bash copy_logs.sh -p="3631" -m="3799" -v="3800" -s="your_bucket_name") 2>> encoding_logs.log
where:
    -h  show this help text
    -p  project id
    -s  server
    -m  mother video id
    -v  video id"

#for parsing command line arguments

#Display message incase no arguments are supplied
if [[ $# -eq 0 ]] ; then
    echo "please provide necessary arguments check help text for guidance:" >> encoding_logs.log
    echo $helptext >> encoding_logs.log
    exit 0
fi


for i in "$@"
do
case $i in
    -p=*|--projectid=*)
    INPUT_PROJECT_ID="${i#*=}"
    shift # past argument=value
    ;;
    -v=*|--videoid=*)
    INPUT_VIDEO_ID="${i#*=}"
    shift # past argument=value
    ;;
    -m=*|--mothervideoid=*)
    INPUT_MOTHER_VIDEO="${i#*=}"
    shift # past argument=value
    ;;
    -s=*|--server=*)
    SERVER="${i#*=}"
    shift # past argument=value
    ;;
    --default)
    DEFAULT=YES
    shift # past argument with no value
    ;;
    *)
    echo 'please provide correct arguments check help text for guidance:'
    echo $helptext
    exit 0
    ;;
esac
done

#print the argumnets read
echo "INPUT PROJECT ID  = ${INPUT_PROJECT_ID}"
echo "INPUT VIDEO ID   = ${INPUT_VIDEO_ID}"
echo "INPUT MOTHER VIDEO ID   = ${INPUT_MOTHER_VIDEO}"
echo "SERVER NAME   = ${SERVER}"

#setting the values for script as per input values
export PROJECT_ID=${INPUT_PROJECT_ID}
export VIDEO_ID=${INPUT_VIDEO_ID}
export SERVER_NAME=${SERVER}
export MOTHER_VIDEO_ID=${INPUT_MOTHER_VIDEO}

echo $AWS_ACCESS_KEY_ID
#this is the place where from you copy the original video which will be transcoded you can alter it as per your need
aws s3 cp  encoding_logs.log s3://$SERVER_NAME/$PROJECT_ID/video/$MOTHER_VIDEO_ID/$VIDEO_ID/

#stop instance
export AWS_DEFAULT_REGION='us-east-1e'
export InstanceId=`curl http://169.254.169.254/latest/meta-data/instance-id;echo`
aws ec2 stop-instances --instance-ids ${InstanceId} --region us-east-1
