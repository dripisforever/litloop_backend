from django.test import TestCase

# Create your tests here.

from django.shortcuts import render

# Create your views here.
from django.shortcuts import  render
from albums.models import Album
import requests

def get_meals(request, track_uri):
    all_meals = {}
    if 'name' in request.GET:
        name = request.GET['name']
        url = 'https://www.themealdb.com/api/json/v1/1/search.php?s=%s' % name

        track_data = sp.track(track_uri)
        # response = requests.get(url)
        # data = response.json()
        # meals = data['meals']
        meals = track_data

        for i in meals:
            # meal_data = Album(
            #     id = i['id'],
            #     name = i['name'],
            #     artist = i['artists'][0].name,
            #
            # )
            # meal_data.save()
            # all_meals = Album.objects.all().order_by('-id')

            Album.objects.filter(
                Q(id = i['id'],) |
                Q(first_name='Robert'),
            ).get_or_create(
                id=i['id'],
                name=i['name'],
                defaults={'first_name': 'Bob'})
            )


    return render (request, 'meals/meal.html', { "all_meals": all_meals} )
    return Response(request, 'meals/meal.html', { "all_meals": all_meals} )
