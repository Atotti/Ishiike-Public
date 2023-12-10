from django.urls import path, include
from . import views

app_name = 'search_syllabus'
urlpatterns = [
    path('search', views.search, name='search'),
]