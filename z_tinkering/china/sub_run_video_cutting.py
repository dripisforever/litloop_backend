# Cutting video-cutting the extra part of the video tail (you need to install ffmpeg here is very simple, ask Du Niang)
import os
import subprocess
import datetime

def substring(date):
    r=date.decode()
    r=r.strip()
    rlist=r.split(":")
    result=(int(rlist[0])*60*60)+(int(rlist[1])*60)+(float(rlist[2]))
    return result


def sub_video():
     # url="/home/facelive/Downloads/videos/"
     # url2="/home/facelive/Downloads/sub_videos/"

     # 硬盘路径(原视频存放路径)
     url="/media/facelive/Elements/videos/"
     # 切割后的视频存放路径
     url2="/media/facelive/Elements/sub_videos/"
     fileList= os.listdir(url)


     for file in fileList:
         #获取当前文件的视频长度
         strcmd=["ffmpeg -i "+url+file+" 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"]
         result=subprocess.run(args=strcmd,stdout=subprocess.PIPE,shell=True)
         date=result.stdout
         print(type(date))
         print(date)
         time=substring(date)
         end=time-4
         sub="ffmpeg -ss 0 -t "+str(end)+" -accurate_seek -i "+url+file+" -codec copy -avoid_negative_ts 1 "+url2+file+''

         videoresult=subprocess.run(args=sub,shell=True)
         print(time)
     print("视频截取完成！！")


def test():
     url = "/home/facelive/Downloads/videos/"
     fileList = os.listdir(url)
     for file in fileList:
         print(file)
