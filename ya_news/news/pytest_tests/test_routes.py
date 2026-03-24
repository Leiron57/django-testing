from http import HTTPStatus

from django.urls import reverse

import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('users:login', None),
        ('users:signup', None),
    )
)
def test_pages_available_for_anonymous_user_get(client, name, args):
    url = reverse(name, args=args)

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_news_detail_page_available_for_anonymous_user(client, news):
    url = reverse('news:detail', args=(news.pk,))

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_logout_page_available_for_anonymous_user(client, news):
    url = reverse('users:logout')

    response = client.post(url)

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_fixture, url_name, expected_status',
    [
        ('author_client', 'news:edit', HTTPStatus.OK),
        ('author_client', 'news:delete', HTTPStatus.OK),
        ('not_author_client', 'news:edit', HTTPStatus.NOT_FOUND),
        ('not_author_client', 'news:delete', HTTPStatus.NOT_FOUND),
    ]
)
def test_comment_edit_delete_permissions(request, client_fixture, url_name, expected_status, comment):
    client = request.getfixturevalue(client_fixture)
    url = reverse(url_name, args=(comment.pk,))
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_redirect_for_anonymous_user(client, comment):
    login_url = reverse('users:login')

    for name in ('news:edit', 'news:delete'):
        url = reverse(name, args=(comment.pk,))
        redirect_url = f'{login_url}?next={url}'

        response = client.get(url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == redirect_url
