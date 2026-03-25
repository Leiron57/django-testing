from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.urls import reverse

from .common import BaseNotesTestSetup

User = get_user_model()


class TestRoutes(BaseNotesTestSetup):
    def test_authenticated_pages_available(self):
        pages = [
            self.NOTES_LIST_URL,
            self.NOTES_ADD_URL,
            self.NOTES_SUCCESS_URL,
        ]

        for url in pages:
            with self.subTest(url=url):
                response = self.client_user1.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK
                )

    def test_anonymous_redirects_to_login(self):
        protected_pages = [
            self.NOTES_LIST_URL,
            self.NOTES_ADD_URL,
        ]

        login_url = self.USERS_LOGIN_URL

        for url in protected_pages:
            with self.subTest(url=url, login_url=login_url):
                response = self.anonymous_client.get(url)
                expected_redirect = f'{login_url}?next={url}'
                self.assertRedirects(
                    response,
                    expected_redirect
                )

    def test_note_detail_access(self):
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
            with self.subTest(
                description=description,
                slug=slug,
                expected_status=expected_status.value,
                url=url
            ):
                response = client.get(url)
                self.assertEqual(
                    response.status_code,
                    expected_status,
                    description
                )

    def test_note_edit_access(self):
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
            with self.subTest(
                description=description,
                slug=slug,
                expected_status=expected_status.value,
                url=url
            ):
                response = client.get(url)
                self.assertEqual(
                    response.status_code,
                    expected_status,
                    description
                )

    def test_note_delete_access(self):
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
            with self.subTest(
                description=description,
                slug=slug,
                expected_status=expected_status.value,
                url=url
            ):
                response = client.get(url)
                self.assertEqual(
                    response.status_code,
                    expected_status,
                    description
                )

    def test_public_pages_available_for_anonymous(self):
        public_pages = [
            self.NOTES_HOME_URL,
            self.USERS_LOGIN_URL,
            self.USERS_SIGNUP_URL,
        ]

        for url in public_pages:
            with self.subTest(url=url):
                response = self.anonymous_client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK
                )

    def test_logout_page_redirects_after_post(self):
        with self.subTest():
            response = self.client_user1.post(self.USERS_LOGOUT_URL)
            login_url = self.USERS_LOGIN_URL
            self.assertEqual(response.status_code, HTTPStatus.FOUND)
            self.assertIn(login_url, response.url)
