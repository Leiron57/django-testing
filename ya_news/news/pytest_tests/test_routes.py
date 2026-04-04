from http import HTTPStatus
import pytest

from .constants import (
    HOME_URL,
    USER_LOGIN_URL,
    USER_SIGNUP_URL,
    USER_LOGOUT_URL,
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url_name',
    (HOME_URL, USER_LOGIN_URL, USER_SIGNUP_URL)
)
def test_pages_available_for_anonymous_user_get(client, url_name):
    response = client.get(url_name)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_news_detail_page_available_for_anonymous_user(
    client,
    news,
    detail_url
):
    response = client.get(detail_url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_logout_page_available_for_anonymous_user(client):
    response = client.post(USER_LOGOUT_URL)
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_fixture, url_fixture, expected_status, news_pk',
    [
        ('author_client', 'edit_url', HTTPStatus.OK, 1),
        ('author_client', 'delete_url', HTTPStatus.OK, 1),
        ('not_author_client', 'edit_url', HTTPStatus.NOT_FOUND, 1),
        ('not_author_client', 'delete_url', HTTPStatus.NOT_FOUND, 1),
    ]
)
def test_comment_edit_delete_permissions(
    request,
    client_fixture,
    url_fixture,
    expected_status,
    news_pk,
    comment
):
    client = request.getfixturevalue(client_fixture)
    url = request.getfixturevalue(url_fixture)
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url_fixture',
    ['edit_url', 'delete_url']
)
def test_redirect_anonymous_user_to_login(client, url_fixture, request):
    target_url = request.getfixturevalue(url_fixture)
    redirect_url = f'{USER_LOGIN_URL}?next={target_url}'
    response = client.get(target_url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == redirect_url
