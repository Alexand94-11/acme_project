from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    path('', views.birthday, name='create'),
    # Маршрут для вывода списка ДР.
    path('list/', views.birthday_list, name='list')
]
