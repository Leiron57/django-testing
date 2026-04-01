from http import HTTPStatus

import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url_fixture',
    ('home_url', 'login_url', 'signup_url')
)
def test_pages_available_for_anonymous_user_get(client, request, url_fixture):
    url = request.getfixturevalue(url_fixture)

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_news_detail_page_available_for_anonymous_user(client, detail_url):
    response = client.get(detail_url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_logout_page_available_for_anonymous_user(client, logout_url):
    response = client.post(logout_url)
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_fixture, url_fixture, expected_status',
    [
        ('author_client', 'edit_url', HTTPStatus.OK),
        ('author_client', 'delete_url', HTTPStatus.OK),
        ('not_author_client', 'edit_url', HTTPStatus.NOT_FOUND),
        ('not_author_client', 'delete_url', HTTPStatus.NOT_FOUND),
    ]
)
def test_comment_edit_delete_permissions(
    request,
    client_fixture,
    url_fixture,
    expected_status,
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
def test_redirect_anonymous_user_to_login(client, comment, request, url_fixture, login_url):
    url = request.getfixturevalue(url_fixture)
    redirect_url = f'{login_url}?next={url}'

    response = client.get(url)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == redirect_url
