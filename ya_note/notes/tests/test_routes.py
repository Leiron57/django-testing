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

    def _get_note_access_test_cases(self):
        return [
            (self.client_user1, self.note1.slug, HTTPStatus.OK),
            (self.client_user1, self.note2.slug, HTTPStatus.NOT_FOUND)
        ]

    def _test_note_access(self, view_name):
        test_cases = self._get_note_access_test_cases()
        for client, slug, expected_status in test_cases:
            url = reverse(view_name, args=(slug,))
            with self.subTest(
                view=view_name,
                slug=slug,
                expected_status=expected_status.value,
                url=url
            ):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_note_detail_access(self):
        self._test_note_access('notes:detail')

    def test_note_edit_access(self):
        self._test_note_access('notes:edit')

    def test_note_delete_access(self):
        self._test_note_access('notes:delete')

    def test_public_pages_available_for_anonymous(self):
        test_cases = [
            ('home_page', self.NOTES_HOME_URL),
            ('login_page', self.USERS_LOGIN_URL),
            ('signup_page', self.USERS_SIGNUP_URL),
        ]

        for page_name, url in test_cases:
            with self.subTest(page=page_name, url=url):
                response = self.anonymous_client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    f"Page {page_name} ({url}) should be accessible"
                )

    def test_logout_page_redirects_after_post(self):
        response = self.client_user1.post(self.USERS_LOGOUT_URL)
        login_url = self.USERS_LOGIN_URL
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn(login_url, response.url)
