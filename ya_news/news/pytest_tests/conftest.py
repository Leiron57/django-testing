import pytest
from django.contrib.auth import get_user_model
from news.models import News, Comment
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

User = get_user_model()


@pytest.fixture
def author(db):
    return User.objects.create_user(username='author', password='password')


@pytest.fixture
def not_author(db):
    return User.objects.create_user(username='reader', password='password')


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
def author(django_user_model):
    return django_user_model.objects.create_user(username='автор', password='password')

@pytest.fixture
def author_client(author) -> Client:
    client = Client()
    client.force_login(author)
    return client

@pytest.fixture
def not_author_client(django_user_model) -> Client:
    user = django_user_model.objects.create_user(username='не автор', password='password')
    client = Client()
    client.force_login(user)
    return client
