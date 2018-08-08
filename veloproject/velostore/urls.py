from django.urls import path
from veloproject.velostore import views


urlpatterns = [
    path('', views.index, name='landing'),
    path('page/<int:page_number>/', views.index, name='index'),
    path('add', views.add, name='add'),
    path('find_page', views.find_page, name='find_page'),
    path('popular', views.popular, name='popular'),
    path('docs', views.docs, name='docs'),

    path('api/get_page/<int:page_number>/', views.api_get_page),  # получение постов по номеру страницы
    path('api/get_all/', views.api_get_all),  # получение всех постов
    path('api/get_popular/', views.api_get_popular),  # получение популярных марок и числа деталей этих марок
    path('api/find', views.api_find_word),  # поиск
    path('api/add', views.api_add),  # добавление поста
]