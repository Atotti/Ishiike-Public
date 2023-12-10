from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

import logging
import requests

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.db.models import Q, Count
from django.urls import reverse

from .forms import QuestionModelForm, CommentModelForm
from .models import Question, QComment, Tag, Department, Faculty
from .serializers import QCommentSerializer, QuestionSerializer, TagSerializer

from rest_framework import viewsets
from .discord_post import post_discord

#import tweepy

logger = logging.getLogger(__name__)


# Create your views here.
class IndexView(generic.ListView):
    queryset = Question.objects.filter(is_public=True).order_by('-created_at')
    template_name = "qanda/index.html"
    context_object_name = 'question_list'

class QuestionListView(generic.ListView):
    queryset = Question.objects.filter(is_public=True).order_by('-created_at')
    template_name = 'qanda/question_list.html'
    context_object_name = 'question_list'

class APIQuestionListView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

class APIQCommentListView(viewsets.ModelViewSet):
    serializer_class = QCommentSerializer
    queryset = QComment.objects.all()

class APITagListView(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class QuestionAndCommentView(generic.FormView):
    template_name = 'qanda/question_detail.html'
    form_class = CommentModelForm

    def form_valid(self, form):
        comment = form.save(commit=False) #保存せずオブジェクト生成する
        comment.question = Question.objects.get(id=self.kwargs['pk'])
        comment.no = QComment.objects.filter(question=self.kwargs['pk']).count() + 1
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('qanda:question', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        #print(Review.objects.get(is_public=self.kwarg['review']))
        ctx = super().get_context_data()
        ctx['qanda'] = Question.objects.annotate(vote_count=Count('vote')).get(id=self.kwargs['pk'])
        ctx['comment_list'] = QComment.objects.filter(question_id=self.kwargs['pk']).order_by('no')
        if ctx['qanda'].is_public: # is_public = Trueの場合のみ返す
            return ctx
        else:
            ctx = super().get_context_data()
            ctx['qanda'] = Question.objects.get(id=1)
            return ctx


class QuestionCreateView(generic.CreateView):
    template_name = 'qanda/create_question.html'
    form_class = QuestionModelForm
    model = Question

    def get_success_url(self):
        message = f"新着の質問 {self.request.META.get('HTTP_X_FORWARDED_PROTO')}://{self.request.META.get('HTTP_HOST')}/qanda/{self.object.id} \n回答する {self.request.META.get('HTTP_X_FORWARDED_PROTO')}://{self.request.META.get('HTTP_HOST')}/admin/QandA/question/{self.object.id}/change/"
        post_discord(message)
        return reverse('qanda:thanks', kwargs={"pk":self.object.id})

    def form_valid(self, form):
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'qanda/create_question.html', ctx)
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'qanda/confirm_question.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('base:top'))

class ThanksView(generic.FormView):
    template_name = 'qanda/thanks.html'
    form_class = CommentModelForm

    def form_valid(self, form):
        comment = form.save(commit=False) #保存せずオブジェクト生成する
        comment.question = Question.objects.get(id=self.kwargs['pk'])
        comment.no = QComment.objects.filter(quesition=self.kwargs['pk']).count() + 1
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('qanda:question', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['qanda'] = Question.objects.get(id=self.kwargs['pk'])
        ctx['comment_list'] = QComment.objects.filter(question_id=self.kwargs['pk']).order_by('no')
        return ctx
    # これはページじゃなくてjsのなんかにしたい

class TagView(generic.ListView):
    template_name = 'qanda/tag.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.filter(tag__url_code = self.kwargs['url_code'], is_public=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag"] = get_object_or_404(Tag, url_code=self.kwargs['url_code'])
        return ctx

class TagOverViewView(generic.ListView):
    queryset = Question.objects.filter(is_public=True).order_by('-created_at')
    template_name = "qanda/tag_overview.html"
    context_object_name = 'question_list'

class FacultyView(generic.ListView):
    template_name = 'qanda/faculty.html'
    context_object_name = 'faculty_list'

    def get_queryset(self):
        return Question.objects.filter(faculty__url_code = self.kwargs['url_code'], is_public=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["faculty"] = get_object_or_404(Faculty, url_code=self.kwargs['url_code'])
        return ctx



def search_question(request):
    query = request.GET.get("q")
    if query:
        questions = Question.objects.all()
        target_questions = questions.filter(
            (Q(content__icontains=query) | Q(anser__icontains=query) ) & Q(is_public=True) #公開されるものに限定
        ).all().order_by('created_at').reverse()
    else:
        target_questions = Question.objects.filter(content__icontains="ban", is_public=True).all() #公開されるものに限定
    questions_list = target_questions.values()
    return render(request, "qanda/qanda_search.html", {"questions": target_questions, "questions_list": questions_list, "query": query})

def get_departments(request, faculty_id):
    departments = Department.objects.filter(faculty_id=faculty_id).values('id', 'department')
    print(departments)
    return JsonResponse(list(departments), safe=False)