import re
from veloproject.velostore.models import Post
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator
from rest_framework.utils import json


def index(request, page_number=1):
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
        .order_by('mark_count')\
        .reverse()

    context = {'posts': populars}
    return render(request, 'popular.html', context)


def docs(request):
    return render(request, 'api_docs.html')


def api_get_all(request):
    posts = Post.objects.values('id', 'title', 'mark', 'price', 'email', 'phone_number')

    return HttpResponse(json.dumps(list(posts), ensure_ascii=False),
                        content_type='application/json; charset=UTF-8',
                        status=200)


def api_get_page(request, page_number=1):
    posts = Post.objects.values('id', 'title', 'mark', 'price', 'email', 'phone_number').order_by('id').reverse()
    current_page = Paginator(posts, 4)
    posts = current_page.page(page_number)

    return HttpResponse(json.dumps(list(posts), ensure_ascii=False),
                        content_type='application/json; charset=UTF-8',
                        status=200)


def api_get_popular(request):
    populars = Post.objects.values('mark') \
        .annotate(mark_count=Count('mark')) \
        .filter(mark_count__gte=5) \
        .order_by('mark_count')\
        .reverse()

    return HttpResponse(json.dumps(list(populars), ensure_ascii=False),
                        content_type='application/json; charset=UTF-8',
                        status=200)


def api_find_word(request):
    find_word = request.GET.get('find_word')
    if find_word:
        found = Post.objects.values('id', 'title', 'mark', 'phone_number', 'email')\
            .filter(
            Q(title__icontains=find_word.lower())|
            Q(mark__icontains=find_word.lower()))
    else:
        found = [{'status': 'error'}]
        return HttpResponse(json.dumps(list(found), ensure_ascii=False),
                        content_type='application/json; charset=UTF-8',
                        status=400)
    return HttpResponse(json.dumps(list(found), ensure_ascii=False),
                        content_type='application/json; charset=UTF-8',
                        status=200)


def api_add(request):
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    PHONE_REGEX = re.compile(r"7\d{3}\d{7}")

    price = request.GET.get('price')  # прайс может быть нулевым, остальные проверю трайкэчем
    try:
        title = request.GET['title']
        mark = request.GET['mark']
        email = request.GET['email']
        phone = request.GET['phone']
    except MultiValueDictKeyError:
        rezult = [{'status': 'error'}]
        return HttpResponse(json.dumps(list(rezult), ensure_ascii=False),
                            content_type='application/json; charset=UTF-8',
                            status=400)

    if not EMAIL_REGEX.match(email) and not PHONE_REGEX.match(phone):
        rezult = [{'status': 'error_regex'}]
        return HttpResponse(json.dumps(list(rezult), ensure_ascii=False),
                            content_type='application/json; charset=UTF-8',
                            status=400)

    Post.objects.create(title=title, mark=mark, price=price, email=email, phone_number='+'+phone)
    rezult = [{'status': 'ok'}]
    return HttpResponse(json.dumps(list(rezult), ensure_ascii=False),
                        content_type='application/json; charset=UTF-8',
                        status=200)