import pytest
from http import HTTPStatus
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from django.test import TestCase


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news):
    url = reverse('news:detail', args=(news.pk,))
    data = {'text': 'Текст комментария'}

    client.post(url, data=data)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_create_comment(author_client, news, author):
    url = reverse('news:comment', args=(news.pk,))
    data = {'text': 'Текст комментария'}

    response = author_client.post(url, data=data)
    assert response.status_code == HTTPStatus.FOUND

    expected_url = reverse('news:detail', args=(news.pk,)) + '#comments'
    assert response.url == expected_url

    comment = Comment.objects.get()
    assert comment.text == data['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, news):
    url = reverse('news:detail', args=(news.pk,))
    data = {'text': f'Текст с запрещённым словом: {BAD_WORDS[0]}'}

    response = author_client.post(url, data=data)

    TestCase().assertFormError(
        response,
        form='form',
        field='text',
        errors=[WARNING]
    )

    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    edit_url = reverse('news:edit', args=(comment.pk,))
    data = {'text': 'Обновлённый комментарий'}

    response = author_client.post(edit_url, data=data)
    assert response.status_code == HTTPStatus.OK

    comment.refresh_from_db()
    assert comment.text == data['text']


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
    not_author_client,
    news,
    author
):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    edit_url = reverse('news:edit', args=(comment.pk,))
    data = {'text': 'Попытка изменить чужой комментарий'}

    response = not_author_client.post(edit_url, data=data)
    assert response.status_code == HTTPStatus.NOT_FOUND

    comment.refresh_from_db()
    assert comment.text == 'Текст комментария'


@pytest.mark.django_db
def test_author_can_delete_comment(author_client, news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )

    delete_url = reverse('news:delete', args=(comment.pk,))
    url_to_comments = reverse('news:detail', args=(news.pk,)) + '#comments'

    response = author_client.post(delete_url)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == url_to_comments
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(
    not_author_client,
    news,
    author
):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    delete_url = reverse('news:delete', args=(comment.pk,))

    response = not_author_client.post(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
