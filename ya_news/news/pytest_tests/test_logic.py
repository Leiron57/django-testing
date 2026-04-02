from http import HTTPStatus
from django.test import Client
from news.models import Comment

import pytest
from pytest_django.asserts import assertFormError


from .constants import (
    WARNING,
    BAD_WORDS,
    get_comment_url,
    get_detail_url,
    get_edit_url,
    get_delete_url,
    get_detail_with_comments_url
)


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news):
    data = {'text': 'Текст комментария'}
    client.post(get_comment_url(news), data=data)
    assert Comment.objects.count() == 0



@pytest.mark.django_db
def test_user_can_create_comment(author_client, news, author):
    comment_text = 'Текст комментария'
    form_data = {'text': comment_text}
    expected_redirect_url = get_detail_with_comments_url(news)

    response = author_client.post(get_comment_url(news), data=form_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == expected_redirect_url

    assert Comment.objects.count() == 1

    comment = Comment.objects.get()
    assert comment.text == comment_text
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize('bad_words', BAD_WORDS)
def test_user_cant_use_bad_words(
    author_client: Client,
    bad_words,
    news
) -> None:
    bad_words_data = {'text': f'Какой-то текст, {bad_words}, еще текст'}

    response = author_client.post(get_detail_url(news), data=bad_words_data)

    form = response.context['form']
    assertFormError(
        form=form,
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, comment):
    data = {'text': 'Обновлённый комментарий'}

    response = author_client.post(get_edit_url(comment), data=data)

    assert response.status_code == HTTPStatus.FOUND

    comment.refresh_from_db()
    assert comment.text == data['text']


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
    not_author_client,
    comment,
):
    data = {'text': 'Попытка изменить чужой комментарий'}

    response = not_author_client.post(get_edit_url(comment), data=data)

    assert response.status_code == HTTPStatus.NOT_FOUND

    comment.refresh_from_db()
    assert comment.text == 'Текст комментария'


@pytest.mark.django_db
def test_author_can_delete_comment(
    author_client,
    comment,
    news
):
    response = author_client.post(get_delete_url(comment))

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == get_detail_with_comments_url(news)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(
    not_author_client,
    comment
):
    response = not_author_client.post(get_delete_url(comment))

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1