import re

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView, FormView
from django.views.generic.base import View
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth import logout

from veloproject.velostore.models import Post
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator
from rest_framework.utils import json


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = '/login'
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(RegisterFormView, self).get(self, request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(LoginFormView, self).get(self, request, *args, **kwargs)

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(LoginFormView, self).form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class IndexView(View):
    def get(self, request, page_number=1):
        posts = Post.objects.all().order_by('id').reverse()
        current_page = Paginator(posts, 4)
        marks = Post.objects.values('mark')\
            .annotate(mark_count=Count('mark'))\
            .filter(mark_count__gte=1)\
            .order_by('mark_count')
        context = {'posts': current_page.page(page_number), 'marks': marks}
        return render(request, 'index.html', context)


class AddView(View):
    def post(self, request):
        if request.POST:
            title = request.POST['title']
            mark = request.POST['mark']
            price = request.POST['price']
            email = request.POST['email']
            phone = request.POST['phone']
            if price == '':
                Post.objects.create(title=title, mark=mark, price=None, email=email, phone_number=phone, name=request.user)
            else:
                Post.objects.create(title=title, mark=mark, price=price, email=email, phone_number=phone, name=request.user)
        return HttpResponseRedirect('/')


class FindPageView(View):
    def get(self, request):
        if request.GET:
            find_word = request.GET['find_word']

            found = Post.objects.values('id', 'title', 'mark', 'price', 'phone_number', 'email') \
                .filter(
                Q(title__icontains=find_word.lower()) |
                Q(mark__icontains=find_word.lower()))
            context = {'posts': found}
            return render(request, 'find_page.html', context)


class PopularView(View):
    def get(self, request):
        populars = Post.objects.values('mark')\
            .annotate(mark_count=Count('mark'))\
            .filter(mark_count__gte=5)\
            .order_by('mark_count')\
            .reverse()

        context = {'posts': populars}
        return render(request, 'popular.html', context)


class DocsView(View):
    def get(self, request):
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