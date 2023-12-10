from django.shortcuts import render
from .models import SyllabusBaseInfo
from django.db.models import Q

# Create your views here.


def search(request):
    query = request.GET.get("q")
    if query:
        reviews = SyllabusBaseInfo.objects.using('subdb').all()
        target_reviews = reviews.filter(
            Q(name__icontains=query) | Q(teacher__icontains=query) | Q(season__icontains=query) | Q(type__icontains=query) | Q(period__icontains=query) | Q(day__icontains=query)
        ).using('subdb').all()
    else:
        target_reviews = SyllabusBaseInfo.objects.using('subdb').filter(
            Q(name__icontains="呪呪呪") # ここぼくが書いたコード史上最低の実装
        ).using('subdb').all()

    reviews_list = target_reviews.values()
    return render(request, "search_syllabus/search.html", {"reviews": target_reviews, "reviews_list": reviews_list, "query": query})