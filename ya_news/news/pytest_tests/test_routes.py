import pytest
from http import HTTPStatus
from django.urls import reverse


@pytest.mark.parametrize(
    'name',
    ('news:home', 'news:detail', 'users:login', 'users:signup', 'users:logout')
)
def test_pages_availability_for_anonymous_user(client, name, news):
    args = (news.pk,) if name == 'news:detail' else None
    url = reverse(name, args=args)

    if name == 'users:logout':
        response = client.post(url)
        assert response.status_code == HTTPStatus.FOUND
    else:
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_fixture, status',
    (
        ('author_client', HTTPStatus.OK),
        ('not_author_client', HTTPStatus.NOT_FOUND),
    )
)
def test_comment_edit_delete_available_only_for_author(
    request, client_fixture, status, comment
):
    client = request.getfixturevalue(client_fixture)

    for name in ('news:edit', 'news:delete'):
        url = reverse(name, args=(comment.pk,))
        response = client.get(url)
        assert response.status_code == status


@pytest.mark.django_db
def test_redirect_for_anonymous_user(client, comment):
    login_url = reverse('users:login')

    for name in ('news:edit', 'news:delete'):
        url = reverse(name, args=(comment.pk,))
        redirect_url = f'{login_url}?next={url}'

        response = client.get(url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == redirect_url
