from http import HTTPStatus
import pytest
from django.urls import reverse
from .constants import (
    HOME_URL,
    USER_LOGIN,
    USER_SIGNUP,
    USER_LOGOUT,
    NEWS_DETAIL_URL,
    NEWS_EDIT_URL,
    NEWS_DELETE_URL,
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url_name',
    (HOME_URL, USER_LOGIN, USER_SIGNUP)
)
def test_pages_available_for_anonymous_user_get(client, url_name):
    url = reverse(url_name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_news_detail_page_available_for_anonymous_user(client, news):
    url = reverse(NEWS_DETAIL_URL, args=(news.pk,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_logout_page_available_for_anonymous_user(client):
    url = reverse(USER_LOGOUT)
    response = client.post(url)
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_fixture, url_name, expected_status, news_pk',
    [
        ('author_client', NEWS_EDIT_URL, HTTPStatus.OK, 1),
        ('author_client', NEWS_DELETE_URL, HTTPStatus.OK, 1),
        ('not_author_client', NEWS_EDIT_URL, HTTPStatus.NOT_FOUND, 1),
        ('not_author_client', NEWS_DELETE_URL, HTTPStatus.NOT_FOUND, 1),
    ]
)
def test_comment_edit_delete_permissions(
    request,
    client_fixture,
    url_name,
    expected_status,
    news_pk,
    comment
):
    client = request.getfixturevalue(client_fixture)
    url = reverse(url_name, args=(comment.pk,))
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url_name',
    [NEWS_EDIT_URL, NEWS_DELETE_URL]
)
def test_redirect_anonymous_user_to_login(
    client,
    url_name,
    news
):
    target_url = reverse(url_name, args=(news.pk,))
    login_url = reverse(USER_LOGIN)
    redirect_url = f'{login_url}?next={target_url}'
    response = client.get(target_url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == redirect_url
