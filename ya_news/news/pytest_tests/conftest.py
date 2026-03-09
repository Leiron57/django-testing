import pytest
from django.contrib.auth import get_user_model
from news.models import News, Comment
from django.test.client import Client

User = get_user_model()

@pytest.fixture
def news(db):
    return News.objects.create(
        title='Test News',
        text='Test content'
    )


@pytest.fixture
def comment(db, author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Test comment'
    )


@pytest.fixture
def author(django_user_model: Any) -> Any:
    return django_user_model.objects.create(username='author')


@pytest.fixture
def not_author(django_user_model: Any) -> Any:
    return django_user_model.objects.create(username='reader')


@pytest.fixture
def author_client(author: Any) -> Client:
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author) -> Client:
    client = Client()
    client.force_login(not_author)
    return client
