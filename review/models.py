from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.models import Title


class Review(models.Model):
    title = models.ForeignKey(Title, verbose_name='Объект обзора',
                              on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField('Текст')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.PositiveSmallIntegerField('Оценка',
                                             validators=[
                                                 MinValueValidator(1),
                                                 MaxValueValidator(10)
                                             ])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    review = models.ForeignKey(Review, verbose_name='Обзор',
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField('Текст')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
