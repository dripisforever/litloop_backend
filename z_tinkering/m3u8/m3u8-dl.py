# REFERENCE: https://youtu.be/p07ZZZVL72E?t=1051
import m3u8
import requests
import subprocess

url = "https://vp.nyt.com/video/hls/2017/12/01/74857_1_guide-team-building-2_wg/index-f1-v1.m3u8"
r = requests.get(url)

m3u8_master = m3u8.loads(r.text)


playlist_url = m3u8_master.data['playlist'][0]['uri']
r = requests.get(playlist_url)
playlist = m3u8.loads(r.text)
playlist_segments_uri = playlist.data['segments'][0]['uri']

r = requests.get(playlist_segments_uri)
with open("video.ts", wb) as f:
    for segment in playlist.data['segments']:
        url = segment['uri']
        r = requests.get(url)
        f.write(r.content)


subprocess.run(['ffmpeg', '-i', 'video.ts', 'vid1.mp4'])
