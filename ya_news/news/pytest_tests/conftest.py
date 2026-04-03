from datetime import timedelta

from django.test import Client
from django.utils import timezone

import pytest
from django.urls import reverse


from news.models import News, Comment
from .constants import (
    NEWS_COUNT_FOR_TESTING, 
    NEWS_DETAIL_URL, 
    NEWS_COMMENT_URL, 
    NEWS_EDIT_URL, 
    NEWS_DELETE_URL
)

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
def create_test_news():
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
    comment_objects = [
        Comment(
            news=news,
            author=author,
            text=f'Текст {index}',
            created=now + timedelta(days=index)
        )
        for index in range(10)
    ]
    Comment.objects.bulk_create(comment_objects)
    return Comment.objects.filter(news=news)


@pytest.fixture
def detail_url(news): 
    return reverse(NEWS_DETAIL_URL, args=(news.pk,)) 


@pytest.fixture
def comment_url(news): 
    return reverse(NEWS_COMMENT_URL, args=(news.pk,)) 


@pytest.fixture
def edit_url(comment): 
    return reverse(NEWS_EDIT_URL, args=(comment.pk,)) 


@pytest.fixture
def delete_url(comment): 
    return reverse(NEWS_DELETE_URL, args=(comment.pk,)) 


@pytest.fixture
def detail_with_comments_url(news): 
    return f'{reverse(NEWS_DETAIL_URL, args=(news.pk,))}#comments'
