from django.test import Client
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone

import pytest

from news.models import News, Comment
from .constants import NEWS_COUNT_FOR_TESTING


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='author')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='reader')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def news_count(settings):
    """Возвращает количество новостей для тестирования (на 1 больше лимита)."""
    return settings.NEWS_COUNT_ON_HOME_PAGE + 1


@pytest.fixture
def create_test_news(news_count):
    """Создаёт набор тестовых новостей с разными датами."""
    today = timezone.now()
    news_objects = [
        News(
            title=f'Новость {index}',
            text='Просто текст',
            date=today - timedelta(days=index)
        )
        for index in range(NEWS_COUNT_FOR_TESTING)
    ]
    News.objects.bulk_create(news_objects)
    return News.objects.all()


@pytest.fixture
def create_testcomments(news, author):
    """Создаёт набор тестовых комментариев с разными датами создания."""
    now = timezone.now()
    comments = []
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст {index}',
            created=now + timedelta(days=index)
        )
        comments.append(comment)
    return comments
