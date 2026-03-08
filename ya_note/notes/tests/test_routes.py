from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.other_user = User.objects.create(username='Чужой')
        cls.note = Note.objects.create(
            title='Заметка',
            text='Текст',
            author=cls.author
        )

        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.other_client = Client()
        cls.other_client.force_login(cls.other_user)

        cls.anonymous_client = Client()

    def test_home_page_available_for_anonymous(self):
        url = reverse('news:home')
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_available_for_authenticated_user(self):
        urls = (
            reverse('notes:list'),
            reverse('notes:add'),
            reverse('notes:success'),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_note_pages_only_for_author(self):
        note_id = self.note.id
        urls = (
            reverse('notes:detail', args=(note_id,)),
            reverse('notes:edit', args=(note_id,)),
            reverse('notes:delete', args=(note_id,)),
        )
        for url in urls:
            with self.subTest(url=url, user='author'):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

        for url in urls[1:]:
            with self.subTest(url=url, user='other'):
                response = self.other_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_redirect_for_anonymous_user(self):
        note_id = self.note.id
        login_url = reverse('users:login')
        urls = (
            reverse('notes:list'),
            reverse('notes:add'),
            reverse('notes:success'),
            reverse('notes:detail', args=(note_id,)),
            reverse('notes:edit', args=(note_id,)),
            reverse('notes:delete', args=(note_id,)),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.anonymous_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)
                self.assertRedirects(response, f'{login_url}?next={url}')

    def test_auth_pages_available_for_all(self):
        login_url = reverse('users:login')
        signup_url = reverse('users:signup')
        logout_url = reverse('users:logout')

        for url in (login_url, signup_url):
            with self.subTest(url=url):
                response = self.anonymous_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

                response_auth = self.author_client.get(url)
                self.assertEqual(response_auth.status_code, HTTPStatus.OK)

        for client in (self.anonymous_client, self.author_client):
            with self.subTest(url=logout_url, client=client):
                response = client.post(logout_url)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)
                self.assertIn(login_url, response.url)