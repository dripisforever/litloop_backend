path('websites/stats', website_stat)

def website_stat(self, request, array_data):
    # ref https://stackoverflow.com/questions/12101658/how-to-get-an-array-in-django-posted-via-ajax
    array_data = request.GET.getlist('data')
    array_data = request.GET.getlist('data[]')
    array_data = request.POST.getlist('data

    for data in array_data:

        stat = Website.objects.get(url=data[url])
        return stat

    for artist_data in track_data['artists']:
        artist_uri = artist_data['id']
        artist_data = sp.artist(artist_uri)
        Artist.create(**artist_data)
