from datetime import datetime

from django.conf import settings
from django.db import models


class News(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateField(default=datetime.today)

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = 'Новости'
        verbose_name = 'Новость'
        app_label = 'ya_news.news'

    def __str__(self):
        return self.title


class Comment(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        app_label = 'ya_news.news'

    def __str__(self):
        return self.text[:50]
