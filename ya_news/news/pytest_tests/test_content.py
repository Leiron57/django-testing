import pytest

from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from news.models import News, Comment
from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client):
    today = timezone.now()

    News.objects.bulk_create([
        News(
            title=f'Новость {index}',
            text='Просто текст',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ])

    url = reverse('news:home')
    response = client.get(url)

    object_list = response.context['object_list']

    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client):
    today = timezone.now()

    News.objects.bulk_create([
        News(
            title=f'Новость {index}',
            text='Просто текст',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ])

    url = reverse('news:home')
    response = client.get(url)

    object_list = response.context['object_list']

    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)

    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, news, author):
    now = timezone.now()

    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()

    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)

    news_obj = response.context['news']
    all_comments = news_obj.comment_set.all()

    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)

    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)

    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, news):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.get(url)

    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)