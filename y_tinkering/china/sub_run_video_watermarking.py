import os
import subprocess
import datetime

def logo_video():

     # 硬盘路径
    url = "/media/facelive/Elements/videos/"
    url3="/media/facelive/Elements/logo_videos/"
    fileList = os.listdir(url)

    for file in fileList:

        sub = "ffmpeg -i "+url+file+" -i /home/facelive/Downloads/image/11.png -filter_complex overlay=W-w " + url3 + file + ''

        videoresult = subprocess.run(args=sub, shell=True)
    print("视频logo完成！！")
