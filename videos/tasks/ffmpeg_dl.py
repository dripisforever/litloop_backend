#ref https://github.com/dreglad/om-backend/blob/1f24d36e4ae2e43238d460b4fb0227fe353510ec/django/dvr/tasks/videos.py

@shared_task
def download_video_ffmpeg(url, filename, video_pk=None):
    if video_pk: video = Video.objects.get(pk=video_pk)

    if not os.path.isdir(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    cmd = 'ffmpeg -y -i "{}" -c copy {}'.format(url, filename)
    thread = pexpect.spawn(cmd)
    cpl = thread.compile_pattern_list([
        pexpect.EOF,
        'Duration: (\d\d:\d\d:\d\d\.?\d*)',
        'time=(\d\d:\d\d:\d\d\.?\d*)'
        ])
    prev_progress, duration, progress = None, 0, 0
    while True:
        i = thread.expect_list(cpl, timeout=None)
        if i == 0: # EOF
            print('subprocess finished')
            return
        elif i == 1:
            duration = thread.match.group(1)
            print('duration', duration)
        elif i == 2:
            progress_time = thread.match.group(1)
            print(progress_time)
        if video_pk and duration and (progress != prev_progress):
            pass
    thread.close()
