from django.contrib import admin
from django.urls import path, include
from veloproject.velostore import views


urlpatterns = [
    path('', views.index, name='landing'),
    path('add', views.add, name='add'),
    path('find_page', views.find_page, name='find_page'),
    path('popular', views.popular, name='popular'),
    path('page/<int:page_number>/', views.index, name='index'),

    path('find', views.api_find, name='find'),
    path('api/get_posts/<int:page_number>/', views.api_get_all),
    path('api/get_posts/', views.api_get_all),
    path('api/get_popular/', views.api_get_popular),
    path('api/find', views.api_find_word),
    path('api/add', views.api_add),
]