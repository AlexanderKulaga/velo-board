from django.urls import path
from veloproject.velostore import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='landing'),

    path('register', views.RegisterFormView.as_view(), name='register'),
    path('login', views.LoginFormView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),

    path('page/<int:page_number>/', views.IndexView.as_view(), name='index'),
    path('add', views.AddView.as_view(), name='add'),
    path('find_page', views.FindPageView.as_view(), name='find_page'),
    path('popular', views.PopularView.as_view(), name='popular'),
    path('docs', views.DocsView.as_view(), name='docs'),

    path('api/get_page/<int:page_number>/', views.api_get_page),  # получение постов по номеру страницы
    path('api/get_all/', views.api_get_all),  # получение всех постов
    path('api/get_popular/', views.api_get_popular),  # получение популярных марок и числа деталей этих марок
    path('api/find', views.api_find_word),  # поиск
    path('api/add', views.api_add),  # добавление поста
]