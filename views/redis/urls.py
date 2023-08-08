from django.conf.urls import url
from .views import view_books, view_cached_books


urlpatterns = [
    url(r'^$', view_books),
    url(r'^cache/', view_cached_books),
]


# $ loadtest -n 100 -k  http://localhost:8000/store/cache/
