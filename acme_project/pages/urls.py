from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    # Т.к. вместо view-функции используется класс, убираем вызов функции:
    # path('', views.homepage, name='homepage'),
    path('', views.HomePage.as_view(), name='homepage'),
]
