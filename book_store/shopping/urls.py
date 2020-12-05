from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('rating', views.main, name='rating'),
    re_path(r'^ratings/', include('star_ratings.urls', namespace='ratings')),
]
