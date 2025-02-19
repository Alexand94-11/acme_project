# birthday/views.py
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday, Congratulation
from .utils import calculate_birthday_countdown

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Импортируем класс ошибки (в данном случае - 403).
from django.core.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404, redirect


# Будут обработаны POST-запросы только от залогиненных пользователей.
@login_required
def add_comment(request, pk):
    # Получаем объект дня рождения или выбрасываем 404 ошибку.
    birthday = get_object_or_404(Birthday, pk=pk)
    # Функция должна обрабатывать только POST-запросы.
    form = CongratulationForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        congratulation = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        congratulation.author = request.user
        # В поле birthday передаём объект дня рождения.
        congratulation.birthday = birthday
        # Сохраняем объект в БД.
        congratulation.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('birthday:detail', pk=pk)


"""
# Класс CongratulationCreateView выполняет ту же работу,
# что и функция add_comment().
from django.urls import reverse


class CongratulationCreateView(LoginRequiredMixin, CreateView):
    birthday = None
    model = Congratulation
    form_class = CongratulationForm

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    # Переопределяем get_success_url()
    def get_success_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})
# А чтобы вся эта красота заработала — надо поменять маршрут и вместо функции
# add_comment() указать CongratulationCreateView.as_view(), как и полагается
# при работе с CBV.
"""


@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    # Переопределяем метод валидации, чтобы передавать объект пользователя
    # в поле объекта формы.
    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


"""
# Добавляем миксин для тестирования пользователей, обращающихся к объекту.
# Класс UserPassesTestMixin унаследован от AccessMixin, который по умолчанию
# переадресует анонимных пользователей на страницу логина. Поэтому при
# использовании UserPassesTestMixin миксин LoginRequiredMixin можно
# не использовать.
class BirthdayUpdateView(UserPassesTestMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm

    # Определяем метод test_func() для миксина UserPassesTestMixin:
    def test_func(self):
        # Получаем текущий объект.
        object = self.get_object()
        # Метод вернёт True или False.
        # Если пользователь - автор объекта, то тест будет пройден.
        # Если нет, то будет вызвана ошибка 403.
        return object.author == self.request.user
"""


ADMIN_LOGIN = 'Alexander'


# Описываем собственный миксин, унаследованный от UserPassesTestMixin, чтобы
# добавить его в нужные классы и не загромождать код.
class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user or ADMIN_LOGIN


class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        return context


