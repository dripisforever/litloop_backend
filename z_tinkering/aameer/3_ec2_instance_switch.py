import boto
import time
import json
import simplejson
import datetime
from boto.s3.connection import S3Connection
from django.conf import settings

# AWS credentials
aws_key = settings.AWS_ACCESS_KEY_ID
aws_secret = settings.AWS_SECRET_ACCESS_KEY


def get_conection():
    conn = boto.connect_ec2(aws_key, aws_secret)
    return conn


def get_watermark_position(video):
    #based on the parent video watermark position choose one from below
    #1.Bottom left
    #2.Bottom center
    #3.Bottom right
    #4.Middle left
    #5.Middle center
    #6.Middle right
    #7.Top left
    #8.Top center
    #9.Top right
    # you can get it for other positions too
    if video.watermark_pos == 'top':
        burned_position = '8'
    elif video.watermark_pos == 'middle':
        burned_position = '5'
    elif video.watermark_pos == 'bottom':
        burned_position = '2'
    else:
        print("This value of watermark position not known, using default")
        burned_position = '2'
    return burned_position


def get_video_duration(video):
    #add the watermark and send the time for both the full length burned watermark  and also add the position for the visible watermark
    try:
        # you must have video duration in milliseconds
        video_duration_in_ms=56000
        miliseconds = int(video_duration_in_ms)
        hours, milliseconds = divmod(miliseconds, 3600000)
        minutes, milliseconds = divmod(miliseconds, 60000)
        seconds = float(milliseconds) / 1000
        burnedin_end_time = "%i:%02i:%06.3f" % (hours, minutes, seconds)
        #'0:00:52.254'
        return burnedin_end_time
    except Exception as durexecp:
        print(durexecp)


def get_video_details(video):
    try:
        #get base file
        #some_s3_link/test_file.mo4
        original_base_file = video.original_url.split('/')[-1]#test_file.mp4
        #get watermark position
        burned_position = get_watermark_position(video)
        #get video durations
        burnedin_end_time = get_video_duration(video)
        return original_base_file,burned_position, burnedin_end_time
    except Exception as vnaexp:
        print('Some issue occured while getting video details')
        print(vnaexp)


def keyexistsonS3(key):
    conn = S3Connection(aws_secret_access_key=aws_secret,aws_access_key_id=aws_key)
    bucket = conn.get_bucket(settings.AWS_BUCKET_NAME, validate=True)
    try:
        # Will hit the API to check if it exists.
        possible_key = bucket.get_key(key)
        if possible_key:
            return True
        else:
            return False
    except Exception as e:
        return False


def transcode_request_for_ec2(watermark_text,mother_video):

    mother_video_id =str(mother_video.id)
    new_video = mother_video
    new_video.pk = None #django shuould set it
    new_video.save()
    project_id = str(new_video.project.id)
    #for simple test you can just input these values, new video has most details same as old one except the watermarking
    original_base_file, burned_position, hidden_position, burnedin_end_time, h_burnedin_start_time, h_burnedin_end_time = get_video_details(new_video)

    video_id = str(new_video.id)

    bucket_name = settings.AWS_BUCKET_NAME

    # Connect to EC2
    conn = get_conection()


    #we can add a parameter to check which formats we need in future
    BOOTSTRAP_SCRIPT = """#!/bin/bash -ex
    exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
    echo BEGIN
    date
    cd /home/ubuntu/
    pwd
    while  [  ! -f ./encoding_script_watermarked.sh ];   do      sleep 2;echo "loading script...";   done
    echo "script loaded"
    ((time bash ./encoding_script_watermarked.sh -p='%(PROJECT_ID)s' -m='%(MOTHER_VIDEO_ID)s' -v='%(VIDEO_ID)s' -f='%(FILE_NAME)s' -b="%(BURNED_END_TIME)s" -a="%(BURNED_POSITION)s" -w="%(WATERMARK_TEXT)s" -s='%(BUCKET_NAME)s') &>> encoding_logs.log; bash ./copy_logs.sh -p='%(PROJECT_ID)s' -m='%(MOTHER_VIDEO_ID)s' -v='%(VIDEO_ID)s' -s='%(BUCKET_NAME)s')
    echo END
    """

    burned_end_time= str(burnedin_end_time)

    startup = BOOTSTRAP_SCRIPT % {
        'PROJECT_ID': project_id,
        'VIDEO_ID': video_id,
        'FILE_NAME': original_base_file,
        'BURNED_END_TIME': burned_end_time,
        'BURNED_POSITION': burned_position,
        'WATERMARK_TEXT': watermark_text,
        'MOTHER_VIDEO_ID':mother_video_id,
        'BUCKET_NAME': bucket_name}

    print(startup)

    instance_reservation = conn.run_instances(
        image_id="ami-ac3640c1",# use the ami for the image which we created earlier
        instance_type="c3.xlarge",#instance type you want to use
        key_name="your_key_file",
        security_groups=["ffmpeg-test-security-group"],
        user_data=startup
    )
    instance = instance_reservation.instances[0]
    print(instance)

    #wait till the instance is not running
    while instance.state != 'running':
        print ('...instance is %s' % instance.state)
        time.sleep(10)
        instance.update()

    #tag instcance once its running
    instance_name = str(mother_video_id)+'-'+str(video_id)+'-'+str(datetime.datetime.now())
    print(instance_name)
    instance.add_tag("Name",instance_name)

    #now the instance is running we should check for processed data in s3 after some avegare time

    #wait till instance has not stopped
    while instance.state != 'stopped':
        print ('...instance is %s' % instance.state)
        time.sleep(10)
        instance.update()

    #check if the files are present on s3, .ts files , index files and master file
    if keyexistsonS3(project_id+'/video/'+mother_video_id+'/'+video_id+'/'+'master_'+project_id+'_'+video_id+'.m3u8'):

        master_url_tobe_saved = 'https://'+str(settings.AWS_BUCKET_NAME)+'.s3.amazonaws.com/'+project_id+'/video/'+mother_video_id+'/'+video_id+'/'+'master_'+project_id+'_'+video_id+'.m3u8'
        print(master_url_for_hls_video)
    else:
        #if not then process failed and we can retry and report and should never terminate the instance, also get a failuer mail
        print('some s3 files are missing something went haywire with instance %s' % instance)
        return None


def generate_burned_watermark_screener():
    #I am using a video object here for simplicity
    mother_video_id ="3627"
    watermark_text ="Ec2 test 104"
    mother_video = Videos.objects.get(id=mother_video_id)


    #generate the burned watermark video
    print('calling ec2')
    #pdb.set_trace()
    burned_video = transcode_request_for_ec2(watermark_text,mother_video)

    print('got the video')
    print(burned_video)
