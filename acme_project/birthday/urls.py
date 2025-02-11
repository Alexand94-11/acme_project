from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    path('', views.birthday, name='create'),
    # Маршрут для вывода списка ДР.
    path('list/', views.birthday_list, name='list'),
    # Путь для редактирования записей.
    path('<int:pk>/edit/', views.birthday, name='edit'),
    # Маршрут для удаления записи.
    path('<int:pk>/delete/', views.delete_birthday, name='delete'),
]
