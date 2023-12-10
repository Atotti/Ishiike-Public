from django.contrib import admin
from django import views
from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'questionList', views.APIQuestionListView, 'questionList')
router.register(r'commentList', views.APIQCommentListView, 'commentList')
router.register(r'tagList', views.APITagListView, 'tagList')

app_name = 'qanda'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('question-list/', views.QuestionListView.as_view(), name='question_list'),
    path('<int:pk>/', views.QuestionAndCommentView.as_view(), name='question'),
    path('create-question/', views.QuestionCreateView.as_view(), name='create_question'),
    path('tag_over_view/', views.TagOverViewView.as_view(), name='tag_over_view'),
    path('tag/<str:url_code>/', views.TagView.as_view(), name='tag'),
    path('faculty/<str:url_code>/', views.FacultyView.as_view(), name='faculty'),
    path('thanks/<int:pk>', views.ThanksView.as_view(), name="thanks"),
    path('search', views.search_question, name="search"),
    path('get_departments/<int:faculty_id>/', views.get_departments, name="get_departments"),
]

