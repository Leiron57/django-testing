from datetime import timedelta
from django.test import Client
from django.urls import reverse
from django.utils import timezone
import pytest

from news.models import News, Comment
from .constants import (
    NEWS_COUNT_FOR_TESTING,
    NEWS_DETAIL_URL,
    NEWS_COMMENT_URL,
    NEWS_EDIT_URL,
    NEWS_DELETE_URL,
    USER_LOGIN,
    USER_LOGOUT,
    USER_SIGNUP,
    HOME_URL,
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
def home_url():
    return reverse(HOME_URL)


@pytest.fixture
def detail_url(news):
    """URL страницы новости."""
    return reverse(NEWS_DETAIL_URL, args=(news.pk,))


@pytest.fixture
def comment_url(news):
    """URL для добавления комментария к новости."""
    return reverse(NEWS_COMMENT_URL, args=(news.pk,))


@pytest.fixture
def edit_url(comment):
    """URL для редактирования комментария."""
    return reverse(NEWS_EDIT_URL, args=(comment.pk,))


@pytest.fixture
def delete_url(comment):
    """URL для удаления комментария."""
    return reverse(NEWS_DELETE_URL, args=(comment.pk,))


@pytest.fixture
def detail_with_comments_url(news):
    """URL страницы новости с якорем на комментарии."""
    return f'{reverse(NEWS_DETAIL_URL, args=(news.pk,))}#comments'


@pytest.fixture
def login_url():
    """URL страницы логина."""
    return reverse(USER_LOGIN)


@pytest.fixture
def logout_url():
    """URL страницы логаута."""
    return reverse(USER_LOGOUT)


@pytest.fixture
def signup_url():
    """URL страницы регистрации."""
    return reverse(USER_SIGNUP)


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
