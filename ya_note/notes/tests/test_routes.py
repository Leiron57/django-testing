from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.urls import reverse

from yanote.common import BaseNotesTestSetup

User = get_user_model()

class TestRoutes(BaseNotesTestSetup):
    def test_home_page_available_for_anonymous(self):
        response = self.anonymous_client.get(self.NOTES_HOME_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_list_page_available_for_authenticated(self):
        response = self.client_user1.get(self.NOTES_LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_add_page_available_for_authenticated(self):
        response = self.client_user1.get(self.NOTES_ADD_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_success_page_available_for_authenticated(self):
        response = self.client_user1.get(self.NOTES_SUCCESS_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_anonymous_redirects_to_login_for_list(self):
        login_url = self.USERS_LOGIN_URL
        response = self.anonymous_client.get(self.NOTES_LIST_URL)
        self.assertRedirects(response, f'{login_url}?next={self.NOTES_LIST_URL}')

    def test_anonymous_redirects_to_login_for_add(self):
        login_url = self.USERS_LOGIN_URL
        response = self.anonymous_client.get(self.NOTES_ADD_URL)
        self.assertRedirects(response, f'{login_url}?next={self.NOTES_ADD_URL}')

    def test_anonymous_redirects_to_login_for_detail(self):
        url = reverse('notes:detail', args=(self.note1.slug,))
        login_url = self.USERS_LOGIN_URL
        response = self.anonymous_client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_anonymous_redirects_to_login_for_edit(self):
        url = reverse('notes:edit', args=(self.note1.slug,))
        login_url = self.USERS_LOGIN_URL
        response = self.anonymous_client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_anonymous_redirects_to_login_for_delete(self):
        url = reverse('notes:delete', args=(self.note1.slug,))
        login_url = self.USERS_LOGIN_URL
        response = self.anonymous_client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_author_can_view_note_detail(self):
        url = reverse('notes:detail', args=(self.note1.slug,))
        response = self.client_user1.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_other_user_cannot_view_note_detail(self):
        url = reverse('notes:detail', args=(self.note2.slug,))
        response = self.client_user1.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_author_can_edit_note(self):
        url = reverse('notes:edit', args=(self.note1.slug,))
        response = self.client_user1.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_other_user_cannot_edit_note(self):
        url = reverse('notes:edit', args=(self.note2.slug,))
        response = self.client_user1.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_author_can_delete_note(self):
        url = reverse('notes:delete', args=(self.note1.slug,))
        response = self.client_user1.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_other_user_cannot_delete_note(self):
        url = reverse('notes:delete', args=(self.note2.slug,))
        response = self.client_user1.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_login_page_available_for_anonymous(self):
        response = self.anonymous_client.get(self.USERS_LOGIN_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_signup_page_available_for_anonymous(self):
        response = self.anonymous_client.get(self.USERS_SIGNUP_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_logout_page_redirects_after_post(self):
        response = self.client_user1.post(self.USERS_LOGOUT_URL)
        login_url = self.USERS_LOGIN_URL
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn(login_url, response.url)