'''from django.shortcuts import render, get_object_or_404, redirect

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown
# Импортируем модель дней рождения для работы ф-ции birthday_list.
from .models import Birthday
# Импортируем класс пагинатора для постраничного вывода.
from django.core.paginator import Paginator
# Импортируем CBV-классы.
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
# Импортируем функцию, которая возвращает строку с URL нужной страницы
# при непосредственном обращении к CBV во время работы веб-сервера
from django.urls import reverse_lazy


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    """Заменяет функцию birthday_list."""
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context

"""
class BirthdayCreateView(CreateView):
    # Заменяет функцию birthday. Используется для создания записи.
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # Этот класс сам может создать форму на основе модели!
    # Нет необходимости отдельно создавать форму через ModelForm.
    # Указываем поля, которые должны быть в форме:
    # fields = '__all__'
    # Указываем имя формы:
    form_class = BirthdayForm
    # Явным образом указываем шаблон:
    template_name = 'birthday/birthday.html'
    # Указываем namespace:name страницы, куда будет перенаправлен пользователь
    # после создания объекта:
    success_url = reverse_lazy('birthday:list')


class BirthdayUpdateView(UpdateView):
    # Заменяет функцию birthday. Используется для редактирования записи.
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list')
"""


# Создаём миксин, чтобы не дублировать код при создании CBV-классов.
class BirthdayMixin:
    model = Birthday
    form_class = BirthdayForm
    # Т.к. создан шаблон birthday_form.html, указывать явно
    # название шаблона не нужно.
    # template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list')


# Добавляем миксин первым по списку родительских классов.
class BirthdayCreateView(BirthdayMixin, CreateView):
    # Не нужно описывать атрибуты: все они унаследованы от BirthdayMixin.
    pass


class BirthdayUpdateView(BirthdayMixin, UpdateView):
    # И здесь все атрибуты наследуются от BirthdayMixin.
    pass


class BirthdayDeleteView(DeleteView):
    """Заменяет функцию delete_birthday."""
    model = Birthday
    # Убираем вызов шаблона, т.к. используется свой шаблон с ожидаемым именем.
    # template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list')


"""
# Вариант компоновки кода с 2 миксинами.
class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayFormMixin:
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'


class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin, CreateView):
    pass


class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin, UpdateView):
    pass


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    pass
"""


# Добавим опциональный параметр pk для редактирования объекта.
def birthday(request, pk=None):
    """
    # Если есть параметры GET-запроса...
    if request.GET:
        # ...передаём параметры запроса в конструктор класса формы.
        form = BirthdayForm(request.GET)
        # Если данные валидны...
        if form.is_valid():
            # ...то считаем, сколько дней осталось до дня рождения.
            # Пока функции для подсчёта дней нет — поставим pass:
            pass
    # Если нет параметров GET-запроса.
    else:
        # То просто создаём пустую форму.
        form = BirthdayForm()
    """
    # Если в запросе указан pk (если получен запрос на редактирование объекта):
    if pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Birthday, pk=pk)
    # Если в запросе не указан pk
    # (если получен запрос к странице создания записи):
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    # Передаём в форму либо данные из запроса, либо None.
    # В случае редактирования прикрепляем объект модели.
    # Тот же код(закомментированный), но с использованием трюка:
    form = BirthdayForm(
        request.POST or None,
        # Указываем, что в запросе могут передаваться файлы.
        files=request.FILES or None,
        instance=instance
    )
    # Создаём словарь контекста сразу после инициализации формы.
    context = {'form': form}
    # Если форма валидна...
    if form.is_valid():
        # ...сохраняем данные из формы в БД:
        # form.save()
        # Создаем объект модели без его сохранения.
        instance = form.save(commit=False)
        # Присваиваем полю объекта "author" нужное значение.
        instance.author = request.user
        # Сохраняем объект модели в БД(сохраняем именно объект модели, а не
        # форму, т.к. значение поля author записано именно в объект модели)
        instance.save()
        # ...вызываем функцию подсчёта дней:
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})
    # Указываем нужный шаблон и передаём в него словарь контекста.
    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    # Получаем список всех объектов с сортировкой по id.
    birthdays = Birthday.objects.order_by('id')
    # Создаём объект пагинатора с количеством 10 записей на страницу.
    paginator = Paginator(birthdays, 10)
    """
    # Передаём их в контекст шаблона.
    context = {'birthdays': birthdays}
    """
    # Получаем из запроса значение параметра page.
    page_number = request.GET.get('page')
    # Получаем запрошенную страницу пагинатора.
    # Если параметра page нет в запросе или его значение не приводится к числу,
    # вернётся первая страница.
    page_obj = paginator.get_page(page_number)
    # Вместо полного списка объектов передаём в контекст
    # объект страницы пагинатора
    context = {'page_obj': page_obj}
    return render(request, 'birthday/birthday_list.html', context)


"""
def edit_birthday(request, pk):
    # Находим запрошенный объект для редактирования по первичному ключу
    # или возвращаем 404 ошибку, если такого объекта нет.
    # При поиске объекта дополнительно указываем текущего пользователя.
    # instance = get_object_or_404(Birthday, pk=pk, author=request.user)
    # В этом варианте возвращаем другую ошибку(не 404, а 403).
    # Получаем нужный объект.
    instance = get_object_or_404(Birthday, pk=pk)
    # Проверяем, кто автор объекта.
    if instance.author != request.user:
        # Здесь может быть как вызов ошибки, так и редирект на нужную страницу.
        raise PermissionDenied
    # Связываем форму с найденным объектом: передаём его в аргумент instance.
    form = BirthdayForm(request.POST or None, instance=instance)
    # Всё остальное без изменений.
    context = {'form': form}
    # Сохраняем данные, полученные из формы, и отправляем ответ:
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)
"""


def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку.
    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('birthday:list')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'birthday/birthday.html', context)
'''
