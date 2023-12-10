import logging
import requests

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView
from django.contrib import messages
from django.db.models import Q, Count
from django.urls import reverse

from django.core.paginator import Paginator
from .forms import InquiryForm, ReviewModelForm, CommentModelForm
from .models import Period, Review, Day, Comment, Semester, Vote
from .serializers import CommentSerializer, ReviewSerializer, DaySerializer, SemesterSerializer, PeriodSerializer
from .tweet import CreateTweet
from socket import gethostname

from rest_framework import viewsets

#import tweepy

logger = logging.getLogger(__name__)

# 検索
def search_review(request):
    query = request.GET.get("q")
    if query:
        reviews = Review.objects.all()
        target_reviews = reviews.filter(
            Q(title__icontains=query) & Q(is_public=True) #公開されるものに限定
        ).all().order_by('created_at').reverse()
    else:
        target_reviews = Review.objects.filter(title__icontains="ban", is_public=True).all() #公開されるものに限定

    reviews_list = target_reviews.values()
    return render(request, "search.html", {"reviews": target_reviews, "reviews_list": reviews_list, "query": query})


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "index.html"

class AboutView(generic.TemplateView):
    template_name = "about.html"

class HowtoView(generic.TemplateView):
    template_name = "howto.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('review:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquary sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class ReviewListView(ListView):
    queryset = Review.objects.filter(is_public=True).order_by('-created_at')
    template_name = 'review_list.html'
    context_object_name = 'review_list'
    paginate_by = 50

class APIReviewListView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

class APICommentListView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class APIDayListView(viewsets.ModelViewSet):
    serializer_class = DaySerializer
    queryset = Day.objects.all()

class APISemesterListView(viewsets.ModelViewSet):
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()

class APIPeriodListView(viewsets.ModelViewSet):
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()

class ReviewAndCommentView(generic.FormView):
    template_name = 'review_detail.html'
    form_class = CommentModelForm

    def form_valid(self, form):
        comment = form.save(commit=False) #保存せずオブジェクト生成する
        comment.review = Review.objects.get(id=self.kwargs['pk'])
        comment.no = Comment.objects.filter(review=self.kwargs['pk']).count() + 1
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('review:review', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        #print(Review.objects.get(is_public=self.kwarg['review']))
        ctx = super().get_context_data()
        ctx['review'] = Review.objects.annotate(vote_count=Count('vote')).get(id=self.kwargs['pk'])
        ctx['comment_list'] = Comment.objects.filter(review_id=self.kwargs['pk']).order_by('no')
        forwarded_addresses = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded_addresses:
            ip_adress = forwarded_addresses.split(',')[0] # heroku経由でクライアントのipアドレスを取得
        else:
            ip_adress = self.request.META.get("REMOTE_ADDR") # ローカル環境でクライアントのipアドレスを取得
        ctx['liked'] = Vote.objects.filter(review_id=self.kwargs['pk'], ip_address=ip_adress) # 参考になったを既に押しているか判断するflag [bool]
        if ctx['review'].is_public: # is_public = Trueの場合のみ返す
            return ctx
        else:
            ctx = super().get_context_data()
            ctx['review'] = Review.objects.get(id=1)
            return ctx


class ReviewCreateView(generic.CreateView):
    template_name = 'create_review.html'
    form_class = ReviewModelForm
    model = Review
    def get_success_url(self) -> str:
        message=f"石池に『{self.object.title}』のクチコミが追加されました! #石池 {self.request.META.get('HTTP_X_FORWARDED_PROTO')}://{self.request.META.get('HTTP_HOST')}/{self.object.id}"
        print(message)
        if gethostname() != "DESKTOP-ABEN90S":
            print("本番環境")
            CreateTweet(message) # 本番環境でのみツイート
        return reverse('review:thanks', kwargs={"pk":self.object.id})

    def form_valid(self, form):
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'confirm_review.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'create_review.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('base:top'))

class ThanksView(generic.FormView):
    template_name = 'thanks.html'
    form_class = CommentModelForm

    def form_valid(self, form):
        comment = form.save(commit=False) #保存せずオブジェクト生成する
        comment.review = Review.objects.get(id=self.kwargs['pk'])
        comment.no = Comment.objects.filter(review=self.kwargs['pk']).count() + 1
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('review:review', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['review'] = Review.objects.get(id=self.kwargs['pk'])
        ctx['comment_list'] = Comment.objects.filter(review_id=self.kwargs['pk']).order_by('no')
        return ctx
    # これはページじゃなくてjsのなんかにしたい

class DayView(generic.ListView):
    template_name = 'day.html'
    context_object_name = 'review_list'

    def get_queryset(self):
        return Review.objects.filter(day__url_code = self.kwargs['url_code'], is_public=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["day"] = get_object_or_404(Day, url_code=self.kwargs['url_code'])
        return ctx

class PeriodView(generic.ListView):
    template_name = 'period.html'
    context_object_name = 'review_list'

    def get_queryset(self):
        return Review.objects.filter(period__url_code = self.kwargs['url_code'], is_public=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["period"] = get_object_or_404(Period, url_code=self.kwargs['url_code'])
        return ctx

class SemesterView(generic.ListView):
    template_name = 'semester.html'
    context_object_name = 'review_list'

    def get_queryset(self):
        return Review.objects.filter(semester__url_code = self.kwargs['url_code'], is_public=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["semester"] = get_object_or_404(Semester, url_code=self.kwargs['url_code'])
        return ctx
