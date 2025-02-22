from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    # Путь для создания записи с использованием view-функции:
    # path('', views.birthday, name='create'),
    # Путь для создания записи с использованием CBV-класса:
    path('', views.BirthdayCreateView.as_view(), name='create'),
    # Маршрут для вывода списка ДР с использованием view-функции:
    # path('list/', views.birthday_list, name='list'),
    # Маршрут для вывода списка ДР с использованием CBV-класса:
    path('list/', views.BirthdayListView.as_view(), name='list'),
    # Путь для отображения отдельной записи:
    path('<int:pk>/', views.BirthdayDetailView.as_view(), name='detail'),
    # Маршрут для запроса авторизации:
    path('login_only/', views.simple_view),
    # Путь для редактирования записи с использованием view-функции:
    # path('<int:pk>/edit/', views.birthday, name='edit'),
    # Путь для редактирования записи с использованием CBV-класса:
    path('<int:pk>/edit/', views.BirthdayUpdateView.as_view(), name='edit'),
    # Маршрут для удаления записи:
    # path('<int:pk>/delete/', views.delete_birthday, name='delete'),
    # Маршрут для удаления записи с использованием CBV-класса:
    path(
        '<int:pk>/delete/',
        views.BirthdayDeleteView.as_view(),
        name='delete'
    ),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
]
