# from __future__ import absolute_import
from django.urls import path
from views.views import (
    ViewsUP
)



urlpatterns = [

    path('up', ViewsUP.as_view())

]
