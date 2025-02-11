# birthday/views.py
from django.shortcuts import render

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm


def birthday(request):
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
    # Тот же код, но с использованием трюка:
    form = BirthdayForm(request.GET or None)
    if form.is_valid():
        pass
    # Передаём форму в словарь контекста:
    context = {'form': form}
    # Указываем нужный шаблон и передаём в него словарь контекста.
    return render(request, 'birthday/birthday.html', context)
