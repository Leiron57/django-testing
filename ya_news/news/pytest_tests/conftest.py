import pytest
from django.contrib.auth import get_user_model
from news.models import News, Comment
from django.test.client import Client
from typing import Any
import pytest


@pytest.fixture
def author(dajngo_user_model: Any) -> Any:
    return dajngo_user_model.objects.create(username='author')


@pytest.fixture
def not_author(dajngo_user_model: Any) -> Any:
    return dajngo_user_model.objects.create(username-'reader')


@pytest.fixture
def author_client(author: Any) -> Any:
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author: Any) -> Any:
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
        author=author,
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )