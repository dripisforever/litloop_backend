from django.shortcuts import render
from videos.stackoverflow.sub_call_tasks import encode_mp4

# Create your views here.
@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data:
                user = request.user
                #
                #
                # No IDEA WHAT TO DO NEXT
                #
                #
                return HttpResponseRedirect('/')

    else:
        form = VideoForm()
        return render(request, 'upload_video.html', {
            'form':form
            })


class UploadAudioFileView(FormView):
    template_name = 'upload.html'
    form_class = AudioFileFrom

    def form_valid(self, form):
        audio_file = AudioFile(
            name=self.get_form_kwargs().get('data')['name'],
            mp3_file=self.get_form_kwargs().get('files')['mp3_file']
        )
        audio_file.save()
        transcode_mp3.delay(audio_file.id)
        return HttpResponseRedirect(reverse('audio:detail', kwargs={'pk': audio_file.pk}))


# def get_progress(request, task_id):
#     result = AsyncResult(task_id)
#     response_data = {
#         'state': result.state,
#         'details': result.info,
#     }
#     return HttpResponse(json.dumps(response_data), content_type='application/json')
