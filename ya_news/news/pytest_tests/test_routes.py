import pytest
from http import HTTPStatus
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name,args,expected_status",
    [
        ("news:home", None, HTTPStatus.OK),
        ("news:detail", lambda news: (news.id,), HTTPStatus.OK),
        ("users:login", None, HTTPStatus.OK),
        ("users:signup", None, HTTPStatus.OK),
    ]
)

def test_pages_get_available_for_anonymous(
    client,
    news,
    name,
    args,
    expected_status
):
    resolved_args = args(news) if callable(args) else args
    url = reverse(name, args=resolved_args)
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_logout_redirect_for_anonymous(client):
    logout_url = reverse('users:logout')
    response = client.post(logout_url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(reverse('users:login'))


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
        url = reverse(name, args=(comment.id,))
        response = client.get(url)
        assert response.status_code == status


@pytest.mark.django_db
def test_redirect_for_anonymous_user(client, comment):
    login_url = reverse('users:login')

    for name in ('news:edit', 'news:delete'):
        url = reverse(name, args=(comment.id,))
        redirect_url = f'{login_url}?next={url}'

        response = client.get(url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == redirect_url
