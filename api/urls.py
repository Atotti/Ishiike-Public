from django.urls import path
from . import views
# from django.views.decorators.csrf import csrf_exempt

app_name = 'api'

urlpatterns = [
    path('v1/vote/', views.CreateVoteView.as_view(), name='create_vote'),
]
