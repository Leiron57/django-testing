from http import HTTPStatus
from django.test import Client
import pytest
from pytest_django.asserts import assertFormError
from .constants import WARNING, BAD_WORDS
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, comment_url):
    data = {'text': 'Текст комментария'}

    client.post(comment_url, data=data)

    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_create_comment(
    author_client,
    news,
    author,
    comment_url,
    detail_with_comments_url
):
    data = {'text': 'Текст комментария'}

    response = author_client.post(comment_url, data=data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == detail_with_comments_url
    assert Comment.objects.count() == 1

    comment = Comment.objects.get()
    assert comment.text == data['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize('bad_words', BAD_WORDS)
def test_user_cant_use_bad_words(
    author_client: Client,
    bad_words,
    detail_url
) -> None:
    bad_words_data = {'text': f'Какой-то текст, {bad_words}, еще текст'}

    response = author_client.post(detail_url, data=bad_words_data)

    form = response.context['form']
    assertFormError(
        form=form,
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, comment, edit_url):
    data = {'text': 'Обновлённый комментарий'}

    response = author_client.post(edit_url, data=data)

    assert response.status_code == HTTPStatus.FOUND

    comment.refresh_from_db()
    assert comment.text == data['text']


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
    not_author_client,
    comment,
    edit_url
):
    data = {'text': 'Попытка изменить чужой комментарий'}

    response = not_author_client.post(edit_url, data=data)

    assert response.status_code == HTTPStatus.NOT_FOUND

    comment.refresh_from_db()
    assert comment.text == 'Текст комментария'


@pytest.mark.django_db
def test_author_can_delete_comment(
    author_client,
    delete_url,
    detail_with_comments_url
):
    response = author_client.post(delete_url)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == detail_with_comments_url
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(
    not_author_client,
    delete_url
):
    response = not_author_client.post(delete_url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
