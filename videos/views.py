from django.shortcuts import render

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
