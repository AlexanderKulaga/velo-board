from django.db.models import Count, Q
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from rest_framework.utils import json

from veloproject.velostore.models import Post
from django.core.paginator import Paginator
from django.core import serializers


def index(request, page_number=1):
    #return HttpResponse('Стартовая страница')
    posts = Post.objects.all().order_by('id').reverse()
    current_page = Paginator(posts, 4)
    marks = Post.objects.values('mark')\
        .annotate(mark_count=Count('mark'))\
        .filter(mark_count__gte=1)\
        .order_by('mark_count')
    context = {'posts': current_page.page(page_number), 'marks': marks}
    return render(request, 'index.html', context)


def add(request):
    if request.POST:
        title = request.POST['title']
        mark = request.POST['mark']
        price = request.POST['price']
        email = request.POST['email']
        phone = request.POST['phone']
        if price == '':
            Post.objects.create(title=title, mark=mark, price=None, email=email, phone_number=phone)
        else:
            Post.objects.create(title=title, mark=mark, price=price, email=email, phone_number=phone)
    return HttpResponseRedirect('/')


def api_find(request):
    if request.GET:
        find_word = request.GET['find_word']

        found = Post.objects.values('id', 'title', 'mark', 'price', 'phone_number', 'email') \
            .filter(
            Q(title__icontains=find_word.lower()) |
            Q(mark__icontains=find_word.lower()))

    return HttpResponse(json.dumps(list(found), ensure_ascii=False),
                            content_type='application/json; charset=UTF-8',
                            status=200)


def find_page(request):
    if request.GET:
        find_word = request.GET['find_word']

        found = Post.objects.values('id', 'title', 'mark', 'price', 'phone_number', 'email') \
            .filter(
            Q(title__icontains=find_word.lower()) |
            Q(mark__icontains=find_word.lower()))
        context = {'posts': found}

        return render(request, 'find_page.html', context)


def popular(request):
    populars = Post.objects.values('mark')\
        .annotate(mark_count=Count('mark'))\
        .filter(mark_count__gte=5)\
        .order_by('mark_count')

    context = {'posts': populars}
    return render(request, 'popular.html', context)


def api_get_all(request, page_number=1):
    posts = Post.objects.values('id', 'title', 'mark').order_by('id').reverse()
    current_page = Paginator(posts, 4)
    posts = current_page.page(page_number)

    return HttpResponse(json.dumps(list(posts), ensure_ascii=False),
                        content_type='application/json; charset=UTF-8',
                        status=200)


def api_get_popular(request):
    populars = Post.objects.values('mark') \
        .annotate(mark_count=Count('mark')) \
        .filter(mark_count__gte=5) \
        .order_by('mark_count')

    return HttpResponse(json.dumps(list(populars), ensure_ascii=False),
                        content_type='application/json; charset=UTF-8',
                        status=200)


def api_find_word(request):
    find_word = request.GET['find_word']

    found = Post.objects.values('id', 'title', 'mark', 'phone_number', 'email')\
        .filter(
        Q(title__icontains=find_word.lower())|
        Q(mark__icontains=find_word.lower()))

    return HttpResponse(json.dumps(list(found), ensure_ascii=False),
                        content_type='application/json; charset=UTF-8',
                        status=200)


def api_add(request):
    title = request.GET['title']
    mark = request.GET['mark']
    price = request.GET['price']
    email = request.GET['email']
    phone = request.GET['phone']
    Post.objects.create(title=title, mark=mark, price=price, email=email, phone_number=phone)
    return HttpResponseRedirect('/')