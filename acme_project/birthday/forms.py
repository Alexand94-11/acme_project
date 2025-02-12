# birthday/forms.py
from django import forms

# Импортируем класс модели Birthday.
from .models import Birthday

"""
# Пример использования класса форм:
class BirthdayForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=20)
    last_name = forms.CharField(
        label='Фамилия', required=False, help_text='Необязательное поле'
    )
    birthday = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
"""


# Пример использования класса ModelForm:
class BirthdayForm(forms.ModelForm):
    # Удаляем все описания полей.

    # Все настройки задаём в подклассе Meta.
    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Birthday
        # Указываем, что надо отобразить все поля.
        fields = '__all__'
        # Указываем, что для поля с ДР используется виджет.
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }
