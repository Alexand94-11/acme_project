from django.db import models

# Импортируем функцию-валидатор.
from .validators import real_age


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
    )
    # Добавляем валидатор для проверки возраста.
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    # Добавляем изображения, которые будем загружать в отдельную папку.
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)

    class Meta:
        # Проверка на уникальность записи:
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )
