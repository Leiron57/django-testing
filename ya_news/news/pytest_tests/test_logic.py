
from http import HTTPStatus

from django.test import Client

import pytest
from pytest_django.asserts import assertFormError


from .constants import (
    get_news_detail_url,
    get_news_comment_url,
    get_comment_edit_url,
    get_comment_delete_url,
    get_news_detail_with_comments_url,
    WARNING,
    BAD_WORDS
)
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news):
    url = get_news_comment_url(news.pk)
    data = {'text': 'Текст комментария'}

    client.post(url, data=data)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_create_comment(author_client, news, author):
    # Arrange (подготовка данных)
    url = get_news_comment_url(news.pk)
    data = {'text': 'Текст комментария'}
    expected_redirect_url = get_news_detail_with_comments_url(news.pk)

    # Act (выполнение действия — работа бизнес‑логики)
    response = author_client.post(url, data=data)

    # Assert (проверки результатов)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == expected_redirect_url
    assert Comment.objects.count() == 1

    comment = Comment.objects.get()
    assert comment.text == data['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize('bad_words', BAD_WORDS)
def test_user_cant_use_bad_words(
    author_client: Client,
    news,
    bad_words
) -> None:
    detail_url = get_news_detail_url(news.pk)
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
def test_author_can_edit_comment(author_client, comment):
    edit_url = get_comment_edit_url(comment.pk)
    data = {'text': 'Обновлённый комментарий'}

    response = author_client.post(edit_url, data=data)

    assert response.status_code == HTTPStatus.FOUND

    comment.refresh_from_db()
    assert comment.text == data['text']


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
    not_author_client,
    comment
):
    edit_url = get_comment_edit_url(comment.pk)
    data = {'text': 'Попытка изменить чужой комментарий'}

    response = not_author_client.post(edit_url, data=data)
    assert response.status_code == HTTPStatus.NOT_FOUND

    comment.refresh_from_db()
    assert comment.text == 'Текст комментария'


@pytest.mark.django_db
def test_author_can_delete_comment(author_client, comment, news):
    delete_url = get_comment_delete_url(comment.pk)
    url_to_comments = get_news_detail_with_comments_url(news.pk)

    response = author_client.post(delete_url)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == url_to_comments
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(
    not_author_client,
    comment
):
    delete_url = get_comment_delete_url(comment.pk)
    response = not_author_client.post(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
