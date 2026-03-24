from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from yanote.common import BaseNotesTestSetup

User = get_user_model()

class TestRoutes(BaseNotesTestSetup):
    def test_authenticated_pages_available(self):
        """Проверяет доступность страниц для авторизованных пользователей."""
        pages = [
            (self.NOTES_LIST_URL, 'Список заметок'),
            (self.NOTES_ADD_URL, 'Добавление заметки'),
            (self.NOTES_SUCCESS_URL, 'Страница успеха'),
        ]

        for url, description in pages:
            with self.subTest(page=description):
                response = self.client_user1.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница "{description}" должна быть доступна авторизованному пользователю'
                )

    def test_anonymous_redirects_to_login(self):
        """Проверяет редирект анонимных пользователей на страницу логина."""
        protected_pages = [
            (self.NOTES_LIST_URL, 'Список заметок'),
            (self.NOTES_ADD_URL, 'Добавление заметки'),
        ]

        login_url = self.USERS_LOGIN_URL

        for url, description in protected_pages:
            with self.subTest(page=description):
                response = self.anonymous_client.get(url)
                expected_redirect = f'{login_url}?next={url}'
                self.assertRedirects(
                    response,
                    expected_redirect,
                    msg_prefix=f'Анонимный пользователь должен быть перенаправлен на логин для "{description}"'
                )

    def test_note_detail_access(self):
        """Проверяет доступ к странице детализации заметки."""
        test_cases = [
            (
                self.client_user1,
                self.note1.slug,
                HTTPStatus.OK,
                'Автор должен видеть свою заметку'
            ),
            (
                self.client_user1,
                self.note2.slug,
                HTTPStatus.NOT_FOUND,
                'Пользователь не должен видеть чужую заметку'
            ),
        ]

        for client, slug, expected_status, description in test_cases:
            url = reverse('notes:detail', args=(slug,))
            with self.subTest(description=description, slug=slug):
                response = client.get(url)
                self.assertEqual(
                    response.status_code,
                    expected_status,
                    description
                )

    def test_note_edit_access(self):
        """Проверяет доступ к странице редактирования заметки."""
        test_cases = [
            (
                self.client_user1,
                self.note1.slug,
                HTTPStatus.OK,
                'Автор может редактировать свою заметку'
            ),
            (
                self.client_user1,
                self.note2.slug,
                HTTPStatus.NOT_FOUND,
                'Пользователь не может редактировать чужую заметку'
            ),
        ]

        for client, slug, expected_status, description in test_cases:
            url = reverse('notes:edit', args=(slug,))
            with self.subTest(description=description, slug=slug):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status, description)

    def test_note_delete_access(self):
        """Проверяет доступ к странице удаления заметки."""
        test_cases = [
            (
                self.client_user1,
                self.note1.slug,
                HTTPStatus.OK,
                'Автор может удалять свою заметку'
            ),
            (
                self.client_user1,
                self.note2.slug,
                HTTPStatus.NOT_FOUND,
                'Пользователь не может удалять чужую заметку'
            ),
        ]

        for client, slug, expected_status, description in test_cases:
            url = reverse('notes:delete', args=(slug,))
            with self.subTest(description=description, slug=slug):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status, description)

    def test_public_pages_available_for_anonymous(self):
        """Проверяет доступность публичных страниц для анонимных пользователей."""
        public_pages = [
            (self.NOTES_HOME_URL, 'Главная страница'),
            (self.USERS_LOGIN_URL, 'Страница логина'),
            (self.USERS_SIGNUP_URL, 'Страница регистрации'),
        ]

        for url, description in public_pages:
            with self.subTest(page=description):
                response = self.anonymous_client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f'Страница "{description}" должна быть доступна анонимному пользователю'
                )

    def test_logout_page_redirects_after_post(self):
        """Проверяет редирект после выхода из системы."""
        response = self.client_user1.post(self.USERS_LOGOUT_URL)
        login_url = self.USERS_LOGIN_URL
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn(login_url, response.url)
