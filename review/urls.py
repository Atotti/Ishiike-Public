from django.contrib import admin
from django import views
from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'reviewList', views.APIReviewListView, 'reviewList')
router.register(r'commentList', views.APICommentListView, 'commentList')
router.register(r'periodList', views.APIPeriodListView, 'periodList')
router.register(r'semesterList', views.APISemesterListView, 'semesterList')
router.register(r'dayList', views.APIDayListView, 'dayList')

app_name = 'review'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('api/', include(router.urls)),
    path('howto/', views.HowtoView.as_view(), name="howto"),
    path('inquiry/', views.InquiryView.as_view(), name='inquiry'),
    path('review-list/', views.ReviewListView.as_view(), name='review_list'),
    path('<int:pk>/', views.ReviewAndCommentView.as_view(), name='review'),
    path('create-review/', views.ReviewCreateView.as_view(), name='create_review'),
    path('day/<str:url_code>/', views.DayView.as_view(), name='day'),
    path('period/<str:url_code>/', views.PeriodView.as_view(), name='period'),
    path('semester/<str:url_code>/', views.SemesterView.as_view(), name='semester'),
    path('thanks/<int:pk>', views.ThanksView.as_view(), name="thanks"),
    path('search', views.search_review, name="search"),
]

