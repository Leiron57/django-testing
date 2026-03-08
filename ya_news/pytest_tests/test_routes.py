import pytest
from django.contrib.auth import get_user_model
from news.models import News, Comment

User = get_user_model()


@pytest.fixture
def author(db):
    return User.objects.create_user(username='Автор', password='password')


@pytest.fixture
def not_author(db):
    return User.objects.create_user(username='Читатель', password='password')


@pytest.fixture
def news(db, author):
    """Создаём объект новости"""
    return News.objects.create(
        title='Заголовок',
        text='Текст',
        author=author
    )


@pytest.fixture
def comment(db, author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Комментарий'
    )


@pytest.fixture
def author_client(client, author):
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(client, not_author):
    client.force_login(not_author)
    return client
