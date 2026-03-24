import pytest

from django.urls import reverse

from constant import HOME_URL, get_news_detail_url
from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client, create_test_news, settings):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, create_test_news):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    assert all_dates == sorted(all_dates, reverse=True)


@pytest.mark.django_db
def test_comments_order(client, news, create_testcomments):
    url = get_news_detail_url(news.pk)
    response = client.get(url)

    news_obj = response.context['news']
    all_comments = news_obj.comment_set.order_by('created').all()
    all_timestamps = [comment.created for comment in all_comments]

    assert all_timestamps == sorted(all_timestamps, reverse=False)


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news):
    url = get_news_detail_url(news.pk)
    response = client.get(url)

    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, news):
    url = get_news_detail_url(news.pk)
    response = author_client.get(url)

    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
